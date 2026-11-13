---
name: "transposicao-sapt1-pjecalc"
description: "Transpõe cálculo do SAPT1 (ou outro sistema, inclusive o anexo de sentença líquida) para o PJe-Calc 2.16 pelo módulo Cálculo Externo, gerando o .PJC pronto para importar (ou, fora do escopo, com roteiro de telas), com deduções de alvarás e inclusões, e confere o relatório."
---

# Transposição de cálculo do SAPT1 para o PJe-Calc (Cálculo Externo) — v3

Uso: 2ª VT de São Luís (TRT-16), PJe-Calc 2.16. Não se liquida o título; transporta-se um saldo consolidado (principal + juros na data-base do SAPT1), que o PJe-Calc atualiza e do qual deduz os pagamentos.

Serve também para **sentença líquida** (anexo de liquidação com data-base, valores fixados no dispositivo) quando o despacho manda só atualizar e incluir parcela nova (ex.: multa por descumprimento de obrigação de fazer). Os valores do anexo fazem o papel do SAPT1; não refazer a liquidação pela ficha + gerador-pjc (o resultado divergiria dos valores transitados). Crédito bruto do anexo (inclusive FGTS + 40% e multas dos arts. 467/477 pagos ao reclamante) em Verbas Não Tributáveis (principal + juros); INSS segurado e patronal do anexo; custas; honorários pelo roteiro da seção 5. Honorários devidos pelo reclamante com exigibilidade suspensa (justiça gratuita) não entram no cálculo; só no comentário. Não usar ficha de liquidação nem gerador-pjc.

Caminho principal: o Claude gera o .PJC do cálculo externo (seção 3); o Delano importa e liquida. Plano B (fora do escopo do gerador ou importação falhando): o Delano lança na tela com o roteiro COMPLETO entregue de uma vez, sem pedir prints das telas já mapeadas (seção 5).

Restrições do projeto: Claude nunca digita senhas, nunca usa "Excluir" nem "Enviar para o PJe", não opera cálculo em uso pelo Delano, navegador só se ele pedir.

## Validação

Processo [processo Exemplo 12], 10/11/2026: o .PJC gerado (importado como cálculo 128847) liquidou com relatório idêntico ao do cálculo 128821 lançado na tela (total R$ 85.840,44; só mudam o horário e o hífen no lugar do "¿"). Ficha do caso no fim desta skill.

Processo [processo Exemplo 09], 10/11/2026 (plano B, cálculo 128870, planilha ID af1eb15): SAPT1 com INSS do segurado e patronal e sem custas de conhecimento, lançado na tela; total R$ 61.887,89. Validou o lançamento do INSS e o cálculo sem custas de conhecimento; mapeou por print as abas Descontos, Outros Débitos e Débitos do Reclamante (seção 5).

Processo [processo Exemplo 02], 11/11/2026 (plano B, cálculo 128899, sentença líquida ID 2d8e599, data-base 30/07/2026): crédito bruto + INSS segurado e patronal + custas + multa por descumprimento da baixa na CTPS (R$ 1.000,00, juros a partir de 29/09/2026) + honorários de 15% Calculados sobre "(+) Bruto Dev. Reclamante"; total R$ 20.355,64. Validou honorários Calculados e multa com juros a partir de data posterior à data-base.

## 1. Coleta

1. Buscar a última planilha do SAPT1 pelo conector PJe: `piecesSearch` com padrão "R E S U M O" ou "VALORES ATUALIZADOS ATÉ" (tipo PLANILHA DE ATUALIZAÇÃO DE CÁLCULOS); ler com `piecesText`. Atenção: o cabeçalho do SAPT1 pode trazer o número antigo do processo.
2. Extrair:
   - Data-base = "VALORES ATUALIZADOS ATÉ".
   - Para cada item (reclamante, custas, etc.), no último bloco do detalhamento: principal corrigido = "Valor Corrigido em <data-base>"; juros = "Valor Atualizado" − "Valor Corrigido". Conferir que principal + juros = total do resumo.
   - Custas art. 789-A, IX (limitadas ao teto, hoje R$ 638,46): valor único, sem juros.
   - Multas, honorários, INSS, IR, FGTS do resumo.
   - INSS no SAPT1: "TOTAL DO INSS" (segurado, já incluído no bruto do reclamante) e "TOTAL DO INSS EMP. + SAT" (patronal). Usar o "Valor Corrigido em <data-base>" de cada um (o SAPT1 só corrige o INSS, sem juros). Conferir: bruto do reclamante + patronal + custas = TOTAL do resumo.
