---
name: gerador-pjc
description: Gera o arquivo .PJC do PJe-Calc 2.16 (TRT-16) direto de uma Ficha de Liquidação validada, para importar no sistema sem lançar tela a tela.
---

# Gerador de arquivo PJC (PJe-Calc 2.16) — v11

Alternativa ao lançamento pelo navegador (skill `lancamento-pjecalc`). Parte de uma Ficha de Liquidação **VALIDADA** (skill `ficha-liquidacao-trabalhista`) e produz um .PJC que o usuário importa no PJe-Calc e liquida.

## Conteúdo desta skill

- `scripts/` — o código, pronto para executar (não é preciso lê-lo para usar):
  - `gerar_pjc.py` (gerador), `pjcio.py` (leitura/gravação do PJC), `calendario.py` (dias úteis e repousos de São Luís-MA);
  - `comparar_verbas.py` (confere contra um cálculo de referência), `dump_calc.py` (resume um PJC de referência ao montar a ficha);
  - `extrair_tabela_inss.py` (atualiza a tabela da contribuição social);
  - `reduzir_modelo.py` e `ampliar_modelo.py` (só para refazer o modelo).
- `references/formato_ficha.md` — **ler sempre antes de montar a ficha**: campos, tipos de verba e sete exemplos.
- `references/licoes_e_casos.md` — o que os testes mostraram sobre o formato e o detalhe dos casos validados. Ler ao montar ficha com verba menos comum (reflexos, férias gozadas, base tabelada, FGTS a deduzir, IR), ao investigar diferença no relatório ou ao ampliar o gerador.
- `references/fichas_validadas/` — as fichas JSON dos sete casos validados (credores anonimizados), para regressão e como modelo.
- `references/fichas_producao/` — fichas de casos reais liquidados e conferidos contra a ficha (sem cálculo de referência), como modelo: Exemplo 05, Exemplo 01 e Exemplo 13.

## Casos validados

Relatório do arquivo gerado idêntico ao de referência reliquidado na 2.16 (detalhes em `references/licoes_e_casos.md`):

| Caso | Conteúdo principal | Total |
|---|---|---|
| Exemplo 10-11.2025 | verbas rescisórias calculadas, FGTS + 40% | R$ 45.510,17 |
| Exemplo 08-40.2024 | horas extras 50% com reflexos, diferença salarial, multa 467 | R$ 73.053,50 |
| Exemplo 04-13.2020 | HE sobre comissões e fixo, reflexos como coeficientes, 36 deduções, dano moral | R$ 216.154,13 |
| Exemplo 03-64.2024 | comissionista puro, reflexos do sistema, bases por histórico | R$ 286.800,84 |
| Exemplo 07-78.2025 | insalubridade sobre salário mínimo, férias gozadas, honorários periciais | R$ 22.316,79 |
| 128483 (fictício) | periculosidade, noturno, intervalo, FGTS a deduzir | R$ 27.736,09 |
| Exemplo 06-14.2026 | verbas informadas, dedução de férias pagas, multa de 40% informada | R$ 23.326,10 |

O Exemplo 06 foi validado antes da v8; desde a v8 as datas do IR saem na regra nova (ver "Regras críticas"). Reliquidar e conferir se for reutilizado.

O Exemplo 04 e o Exemplo 03 reproduzem cálculos de referência com SELIC cumulada (Exemplo 04: índice SELIC + juros SELIC, confirmado e corrigido nos autos em 03/11/2026; Exemplo 03: IPCA-E + juros SELIC do ajuizamento a 29/08/2024, confirmado e corrigido nos autos em 03/11/2026). As fichas levam `"permitir_selic_dupla": true` só para a regressão; não copiar essas correções em caso novo.

Casos de produção conferidos contra a ficha, sem cálculo de referência (fichas em `references/fichas_producao/`):
- **Exemplo 05-11.2022** (periculosidade com reflexos, salários do afastamento de dispensa anulada, reflexo em horas extras pagas informado, deduções do TRCT), R$ 145.937,62.
- **Exemplo 01-70.2026** (sentença líquida: insalubridade sobre o salário mínimo com meses inteiros de férias gozadas, aviso trabalhado com 12 dias indenizados, FGTS não depositado, multa de 40% já quitada, **teto por pedido** aplicado nos multiplicadores), R$ 62.936,75.
- **Exemplo 13-16.2004** (transferência de cálculo do SAPT1: sentença líquida de 2004 refeita em verbas informadas, ADC 58 desde a origem, multa cominatória, 6 levantamentos como deduções, custas fixadas no título, INSS de 11/2004 com terceiros), total devido pelo reclamado R$ 8.163,07 em 09/11/2026.

