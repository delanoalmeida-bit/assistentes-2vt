# Lições dos testes e casos validados

Consultar ao montar ficha com verba nova, ao investigar diferença no relatório ou ao ampliar o gerador.

## Casos validados (detalhe)
- **[processo Exemplo 10]** (31/10/2026). O arquivo gerado (cálculo 128429) deu relatório idêntico, linha a linha, ao do lançamento pelo navegador (cálculo 128425). Total: R$ 45.510,17.
- **[processo Exemplo 08]** (01/11/2026). Reprodução do cálculo homologado 108996: horas extras 50% com reflexos em RSR, aviso, férias + 1/3 e 13º; diferença salarial com reflexos; multa do art. 467 sobre quatro verbas. O arquivo gerado (cálculo 128458) deu relatório idêntico, valor por valor, ao do próprio 108996 reliquidado na 2.16 (cálculo 128454): R$ 73.053,50 em 31/07/2025.
- **[processo Exemplo 04]** (01/11/2026). Reprodução do cálculo 63343 (feito na 2.7.1, reliquidado na 2.16): horas extras sobre comissões e sobre o salário fixo, com reflexos e "repercussões" lançados como coeficientes mensais sobre histórico; 36 deduções de horas extras pagas; dano moral com data posterior à demissão. O arquivo gerado (cálculo 128462) deu relatório idêntico em valores ao do 63343: bruto R$ 171.258,39, total devido pelo reclamado R$ 216.154,13 em 31/08/2021.
- **[processo Exemplo 03]** (02/11/2026). Reprodução do cálculo 121044 (Calculista do Juízo, feito na 2.14, reliquidado na 2.16): comissionista puro, adicional de horas extras de 50% sobre o histórico de comissões com os **reflexos do próprio sistema** (RSR, aviso, férias + 1/3, 13º); aviso, férias, 13º e multa do art. 477 com base no histórico de comissões; multa do art. 467 sobre aviso, férias, 13º e multa de 40% do FGTS; FGTS a depositar. O arquivo gerado (cálculo 128476) deu relatório idêntico, valor por valor, ao do 121044 reliquidado na 2.16: bruto R$ 229.492,42, total devido pelo reclamado R$ 286.800,84 em 31/05/2026.
- **[processo Exemplo 07]** (02/11/2026). Reprodução do cálculo 123781 (feito e reliquidado na 2.16): adicional de insalubridade de 20% sobre o salário mínimo (tabela do sistema), com as férias gozadas excluídas, reflexos em férias + 1/3 (cinco períodos gozados e as indenizadas) e em 13º, honorários advocatícios calculados e periciais de valor fixo. O arquivo gerado (cálculo 128477) deu relatório idêntico, linha a linha, ao do 123781: bruto R$ 14.288,32, total devido pelo reclamado R$ 22.316,79 em 31/07/2026.
- **Cálculo fictício 128483** ([processo Exemplo 11], 03/11/2026), montado no PJe-Calc só para validar o gerador: periculosidade de 30% sobre histórico de salário-base, adicional noturno de 20% e intervalo intrajornada (divisor pela carga horária, quantidade proporcional), reflexos do noturno em RSR, aviso, férias e 13º, férias gozadas no meio do contrato e depósitos de FGTS a deduzir. O arquivo gerado (cálculo 128491) deu relatório idêntico, linha a linha: bruto R$ 22.820,43, total devido pelo reclamado R$ 27.736,09 em 30/11/2026.
- **[processo Exemplo 06]** (01/11/2026). (Desde a v8 o arquivo deste caso sai com as datas do IR na regra nova; ver "IR" abaixo. Reliquidar e conferir se for reutilizado.) O arquivo gerado (cálculo 128448) bateu com a planilha homologada, verba por verba. Total: R$ 23.326,10 em 31/10/2026. O caso tem verbas informadas, dedução de férias pagas, FGTS a depositar e multa de 40% informada.