3. Verificar se a parcela que o pedido manda "acrescentar" (ex.: multa) JÁ está no total do SAPT1 — se estiver, lançar uma vez só e avisar.
4. Pagamentos: data e valor efetivamente debitado das contas judiciais (o Delano informa a partir dos extratos; usar esses valores). Somar alvarás/resgates da mesma conta/data num único pagamento. Identificação do pagamento: a dica da tela pede os IDs dos documentos (ex.: ID0000001/ID0000002); usar o ID informado pelo Delano (alvarás, ou a certidão que junta os extratos dos resgates). O conector PJe não mostra o ID curto. Honorários contratuais destacados no alvará NÃO entram no cálculo: o pagamento inteiro abate o crédito do reclamante.
5. Ler o despacho que manda incluir parcelas novas (ex.: multa por LMF) para descrição, valor, data-base e credor.
6. Perguntar só o que for decisão: juros na multa (sugestão: aplicar, se integra a condenação em favor do exequente); priorizar juros nos pagamentos (sugestão: sim, art. 354 CC); data de liquidação (padrão: hoje).
7. Critério padrão: IPCA + TAXA_LEGAL a partir da data-base (Lei 14.905/2024), válido para data-base posterior a 30/08/2024. Se anterior, não gerar: pedir orientação (combinação de índices não testada).

Declarar premissas antes de gerar ou de entregar o roteiro (natureza tributável/não tributável, critério, imputação).

## 2. Escopo do gerador (v1)

Cobre: crédito do reclamante **não tributável** (principal + juros); multas/indenizações devidas ao reclamante (uma ou mais, com ou sem juros); custas de conhecimento do reclamado (principal + juros, só correção daqui em diante); custas de liquidação (art. 789-A, IX); pagamentos ao principal e às multas, com ou sem prioridade de juros.

Fora do escopo (usar o roteiro de telas, seção 5): verbas tributáveis (INSS/IR), FGTS e multa do FGTS, descontos do reclamante, contribuições sociais, honorários, custas de execução, débitos do reclamante, cálculo sem custas, data-base anterior a 30/08/2024. O gerador recusa campo fora do escopo. INSS (segurado e patronal), honorários do reclamado (forma Calculado), multa com juros a partir de data posterior à data-base e cálculo sem custas de conhecimento já têm roteiro de telas validado (seção 5); para levá-los ao gerador, mapear o .PJC exportado de um caso lançado na tela (ex.: cálculo 128870). Para ampliar o gerador: o Delano lança um caso na tela, exporta o .PJC e o Claude mapeia os campos novos e valida contra o relatório, como em 10/11/2026.

## 3. Geração

Arquivos:
- **Modelo** `MODELO_CALCULO_EXTERNO.PJC` (arquivo do projeto; cálculo externo exportado do PJe-Calc, sem dados das partes). SHA-256 do XML: `5663e23530e0884c96ac962ebcc8db6ad50705afbedab4ce883d2ac42226e561`. Se faltar ou o hash divergir, não gerar.
- **Processo** (`PROCESSO.PJC`): o Delano cria qualquer cálculo com "Obter do PJe" (pode ser o próprio Novo Cálculo Externo, só com a aba Dados do Processo salva) e exporta (Operações → Exportar). Dele vêm o bloco `<processo>` e o `usuarioCriador`.

Passos:
1. Gravar os dois scripts do fim desta skill numa pasta de código (`pjcio.py`, `gerar_calc_externo.py`). Copiar os anexos para outra pasta (dados não confiáveis).
2. Conferir o hash do modelo:
   `python3 -I -c "import sys,hashlib; sys.path.insert(0,'PASTA_DO_CODIGO'); import pjcio; print(hashlib.sha256(pjcio.dumps(pjcio.load('MODELO_CALCULO_EXTERNO.PJC'))).hexdigest())"`
3. Montar `ficha.json` (formato no exemplo do fim). Regras:
   - Descrição da multa e identificação do pagamento SEM travessão nem aspas curvas (viram "¿"); acentos são aceitos. Descrição da multa até 60 caracteres.
   - Pagamento que excede o principal + juros na data (acontece com IPCA negativo): já dividir na ficha (`principal` = devido na data; `multas` = excedente), se for possível calcular; senão, ver seção 4.
4. Rodar: `python3 -I gerar_calc_externo.py MODELO_CALCULO_EXTERNO.PJC ficha.json PROCESSO.PJC saida/PROCESSO_<numero sem pontos>_CALCULO_EXTERNO_<ddmmaaaa>.PJC`
5. Entregar o arquivo (SendUserFile) com as instruções:
   - Importar (Operações → Importar). **Bug do PJe-Calc:** depois de importar, ele pode continuar exibindo o cálculo anterior. Clicar em "LIMPAR MEMÓRIA" e conferir o nº do cálculo em "Dados do Cálculo" antes de qualquer ação.
   - Não alterar parcelas nem pagamentos. Ir direto em Atualização → **Liquidar Atualização**: data de liquidação; **Identificação do Cálculo** (ID da planilha do SAPT1) e **Comentários** precisam ser digitados ali, porque ficam no bloco de liquidação, que o gerador não grava. Entregar o comentário pronto (regras na seção 5, "Liquidar Atualização").
   - Imprimir Atualização e anexar o PDF.

