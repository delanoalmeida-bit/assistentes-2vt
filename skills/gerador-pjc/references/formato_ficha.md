## Formato da ficha

Campos de `contrato`:
- `marco_prescricional`: opcional. Se `null`, o período das verbas começa na admissão.
- `comentarios`: até 255 caracteres, ou `null`.
- `data_liquidacao`: opcional, no nível raiz da ficha (`"dd/mm/aaaa"`).

Tipos de verba (`verbas[].tipo`):
- `AVISO_PREVIO`: `fgts`, `inss`, `irpf`. Os dias vêm de `contrato.aviso_dias`.
- `FERIAS`: `periodos_indenizados` = `[[início_aquisitivo, fim, avos, pago?], ...]`.
  - O 4º elemento é opcional: valor já pago, a deduzir.
  - Férias gozadas não entram aqui; ficam só em `ferias` com situação GOZADAS.
- `MULTA_477`: sem campos.
- `SALDO_SALARIO`: `periodo`, `fgts`, `base` (ULTIMA_REMUNERACAO), `proporcionalizar`.
- `DECIMO_TERCEIRO`: `periodo`, `avos`, `base` (MAIOR_REMUNERACAO ou histórico), `fgts`.
- `SALARIO_RETIDO`: `periodo`, `fgts`, `base`. Gera uma ocorrência por mês.
- `INFORMADA`: verba de valor fixado.
  - `nome`;
  - `ocorrencias` = `[[data_inicial, data_final, valor], ...]`;
  - `pagamento`: MENSAL ou DESLIGAMENTO. Padrão: MENSAL se houver mais de uma ocorrência;
  - `fgts`, `inss`, `irpf`: padrão false;
  - `assunto_cnj`: opcional, ex.: 8823 saldo de salário, 2540 vale-transporte.

- `HORAS_EXTRAS`: `nome`, `periodo`, `quantidade_mensal`, `multiplicador` (padrão 1,5), `divisor` (número, padrão a carga horária; ou `"CARGA_HORARIA"`, que grava o tipo do sistema), `historico` (padrão ÚLTIMA REMUNERAÇÃO), `fgts`/`inss`/`irpf` (padrão true/true/false), `excluir_faltas_justificadas`, `excluir_faltas_nao_justificadas`, `excluir_ferias_gozadas` (padrão do protótipo), `assunto_cnj` (ex.: 2086 horas extras, 1663 adicional noturno, 2140 intervalo). Serve também para adicional noturno e intervalo.
- `VERBA_HISTORICO`: `nome`, `periodo`, `historico` (nome de um histórico da ficha), `multiplicador`, incidências, `assunto_cnj`. Uma ocorrência por mês; o sistema proporcionaliza a base nos meses incompletos.
- `REFLEXO`: `reflexo` (RSR, AVISO, FERIAS, DECIMO, MULTA_467), `base` (nome de verba já listada antes na ficha), `nome` opcional (padrão "<reflexo> SOBRE <base>"), incidências opcionais (padrão do protótipo), parâmetros opcionais `comportamento`, `periodo_media`, `fracao`, `integralizar`.
  - AVISO: `dias` opcional (padrão `aviso_dias`).
  - FERIAS: `periodos` = `[[início_aquisitivo, fim, avos], ...]` (indenizadas, na demissão); para férias gozadas, `[início_aquisitivo, fim, avos, início_gozo, fim_gozo]`.
  - `periodo` opcional (padrão o da verba-base).
  - `multiplicador` opcional (v10; AVISO, FERIAS e DECIMO): substitui o do protótipo (1; 1,33333333 nas férias) na fórmula e nas ocorrências. Uso: limitação ao teto do pedido (caso Exemplo 01).
  - DECIMO: `ocorrencias` = `[[data, avos], ...]` (20/12 de cada ano e a data da demissão).
  - RSR e MULTA_467: sem campos (as ocorrências seguem a base e o calendário).