- **Atenção ao Exemplo 04 (confirmado):** a correção combina SELIC como índice (desde 02/06/2020) e juros SELIC (desde 03/06/2020), como o cálculo de referência 63343. O erro estava no 63343 desde 2021 (versão 2.7.1, "SELIC (Fazenda Nacional)" nos dois) e passou a todas as atualizações; a de 03/07/2026 mostrava juros de 10,22% de 01/09/2021 a 19/09/2022, a própria SELIC do período, sobre capital já corrigido pela SELIC. Reliquidado em 03/11/2026 (atualização 128538), com SEM_JUROS até 29/08/2024 e IPCA + taxa legal depois: total devido de R$ 323.623,18, contra R$ 473.241,81 na atualização de 03/07/2026. Lição: atualizações herdam a parametrização do cálculo original; corrigir na origem e reliquidar a atualização com os mesmos eventos de pagamento. A ficha validada leva `"permitir_selic_dupla": true` só para continuar reproduzindo a referência.
- **Atenção ao Exemplo 03 (confirmado):** a referência 121044 (sentença líquida de 26/05/2026, conta ID 540c515, homologada em 11/09/2026) manteve o índice IPCA-E até 29/08/2024 e aplicou juros SELIC simples de 19/03/2024 a 29/08/2024, contra a própria sentença (SELIC sem cumulação, vedado outro índice). Corrigido em 03/11/2026 com índice "Sem Correção" de 19/03/2024 a 29/08/2024: total devido de R$ 282.799,66 em 31/05/2026, contra R$ 286.800,84 do original reliquidado na 2.16 (efeito da correção: R$ 4.001,18) e R$ 284.961,94 na conta homologada (versão 2.14). A ficha validada leva `"permitir_selic_dupla": true` só para continuar reproduzindo a referência.
- **Reliquidar em cópia.** Ao corrigir cálculo homologado, trabalhar numa cópia no PJe-Calc; alterar o próprio cálculo deixa o sistema diferente da conta juntada aos autos enquanto o juiz não decide.

## Caso de produção conferido (sem cálculo de referência)
- **[processo Exemplo 05]** (03/11/2026). Periculosidade sobre histórico de salário-base com férias gozadas e reflexos; salários, 13º e férias do período de afastamento de uma dispensa anulada (reintegração); reflexo da periculosidade nas horas extras pagas como verbas informadas mês a mês; deduções do TRCT; dano moral com correção desde o arbitramento; multa por ED protelatórios a cargo do reclamante. Cálculo final 128537, conferido item a item contra a ficha validada: total devido pelo reclamado R$ 145.937,62 em 03/11/2026. Ficha em `references/fichas_producao/ficha_exemplo_05.json`. Lições:
  - **SELIC dupla.** Com SELIC nas combinações de índice e SELIC nas de juros, o relatório informa "corrigidos pelo índice SELIC até 29/08/2024" e "juros SELIC até 29/08/2024": a SELIC entra duas vezes (índice acumulado de 1,81 desde 06/2017 e juros de 45%). Com `SEM_JUROS` de 03/06/2022 a 29/08/2024, os juros caíram para 18,9% e o total de R$ 168.907,95 para R$ 145.094,19. O gerador recusa a combinação desde a v9.
  - **Período aquisitivo das férias.** Reflexo em férias indenizadas com aquisitivo 25/06/2021 a 01/02/2022 (data de dispensa anulada; demissão do cálculo em 02/10/2023): a liquidação recusou ("O período aquisitivo das verbas com característica de Férias está diferente do período aquisitivo gravado na página Férias"), com ou sem o período na página Férias. O sistema só aceita os aquisitivos que ele monta a partir da admissão. O gerador confere desde a v9.
  - **Base do reflexo em férias indenizadas.** O sistema usa o valor do último mês da verba-base, sem integralizar a fração, qualquer que seja a data da ocorrência (01/02/2022 e 31/01/2022 deram a mesma base de R$ 20,23, um dia de fevereiro). Nas férias gozadas a base do mês do gozo sai integralizada. Solução: `VERBA_HISTORICO` de data única (R$ 2.023,00 ÷ 12 × 0,4 × 7 = R$ 472,03).
  - **Data das férias indenizadas.** `FERIAS` e reflexos de férias indenizadas saem na data da demissão e a data fica bloqueada para edição no sistema. A alteração direta no XML importou, mas não resolve a base (item anterior). Para vencimento próprio, usar `VERBA_HISTORICO` de data única.
  - **Nome de verba.** Verba sobre histórico com nome de 67 caracteres: importação recusada com o erro genérico, duas vezes; com 44, importou. O nome vai em `nome` e `descricao`; reflexos (só `nome`) importaram com até 74 (Exemplo 03). O gerador limita a 45 desde a v9.
  - **Lançamento pelo navegador do app.** O PJe do TRT-16 é tratado como site de alto risco: cada ação exige aprovação do usuário, o que inviabiliza lançar dezenas de ocorrências. Preferir verbas informadas no PJC.
  - **Horas extras nos contracheques do Atacadão.** A coluna de referência das horas extras vem em horas:minutos (1,40 = 1h40); converter para decimal e conferir contra o valor pago.