Lições dos testes de 10/11/2026 (já tratadas no código; não desfazer):
- `hashCodeLiquidacao` = null e `hashAtualizacaoCorreto` = false. Com `true` sem o bloco `atualizacao`, a importação falha ("A operação não pôde ser concluída e o cálculo não foi importado").
- `apuracoesDeJuros` NÃO é resultado no cálculo externo: guarda o principal corrigido na data-base. Sem ele, o "Principal" da tela de pagamento fica desabilitado e a liquidação recusa ("Os pagamentos realizados em ... estão inválidos").
- O sistema grava a data-base em todas as datas do cálculo (admissão, demissão, ajuizamento, data de liquidação do cálculo, verbas internas, vencimentos de multas e custas).
- O sistema cria verbas internas a partir das parcelas ("VERBAS NÃO TRIBUTÁVEIS" com o principal; "CONTRIBUIÇÃO SOCIAL SALARIOS DEVIDOS" zerada). O gerador mantém a primeira coerente com a ficha.
- Cada multa existe em dois lugares: `<multas>` e a lista da parcela, ligados por `internalRef`.

## 4. Conferência do relatório

- Valores-base em "Data Últ. Atualização" = SAPT1 (principal, juros, custas, multa).
- Critério: IPCA e Taxa Legal a partir da data-base.
- Cada pagamento: soma do "Pago" = valor do pagamento; imputação conforme decidido. Com prioridade de juros, juros pagos = juros devidos. Juros pagos proporcionais (juros devidos × pagamento ÷ total devido) indicam "Priorizar Pagamento de Juros" desmarcado naquele pagamento: conferir pagamento a pagamento.
- Com INSS: contribuição social no resumo = segurado + patronal (sem dobra); "Desconto da Contribuição Social" no crédito do reclamante, corrigido pelo IPCA; base de juros = principal corrigido menos o desconto; SELIC desde a competência da data-base. Se a contribuição sumir do resumo, verificar se "Aplicar Lei 11.941/2009" foi desmarcado.
- Conferir se todas as parcelas do SAPT1 aparecem no resumo (custas esquecidas não geram erro, só somem).
- Nenhuma diferença negativa no Principal Corrigido. Se houver (pagamento excedente), o Delano edita o pagamento na tela (lápis): Principal = devido na data (principal corrigido + juros do relatório); ☑ Multas/Indenizações devidas ao Reclamante = excedente. Liquidar de novo. Nas multas, o sistema não aplica a prioridade de juros (diferença pequena; aceitar).
- Multa na coluna do reclamante; custas só com correção. Custas de liquidação passam alguns reais do teto pela correção (não há como travar; avisar).
- Total devido = líquido do reclamante + custas (+ demais).
- Honorários Calculados: base = Total Parcial dos Créditos do Reclamante (bruto, com multas); recalcular o valor na data-base e conferir com o do título.
- Parcela nova com juros a partir de data posterior: linha "Juros de Mora de <vencimento> até <liquidação>".
- Registrar resíduos de centavos sem exigir correção.

## 5. Plano B: roteiro de telas (mapeadas em 10/11/2026, processo [processo Exemplo 12])

### Cálculo > Novo Cálculo Externo
- Aba Dados do Processo: "Obter do PJe" + "PJe:Buscar". Não alterar. Número, Tipo e Data de Criação são preenchidos pelo sistema ao salvar.
- Aba Parâmetros do Cálculo Externo:
  - Data da Última Atualização: data-base do SAPT1.
  - Índice Trabalhista: IPCA (a tela abre em IPCA-E — trocar). Não combinar; não ignorar taxa negativa.
  - Tabela de Juros: TAXA LEGAL (a tela abre em "Sem Juros" — trocar). Vale para data-base posterior a 30/08/2024 (Lei 14.905/2024); se anterior, pedir print das opções de combinação.
  - Bases de Juros ("Verba (-) Contribuição Social") e FGTS: manter.
  - Contribuição Social: manter o padrão da tela (Salários Devidos: ☑ Aplicar Lei 11.941/2009; Trabalhista ☑ Correção ☐ Juros; Previdenciária ☐ Correção ☐ Juros). NUNCA desmarcar "Aplicar Lei 11.941/2009": em 10/11/2026 (cálculo 128870) isso fez o INSS sumir do resumo e o desconto do segurado sair do crédito do reclamante, mas a base de juros continuou descontada (relatório incoerente). Efeito do padrão: o INSS recebe SELIC desde a competência da data-base, sem IPCA (o SAPT1 só corrigia; diferença pequena, aceita pelo Delano). Avisar nas premissas.
  - Apurar Imposto de Renda: desmarcar se o SAPT1 tem IR zero.
  - Custas: só "Aplicar Correção" (índice trabalhista); sem juros, sem teto.
  - Salvar.

### Cálculo Externo > Parcelas Atualizáveis
Abas: Créditos do Reclamante / Descontos dos Créditos do Reclamante / Outros Débitos do Reclamado / Débitos do Reclamante. Marcar só o que existe no SAPT1.

