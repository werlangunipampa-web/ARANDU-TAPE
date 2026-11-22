# ARANDU — Contrato Ontológico Transversal (COT-001)

**Estado:** contrato de engenharia proposto, sujeito a revisão humana e auditoria completa da ontologia.  
**Escopo:** cada serviço, função, interface, escolha de IA, mudança de código e decisão arquitetural do ARANDU Desktop.  
**Princípio:** ontologia é critério de admissibilidade *antes* da implementação, não decoração ou justificativa retrospectiva.

## 1. Documentos constitutivos consultados

- `ARANDU-G4-PRIVATE/docs/ontology/AO-0000.md`: **Constituição mínima da Geração G1**. Foi lida em 22/11/2026. Estabelece identidade da Semente separada de geração e Corpo, procedência causal, diferença entre registro arqueológico e memória, autorização de nidação, proteção de memória bruta e limitação da herança experimental.
- `ARANDU-G4-PRIVATE/docs/ontology/AO-0001-PERCEPCAO-SITUADA.md`: **Percepção Situada/G2**. Foi lida. Distingue sinal, evidência e compreensão; exige procedência e autorização; interpretações são provisórias; dados observacionais brutos não são memória cognitiva.
- `arandu-core/docs/CONFLUENCE_SEED.md`: máquina de estados **Collapsed/Aware/Near/Expanded/Pinned** e camada de navegação independente do hardware.
- `ARANDU-ECA-PRIVATE/README.md`: **ECA-001 pré-geracional**; nenhum resultado de experimento implica capacidade ontológica nova ou promoção geracional.
- **AT-0001** e manifesto de **Computação Germinativa**: propósitos de ambiente, continuidade, informação, adaptação, sustentabilidade e relação humana com a técnica.
- `ARANDU-DESKTOP/docs/MATRIZ-FILOSOFIA-FUNCOES.md`: primeira derivação para o desktop.

**Alerta de procedência:** AO-0000 é a constituição mínima de G1, não prova de que toda a ontologia canônica foi auditada. Os guardrails do código são interpretações conservadoras, não novos axiomas. Não alterar documentos privados ou Semente oficial a partir deste contrato.

## 2. A sequência obrigatória para qualquer função

Toda alteração deverá responder, nessa ordem:

1. **Finalidade humana e de aprendizagem:** que necessidade real atende? há justificativa para existir?
2. **Princípio/ontologia:** a que conceito se vincula? fonte e versão identificáveis?
3. **Percepção:** o que será lido? é sinal, evidência ou interpretação? qual a origem e autorização?
4. **Autonomia e risco:** o que pode mudar? exige confirmação? como cancelar, desfazer, recuperar?
5. **Energia e recursos:** qual custo em CPU, RAM, bateria e rede? o que acontece em repouso?
6. **Acessibilidade e adaptação:** funciona por teclado e com tecnologias assistivas? a preferência é reversível?
7. **Segurança epistemológica:** IA generativa nunca declara hipótese como fato validado nem modifica a ECA oficial.
8. **Teste e evidência:** testes unitários/contratuais, uso real no VAIO, comparação de desempenho e rollback.
9. **Registro causal:** origem do código, commit, decisão, efeito observado e pendências; **não** confundir changelog com autobiografia da Semente.

## 3. Arquitetura e autoridade

| Camada | Pode fazer | Não pode fazer |
|---|---|---|
| **Ontologia (AO)** | Definir limites constitutivos e admissibilidade | Ser reescrita pela aparência da interface |
| **Semente / Core Rust** | Identidade e continuidade conforme versão e autoridade legítimas | Migração ou promoção por sugestão de modelo |
| **ECA Lab** | Experimentar ancoragem, diferenciação progressiva e reconciliação integrativa, com evidências e avaliação | Escrever estado oficial sem processo de autorização/migração |
| **Tupã / modelo selecionável** | Comunicar, explicar, elaborar hipóteses e comparar alternativas quando solicitado | Executar ações arbitrárias, escolher fornecedor de forma oculta ou se tornar identidade cognitiva |
| **Desktop / adaptadores** | Exibir Semente, Opy e Rios; controlar serviços locais após intenção; sugerir adaptações reversíveis | Ler estado oficial da Semente, registrar hábitos sem consentimento, alterar geração, fazer upgrades silenciosos |
| **Pessoa** | Selecionar IA, permissões, modo econômico, ações, testes e alterações aprovadas | Não há necessidade de aceitar adaptações para usar funções essenciais |