- `VERBA_HISTORICO` (campos completos): `divisor` (padrão 1), `quantidade` (padrão 1), `proporcionalizar_quantidade` (padrão false), `proporcionalizar_base` (padrão true), `excluir_faltas_justificadas`, `excluir_faltas_nao_justificadas`, `excluir_ferias_gozadas` (padrão do protótipo: false, true, true). Uma verba de data única (ex.: FGTS de um mês, repercussão no saldo de salário) usa `periodo` com a mesma data nas duas pontas.
- `AVISO_PREVIO` e `MULTA_477`: `periodo` opcional (no 108996, só a data da demissão; sem ele, todo o contrato, como nos casos Exemplo 10 e Exemplo 06).
- `DECIMO_TERCEIRO`: `nome`, `inss` e `irpf` opcionais; `ocorrencias` opcional = `[[data, avos, ativa?], ...]` (padrão: uma, na demissão, com `avos`).
- `AVISO_PREVIO`, `FERIAS`, `MULTA_477`, `DECIMO_TERCEIRO`: `base` = MAIOR_REMUNERACAO (padrão), ULTIMA_REMUNERACAO ou o nome de um histórico da ficha.
- `FERIAS`: `multiplicador` opcional (padrão 1.33333333; o 121044 usa 1.3333).
- `VERBA_HISTORICO`: `base_tabelada` (ex.: SALARIO_MINIMO) em lugar de `historico`.
- `VERBA_HISTORICO` com `excluir_ferias_gozadas`: mês inteiro dentro do gozo não gera ocorrência (v10). O reflexo de férias gozadas desse período vai como `VERBA_HISTORICO` de data única no início do gozo (caso Exemplo 01).
- Honorários: `tipo` (padrão SUCUMBENCIAIS; ex.: ADVOCATICIOS, PERICIAIS_ENGENHEIRO) e `descricao` opcionais; para valor informado, `valor` em lugar de `aliquota`/`base`; `vencimento` (padrão a data da liquidação), `indice` (outro índice de correção) e `juros_a_partir` opcionais.

Restrições verificadas pelo gerador antes de gerar (v9; origem em `licoes_e_casos.md`, caso Exemplo 05):
- **Nome de verba que não é reflexo: até 45 caracteres.** O nome vai também para `descricao`, e um nome de 67 caracteres derrubou a importação com o erro genérico. Reflexos não gravam `descricao` e importaram com até 74.
- **Períodos aquisitivos** de `FERIAS` e de `REFLEXO` de férias: só os que o sistema monta a partir da admissão, ou seja, do aniversário da admissão até a véspera do seguinte; o último pode terminar na demissão ou no fim do aviso projetado. Outro fim (ex.: a data de uma dispensa anulada) faz a liquidação recusar com "período aquisitivo ... diferente do gravado na página Férias".
- **SELIC não se soma a outro índice nem a outros juros** (ADC 58). A partir do ajuizamento, só duas combinações valem no mesmo período: índice `SELIC` com juros `SEM_JUROS` (ex.: índice `[["SELIC", "<ajuizamento>"], ["IPCA", "30/08/2024"]]` e juros `[["SEM_JUROS", "<dia seguinte>"], ["TAXA_LEGAL", "30/08/2024"]]`), ou índice `SEM_CORRECAO` com juros `SELIC` (exemplo 7). Só para reproduzir um cálculo de referência com outra combinação: `"permitir_selic_dupla": true` em `correcao`.

Avisos (o gerador gera, mas avisa):
- Reflexo em **férias indenizadas** cuja verba-base termina em mês incompleto: o sistema toma como base o valor do último mês da verba, sem integralizar (Exemplo 05: um dia de fevereiro deu R$ 15,73 em vez de R$ 472,03). Lançar então como `VERBA_HISTORICO` de data única (histórico ÷ 12 × adicional × 1,3333 × avos, multiplicador já combinado; ex.: 0,3 × 1,3333 = 0,4).
- `FERIAS` e reflexos de férias indenizadas saem sempre com a ocorrência na data da demissão, e a data fica bloqueada no sistema. Férias com vencimento próprio (ex.: as do período de afastamento de uma dispensa anulada, devidas na reintegração) → `VERBA_HISTORICO` de data única naquela data, sem incidências.

Outros campos:
- `contrato.termino_calculo` e `contrato.inicio_calculo`: opcionais (`dd/mm/aaaa`).
- Históricos extras: `fixa` opcional (padrão false = variável); `proporcionalizar_inss` opcional (padrão false).
- `multas[]`: `descricao`, `valor`, `vencimento`, `juros_a_partir` (ou null), `credor_devedor` (padrão RECLAMANTE_RECLAMADO; dedução = RECLAMADO_RECLAMANTE), `indice` opcional (ex.: IPCA; sem ele, o índice trabalhista).
- `custas`: `reclamado_conhecimento` (CALCULADA_2_POR_CENTO, INFORMADA, NAO_SE_APLICA); com INFORMADA, `valor` e `vencimento` (v11; ex.: custas fixadas na sentença, Exemplo 13). Custas de liquidação: marcar na tela.
- `inss`: `devidos`, `pagos`, `empresa`, `sat` e, opcional, `terceiros` (v11; ex.: 5.8), gravado no cabeçalho e em cada ocorrência.
- `historicos.ultima_remuneracao`: opcional; sem ele o histórico ÚLTIMA REMUNERAÇÃO não é criado (e as verbas que o usam não podem ser geradas).

Campos de `fgts`:
- `destino`;
- `multa`: QUARENTA_POR_CENTO ou null (sem multa no FGTS);
- `multa_informada`: opcional. Se presente, a multa sai INFORMADA com esse valor;
- `incidencia`, `excluir_aviso_da_multa`, `inicio`, `fim`;
- `multa_467`: opcional (padrão false). Multa do art. 467 sobre a multa de 40%;
- `depositos`: opcional, `{"mm/aaaa": valor, ...}`, FGTS já depositado a deduzir no mês.