- **[processo Exemplo 01]** (05/11/2026). Sentença líquida (minuta), adicional de insalubridade de 40% sobre o salário mínimo com férias gozadas, reflexos em aviso (12 dias indenizados de aviso trabalhado), 13º e férias + 1/3, FGTS não depositado sobre histórico próprio, **teto por pedido** (valor da inicial na data do ajuizamento). Cálculo final 128639: total devido pelo reclamado R$ 62.936,75 em 05/11/2026. Ficha em `references/fichas_producao/ficha_exemplo_01.json`. Lições:
  - **Mês inteiro de férias gozadas** (fevereiro de 2023 e de 2024, gozo de 01/02 a 02/03 e de 01/02 a 01/03): com "excluir férias gozadas", não sobra dia no mês e a v9 parava com divisão por zero. Desde a v10 o mês fica sem ocorrência; o PJe-Calc importou e liquidou sem o mês, como esperado.
  - **Reflexo em férias gozadas cujo gozo cobre um mês inteiro:** o sistema toma como base o adicional do mês do gozo; sem ocorrência no mês, a base saiu com os dias de março (R$ 34,72 e R$ 18,83 em vez de R$ 520,80 e R$ 564,80). Solução: `VERBA_HISTORICO` de data única no início do gozo, base SALARIO_MINIMO, multiplicador 0,4 × 4/3 = 0,53333333, com INSS e IR (R$ 694,40 e R$ 753,07). Os períodos com gozo parcial no mês continuam como `REFLEXO`.
  - **Projeção do aviso trabalhado:** com aviso de 42 dias, 30 trabalhados e 12 indenizados, `projetar_aviso: false`, `aviso_dias: 12`, reflexo AVISO com `dias: 12` e avos de 13º e férias informados um a um. O sistema mostra "Prazo de Aviso Prévio: Calculado" e não projeta.
  - **Base dos reflexos no mês incompleto da demissão** (20 dias de dezembro): no 13º e no aviso a base saiu integralizada (R$ 607,20), com os padrões de base fixa (valor mensal, fração integralizada). Nas férias proporcionais (indenizadas) o problema conhecido continua: usar `VERBA_HISTORICO` de data única.
  - **Teto por pedido (limitação aos valores da inicial):** liquidar uma cópia na data do ajuizamento, calcular k = teto ÷ valor de cada verba excedente e multiplicar o multiplicador por k. Reflexos sobre verba reduzida: multiplicador × (k_reflexo ÷ k_base); reflexo abaixo do teto: × (1 ÷ k_base), para não cair junto. Assim INSS e IR incidem só sobre o valor limitado (a dedução como multa deixaria as incidências sobre o valor cheio). O resultado é quase linear em k; a contribuição progressiva do segurado (os juros incidem após a dedução) deixou o adicional R$ 0,07 acima; arredondar o multiplicador para baixo e reliquidar na data do ajuizamento. Desde a v10 o `REFLEXO` aceita `multiplicador`; o sistema leu 0,98090541 (13º), 1,04176049 (aviso) e 1,29270700 (férias).
  - **Multa de 40% com a já paga a deduzir:** comparar 40% de todos os depósitos devidos (extrato + FGTS deferido) com a multa já depositada; aqui deu R$ 2.819,79 contra R$ 3.194,03 pagos, sem saldo, e o FGTS saiu com `multa: null` e explicação no comentário.