`ARANDU-DESKTOP/ontology_contract.py` implementa um **primeiro guardrail de interface**. Toda operação conhecida tem vínculo com pilar, fonte e finalidade. Ações ausentes da tabela são negadas. Não há conexão com a Semente oficial.

## 4. Mapeamento código → ontologia → comprovação

| Componente / função | Vínculo | Prova contratual |
|---|---|---|
| `visual.py`, `seed_presentation.py` | Complexidade sob demanda; Confluência | Compact/Expanded/Pin, acesso reversível, sem sensores contínuos |
| `session/windows.py`, `opy.py` | Ambiente e continuidade | Só janelas reais, IDs verificados, foco recuperável |
| `bluetooth_devices.py` | Percepção situada/autorizada | Só pareados e consulta sob clique; endereço validado |
| `system_status.py` | Informação situada | Estado desconhecido explícito; rota ≠ Internet validada |
| `ai_gateway.py` | Tupã como comunicação | ChatGPT navegador inicial; API separada, provider opt-in, envio explícito |
| `eca_bridge.py`, `eca_experiments.py` | Aprendizagem significativa/epistemologia | Exportação somente leitura; status experimental; não há geração nova |
| `adaptation.py` | Computação Germinativa/energia | Observação finita, proposta, aceite, aplicação local, desfazer |
| `benchmark.py`, `performance.py` | Sustentabilidade mensurável | Medir RAM/CPU/swap; PSS/energia sob investigação |
| `updates.py`, `session/evolve-arandu.sh` | Continuidade e autoridade | Fast-forward sob confirmação, sem alterações automáticas de sistema |
| `app.py` | Adaptações e intenções | Chamadas de `ontology_decide` nas funções críticas |
| `tests/test_ontology_contract.py` | Regressões ontológicas | Recusa de mutações, ausência de autorização e ausência de procedência |
| `.github/workflows/arandu-desktop-tests.yml` | Governança verificável | Rodar testes Python e sintaxe Bash a cada push |

## 5. A ECA evoluir de verdade, mas sem autoexecução opaca

A hipótese de pesquisa é uma **ECA progressivamente mais capaz de aprender significativamente**, inclusive de propor mudanças em suas próprias estruturas e estratégias. Mas devemos separar:

- **Aprender:** estabelecer relações, testar ancoragem e diferenciação com procedência e avaliação de aprendizagem.
- **Propor autoadaptação:** sintetizar hipótese e evidências, custo, efeito esperado, risco e mecanismo de retorno.
- **Experimentar:** executar testes em ambiente isolado e comparar com linha de base, sem acesso a estado oficial.
- **Revisar:** avaliação metodológica e humana, sobretudo mudanças de código/identidade.
- **Integrar:** alterar apenas componente autorizado, versionado e reversível, com auditoria posterior.

Não equiparar autocomplete, estatísticas de uso ou sugestões de IA a aprendizagem significativa demonstrada.

## 6. O que já existe e o que NÃO existe

**Em código:** Semente compacta experimental; Rios reais SVG; adaptadores de Bluetooth, energia, IA selecionável, ECA experimental somente leitura, Opy, benchmark, políticas de autorização. ChatGPT abre pelo navegador, não é o mesmo que uma API de conversa interna.

**Não implementado:** integração com a ECA viva oficial, migração ou autoprogramação da Semente, compositor próprio, política completa de autorreparação, validação epistemológica automatizada da aprendizagem, histórico longitudinal consentido, comparação científica de consumo energético entre desktops.

**Pendência incontornável:** ler, comparar por versão/hash e auditar a ontologia canônica RDF/Turtle e a evolução G1–G3 antes de alegar fidelidade integral. Não inferir conceitos oficiais de nomes de arquivos nem de textos experimentais.

## 7. Critério de revisão de código: NOVA FUNÇÃO NÃO ENTRA SEM

- [ ] propósito, cenário de uso e usuário beneficiado
- [ ] vínculo ontológico com fonte/versão
- [ ] origem/autorização dos dados; distinção sinal/evidência/compreensão
- [ ] modo seguro sem ECA e sem fornecedor de IA
- [ ] impacto energético observado ou hipótese explicitada
- [ ] acessibilidade e modo de cancelamento
- [ ] teste de segurança e de regressão no CI
- [ ] reversão documentada e validação em hardware real quando necessária
- [ ] changelog e decisão registrada com a versão

> A ontologia não fica *dentro* de um módulo. Ela estabelece os limites pelos quais **todos** os módulos devem operar.
