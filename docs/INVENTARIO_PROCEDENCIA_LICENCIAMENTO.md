# Inventário de autoria, procedência e licenciamento — ARANDU TAPE

**Snapshot:** 72ff2b2a863e1cb8a885abfe8c3b2a3444d1ebc3. **Data:** 24/11/2026 (Brasília). **Parecer:** depósito científico ainda não autorizado por esta auditoria.

## Escopo e metodologia
133 arquivos inventariados na árvore pública; análise de histórico, documentação e conversas de desenvolvimento acessíveis; triagem direcionada de 19 ativos gráficos (18 SVG e 1 JPEG) e 20 arquivos centrais de código/configuração. Não constitui busca exaustiva de similaridade, prova de autoria jurídica, varredura integral de segredos ou validação de todo o conteúdo. Uma tentativa de varredura integral excedeu o limite de chamadas; não atribuir resultados não obtidos. Nenhum repositório privado foi aberto ou alterado.

## Inventário
| Grupo | Evidência | Parecer |
| --- | --- | --- |
| Semente, Rios, medalhões | Histórico de desenvolvimento descreve identidade própria; SVGs e commit inicial 1c4a9e4af538f6f97e10885bf7b946c240e953ed | Desenvolvimento rastreável; origem individual e direitos não certificados |
| Marca, papel e grafismos | SVGs locais; geometria vetorial, sem marcadores explícitos de licença/autoria nem referências href/src externas detectadas | Confirmar direitos e procedência cultural; não reivindicar autenticidade tradicional |
| paisagem.jpg | Blob 5e4035b3c9f5f7482a6dcdc9d4290ea1aa1491d5; commit inicial; utilizado em mapview.py | Origem não localizada nos históricos disponíveis; substituir por recurso de procedência verificável se não comprovada |
| TOPBAR | Commits 61ab6ced8fc059b1bf3e04abb0c223d7c40132dd e 14d0534c5ac00c68b9b33acea38e172f107ac679; código presente | Confirmar eventual derivação de terceiros; histórico de commits não prova titularidade |
| Confluência / GTK4 | Código e testes no GitHub; históricos de criação assistida por IA e decisões humanas no projeto | Candidatos públicos; não atribuir cada arquivo à IA ou a um autor sem evidência |
| Rust experimental público | Cargo.toml declara MIT; implementação mínima local, sem dependências declaradas nesse manifesto | Preservar declaração existente; confirmar titulares e incluir aviso correspondente quando autorizado |
| ECA/Tupã | Adaptadores locais, exportação explícita e contratos; não demonstram importação direta do núcleo privado nos arquivos examinados | Revisar divulgação de contratos e experimentos; manter núcleo privado fora de qualquer release |
| Bibliotecas e ferramentas | Python, PyGObject, GTK, Cairo, GNOME Shell/GJS, Gio, GLib, Clutter, St, Libadwaita, utilitários da distribuição | Dependências externas; verificar versões, licenças e avisos de itens efetivamente redistribuídos |
| Documentação | CITATION.cff e política científica em main | Confirmar autores e titularidade; CC BY 4.0 apenas proposta |

### Ativos gráficos conferidos
Confluência: diamond.svg, document.svg, files.svg, flower.svg, frequent.svg, marca.svg, memory.svg, open.svg, papel-e1.svg, rios.svg, semente.svg, woven.svg, paisagem.jpg.
TOPBAR: arandu-mark.svg, band-arandu.svg, band-kaaguy.svg, band-tape.svg, band-trama.svg, band-yvy.svg.
Todos os 18 SVGs foram recuperados e examinados quanto a marcadores textuais de licença/autoria e links externos explícitos; nenhum marcador pesquisado encontrado. JPEG recuperado em base64, sem confirmação de autoria ou origem.

### Triagem de código
20 arquivos centrais examinados por padrões de credenciais (chaves privadas PEM e formatos comuns de tokens GitHub, OpenAI, Google e AWS): nenhum padrão encontrado nesses 20. Isto não garante inexistência de segredos. Referências de pesquisa detectadas em app.py, eca_experiments.py e ontology_contract.py; exigem revisão de divulgação. Cargo.toml foi o único desses arquivos com marcador explícito de licença detectado. Não há LICENSE geral na árvore examinada.

## Titularidade e autorização
Lei 9.609/1998, art. 4º, distingue software relacionado às atribuições do vínculo e criação independente sem relação funcional nem recursos institucionais. A Resolução CONSUNI/UNIPAMPA 338/2022, arts. 59 e 62–65, trata da titularidade das criações e do emprego de recursos institucionais. A condição de docente, isoladamente, não resolve a titularidade. Consultar a Divisão de Inovação Tecnológica (dit@unipampa.edu.br) com declaração factual sobre vínculo, recursos, colaboradores e finalidade do projeto.

Fontes:
- https://www.planalto.gov.br/ccivil_03/leis/l9609.htm
- https://sites.unipampa.edu.br/consuni/files/2022/05/res-_338_2022-politica-de-inovacao.pdf
- https://sites.unipampa.edu.br/inovacao/equipe-agipampa/
- https://help.zenodo.org/docs/github/archive-software/github-upload/
- https://help.zenodo.org/docs/deposit/describe-records/licenses/

## Próximas condições de release
1. Resolver origem da paisagem e dos grafismos, incluindo eventual substituição autorizada.
2. Confirmar autoria e titulares; obter manifestação institucional quando aplicável.
3. Aprovar licença da interface (GPL-3.0 é proposta, não licença concedida), preservar licenças e avisos de terceiros.
4. Revisar integralmente o snapshot, inclusive referências de pesquisa, credenciais e binários; comprovar independência dos núcleos privados.
5. Testar no Linux Mint e conferir CI do commit candidato.
6. Autorizar e publicar release do snapshot específico, verificar DOI e licenças no registro Zenodo.

Não se declara originalidade integral nem se atribui licença por inferência. Nenhum DOI foi gerado nesta etapa.