Exemplo 1, verbas calculadas (Exemplo 10):

```json
{
 "_fonte": "Ficha de Liquidação [processo Exemplo 10], validada em 30/10/2026 e revista em 31/10/2026",
 "contrato": {"admissao": "18/11/2019", "demissao": "10/10/2024", "ajuizamento": "16/10/2025", "maior_remuneracao": 1429.59, "ultima_remuneracao": 1429.59, "prescricao_quinquenal": true, "prescricao_fgts": true, "marco_prescricional": "16/10/2020", "aviso_dias": 42, "projetar_aviso": true, "fim_projetado": "21/11/2024", "carga_horaria": 220, "comentarios": null},
 "ferias": [{"relativa": "2019/2020", "aquisitivo": ["18/11/2019", "17/11/2020"], "situacao": "GOZADAS", "gozo": ["01/07/2021", "30/07/2021"]}, {"relativa": "2020/2021", "aquisitivo": ["18/11/2020", "17/11/2021"], "situacao": "INDENIZADAS"}, {"relativa": "2021/2022", "aquisitivo": ["18/11/2021", "17/11/2022"], "situacao": "INDENIZADAS"}, {"relativa": "2022/2023", "aquisitivo": ["18/11/2022", "17/11/2023"], "situacao": "INDENIZADAS"}],
 "historicos": {"ultima_remuneracao": {"valor": 1429.59, "inicio": "11/2019", "fim": "10/2024", "fgts": false, "inss": false}, "SALARIOS BASE FGTS": {"fgts": true, "inss": false, "proporcionalizar_fgts": false, "faixas": [["10/2020", "12/2020", 1111.77], ["01/2021", "12/2021", 1111.77], ["01/2022", "12/2022", 1224.73], ["01/2023", "04/2023", 1302.0], ["05/2023", "12/2023", 1320.0], ["01/2024", "04/2024", 1412.0], ["05/2024", "09/2024", 1429.59], ["10/2024", "10/2024", 476.53]], "decimo_terceiro_nov_dez": {"2020": 1111.77, "2021": 1111.77, "2022": 1224.73, "2023": 1320.0}}},
 "verbas": [{"tipo": "AVISO_PREVIO", "fgts": true, "inss": false, "irpf": false}, {"tipo": "FERIAS", "periodos_indenizados": [["18/11/2020", "17/11/2021", 12], ["18/11/2021", "17/11/2022", 12], ["18/11/2022", "17/11/2023", 12], ["18/11/2023", "21/11/2024", 12]]}, {"tipo": "MULTA_477"}, {"tipo": "SALARIO_RETIDO", "periodo": ["01/06/2024", "30/09/2024"], "fgts": false, "base": "ULTIMA_REMUNERACAO"}, {"tipo": "SALDO_SALARIO", "periodo": ["01/10/2024", "10/10/2024"], "fgts": false, "base": "ULTIMA_REMUNERACAO", "proporcionalizar": true}, {"tipo": "DECIMO_TERCEIRO", "periodo": ["01/01/2024", "10/10/2024"], "avos": 11, "base": "MAIOR_REMUNERACAO", "fgts": true}],
 "multas": [{"descricao": "DANO MORAL", "valor": 2000.0, "vencimento": "28/08/2026", "juros_a_partir": "28/08/2026"}],
 "fgts": {"destino": "PAGAR", "multa": "QUARENTA_POR_CENTO", "incidencia": "SOBRE_O_TOTAL_DEVIDO", "excluir_aviso_da_multa": false, "inicio": "16/10/2020", "fim": "10/10/2024"},
 "inss": {"devidos": ["16/10/2020", "10/10/2024"], "pagos": ["18/11/2019", "10/10/2024"], "empresa": 20, "sat": 3},
 "correcao": {"indice": "IPCAE", "outro_indice": "IPCA", "outro_a_partir": "30/08/2024", "juros_pre_judicial": true, "juros": "SEM_JUROS", "combinacoes_juros": [["TAXA_LEGAL", "30/08/2024"]], "combinacoes_indice": [["IPCA", "30/08/2024"]]},
 "honorarios": [{"credor": "CHRISTIAN SILVA DE BRITO", "doc": "05664484322", "aliquota": 15, "base": "BRUTO_MENOS_CONTRIBUICAO_SOCIAL", "devedor": "RECLAMADO"}],
 "custas": {"reclamado_conhecimento": "CALCULADA_2_POR_CENTO"},
 "seguro_desemprego": false
}
```

Exemplo 2, verbas informadas, férias com dedução, FGTS a depositar com multa informada (Exemplo 06). Só as partes que diferem do exemplo 1:

