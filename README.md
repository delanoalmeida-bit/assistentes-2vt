# Assistentes de IA — 2ª Vara do Trabalho de São Luís/MA (TRT-16)

Skills e Projetos do Claude usados pela Secretaria da 2ª VT de São Luís.

> Repositório privado. Os números de processo citados nos exemplos foram trocados por rótulos genéricos ("Exemplo 01", "Exemplo 02"…).

## Projetos (`projetos/`)

| Pasta | Projeto no Claude | Arquivos de conhecimento |
|---|---|---|
| `execucao/` | Despachos e Decisões em Execução Trabalhista | `diretrizes-execucao.md` |
| `conhecimento/` | Despachos e Decisões na fase de Conhecimento | `diretrizes conhecimento.MD` |
| `assistente-calculista/` | Assistente Calculista | `MODELO CALCULO EXTERNO.PJC`, `MODELO GERADOR PJC.PJC` |

Cada pasta tem um `INSTRUCOES.md` com o texto das instruções do Projeto. Para recriar um Projeto: crie um Projeto no Claude, cole o conteúdo de `INSTRUCOES.md` (sem a seção "Arquivos do Projeto") nas instruções e envie os arquivos de conhecimento da pasta.

## Skills (`skills/`)

| Skill | Para que serve |
|---|---|
| `triagem-email-2vt` | Triagem diária do e-mail institucional (vt2slz@trt16.jus.br) |
| `triagem-diaria-minutar-despacho` | Triagem dos processos que entraram na tarefa Minutar Despacho |
| `ficha-liquidacao-trabalhista` | Monta a Ficha de Liquidação a partir do título executivo |
| `gerador-pjc` | Gera o .PJC do PJe-Calc 2.16 a partir da ficha validada |
| `lancamento-pjecalc` | Lança a ficha no PJe-Calc web, tela a tela |
| `transposicao-sapt1-pjecalc` | Transpõe cálculo do SAPT1 para o PJe-Calc (Cálculo Externo) |
| `minutador-de-idpj-e-redirecionamento-execucao` | Minutas de IDPJ e inclusão de sócios |
| `minutador-de-incidentes-de-execucao` | Minutas sobre pedidos de execução, penhora e bloqueios |
| `analista-de-embargos-e-impugnacoes-execucao` | Minutas de decisão em embargos à execução e impugnações |
| `skill-planner` | Mentor para planejar e criar novas skills |

Para instalar uma skill no Claude: compacte a pasta da skill em .zip e envie na área de Skills das configurações do Claude.