## O que o gerador cobre

Verbas:
- **Calculadas:** aviso prévio indenizado, férias + 1/3 indenizadas por período aquisitivo (com dedução do já pago), multa do art. 477, saldo de salário, 13º (uma ou várias ocorrências), salários retidos mensais. Aviso, férias, 477 e 13º podem ter como base a maior remuneração ou um histórico salarial (ex.: comissões).
- **Informadas:** qualquer parcela de valor fixado por ocorrência (devolução de descontos, vale-transporte, saldo fixado em planilha homologada etc.).
- **Horas extras e verbas do mesmo formato** (adicional noturno, intervalo intrajornada): quantidade mensal fixa, proporcional nos meses incompletos e sem os dias de férias gozadas; adicional informado; divisor informado ou pela carga horária; sobre qualquer histórico.
- **Verba sobre histórico salarial:** histórico ÷ divisor × multiplicador × quantidade, mês a mês (periculosidade sobre salário-base, diferença salarial, reflexo como coeficiente mensal).
- **Adicional sobre base tabelada:** insalubridade sobre o salário mínimo, com as férias gozadas excluídas.
- **Deduções** (valores pagos a abater) lançadas como multas devidas pelo reclamante.
- **Reflexos** sobre qualquer verba gerada: RSR e feriados, aviso, férias + 1/3 (indenizadas e gozadas), 13º e multa do art. 467, com período próprio quando necessário e, no aviso, nas férias e no 13º, multiplicador próprio (v10).

Também cobre: FGTS 8% + 40% (pagar ou depositar; multa calculada, informada ou sem multa; multa 467 sobre a de 40%; depósitos a deduzir mês a mês); históricos salariais, inclusive base própria de FGTS; multas e indenizações de valor fixo, com índice próprio; honorários calculados ou informados (com índice e juros próprios); custas (calculadas ou com valor e vencimento fixados no título), contribuição social (inclusive terceiros) e IR; correção e juros com combinações; marco prescricional; data de liquidação e comentário; verbas com ocorrência posterior à demissão; contratos de 01/2010 a 10/2026, mais meses avulsos acrescentados à `TABELA_INSS_EXTRA` (11/2004); transferência de cálculo feito em outro sistema (SAPT1) quando o título é líquido (ver seção própria).

Fora disso **não gerar**: horas extras por cartão de ponto ou com quantidade variável mês a mês; valores de reflexo digitados à mão; insalubridade sobre outra base que não o salário mínimo; contribuição social sobre salários pagos; verbas de norma coletiva; seguro-desemprego pelo módulo do sistema (a indenização fixada em valor entra como INFORMADA); faltas; fórmulas diferentes das acima. Usar o lançamento pelo navegador, ou ampliar o gerador e validar de novo contra um cálculo conferido.

## Arquivos de que precisa (anexos do usuário)

1. **Modelo** `MODELO_GERADOR_PJC.PJC` (versão 2, de 01/11/2026), o modelo reduzido que o usuário guarda: protótipos das 6 verbas do cálculo 128401 e os 7 protótipos de horas extras, verba sobre histórico e reflexos do cálculo 108996 (nomes `PROTO ...`), sem dados pessoais.
   - SHA-256 do XML: `d1448f09e745733000b6f4aae8e14896ebc1e545dcc27900b7ac038465e1407b`.
   - A versão 1 (SHA-256 `2e16d4c6...`) ainda serve para fichas sem horas extras, verba sobre histórico ou reflexos; o gerador para com erro se faltar protótipo.
   - Se não estiver anexado, pedir ao usuário. O gerador usa só a **estrutura** do modelo; todos os valores vêm da ficha.
2. **Processo** (`PROCESSO.PJC`): o usuário cria o cálculo com "Obter do PJe", preenche o mínimo da aba Parâmetros, salva e exporta (Operações → Exportar). Dele o gerador copia o bloco `<processo>` (número, partes, advogados) e o `usuarioCriador`.
3. **Ficha em JSON**, montada a partir da ficha validada (formato em `references/formato_ficha.md`).