```json
{
 "contrato": {"admissao": "15/07/2024", "demissao": "19/03/2026", "ajuizamento": "09/04/2026", "maior_remuneracao": 1326.27, "ultima_remuneracao": 1326.27, "prescricao_quinquenal": false, "prescricao_fgts": false, "marco_prescricional": null, "aviso_dias": 33, "projetar_aviso": true, "fim_projetado": "21/04/2026", "carga_horaria": 220, "comentarios": "Valores da planilha homologada em 13/10/2026 (ID 4f442a5), adequada ao acórdão. Seguro-desemprego e guias não apurados: obrigação de fazer não convertida, depende de prévia intimação da reclamada. Custas de R$ 386,71 recolhidas em 17/08/2026."},
 "ferias": [{"relativa": "2024/2025", "aquisitivo": ["15/07/2024", "14/07/2025"], "situacao": "INDENIZADAS"}],
 "historicos": {"ultima_remuneracao": {"valor": 1326.27, "inicio": "07/2024", "fim": "03/2026", "fgts": false, "inss": false}},
 "verbas": [
  {"tipo": "INFORMADA", "nome": "SALDO DE SALÁRIO", "assunto_cnj": 8823, "pagamento": "DESLIGAMENTO", "fgts": true, "inss": true, "irpf": true, "ocorrencias": [["01/03/2026", "19/03/2026", 839.94]]},
  {"tipo": "AVISO_PREVIO", "fgts": false, "inss": false, "irpf": false},
  {"tipo": "DECIMO_TERCEIRO", "periodo": ["01/01/2026", "19/03/2026"], "avos": 4, "base": "MAIOR_REMUNERACAO", "fgts": true},
  {"tipo": "FERIAS", "periodos_indenizados": [["15/07/2024", "14/07/2025", 12, 1331.56], ["15/07/2025", "21/04/2026", 9]]},
  {"tipo": "INFORMADA", "nome": "DEVOLUÇÃO DE DESCONTOS INDEVIDOS", "pagamento": "MENSAL", "ocorrencias": [["01/09/2025", "30/09/2025", 1099.29], ["01/10/2025", "31/10/2025", 1009.12], ["01/11/2025", "30/11/2025", 633.57], ["01/12/2025", "31/12/2025", 258.02]]},
  {"tipo": "INFORMADA", "nome": "INDENIZAÇÃO SUBSTITUTIVA DO VALE-TRANSPORTE", "assunto_cnj": 2540, "pagamento": "MENSAL", "ocorrencias": [["01/01/2026", "31/01/2026", 166.67], ["01/02/2026", "28/02/2026", 166.67], ["01/03/2026", "19/03/2026", 166.66]]}
 ],
 "multas": [{"descricao": "INDENIZAÇÃO POR DANO MORAL", "valor": 10000.0, "vencimento": "09/04/2026", "juros_a_partir": "09/04/2026"}],
 "fgts": {"destino": "DEPOSITAR", "multa": "QUARENTA_POR_CENTO", "multa_informada": 940.98, "incidencia": "SOBRE_O_TOTAL_DEVIDO", "excluir_aviso_da_multa": false, "inicio": "15/07/2024", "fim": "19/03/2026"},
 "inss": {"devidos": ["15/07/2024", "19/03/2026"], "pagos": ["15/07/2024", "19/03/2026"], "empresa": 20, "sat": 3},
 "honorarios": [{"credor": "ADRIANA FABIOLA MARTINS SOUSA DE JESUS", "doc": "64546888104", "aliquota": 11.5, "base": "BRUTO", "devedor": "RECLAMADO"}],
 "custas": {"reclamado_conhecimento": "NAO_SE_APLICA"}
}
```

Exemplo 3, horas extras e reflexos (Exemplo 08, só a parte que difere):