## O que os testes mostraram sobre o formato

**Estrutura do arquivo**
- O PJC é um ZIP com uma única entrada XML: ISO-8859-1, acentos como entidades numéricas, datas em milissegundos à meia-noite de Brasília. `pjcio` lê e grava de forma idêntica byte a byte.

**O que o sistema recalcula e o que lê do arquivo**
- Podem ser omitidos, porque o sistema recalcula: `gprec`, `dadosEstruturados`, `apuracoesDeJuros` e o hash (`null`).
- Devidos calculados, bases e índices gravados nas ocorrências são recalculados.
- O `pago` gravado na ocorrência **é usado**. Assim funciona a dedução de férias já pagas.
- O `devido` de ocorrência com `valor` = INFORMADO também é usado. A tag-filha de `verbaDeCalculo` precisa ser `Informada` ou `Calculada`, igual à verba.
- Ids podem ser quaisquer números únicos, porque a importação cria novo cálculo e novos ids.

**Ocorrências**
- O sistema **NÃO recria ocorrências na importação.**
  - Sem ocorrências, as verbas saem zeradas.
  - Sem as ocorrências do FGTS, a liquidação dá erro.
  - O gerador escreve todas: verbas, FGTS e contribuição social. Isso também preserva desativações, como a de férias gozadas, que simplesmente não são geradas.

**Importação recusada**
- Comentário longo derruba a importação inteira com "Erro. A operação não pôde ser concluída e o cálculo não foi importado". Não há mensagem que aponte a causa.
- Teste de 01/11/2026: 242 caracteres importou; 450 não. O gerador recusa acima de 255.
- Nome de verba não reflexa acima de 45 caracteres também derruba a importação (Exemplo 05); o gerador recusa.
- Se a importação falhar com esse erro genérico por outro motivo, isolar por eliminação: gerar variantes, cada uma sem um elemento novo, e ver qual importa.

**Dados que vêm do modelo e precisam ser trocados**
- O histórico de validação (`historicosValidacao`), as datas de criação e de liquidação e o `usuarioCriador` são do cálculo-modelo. O gerador limpa o histórico de validação.
- A data de liquidação é `data_liquidacao` da ficha ou, se ausente, o dia da geração.
- O `usuarioCriador` vem do PJC do processo.

**Contribuição social: teto e alíquota do segurado**
- O teto (`valorTetoSegurado`) é **lido do arquivo**, não recalculado. Ele limita a contribuição do segurado em cada mês: G = menor entre (teto − contribuição sobre salário pago) e (salário de contribuição × alíquota).
- A alíquota sobre o salário devido é **recalculada** pelo sistema conforme a faixa. Teste Q, 01/11/2026: salário de R$ 3.000,00 em 2019, gravado com 8%, liquidou a 11% (R$ 330,00 por mês).
- O gerador grava teto e alíquota a partir de `TABELA_INSS`, extraída do próprio PJe-Calc (cálculo de referência 128449, cobertura de 01/2010 a 10/2026). Fora da cobertura, o gerador **para com erro**, sem chutar.
- Atualizar a tabela (em janeiro de cada ano, ou quando o gerador parar):
  1. o usuário cria um cálculo descartável com admissão em 01/01/2010 e demissão na data mais recente aceita;
  2. na Contribuição Social, coloca os períodos dos salários devidos e dos salários pagos cobrindo o contrato todo; regera, salva e exporta;
  3. rodar `python3 -I extrair_tabela_inss.py CALCULO.PJC` e substituir as três linhas `TABELA_INSS*` em `scripts/gerar_pjc.py`.
- O gerador não escreve ocorrências de **salários pagos**: a contribuição sobre salário pago fica zero. Isso está correto enquanto não houver salário pago a considerar. Se um caso exigir, ampliar e testar antes.