Mapeamento testado:
| SAPT1 | Aba › Parcela | Campos |
|---|---|---|
| Crédito do reclamante sem INSS/IR | Créditos › Verbas Não Tributáveis | Valor da Parcela = principal corrigido; Valor dos Juros = juros (NUNCA o total na parcela: geraria juros sobre juros). Índice e taxa vêm dos parâmetros. |
| Multa por LMF a favor do reclamante | Créditos › Multa/Indenização Devida ao Reclamante (+) | Descrição (sem travessão "–": vira "¿"; usar hífen), Tipo Informado, Valor da Parcela, Índice Trabalhista, Aplicar Juros conforme decisão. OBRIGATÓRIO clicar no "+" para gravar a linha na tabela antes de Salvar (senão os campos se perdem). |
| Custas de conhecimento pelo reclamado | Outros Débitos › Custas de Conhecimento Devidas pelo Reclamado | Informado; parcela = corrigido; juros = juros do SAPT1. Tela fixa: índice trabalhista, sem juros. |
| Custas art. 789-A, IX | Outros Débitos › Custas de Liquidação | Informado; valor único. O sistema corrige pelo IPCA e passa do teto (poucos reais) — não há como travar; avisar. |
| INSS do segurado ("TOTAL DO INSS") | Descontos › Contribuição Social Segurado (descontar do principal) **e** Outros Débitos › Contribuição Social Segurado Salários Devidos (recolher à previdência) | Desconto: Valor da Parcela = INSS corrigido; ☑ Corrigir Desconto. Recolher: "Parcelas vencidas até Fev/2009" = 0,00; "Parcelas a partir de Mar/2009" = INSS corrigido; juros em branco. Vale se todas as competências forem posteriores a mar/2009; senão, pedir orientação. Os dois lançamentos NÃO duplicam: o resumo mostra uma só contribuição social. O crédito continua em Verbas Não Tributáveis pelo bruto. |
| INSS empregador + SAT | Outros Débitos › Contribuição Social Patronal Salários Devidos | "até Fev/2009" = 0,00; "a partir de Mar/2009" = valor corrigido; juros em branco. |
| Sem custas de conhecimento | Outros Débitos | Não marcar Custas de Conhecimento; o cálculo funciona só com Custas de Liquidação. |
| Honorários sucumbenciais em % sobre o crédito | Outros Débitos › Honorários Devidos pelo Reclamado | Tipo de Honorário; Descrição; Credor + CPF (advogados no bloco `<Advogado>` do .PJC do processo); Apurar IR conforme o título (desmarcado se omisso e o anexo não reteve); Tipo do Valor **Calculado**; Base de Cálculo **"(+) Bruto Dev. Reclamante"**; Alíquota = % do título; clicar no "+". Na data-base reproduz o valor do título (15% × bruto) e acompanha automaticamente parcelas novas do crédito (ex.: multa). Uma linha só: não lançar honorários separados sobre a multa. |
| Honorários em valor fixo (Informado) | Outros Débitos › Honorários Devidos pelo Reclamado | "Valor dos Juros" só habilita com ☑ Aplicar Juros, que exige "A partir de"; com essa data, a tela RECUSA juros já calculados (tooltip: deixar em branco). Consequência: perdem-se os juros até a data-base e os novos juros só começam na data informada. Preferir Calculado. Se inevitável: Valor da Parcela = principal + juros juntos, juros a partir da data-base (pequeno juros sobre juros; avisar). |
| Parcela nova com vencimento posterior à data-base (ex.: multa por descumprimento de obrigação de fazer) | Créditos › Multa/Indenização Devida ao Reclamante | ☑ Aplicar Juros, "A partir de" = vencimento. Não há campo de início da correção: o IPCA corre desde a data-base (diferença pequena; avisar nas premissas). |

Campos mapeados por print em 10/11/2026, mas sem uso testado (indicar o campo e conferir no relatório):
- Descontos dos Créditos do Reclamante: Previdência Privada (valor, índice); Pensão Alimentícia (alíquota, incidir sobre juros, base: principal tributável/não tributável/FGTS); Multa/Indenização Devida a Terceiros pelo Reclamante (descrição, credor, informado/calculado, valor, juros, índice, aplicar juros, "+"); Honorários Devidos pelo Reclamante (tipo, descrição, credor, CPF/CNPJ/CEI e número, apurar IR, valor, juros, índice, aplicar juros, "+"); Custas de Conhecimento Devidas pelo Reclamante (valor, juros; índice trabalhista, sem juros).
- Outros Débitos do Reclamado: Multa sobre Contribuição Social Salários Devidos (datas iniciais até fev/2009 e a partir de mar/2009; 0,33% por dia, até 20%); Contribuição Social Salários Pagos (pacto: valor, juros) e sua multa; Juros sobre Previdência Privada; Multa/Indenização Devida a Terceiros pelo Reclamado; Honorários Devidos pelo Reclamado (testado em 11/11/2026: ver tabela acima; a tela tem Tipo do Valor Informado/Calculado, Base de Cálculo e Alíquota); Contribuição Social 10% e 0,5% (LC 110/2001: valor, índice); Custas de Execução (valor, juros; sem juros).
- Débitos do Reclamante: Multa/Indenização a Terceiros, Honorários e Custas de Conhecimento pelo Reclamante (mesmos campos acima).
- Os campos só aparecem quando a opção é marcada.