```json
{
 "data_liquidacao": "31/07/2025",
 "historicos": {"ultima_remuneracao": {"valor": 2279.64, "inicio": "11/2022", "fim": "05/2024", "fgts": false, "inss": false},
                "BASE GRATIFICAÇÃO 10%": {"fgts": false, "inss": false, "faixas": [["11/2023", "05/2024", 2072.40]]}},
 "verbas": [
  {"tipo": "AVISO_PREVIO", "fgts": false, "inss": false, "irpf": false, "periodo": ["18/05/2024", "18/05/2024"]},
  {"tipo": "VERBA_HISTORICO", "nome": "DIFERENÇA SALARIAL", "historico": "BASE GRATIFICAÇÃO 10%", "multiplicador": 0.1, "periodo": ["01/11/2023", "18/05/2024"], "fgts": true, "inss": true, "irpf": false, "assunto_cnj": 2458},
  {"tipo": "REFLEXO", "reflexo": "AVISO", "base": "DIFERENÇA SALARIAL"},
  {"tipo": "HORAS_EXTRAS", "nome": "HORAS EXTRAS 50%", "quantidade_mensal": 102.72, "multiplicador": 1.5, "divisor": 220, "periodo": ["10/11/2022", "18/05/2024"], "fgts": true, "inss": true, "irpf": false, "assunto_cnj": 2086},
  {"tipo": "REFLEXO", "reflexo": "AVISO", "base": "HORAS EXTRAS 50%"},
  {"tipo": "FERIAS", "periodos_indenizados": [["10/11/2022", "09/11/2023", 12], ["10/11/2023", "20/06/2024", 6]]},
  {"tipo": "REFLEXO", "reflexo": "FERIAS", "base": "DIFERENÇA SALARIAL", "periodos": [["10/11/2022", "09/11/2023", 12], ["10/11/2023", "20/06/2024", 7]]},
  {"tipo": "REFLEXO", "reflexo": "FERIAS", "base": "HORAS EXTRAS 50%", "periodos": [["10/11/2022", "09/11/2023", 12], ["10/11/2023", "20/06/2024", 7]]},
  {"tipo": "REFLEXO", "reflexo": "MULTA_467", "base": "AVISO PRÉVIO"},
  {"tipo": "REFLEXO", "reflexo": "MULTA_467", "base": "FÉRIAS + 1/3"},
  {"tipo": "INFORMADA", "nome": "SALDO DE SALÁRIO", "assunto_cnj": 8823, "pagamento": "DESLIGAMENTO", "fgts": false, "inss": true, "irpf": false, "ocorrencias": [["01/05/2024", "18/05/2024", 820.67]]},
  {"tipo": "REFLEXO", "reflexo": "MULTA_467", "base": "SALDO DE SALÁRIO", "integralizar": "NAO"},
  {"tipo": "DECIMO_TERCEIRO", "nome": "13º SALÁRIO PROP 5/12", "periodo": ["18/05/2024", "18/05/2024"], "avos": 5, "base": "MAIOR_REMUNERACAO", "fgts": false, "irpf": false},
  {"tipo": "REFLEXO", "reflexo": "MULTA_467", "base": "13º SALÁRIO PROP 5/12"},
  {"tipo": "MULTA_477", "periodo": ["18/05/2024", "18/05/2024"]},
  {"tipo": "REFLEXO", "reflexo": "RSR", "base": "HORAS EXTRAS 50%"},
  {"tipo": "REFLEXO", "reflexo": "DECIMO", "base": "DIFERENÇA SALARIAL", "ocorrencias": [["20/12/2023", 12], ["18/05/2024", 6]]},
  {"tipo": "REFLEXO", "reflexo": "DECIMO", "base": "HORAS EXTRAS 50%", "ocorrencias": [["20/12/2022", 2], ["20/12/2023", 12], ["18/05/2024", 6]]}
 ],
 "fgts": {"destino": "PAGAR", "multa": "QUARENTA_POR_CENTO", "incidencia": "SOBRE_O_TOTAL_DEVIDO", "excluir_aviso_da_multa": true, "inicio": "10/11/2022", "fim": "18/05/2024"},
 "correcao": {"indice": "IPCAE", "outro_indice": "IPCA", "outro_a_partir": "30/08/2024", "juros_pre_judicial": false, "juros": "SEM_JUROS", "combinacoes_juros": [["TAXA_LEGAL", "11/10/2024"]], "combinacoes_indice": [["IPCA", "30/08/2024"]]},
 "honorarios": [{"credor": "NOME DO CREDOR", "doc": "CPF", "aliquota": 15, "base": "BRUTO", "devedor": "RECLAMADO", "tipo": "ADVOCATICIOS", "descricao": "HONORÁRIOS ADVOCATÍCIOS"}],
 "custas": {"reclamado_conhecimento": "CALCULADA_2_POR_CENTO"}
}
```

Exemplo 4, verbas sobre histórico com coeficientes e deduções (Exemplo 04, trechos). Atenção: a correção deste exemplo reproduz um cálculo de referência que combina SELIC como índice e como juros (ver as restrições acima); não copiar essa combinação em caso novo:

```json
{
 "data_liquidacao": "31/08/2021",
 "historicos": {"VALOR DA COMISSÃO": {"fgts": false, "inss": false, "fixa": true, "faixas": [["05/2016", "11/2019", 3000.0]]}},
 "verbas": [
  {"tipo": "VERBA_HISTORICO", "nome": "AD 55% H EXTRAS (SOBRE COMISSÕES)", "historico": "VALOR DA COMISSÃO", "periodo": ["16/05/2016", "25/11/2019"], "divisor": 220, "multiplicador": 0.55, "quantidade": 127.73, "proporcionalizar_quantidade": true, "proporcionalizar_base": false, "excluir_faltas_justificadas": false, "excluir_faltas_nao_justificadas": false, "excluir_ferias_gozadas": false, "fgts": false, "inss": true, "irpf": false, "assunto_cnj": 2581},
  {"tipo": "VERBA_HISTORICO", "nome": "REPERCUSSÃO DAS COMISSÕES EM SALDO DE SALÁRIO", "historico": "VALOR DA COMISSÃO", "periodo": ["25/11/2019", "25/11/2019"], "divisor": 30, "multiplicador": 1, "quantidade": 25, "proporcionalizar_quantidade": false, "proporcionalizar_base": false, "excluir_faltas_justificadas": false, "excluir_faltas_nao_justificadas": false, "excluir_ferias_gozadas": false, "fgts": false, "inss": true, "irpf": false, "assunto_cnj": 2581},
  {"tipo": "INFORMADA", "nome": "INDENIZAÇÃO POR DANO MORAL", "pagamento": "MENSAL", "ocorrencias": [["18/03/2021", "18/03/2021", 12446.1]], "fgts": false, "inss": false, "irpf": false, "assunto_cnj": 55220}
 ],
 "multas": [{"descricao": "DEDUÇÃO H EXTRA C/ 55% AGO 2016", "credor_devedor": "RECLAMADO_RECLAMANTE", "valor": 327.36, "vencimento": "31/08/2016", "juros_a_partir": "02/06/2020"}],
 "fgts": {"destino": "PAGAR", "multa": null, "incidencia": "SOBRE_O_TOTAL_DEVIDO", "excluir_aviso_da_multa": true, "inicio": "16/05/2016", "fim": "25/11/2019"},
 "inss": {"devidos": ["16/05/2016", "18/03/2021"], "pagos": ["16/05/2016", "25/11/2019"], "empresa": 20, "sat": 3},
 "correcao": {"indice": "IPCAE", "outro_indice": "SELIC", "outro_a_partir": "02/06/2020", "juros_pre_judicial": false, "juros": "SEM_JUROS", "combinacoes_juros": [["SELIC", "03/06/2020"]], "combinacoes_indice": [["SELIC", "02/06/2020"]]}
}
```

Exemplo 5, comissionista com reflexos do sistema (Exemplo 03, trechos):

```json
{
 "contrato": {"admissao": "04/10/2021", "demissao": "21/03/2023", "ajuizamento": "18/03/2024", "maior_remuneracao": null, "ultima_remuneracao": null, "prescricao_quinquenal": false, "prescricao_fgts": false, "marco_prescricional": null, "aviso_dias": 33, "projetar_aviso": true, "carga_horaria": 220, "comentarios": null},
 "historicos": {"SALÁRIO BASE - COMISSÕES": {"fixa": true, "fgts": true, "proporcionalizar_fgts": true, "inss": false, "faixas": [["10/2021", "03/2023", 8823.99]]}},
 "verbas": [
  {"tipo": "HORAS_EXTRAS", "nome": "ADICIONAL DE HORAS EXTRAS _ 50%", "historico": "SALÁRIO BASE - COMISSÕES", "quantidade_mensal": 42.8, "multiplicador": 0.5, "divisor": 220, "periodo": ["04/10/2021", "21/03/2023"], "fgts": true, "inss": true, "irpf": true, "assunto_cnj": 2086},
  {"tipo": "AVISO_PREVIO", "base": "SALÁRIO BASE - COMISSÕES", "fgts": false, "inss": false, "irpf": false},
  {"tipo": "REFLEXO", "reflexo": "AVISO", "base": "ADICIONAL DE HORAS EXTRAS _ 50%", "fgts": false, "inss": false, "irpf": false},
  {"tipo": "FERIAS", "base": "SALÁRIO BASE - COMISSÕES", "multiplicador": "1.3333", "periodos_indenizados": [["04/10/2021", "03/10/2022", 12], ["04/10/2022", "23/04/2023", 6]]},
  {"tipo": "DECIMO_TERCEIRO", "nome": "13º SALÁRIO", "base": "SALÁRIO BASE - COMISSÕES", "periodo": ["04/10/2021", "21/03/2023"], "avos": 3, "fgts": false, "inss": true, "irpf": true, "ocorrencias": [["20/12/2021", 3, false], ["20/12/2022", 12], ["21/03/2023", 3]]},
  {"tipo": "REFLEXO", "reflexo": "MULTA_467", "base": "13º SALÁRIO"},
  {"tipo": "MULTA_477", "base": "SALÁRIO BASE - COMISSÕES", "periodo": ["04/10/2021", "21/03/2023"]},
  {"tipo": "REFLEXO", "reflexo": "RSR", "base": "ADICIONAL DE HORAS EXTRAS _ 50%", "fgts": false, "inss": true, "irpf": true},
  {"tipo": "VERBA_HISTORICO", "nome": "SALDO DE SALÁRIO FEVEREIRO DE 2023 16 DIAS", "historico": "SALÁRIO BASE - COMISSÕES", "periodo": ["28/02/2023", "28/02/2023"], "divisor": 28, "multiplicador": 1, "quantidade": 16, "proporcionalizar_quantidade": false, "proporcionalizar_base": false, "excluir_faltas_nao_justificadas": false, "excluir_ferias_gozadas": false, "fgts": false, "inss": true, "irpf": true, "assunto_cnj": 2581}
 ],
 "multas": [{"descricao": "INDENIZAÇÃO POR DANO MORAL", "valor": 20000.0, "vencimento": "25/05/2026", "juros_a_partir": "19/03/2024", "indice": "IPCA"}],
 "fgts": {"destino": "DEPOSITAR", "multa": "QUARENTA_POR_CENTO", "multa_467": true, "incidencia": "SOBRE_O_TOTAL_DEVIDO", "excluir_aviso_da_multa": true, "inicio": "04/10/2021", "fim": "21/03/2023"},
 "inss": {"devidos": ["04/10/2021", "21/03/2023"], "pagos": ["04/10/2021", "21/03/2023"], "empresa": 20, "sat": 1},
 "correcao": {"indice": "IPCAE", "outro_indice": "IPCA", "outro_a_partir": "30/08/2024", "juros_pre_judicial": false, "juros": "SEM_JUROS", "combinacoes_juros": [["SELIC_FAZENDA", "19/03/2024"], ["TAXA_LEGAL", "30/08/2024"]], "combinacoes_indice": [["IPCA", "30/08/2024"]]}
}
```