**Horas extras e reflexos (testes S0, S1 e T, 01/11/2026)**
- Reflexo é um tipo próprio de verba (`Reflexo`, com `FormulaReflexo`); a base é outra verba, ligada por `ItemBaseVerba`. O gerador escreve primeiro a verba-base completa e, no reflexo, só a referência; o sistema importou assim sem problema.
- As **bases** dos reflexos (médias) são recalculadas na liquidação. Os **dias úteis (divisor) e repousos (quantidade) do RSR são lidos do arquivo**: teste S1, com 30 e 1 gravados, derrubou o RSR de 6.832,18 para 1.069,05. Por isso o gerador calcula o calendário (`calendario.py`).
- Calendário de São Luís-MA no PJe-Calc: domingos; feriados nacionais (Consciência Negra, 20/11, só a partir de 2024); 28/07 (estadual); 29/06 e 08/09 (municipais); pontos facultativos Carnaval (só a terça), Sexta-feira Santa e Corpus Christi. **08/12 e 24/06 não são feriados no sistema.** Sábado é dia útil. Validado contra os 202 meses do cálculo-calendário 128456 (01/2010 a 10/2026), sem divergência; fora desse intervalo o gerador para. Para ampliar: cálculo descartável com horas extras e o reflexo de RSR ativo, regerar, exportar, conferir.
- Meses incompletos: horas extras = quantidade × dias / 30; `quantidadeIntegral` = quantidade cheia. RSR, verba sobre histórico e multa do art. 467 gravam `quantidadeIntegral` = quantidade × 30 / dias.
- Parâmetros de média do reflexo dependem da base: base **variável** (horas extras) usa os padrões do protótipo (média pela quantidade; últimos 12 meses no aviso, período aquisitivo nas férias, ano civil no 13º; fração mantida; base integralizada). Base **fixa** (diferença salarial) usa valor mensal, período aquisitivo, fração integralizada e base não integralizada. A multa do art. 467 usa valor mensal; sobre o saldo de salário, base não integralizada (`"integralizar": "NAO"` na ficha). Todos podem ser forçados na ficha.
- Avos dos reflexos podem diferir da verba principal: no 108996, férias proporcionais principais com 6/12 (sentença) e reflexos com 7/12 (com a projeção do aviso). A ficha traz os avos de cada reflexo.
- Cálculo feito na 2.13.2 e reliquidado na 2.16 muda o valor corrigido (índices revistos): o 108996 homologado dava R$ 72.688,73 e, reliquidado na 2.16 na mesma data, R$ 73.053,50, com devidos idênticos. Para validar, comparar com o cálculo reliquidado na 2.16, não com o relatório antigo.
- Ano do recebimento no IR (`dataInicioAnoRecebimento`) = ano da liquidação; vencimento dos honorários = data da liquidação.

**Cálculos antigos com coeficientes e deduções (testes U e U2, 01/11/2026)**
- Ocorrência de verba depois da demissão exige `dataTerminoCalculo` igual ou posterior a ela; sem isso o sistema recusa a liquidação ("As ocorrências das verbas não podem ultrapassar a data da demissão..."). O gerador põe a data da última ocorrência, ou a de `contrato.termino_calculo`.
- Contribuição social: a ocorrência de 13º em dezembro só existe durante o contrato; o período de salários devidos pode ir além da demissão (no 63343, até a data do dano moral).
- Sem verba com incidência de IR, as datas de anos anteriores do IR ficam nulas.
- Quantidade proporcional nos meses incompletos = quantidade × dias / 30 (o sistema grava com 25 casas; o gerador, com 10 — diferença sem efeito). Quantidade não proporcional: fica cheia, e `quantidadeIntegral` = quantidade × menor(30, dias do mês) / dias (ver teste V).
- Deduções lançadas como multa: `tipoCredorDevedor` = RECLAMADO_RECLAMANTE (entram negativas no bruto). Juros a partir do ajuizamento, como no original.
- Histórico "ÚLTIMA REMUNERAÇÃO" é criado sempre que a ficha traz `ultima_remuneracao` (aparece como coluna a mais no relatório quando nenhuma verba o usa; sem efeito em valores).