Não testado nem mapeado (pedir print, não supor): Verbas Tributáveis, FGTS, Multa do FGTS.

Salvar e conferir se os valores permaneceram.

### Atualização > Dados do Pagamento > Novo (um por data)
- Data do Pagamento; Valor Total do Pagamento; Identificação (conta judicial e alvarás).
- Pagamento de Precatório: desmarcado.
- Aba Créditos do Reclamante: Valor de Pagamento para Créditos do Reclamante = total; Priorizar Pagamento de Juros conforme decisão; ☑ Principal › Valor = total (cobre principal e juros). "Apurar" desmarcado.
- Outras abas: nada, salvo se o pagamento quitou custas.
- Se o pagamento exceder principal + juros na data (ver relatório: "Principal Corrigido" negativo), editar o pagamento (lápis) e dividir: Principal = devido na data; ☑ Multas/Indenizações devidas ao Reclamante = excedente. Obs.: na parcela de multas o sistema não prioriza juros (diferença pequena; aceitar).
- Não usar as telas Pensão Alimentícia, Multas e Indenizações, Honorários e Custas Judiciais do menu Atualização (duplicaria valores já lançados como parcelas).

### Atualização > Liquidar Atualização (vale também para o caminho do gerador)
- Data de Liquidação: hoje (ou a escolhida).
- Identificação do Cálculo: o ID da planilha do SAPT1.
- Atualização de Precatório/RPV: desmarcado.
- Comentários: até ~480 caracteres (o campo corta em ~500). Sem travessão. Conferir no relatório se a 1ª letra não foi cortada (ocorreu uma vez: "RANSPOSIÇÃO"). Modelo:
  "Transposição do cálculo SAPT1 (ID <id>), atualizado até <data>: crédito da reclamante R$ <total> (principal <p> + juros <j>); custas de conhecimento R$ <c>; custas art. 789-A, IX, CLT R$ <l>; multa por LMF R$ <m> (IDs <ids>). Após <data>: IPCA + taxa legal. Deduzidos alvarás: R$ <v1> em <d1> e R$ <v2> em <d2>, imputados primeiro nos juros."
- Com INSS, incluir no comentário, após o crédito: "com INSS empregado R$ <s>; INSS empregador R$ <p>".
- Liquidar; depois Imprimir Atualização; Delano anexa o PDF.
- Se a planilha juntada ao PJe estiver errada e as partes ainda não tiverem ciência, o Delano a exclui e junta a nova; usar o ID novo no despacho.

## 6. Despacho

Oferecer minuta: menciona a planilha já juntada (pedir o ID), remete às providências já determinadas em decisão anterior (pedir o ID; ex.: mandado ao INSS) em vez de repeti-las, o cálculo SAPT1 de origem, as deduções, o saldo por credor e as providências do despacho anterior (alvará com retenção de honorários contratuais, se houver; SISBAJUD/teimosinha). Apontar como premissas: ordem de imputação do saldo (crédito antes das custas), limite das custas de liquidação ao teto, prazo de manifestação, se a teimosinha já foi renovada.

## Exemplo de ficha (caso validado Exemplo 12-57.2009)

```json
{
  "_processo": "[processo Exemplo 12]",
  "_origem": "SAPT1 ID 8ef61f7; despacho c36cabf",
  "data_base": "31/07/2026",
  "data_criacao": "10/11/2026",
  "correcao": {"indice": "IPCA", "juros": "TAXA_LEGAL"},
  "credito_nao_tributavel": {"principal": 429033.81, "juros": 261820.63},
  "multas_reclamante": [
    {"descricao": "MULTA POR LITIGÂNCIA DE MÁ-FÉ (10%) - IDS 3818FD5 E C36CABF", "valor": 69085.44, "juros": 0, "aplicar_juros": true}
  ],
  "custas_conhecimento_reclamado": {"principal": 6806.83, "juros": 7085.91},
  "custas_liquidacao": {"principal": 638.46, "juros": null},
  "pagamentos": [
    {"data": "11/08/2026", "principal": 678948.03, "priorizar_juros": true, "identificacao": "ALVARÁS - CONTA JUDICIAL 1405.042.04867088-0"},
    {"data": "12/08/2026", "principal": 11451.94, "multas": 454.46, "priorizar_juros": false, "identificacao": "ALVARÁS - CONTA JUDICIAL 1405.042.04857457-0"}
  ]
}
```