Exemplo 6, insalubridade sobre o salário mínimo com férias gozadas e honorários periciais (Exemplo 07, trechos):

```json
{
 "contrato": {"admissao": "03/04/2017", "demissao": "05/06/2025", "ajuizamento": "25/07/2025", "maior_remuneracao": null, "ultima_remuneracao": null, "prescricao_quinquenal": true, "prescricao_fgts": true, "marco_prescricional": "25/07/2020", "inicio_calculo": "25/07/2020", "termino_calculo": "31/05/2023", "aviso_dias": 54, "projetar_aviso": true, "carga_horaria": 220, "comentarios": null},
 "ferias": [{"relativa": "2019/2020", "aquisitivo": ["03/04/2019", "02/04/2020"], "situacao": "GOZADAS", "gozo": ["04/03/2021", "02/04/2021"]}, {"relativa": "2024/2025", "aquisitivo": ["03/04/2024", "02/04/2025"], "situacao": "INDENIZADAS"}],
 "historicos": {},
 "verbas": [
  {"tipo": "VERBA_HISTORICO", "nome": "ADICIONAL DE INSALUBRIDADE 20%", "base_tabelada": "SALARIO_MINIMO", "periodo": ["25/07/2020", "31/05/2023"], "divisor": 1, "multiplicador": 0.2, "quantidade": 1, "proporcionalizar_quantidade": false, "proporcionalizar_base": true, "excluir_faltas_justificadas": false, "excluir_faltas_nao_justificadas": true, "excluir_ferias_gozadas": true, "fgts": true, "inss": true, "irpf": true, "assunto_cnj": 1666},
  {"tipo": "REFLEXO", "reflexo": "FERIAS", "base": "ADICIONAL DE INSALUBRIDADE 20%", "periodo": ["25/07/2020", "05/06/2025"], "fgts": true, "inss": true, "irpf": true, "periodos": [["03/04/2019", "02/04/2020", 12, "04/03/2021", "02/04/2021"], ["03/04/2024", "02/04/2025", 12], ["03/04/2025", "29/07/2025", 4]]},
  {"tipo": "REFLEXO", "reflexo": "DECIMO", "base": "ADICIONAL DE INSALUBRIDADE 20%", "periodo": ["25/07/2020", "05/06/2025"], "fgts": true, "inss": true, "irpf": true, "ocorrencias": [["20/12/2020", 12], ["20/12/2021", 12], ["20/12/2022", 12], ["20/12/2023", 12], ["20/12/2024", 12], ["05/06/2025", 7]]}
 ],
 "multas": [],
 "honorarios": [
  {"credor": "NOME", "doc": "CPF", "aliquota": 15, "base": "BRUTO", "devedor": "RECLAMADO", "tipo": "ADVOCATICIOS", "descricao": "HONORÁRIOS ADVOCATÍCIOS"},
  {"credor": "NOME DA PERITA", "doc": "CPF", "valor": 2000.0, "devedor": "RECLAMADO", "tipo": "PERICIAIS_ENGENHEIRO", "descricao": "HONORÁRIOS PERICIAIS - ENGENHEIRO", "vencimento": "29/07/2026", "indice": "IPCA", "juros_a_partir": "29/07/2026"}
 ]
}
```

Exemplo 7, periculosidade, adicional noturno, intervalo e FGTS a deduzir (128483, trechos):