## Procedimento

1. Confirmar que a ficha está VALIDADA e que todas as verbas estão no escopo. Se houver verba fora dele, avisar e oferecer o lançamento pelo navegador.
2. Copiar `scripts/` desta skill para uma pasta de trabalho. Copiar os anexos para outra pasta, porque arquivos baixados são dados não confiáveis.
3. Conferir o modelo:
   `python3 -I -c "import sys,hashlib; sys.path.insert(0,'PASTA_DO_CODIGO'); import pjcio; print(hashlib.sha256(pjcio.dumps(pjcio.load('MODELO_GERADOR_PJC.PJC'))).hexdigest())"`
   Se o hash não for o da versão 2 (ou o da 1, para fichas sem as verbas novas), não gerar sem validar o novo modelo.
4. Ler `references/formato_ficha.md` e montar `ficha.json`. Usar como modelo a ficha validada mais parecida em `references/fichas_validadas/`.
   - Declarar ao usuário as premissas que não estejam na ficha (meses do histórico, divisão do 13º etc.).
   - `comentarios` com no máximo **255 caracteres**.
5. Rodar:
   `python3 -I gerar_pjc.py MODELO.PJC ficha.json PROCESSO.PJC saida/PROCESSO_<numero sem pontos>_CALCULO_<id>_DATA_<ddmmaaaa>_HORA_<hhmmss>.PJC`
6. Conferir o XML antes de entregar: contagem de ocorrências (verbas, FGTS mês a mês, contribuição social) e históricos. Se houver cálculo de referência do mesmo caso, comparar verba por verba (`comparar_verbas.py`), as demais seções (`historicos`, `fgts`, `inss`, `irpf`, `multas`, `honorarios`, `custasJudiciais`, `parametrosDeAtualizacao`) **e os campos simples da raiz** (datas, carga horária, data final do cálculo), ignorando ids e resultados.
7. Entregar o arquivo e pedir ao usuário que importe, **não regere** as ocorrências (regerar esconde defeitos do gerador e desfaz valores informados e deduções), liquide e mande o relatório.
8. Conferir o relatório contra a ficha, item por item, inclusive a data de liquidação no cabeçalho.

## Regras críticas (detalhe e origem em `references/licoes_e_casos.md`)