Campos: `data_base` (dd/mm/aaaa); `correcao` (`indice`, `juros`; padrão IPCA/TAXA_LEGAL); `credito_nao_tributavel` (`principal`, `juros`); `multas_reclamante` (lista: `descricao`, `valor`, `juros` (padrão 0), `aplicar_juros` (padrão true), `juros_a_partir` (padrão data-base)); `custas_conhecimento_reclamado` e `custas_liquidacao` (`principal`, `juros` ou null); `pagamentos` (lista: `data`, `principal`, `multas`, `priorizar_juros` (padrão true), `identificacao`); `data_criacao` (opcional, padrão hoje). Campos iniciados por `_` são comentários.

## Script: pjcio.py

```python
import zipfile, xml.etree.ElementTree as ET
DECL=b'<?xml version="1.0" encoding="ISO-8859-1"?>'
def load(p):
    if zipfile.is_zipfile(p):
        with zipfile.ZipFile(p) as z: raw=z.read(z.namelist()[0])
    else: raw=open(p,'rb').read()
    return ET.fromstring(raw)
def dumps(r):
    body=ET.tostring(r,encoding='us-ascii',short_empty_elements=False)
    if body.startswith(b'<?xml'): body=body[body.index(b'?>')+2:].lstrip()
    body=body.replace(b"'",b'&apos;').replace(b'"',b'&quot;')
    return DECL+body
def save(r,out,entry,dt=(2026,10,31,12,0,0)):
    data=dumps(r)
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        zi=zipfile.ZipInfo(entry,date_time=dt); zi.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(zi,data)
    return data
```

## Script: gerar_calc_externo.py