```json
{
 "ferias": [{"relativa": "2024/2025", "aquisitivo": ["17/11/2024", "16/11/2025"], "situacao": "GOZADAS", "gozo": ["18/10/2025", "16/11/2025"]}],
 "historicos": {"SALÁRIO BASE": {"fixa": true, "fgts": true, "proporcionalizar_fgts": true, "inss": true, "proporcionalizar_inss": true, "faixas": [["11/2024", "03/2026", 3000.0]]}},
 "verbas": [
  {"tipo": "VERBA_HISTORICO", "nome": "ADICIONAL DE PERICULOSIDADE 30%", "historico": "SALÁRIO BASE", "periodo": ["17/11/2024", "03/03/2026"], "divisor": 1, "multiplicador": 0.3, "quantidade": 1, "proporcionalizar_quantidade": false, "proporcionalizar_base": true, "fgts": true, "inss": true, "irpf": true, "assunto_cnj": 1681},
  {"tipo": "HORAS_EXTRAS", "nome": "ADICIONAL NOTURNO 20%", "historico": "SALÁRIO BASE", "quantidade_mensal": 1.5, "multiplicador": 0.2, "divisor": "CARGA_HORARIA", "periodo": ["17/11/2024", "03/03/2026"], "excluir_faltas_justificadas": true, "excluir_faltas_nao_justificadas": true, "excluir_ferias_gozadas": true, "fgts": true, "inss": true, "irpf": true, "assunto_cnj": 1663},
  {"tipo": "HORAS_EXTRAS", "nome": "INTERVALO INTRAJORNADA", "historico": "SALÁRIO BASE", "quantidade_mensal": 2, "multiplicador": 1.5, "divisor": "CARGA_HORARIA", "periodo": ["17/11/2024", "03/03/2026"], "excluir_faltas_justificadas": true, "excluir_faltas_nao_justificadas": true, "excluir_ferias_gozadas": true, "fgts": false, "inss": false, "irpf": false, "assunto_cnj": 2140},
  {"tipo": "REFLEXO", "reflexo": "FERIAS", "base": "ADICIONAL NOTURNO 20%", "fgts": false, "inss": true, "irpf": true, "periodos": [["17/11/2024", "16/11/2025", 12, "18/10/2025", "16/11/2025"], ["17/11/2025", "05/04/2026", 5]]},
  {"tipo": "REFLEXO", "reflexo": "RSR", "base": "ADICIONAL NOTURNO 20%", "fgts": false, "inss": true, "irpf": true}
 ],
 "fgts": {"destino": "DEPOSITAR", "multa": null, "incidencia": "SOBRE_O_TOTAL_DEVIDO", "excluir_aviso_da_multa": true, "inicio": "17/11/2024", "fim": "03/03/2026", "depositos": {"11/2024": 240, "12/2024": 240, "01/2025": 240, "02/2025": 240}},
 "correcao": {"indice": "IPCAE", "outro_indice": "SEM_CORRECAO", "outro_a_partir": "03/11/2026", "juros_pre_judicial": true, "juros": "TRD_SIMPLES", "combinacoes_juros": [["SELIC", "03/11/2026"]], "combinacoes_indice": [["SEM_CORRECAO", "03/11/2026"]]},
 "honorarios": []
}
```

No 108996 homologado, o saldo de salário aplicou a proporção de dias duas vezes (base de maio já proporcional × 18/30 = R$ 820,67; o correto seria R$ 1.367,78). Na reprodução foi mantido o valor homologado, como verba informada. Em caso novo, usar `SALDO_SALARIO`.

Valores aceitos pelo sistema (nomes do XML):
- `situacao` das férias: GOZADAS, GOZADAS_PARCIALMENTE, INDENIZADAS, PERDIDAS.
- `destino` do FGTS: PAGAR, DEPOSITAR.
- Tipo da multa do FGTS: CALCULADA, INFORMADA. O gerador escolhe pela presença de `multa_informada`.
- `incidencia` da multa do FGTS: SOBRE_O_TOTAL_DEVIDO, SOBRE_DEPOSITADO_SACADO, SOBRE_DIFERENCA, SOBRE_TOTAL_DEVIDO_MAIS_SAQUE_E_OU_SALDO, SOBRE_TOTAL_DEVIDO_MENOS_SAQUE_E_OU_SALDO.
- Índices: IPCAE, IPCA, SELIC, SEM_CORRECAO...
- Juros: SEM_JUROS, TAXA_LEGAL, TRD_SIMPLES, SELIC, SELIC_FAZENDA (aparece no relatório como "juros SELIC simples")...
- Base dos honorários: BRUTO, BRUTO_MENOS_CONTRIBUICAO_SOCIAL, BRUTO_MENOS_CONTRIBUICAO_SOCIAL_MENOS_PREVIDENCIA_PRIVADA...
- Custas: CALCULADA_2_POR_CENTO, INFORMADA, NAO_SE_APLICA.