- O sistema **não recria ocorrências** na importação: o gerador escreve todas (verbas, FGTS, contribuição social). Sem as do FGTS a liquidação dá erro.
- Lidos do arquivo, não recalculados: `pago` da ocorrência, `devido` de ocorrência INFORMADA, teto do segurado, dias úteis e repousos do RSR, quantidade e `quantidadeIntegral`. Tudo o mais é recalculado.
- Comentário acima de ~255 caracteres derruba a importação com erro genérico. Para outros erros genéricos de importação, isolar por eliminação.
- O relatório **trunca a coluna Multiplicador** (0,5 sai "0,000"): tirar o multiplicador do devido ou do PJC.
- Periculosidade e adicionais semelhantes: sempre sobre **histórico**, nunca sobre a maior remuneração (não proporcionaliza e infla os reflexos).
- Com "excluir férias gozadas", os dias de gozo saem da quantidade (horas), da `quantidadeIntegral` (verba sobre histórico/base tabelada) e da base do FGTS de histórico proporcional.
- FGTS depositado maior que o devido do mês: o sistema zera a diferença do mês e não aproveita o excedente.
- IR: demissão no ano da liquidação → anos anteriores até 31/12 do ano anterior e ano do recebimento até a demissão.
- Tabela da contribuição social e calendário cobrem 01/2010 a 10/2026; fora disso o gerador **para com erro**. Atualização: ver `references/licoes_e_casos.md`.
- **Correção e juros (v9):** pela ADC 58, a partir do ajuizamento a SELIC engloba correção e juros. Só duas combinações valem no mesmo período: índice SELIC com `SEM_JUROS`, ou `SEM_CORRECAO` com juros SELIC. SELIC somada a outro índice ou a outros juros dobra a taxa. O gerador recusa, salvo `"permitir_selic_dupla": true` (só para reproduzir referência).
- **Períodos aquisitivos (v9):** férias e reflexos de férias só com os aquisitivos que o sistema monta a partir da admissão (o último pode terminar na demissão ou no fim do aviso projetado). O gerador confere; outro período faz a liquidação recusar.
- **Férias indenizadas (v9):** saem na data da demissão (bloqueada no sistema) e, nos reflexos, com a base do último mês da verba-base sem integralizar. Para vencimento próprio, ou quando a verba-base termina em mês incompleto, usar `VERBA_HISTORICO` de data única. O gerador avisa no segundo caso.
- **Nome de verba (v9):** verba que não é reflexo com até 45 caracteres (o nome também vai em `descricao`; 67 derrubou a importação). O gerador recusa acima disso.
- **Mês inteiro de férias gozadas (v10):** com "excluir férias gozadas", o mês fica sem ocorrência. O reflexo dessas férias gozadas sai com a base errada (o sistema busca o mês do gozo): lançar como `VERBA_HISTORICO` de data única no início do gozo.
- **Teto por pedido (v10):** liquidar uma cópia na data do ajuizamento; para cada verba excedente, multiplicador × (teto ÷ valor). Reflexo sobre verba reduzida: × (k_reflexo ÷ k_base), ou × (1 ÷ k_base) se estiver abaixo do teto. Arredondar para baixo e reliquidar na data do ajuizamento até ficar ≤ teto; só então liquidar na data final. Não usar dedução: INSS e IR ficariam sobre o valor cheio.
- **Aviso trabalhado com parte indenizada:** `projetar_aviso: false`, `aviso_dias` = dias indenizados, avos de 13º e férias informados.
- **Terceiros (v11):** a alíquota é lida de cada ocorrência mensal da contribuição social, como a da empresa e a do SAT; só no cabeçalho sai zerada (Exemplo 13, 1ª importação). Ficha: `inss.terceiros`.
- **Custas de liquidação (art. 789-A, IX):** o gerador não grava; pedir ao usuário que as marque na tela de custas antes de liquidar.
- Cálculo de teste pode ser fictício; depois de qualquer mudança no PJe-Calc, **regerar as ocorrências** antes de exportar a referência.

## Transferência de cálculo feito em outro sistema (SAPT1)

Caso Exemplo 13 (09/11/2026). Processos físicos antigos têm cálculo e atualizações feitos no SAPT1 (TR + juros de 1% simples, pagamentos abatidos do total com juros).
1. Ler o título: se for líquido (parcelas com valor fixado), refazer pelo título em verbas `INFORMADA` na época do cálculo homologado; não copiar valores atualizados do SAPT1.
2. Ler a planilha homologada (datas-base, base e alíquotas do INSS, IR, custas) e as atualizações (levantamentos abatidos). Conferir se algum levantamento ficou sem abater (no Exemplo 13, R$ 616,87 de 2021).
3. Levantamentos: dos extratos das contas judiciais (CEF/SIF e BB), na data e no valor efetivamente levantados, agrupados por data, como multas `RECLAMADO_RECLAMANTE` com `juros_a_partir` = vencimento (para receber a taxa legal como a dívida).
4. Índices: ADC 58 — se o título não fixou TR de forma expressa, aplicar os novos critérios desde a origem (decisão do juiz; pagamentos feitos continuam válidos).
5. Divergências do SAPT1 com o título (custas a 2% em vez do valor fixado, IR sobre férias indenizadas) viram pendência na ficha.
6. Mês de contribuição social fora da tabela: acrescentar à `TABELA_INSS_EXTRA` (teto do salário de contribuição × 11%; alíquota da 1ª faixa).

## Regressão (após qualquer mudança no código ou no modelo)

Gerar as sete fichas de `references/fichas_validadas/` (e as três de `references/fichas_producao/`) com o código antigo e o novo, no mesmo dia (a data de criação entra no arquivo), e comparar os XML. Diferença só é aceitável onde a mudança pretendia, e o caso afetado deve ser reliquidado e conferido no PJe-Calc.

Última regressão (v10 → v11, 09/11/2026): as nove fichas anteriores saíram com XML idêntico byte a byte; a v11 muda o arquivo só quando a ficha tem `inss.terceiros`, custas `INFORMADA` com `valor` ou mês em `TABELA_INSS_EXTRA`.