```python
"""Gera o .PJC de um Cálculo Externo do PJe-Calc 2.16 (transposição de cálculo do SAPT1).

Uso: python3 -I gerar_calc_externo.py MODELO_CALC_EXTERNO.PJC ficha.json PROCESSO.PJC saida.PJC

O modelo é um cálculo externo exportado pelo próprio PJe-Calc (protótipos de multa e de pagamento).
Do PROCESSO.PJC (cálculo criado com "Obter do PJe") vêm o bloco <processo> e o usuarioCriador.
Todos os valores vêm da ficha. Escopo v1: crédito não tributável (principal + juros), multas devidas
ao reclamante, custas de conhecimento do reclamado, custas de liquidação, pagamentos ao principal
e às multas. Qualquer outra parcela marcada no modelo ou pedida na ficha é recusada.
"""
import copy, datetime, json, sys, os
import xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pjcio

def dt(s): return datetime.datetime.strptime(s, '%d/%m/%Y').date()
def ms(s):  # dd/mm/aaaa -> ms (meia-noite de Brasília, como o PJe-Calc grava)
    d = dt(s); return str(int((datetime.datetime(d.year, d.month, d.day) - datetime.datetime(1970, 1, 1)).total_seconds() * 1000) + 3 * 3600 * 1000)
def num(v):
    if v is None: return 'null'
    s = ('%.2f' % round(float(v) + 0.0, 2)).rstrip('0').rstrip('.')
    return s if s else '0'
def setf(e, tag, val):
    c = e.find(tag)
    if c is None: raise KeyError(f'{e.tag} sem campo {tag}')
    c.text = val

class Ids:
    def __init__(self, root):
        mx = max((int(e.text) for e in root.iter('id') if e.text and e.text.isdigit()), default=0)
        self.n = max(mx, 90_000_000) + 1000
    def __call__(self):
        self.n += 1; return str(self.n)

LIMITE_DESCR = 60    # descrição da multa: 59 caracteres importaram (128821); acima disso não medido
LIMITE_IDENT = 255   # identificação do pagamento: não medido; teto adotado por segurança

def validar(F):
    erros = []
    permitidos = {'data_base', 'correcao', 'credito_nao_tributavel', 'multas_reclamante',
                  'custas_conhecimento_reclamado', 'custas_liquidacao', 'pagamentos', 'data_criacao'}
    for k in F:
        if k not in permitidos and not k.startswith('_'): erros.append(f'campo fora do escopo v1: {k}')
    base = dt(F['data_base'])
    for M in F.get('multas_reclamante', []):
        if len(M['descricao']) > LIMITE_DESCR: erros.append(f'descrição de multa com {len(M["descricao"])} caracteres')
        if any(ch in M['descricao'] for ch in '–—“”'): erros.append('descrição de multa com travessão/aspas curvas (vira "¿")')
    for P in F.get('pagamentos', []):
        if dt(P['data']) < base: erros.append(f'pagamento em {P["data"]} anterior à data-base')
        if P.get('multas') and not F.get('multas_reclamante'): erros.append('pagamento às multas sem multa lançada')
        idt = P.get('identificacao') or ''
        if len(idt) > LIMITE_IDENT: erros.append('identificação de pagamento longa demais')
        if any(ch in idt for ch in '–—“”'): erros.append('identificação de pagamento com travessão/aspas curvas')
    if erros: raise ValueError('ficha recusada:\n- ' + '\n- '.join(erros))

def gerar(modelo, F, proc_src):
    validar(F)
    root = pjcio.load(modelo)
    if root.findtext('calculoExterno') != 'true': raise ValueError('o modelo não é um cálculo externo')
    ids = Ids(root); calc_id = root.findtext('id')
    base_old = root.findtext('dataAjuizamento'); base = ms(F['data_base'])

    # 1. resultados e histórico do cálculo-modelo: fora (o sistema recalcula ao liquidar)
    for t in ('gprec', 'dadosEstruturados'):
        e = root.find(t)
        if e is not None: root.remove(e)
    at = root.find('atualizacao')
    for c in list(at): at.remove(c)
    at.text = 'null'
    setf(root, 'hashCodeLiquidacao', 'null')
    setf(root, 'hashAtualizacaoCorreto', 'false')  # 'true' sem o bloco atualizacao derruba a importação (teste 2, 10/11/2026)
    for t in ('historicosValidacao', 'historicosValidacaoAtualizacao'):
        for s in root.find(t): s.clear()
    # apuracoesDeJuros NÃO é resultado no cálculo externo: guarda o principal corrigido na data-base,
    # e a tela de pagamento lê o "Principal" daqui (sem ele, o Principal fica desabilitado; teste 1, 10/11/2026)
    aj = root.findall('apuracoesDeJuros/Set/ApuracaoDeJuros')
    if len(aj) != 1: raise ValueError('modelo deve ter exatamente uma ApuracaoDeJuros')
    b = dt(F['data_base'])
    setf(aj[0], 'competencia', ms(f'01/{b.month:02d}/{b.year}'))
    setf(aj[0], 'valorCorrigido', num(F['credito_nao_tributavel']['principal']))

    # 2. data-base: o sistema grava a "Data da Última Atualização" em todas as datas do cálculo
    #    (admissão, demissão, ajuizamento, liquidação, verbas internas, vencimentos). Troca toda ocorrência.
    for e in root.iter():
        if e.text == base_old and len(e) == 0: e.text = base
    setf(root, 'dataCriacao', ms(F.get('data_criacao') or datetime.date.today().strftime('%d/%m/%Y')))
    setf(root, 'comentarios', 'null')

    # 3. processo
    src = pjcio.load(proc_src)
    i = list(root).index(root.find('processo'))
    root.remove(root.find('processo')); root.insert(i, copy.deepcopy(src.find('processo')))
    if src.findtext('usuarioCriador'): setf(root, 'usuarioCriador', src.findtext('usuarioCriador'))

    # 4. parâmetros
    PA = root.find('parametrosDeAtualizacao/ParametrosDeAtualizacao')
    CO = F.get('correcao', {})
    setf(PA, 'indiceTrabalhista', CO.get('indice', 'IPCA'))
    setf(PA, 'juros', CO.get('juros', 'TAXA_LEGAL'))
    for t in ('combinarOutroIndice', 'combinarOutroJuros', 'ignorarTaxaNegativa'): setf(PA, t, 'false')
    if PA.findtext('correcaoDasCustas') != 'true' or PA.findtext('jurosDeCustas') != 'false':
        raise ValueError('modelo com parâmetro de custas diferente de "só correção"')

    # 5. créditos do reclamante
    CR = root.find('parcelasAtualizaveisCreditosReclamante/ParcelasAtualizaveisCreditosReclamante')
    for t in ('marcarVerbasTributavel', 'marcarFgts', 'marcarMultaFgts', 'marcarMultaIndenizDevReclamado'):
        if CR.findtext(t) != 'false': raise ValueError(f'modelo com {t} marcado: fora do escopo')
    NT = F['credito_nao_tributavel']
    setf(CR, 'valorParcelaVerbasNaoTributavel', num(NT['principal']))
    setf(CR, 'valorJurosVerbasNaoTributavel', num(NT.get('juros')))
    # verba interna que o sistema cria a partir da parcela não tributável
    vnt = [v for v in root.find('verbas/Set') if v.findtext('nome') == 'VERBAS NÃO TRIBUTÁVEIS']
    if len(vnt) != 1: raise ValueError('modelo sem a verba interna VERBAS NÃO TRIBUTÁVEIS')
    for oc in vnt[0].iter('OcorrenciaDeVerba'):
        setf(oc, 'devido', num(NT['principal'])); setf(oc, 'devidoIntegral', num(round(NT['principal'] * 30, 2)))

    # 6. multas devidas ao reclamante (registro em <multas> + linha da parcela, ligados por internalRef)
    lista = CR.find('listaMultasIndenizDevReclamante/List')
    multas_set = root.find('multas/Set')
    protos_p = list(lista); protos_m = list(multas_set)
    if len(protos_p) < 1 or len(protos_m) < 1: raise ValueError('modelo sem protótipo de multa')
    pp, pm = protos_p[0], protos_m[0]
    for x in protos_p: lista.remove(x)
    for x in protos_m: multas_set.remove(x)
    MS = F.get('multas_reclamante', [])
    setf(CR, 'marcarMultaIndenizDevReclamante', 'true' if MS else 'false')
    for M in MS:
        mid = ids(); juros_ini = ms(M.get('juros_a_partir') or F['data_base'])
        m = copy.deepcopy(pm)
        setf(m, 'id', mid); setf(m, 'versao', '0'); setf(m, 'descricao', M['descricao'])
        setf(m, 'valorMulta', num(M['valor'])); setf(m, 'valorJurosCalcExterno', num(M.get('juros', 0)))
        setf(m, 'dataVencimentoMulta', base); setf(m, 'dataEvento', base)
        setf(m, 'aplicarJurosSobreMulta', 'true' if M.get('aplicar_juros', True) else 'false')
        setf(m, 'dataApartirDeAplicarJuros', juros_ini if M.get('aplicar_juros', True) else 'null')
        m.find('calculo/Calculo/internalRef').text = calc_id
        multas_set.append(m)
        p = copy.deepcopy(pp)
        setf(p, 'id', ids()); setf(p, 'descricao', M['descricao'])
        setf(p, 'valorParcelaInformado', num(M['valor'])); setf(p, 'valorJurosInformado', num(M.get('juros', 0)))
        setf(p, 'aplicarJurosInformado', 'true' if M.get('aplicar_juros', True) else 'false')
        setf(p, 'dataApartirDeAplicarJurosInformado', juros_ini if M.get('aplicar_juros', True) else 'null')
        p.find('multa/Multa/internalRef').text = mid
        lista.append(p)

    # 7. outros débitos do reclamado: custas
    OD = root.find('parcelasAtualizaveisOutrosDebitosReclamado/ParcelasAtualizaveisOutrosDebitosReclamado')
    for c in OD:
        if c.tag.startswith('marcar') and c.tag not in ('marcarCustasConhecimentoReclamado', 'marcarCustasLiquidacao') and c.text != 'false':
            raise ValueError(f'modelo com {c.tag} marcado: fora do escopo')
    CJ = root.find('custasJudiciais/CustasJudiciais')
    CC, CL = F.get('custas_conhecimento_reclamado'), F.get('custas_liquidacao')
    if not CC or not CL: raise ValueError('escopo v1: custas de conhecimento e de liquidação obrigatórias (sem custas: não testado)')
    pc = OD.find('custasConhecimentoReclamado/ParcelasAtualizaveisCustas')
    setf(pc, 'valorParcelaInformado', num(CC['principal'])); setf(pc, 'valorJurosInformado', num(CC.get('juros')))
    pl = OD.find('custasLiquidacao/ParcelasAtualizaveisCustas')
    setf(pl, 'valorParcelaInformado', num(CL['principal'])); setf(pl, 'valorJurosInformado', num(CL.get('juros')))
    setf(CJ, 'valorConhecimentoDoReclamado', num(CC['principal']))
    setf(CJ, 'valorCustasDeLiquidacao', num(CL['principal']))

    # 8. pagamentos
    pset = root.find('pagamentos/Set')
    protos = list(pset)
    if not protos: raise ValueError('modelo sem protótipo de pagamento')
    pg0 = protos[0]
    for x in protos: pset.remove(x)
    for P in F.get('pagamentos', []):
        pr, mu = float(P.get('principal', 0)), float(P.get('multas', 0))
        tot = round(pr + mu, 2)
        g = copy.deepcopy(pg0)
        setf(g, 'id', ids()); setf(g, 'versao', '0')
        setf(g, 'dataCriacao', root.findtext('dataCriacao')); setf(g, 'dataPagamento', ms(P['data']))
        setf(g, 'valorPagamento', num(tot)); setf(g, 'valorParcelaCreditoReclamante', num(tot))
        setf(g, 'valorParcelaPrincipal', num(pr) if pr else 'null')
        setf(g, 'valorParcelaMultasDevidasReclamante', num(mu) if mu else 'null')
        setf(g, 'priorizarPagamentoDeJuros', 'true' if P.get('priorizar_juros', True) else 'false')
        setf(g, 'folhaDoEvento', P.get('identificacao') or 'null')
        g.find('calculo/Calculo/internalRef').text = calc_id
        pset.append(g)

    # 9. integridade das referências
    todos = {e.text for e in root.iter('id')}
    soltos = {e.text for e in root.iter('internalRef')} - todos
    if soltos: raise ValueError(f'referências sem destino: {soltos}')
    return root

if __name__ == '__main__':
    modelo, ficha, proc, out = sys.argv[1:5]
    F = json.load(open(ficha, encoding='utf-8'))
    r = gerar(modelo, F, proc)
    pjcio.save(r, out, os.path.basename(out), dt=datetime.datetime.now().timetuple()[:6])
    print('gerado:', out)
```