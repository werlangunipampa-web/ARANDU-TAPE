"""ARANDU — pontes opt-in para modelos generativos intercambiáveis.

Uma IA generativa é INTERFACE DE LINGUAGEM, nunca núcleo ontológico, ECA ou
autoridade executora. Nada acessa hardware, janelas, arquivos, histórico ou ECA.
Somente a pergunta digitada, após clique em Enviar, pode sair do computador.
Nenhuma credencial é salva; chaves opcionais vêm de variáveis de ambiente.
"""
from __future__ import annotations

import json
import os
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, build_opener, ProxyHandler

PROVIDERS = {
    "off": {"label": "Desligada · sem IA"},
    "ollama": {"label": "Ollama · local", "env": "ARANDU_OLLAMA_MODEL"},
    "openai": {"label": "OpenAI · API externa", "key": "OPENAI_API_KEY",
               "env": "ARANDU_OPENAI_MODEL"},
    "gemini": {"label": "Gemini · API externa", "key": "GEMINI_API_KEY",
               "env": "ARANDU_GEMINI_MODEL"},
    "anthropic": {"label": "Claude · API externa", "key": "ANTHROPIC_API_KEY",
                  "env": "ARANDU_ANTHROPIC_MODEL"},
}

SYSTEM = (
    "Você é apenas uma interface de comunicação com o ARANDU, software livre "
    "de navegação por Semente, Rios e Opy. Responda em português com clareza. "
    "Não afirme ter controlado o computador, executado ações, consultado a ECA "
    "ou recuperado memórias. Não invente estado da máquina. Proponha passos "
    "verificáveis. A ECA, a identidade e a autorização pertencem ao ARANDU e "
    "à pessoa, não ao modelo generativo."
)
_MODEL = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._:/+-]{0,100}$")


class GatewayError(RuntimeError):
    pass


def model_for(provider: str) -> str:
    item = PROVIDERS.get(provider)
    if not item or provider == "off":
        return ""
    return os.environ.get(item["env"], "").strip()


def ready(provider: str, model: str) -> tuple[bool, str]:
    if provider not in PROVIDERS or provider == "off":
        return False, "Selecione explicitamente uma IA para conversar."
    if not isinstance(model, str) or not _MODEL.fullmatch(model):
        return False, "Defina um identificador válido do modelo instalado ou contratado."
    key = PROVIDERS[provider].get("key")
    if key and not os.environ.get(key):
        return False, f"Credencial ausente: variável de ambiente {key}. Não digite a chave na conversa."
    return True, "Local" if provider == "ollama" else "API externa: pergunta enviada ao fornecedor"


def build_request(provider: str, model: str, message: str) -> tuple[str, dict, dict]:
    ok, reason = ready(provider, model)
    if not ok:
        raise GatewayError(reason)
    if not isinstance(message, str) or not message.strip() or len(message) > 2000:
        raise GatewayError("Escreva uma pergunta de até 2.000 caracteres.")
    question = message.strip()
    if provider == "ollama":
        return ("http://127.0.0.1:11434/api/chat",
                {"model": model, "stream": False,
                 "messages": [{"role": "system", "content": SYSTEM},
                              {"role": "user", "content": question}]}, {})
    if provider == "openai":
        return ("https://api.openai.com/v1/responses",
                {"model": model, "instructions": SYSTEM, "input": question,
                 "store": False, "max_output_tokens": 500},
                {"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]})
    if provider == "gemini":
        return ("https://generativelanguage.googleapis.com/v1beta/models/" +
                model + ":generateContent",
                {"systemInstruction": {"parts": [{"text": SYSTEM}]},
                 "contents": [{"role": "user", "parts": [{"text": question}]}],
                 "generationConfig": {"maxOutputTokens": 500}},
                {"x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    return ("https://api.anthropic.com/v1/messages",
            {"model": model, "max_tokens": 500, "system": SYSTEM,
             "messages": [{"role": "user", "content": question}]},
            {"x-api-key": os.environ["ANTHROPIC_API_KEY"],
             "anthropic-version": "2023-06-01"})


def extract_response(provider: str, result: dict) -> str:
    try:
        if provider == "ollama":
            text = result["message"]["content"]
        elif provider == "openai":
            text = " ".join(part["text"]
                            for item in result["output"] if item.get("type") == "message"
                            for part in item.get("content", [])
                            if part.get("type") == "output_text")
        elif provider == "gemini":
            text = " ".join(part["text"] for part in
                            result["candidates"][0]["content"]["parts"]
                            if "text" in part)
        elif provider == "anthropic":
            text = " ".join(part["text"] for part in result["content"]
                            if part.get("type") == "text")
        else:
            raise KeyError("provider")
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise GatewayError("A IA respondeu em um formato inesperado.") from exc
    if not isinstance(text, str) or not text.strip():
        raise GatewayError("A IA não forneceu texto.")
    return text[:6000]


def complete(provider: str, model: str, message: str, timeout: int = 25) -> str:
    """Chamada SOMENTE por ação explícita, em thread externa ao loop GTK."""
    url, payload, headers = build_request(provider, model, message)
    request = Request(url, json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                      headers={"Content-Type": "application/json", **headers}, method="POST")
    # Sem proxy para localhost; APIs externas usam configuração TLS/proxy do SO.
    opener = build_opener(ProxyHandler({})) if provider == "ollama" else build_opener()
    try:
        with opener.open(request, timeout=max(3, min(timeout, 40))) as response:
            raw = response.read(120001)
    except (HTTPError, URLError, OSError, TimeoutError) as exc:
        # Nunca incluir corpo de erro que possa conter credenciais/solicitação.
        raise GatewayError("Não foi possível consultar o provedor. Confira modelo, "
                           "rede, credenciais e permissões.") from exc
    if len(raw) > 120000:
        raise GatewayError("Resposta excedeu o limite permitido.")
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise GatewayError("Resposta inválida do provedor.") from exc
    return extract_response(provider, document)