**Comissionista com reflexos do sistema (teste V, 02/11/2026)**
- O relatório do PJe-Calc **trunca a coluna Multiplicador**: 0,5 sai "0,000" e 1,5 sai "1,000". Ao montar ficha a partir de relatório, tirar o multiplicador do devido (ex.: 8.823,99 ÷ 220 × 0,5 × 42,8 = 858,33), ou do PJC.
- Histórico com incidência de FGTS proporcional: a base do FGTS do mês incompleto é valor × dias / 30 (outubro/2021, 28 dias: 8.235,72). O gerador grava assim.
- Horas extras proporcionais: o sistema grava a quantidade sem arredondar (39,9466…); o gerador grava com 10 casas.
- Verba sobre histórico de data única num mês de 28 dias: `quantidadeIntegral` = quantidade × 28 (16 × 28 = 448); regra adotada: quantidade × menor(30, dias do mês) / dias.
- O PJC pode trazer no conjunto de verbas uma referência vazia (`<internalRef />`) quando a verba (aqui, o 13º) só está definida dentro de um reflexo que a usa como base. `comparar_verbas.py` e `dump_calc.py` acham a verba pelo id.
- Diferenças só de rótulo no relatório (sem efeito em valor): "X QUANTIDADE" no original contra "X AVOS" no gerado, nas fórmulas de férias e 13º.

**Insalubridade sobre o salário mínimo (teste W, 02/11/2026)**
- Base `SALARIO_MINIMO` na `baseTabelada` da fórmula, sem histórico vinculado; o sistema aplica o salário mínimo de cada mês (209,00 em 2020 a 20%, 264,00 em 05/2023). A proporcionalidade da base fica na própria `baseTabelada`.
- Com "excluir férias gozadas" (padrão), os dias de gozo saem do mês: `quantidadeIntegral` = 30 / dias restantes (março com gozo a partir do dia 4: 30/3 = 10; abril com gozo até o dia 2: 30/28). O gerador calcula a partir dos períodos de gozo da lista de férias.
- Reflexo em férias gozadas: ocorrência no período de gozo, com o período aquisitivo, `quantidadeIntegral` = avos (não avos × 30) e `feriasIndenizadas` = false.
- O período do reflexo pode ir além do da verba-base (aqui, até a demissão); os reflexos de anos sem adicional saem zerados, como no original.
- Honorários periciais informados: valor, vencimento, outro índice (IPCA) e juros a partir de data própria.
- Início e fim do cálculo (aba Parâmetros) vêm da ficha (`inicio_calculo`, `termino_calculo`); aqui o fim (31/05/2023) é anterior à demissão.

**Periculosidade, noturno, intervalo e FGTS a deduzir (teste X, 03/11/2026)**
- Cálculo de teste pode ser fictício: o que se valida é se o gerador reproduz o sistema, não o mérito. Montar no PJe-Calc, **regerar as ocorrências** de todas as verbas depois de qualquer mudança (inclusive de férias), liquidar e exportar. Sem regerar, o arquivo fica com ocorrências antigas (no teste, o gozo lançado não chegou às verbas na primeira exportação).
- Periculosidade sobre a **maior remuneração** não se proporcionaliza nos meses incompletos (3 dias de março saíram com os 900,00 cheios) e os reflexos integralizam a fração (aviso de 9.900,00 sobre salário de 3.000,00). Sobre histórico de salário-base com proporcionalidade, saiu correto. Preferir sempre o histórico.
- Horas proporcionais (noturno, intervalo) com "excluir férias gozadas": quantidade = horas × (dias − dias de gozo) / 30 (outubro com 17 dias fora do gozo: 1,5 × 17/30 = 0,85); `quantidadeIntegral` = horas cheias.
- Verba sobre histórico não proporcional: `quantidadeIntegral` = menor(30, dias do mês) / dias restantes depois do gozo (outubro: 30/17).
- Base de FGTS de histórico proporcional também perde os dias de gozo (3.000,00 × 17/30 = 1.700,00).
- Depósito de FGTS maior que o devido do mês: o sistema zera a diferença do mês e não aproveita o excedente nos outros meses.
- Alíquota do segurado: o sistema grava a alíquota efetiva (8,45%, 7,66%...), recalculada na liquidação; o gerador grava a da tabela.
- RSR sobre o noturno conferido com o calendário nos 17 meses (inclui 20/11/2025 e o feriado de 15/11 em sábado).

**Arredondamento**
- 13º na base do FGTS: o adiantamento vai em novembro, com o meio centavo arredondado para cima; dezembro leva o resto. Assim fica igual ao lançamento manual.

**IR**
- Com verbas do mesmo ano do recebimento, a tributação sai normal (art. 12-B), não RRA. É o comportamento do sistema; conferir no relatório.
- Demissão no ano da liquidação: o sistema grava os anos anteriores até 31/12 do ano anterior e o ano do recebimento até a demissão (128483). O gerador faz o mesmo desde a v8; antes, gravava a demissão como fim dos anos anteriores.


**Transferência do SAPT1 (Exemplo 13-16.2004, 09/11/2026)**
- Sentença líquida de 2005 refeita em 10 verbas INFORMADA em 11/2004 (época do cálculo homologado), multa cominatória de R$ 500,00 como multa ao reclamante e 6 levantamentos como deduções; ADC 58 desde a origem (IPCA-E + juros até o ajuizamento, SELIC até 29/08/2024, IPCA + taxa legal). Relatório conferido item a item: total devido pelo reclamado R$ 8.163,07 em 09/11/2026.
- 1ª importação: terceiros zerados. O sistema lê `aliquotaTerceiros` de cada ocorrência de `inssSobreSalariosDevidos` (como `aliquotaEmpresa` e `aliquotaSAT`); gravar só `aliquotaTerceirosFixa` no cabeçalho não basta.
- Custas INFORMADA: `valorConhecimentoDoReclamado` e `dataVencimentoConhecimentoDoReclamado` são lidos (R$ 60,00 em 03/02/2005 → R$ 183,35). Custas de liquidação marcadas na tela: 0,5% sobre bruto + débitos do reclamado.
- Teto do segurado de 11/2004 (R$ 275,96) acrescentado à mão: o sistema aplicou 9% sobre R$ 793,33 = R$ 71,40, igual ao SAPT1. Com o índice de correção da contribuição do segurado a recolher, igual ao das verbas.
- Deduções com `juros_a_partir` = vencimento recebem a mesma SELIC/IPCA e a taxa legal da dívida (abatimento pelo método das parcelas corrigidas, não imputação nos juros do art. 354 do CC).
- O PJe-Calc monta sozinho a tabela de férias a partir das datas do contrato (no Exemplo 13, um período "gozado"); sem efeito em verbas informadas, mas aparece no relatório: ajustar na tela se for juntar aos autos.

## Se for preciso refazer o modelo reduzido

O modelo atual tem duas camadas: (1) `reduzir_modelo.py` aplicado ao cálculo 128401; (2) `ampliar_modelo.py` acrescentando os protótipos de horas extras, verba sobre histórico e reflexos tirados do cálculo 108996 (Exemplo 08-40.2024). Refazer as duas etapas, nessa ordem, e validar os sete casos.


Redução da primeira camada (`scripts/reduzir_modelo.py`; a segunda é `scripts/ampliar_modelo.py`):

Isso só é preciso se o usuário trocar o cálculo-modelo, por exemplo numa nova versão do PJe-Calc. O cálculo de origem precisa ter as 6 verbas listadas em `need` no `reduzir_modelo.py`, um honorário, um histórico ÚLTIMA REMUNERAÇÃO, ocorrências de FGTS e de contribuição social e combinações de índice e de juros.

Depois de reduzir:
- rodar o gerador com o modelo novo e com o antigo, para as duas fichas de exemplo, e comparar as saídas;
- conferir que não sobrou dado pessoal (nomes, CPF/CNPJ, `usuarioCriador`);
- registrar o novo SHA-256 no SKILL.md.

