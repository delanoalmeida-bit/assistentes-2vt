---
name: ficha-liquidacao-trabalhista
description: "Lê o título executivo trabalhista (sentença, ED, acórdãos, trânsito) ou a minuta de sentença ainda não assinada, e monta a Ficha de Liquidação para o PJe-Calc 2.16 — v2: escopo do gerador-pjc v8."
---

# Ficha de Liquidação Trabalhista (PJe-Calc 2.16) — v2

## Objetivo

Ler o título executivo (ou a minuta de sentença) e os documentos do processo e produzir a **Ficha de Liquidação**: os parâmetros que serão lançados no PJe-Calc, na ordem das telas do sistema, cada um com **fonte** e **status**. A ficha é a única entrada da etapa seguinte — o gerador de arquivo (skill `gerador-pjc`, preferencial) ou o lançamento pelo navegador (skill `lancamento-pjecalc`) — e só segue depois de validada pelo usuário.

## Dois modos

| | **Modo título** (liquidação após o trânsito) | **Modo minuta** (sentença líquida) |
|---|---|---|
| Fonte dos parâmetros | sentença + ED + acórdãos + decisões em RR/AIRR + acordo parcial | a minuta de sentença enviada pelo juiz, ainda não assinada |
| Onde está | no PJe (conector) | anexo do usuário (PDF, DOCX ou texto); não está nos autos |
| Trânsito | verificar e registrar | não se aplica |
| Data de liquidação | a indicada pelo usuário ou a do dia | a data prevista de assinatura; se não informada, pendência |
| Pendências | decididas pelo usuário/juiz; o título não muda | podem ser resolvidas **ajustando a redação da minuta** — sugerir o ajuste |

Identificar o modo no início: se o usuário anexar minuta ou falar em "sentença líquida", "minuta" ou "antes de assinar", é o modo minuta. Na dúvida, perguntar.

## Escopo da v2

O escopo acompanha o do `gerador-pjc` v8. Entram:
- **Rescisórias:** saldo de salário, aviso prévio indenizado, 13º, férias + 1/3 (vencidas, proporcionais, em dobro se deferidas), multas dos arts. 477 e 467, salários retidos.
- **Horas extras e verbas do mesmo formato** com **quantidade mensal fixa** (média fixada no título, jornada fixa reconhecida): horas extras, adicional noturno, intervalo intrajornada/interjornada.
- **Adicionais:** insalubridade sobre o salário mínimo; periculosidade sobre o salário-base; diferença salarial ou adicional percentual sobre histórico.
- **Reflexos** em RSR e feriados, aviso, férias + 1/3, 13º, FGTS + 40% e multa do art. 467.
- **Valores fixos:** dano moral/material, ressarcimentos, multas convencionais, indenização substitutiva (seguro-desemprego, vale-transporte), deduções.
- **FGTS** 8% + 40%/20%, a pagar ou depositar, com depósitos a deduzir mês a mês.
- **Acessórios:** contribuição social, IR, correção, juros, honorários (sucumbência e periciais), custas.

**Fora do escopo do gerador** (listar na seção 11 e oferecer o lançamento pelo navegador ou cálculo manual): horas extras por cartão de ponto ou com quantidade variável mês a mês; insalubridade sobre base que não o salário mínimo; verbas de norma coletiva com fórmula própria; faltas a descontar; contribuição social sobre salários pagos; contrato fora de 01/2010 a 10/2026. Se o usuário pedir para incorporar alguma, extrair os parâmetros e registrar o limite como alerta.

## Regras invioláveis

1. **Fidelidade ao título (art. 879, § 1º, CLT)** — ou, no modo minuta, **à minuta**. Lançar só o deferido. Não acrescentar verba por "decorrência lógica", não discutir o mérito, não corrigir o texto. O que parecer faltar vira pendência.
2. **Acórdão substitui a sentença no que a reformou (art. 1.008 CPC).** Verificar também ED, decisões em RR/AIRR e acordo parcial. Parcelas novas deferidas no acórdão sem base fixada viram pendência. (Modo minuta: não se aplica.)
3. **Fundamentação integra o dispositivo** quando este remete a ela. Ler ambos. Divergência entre fundamentação e dispositivo é pendência — no modo minuta, com sugestão de ajuste.
4. **Planilha anexa à sentença** (modo título): seus critérios servem de referência e de opção nas pendências, salvo no que o acórdão alterou. Divergência entre planilha e texto vira alerta.
5. **Não calcular valores.** Quem calcula é o PJe-Calc. Registrar parâmetros, não resultados. Exceções: valores mensais que o sistema precisa receber prontos (histórico salarial, depósitos de FGTS, valores informados), sempre com o critério ao lado; e números de referência para conferência, identificados como tais.
6. **Toda informação tem fonte:** peça + ID do PJe (ou página do anexo) e, quando útil, trecho curto.
7. **Status de cada campo:**
   - **Título** (ou **Minuta**) — expresso na decisão.
   - **Documento** — extraído de CTPS, TRCT, contracheque, extrato do FGTS, cartão de ponto, comprovante, movimentação etc.
   - **Pendente (Pn)** — omisso, ambíguo ou conflitante. Exige decisão humana.
8. **Nunca preencher uma pendência por presunção.** Se duas peças divergem, registrar as duas e marcar pendência, salvo se a decisão fixou o dado.

## Passo 1 — Reunir as peças

**Modo título** — necessárias: inicial; sentença (e planilha anexa); ED e decisões; acórdão(s); certidão de trânsito; despachos posteriores ao trânsito.
**Modo minuta** — necessárias: a minuta (anexo); inicial; contestação; ata(s) de audiência e laudo pericial, se houver.
**Úteis nos dois:** TRCT; CTPS/contrato; ficha de registro; contracheques de todo o período; extrato analítico do FGTS; cartões de ponto; comprovantes de pagamento.

Com o conector do PJe disponível, usar os metadados do processo (datas de admissão/demissão informadas, ajuizamento, partes, advogados) e a busca/leitura de peças. Sem ele, pedir as peças ao usuário. No modo título, verificar na movimentação o que ocorreu após o trânsito (intimações, prazos, cumprimentos).

No modo minuta, a minuta é documento interno não assinado: usá-la só para a ficha, não citá-la como peça dos autos e não juntá-la a nada.

## Passo 2 — Quadro da decisão

Antes da ficha, montar internamente: **verba/pedido | resultado (deferido, indeferido, reformado) | peça e ID (ou página da minuta) | parâmetros fixados | observações**. A ficha nasce desse quadro, não da inicial. A inicial delimita o critério quando a decisão remete a ela ou é omissa.

## Passo 3 — Checagens de coerência (detectam pendências; não autorizam acrescentar verbas)

### Verbas usualmente ligadas a cada modalidade de rescisão

| Modalidade | Verbas usualmente devidas | Multa FGTS |
|---|---|---|
| Sem justa causa / rescisão indireta | saldo, aviso indenizado proporcional, 13º proporcional, férias vencidas e proporcionais + 1/3, FGTS do mês e do aviso | 40% |
| Pedido de demissão | saldo, 13º proporcional, férias vencidas e proporcionais + 1/3 (Súm. 261 TST) | não |
| Justa causa | saldo, férias vencidas + 1/3 (Súm. 171 TST) | não |
| Culpa recíproca | 50% do aviso, do 13º e das férias proporcionais (Súm. 14 TST) | 20% |
| Acordo (art. 484-A CLT) | aviso indenizado pela metade; demais integrais | 20% |

Verba usualmente ligada à modalidade e não deferida: **não acrescentar**; alerta ou pendência.

### Rescisórias, FGTS e acessórios

- **Projeção do aviso** no tempo de serviço para 13º e férias (art. 487, § 1º, CLT; OJ 82 SDI-1).
- **FGTS:** incide sobre aviso indenizado (Súm. 305) e 13º; não incide sobre férias indenizadas + 1/3 (OJ 195). Rescisórias deferidas sem menção ao FGTS sobre elas: pendência.
- **FGTS não depositado:** período, inclusão do 13º, destino (depositar ou pagar). Com conversão em pagamento cominada e prazo vencido sem comprovação, propor pagamento direto.
- **FGTS depositado a deduzir:** usar o extrato analítico, mês a mês por competência (valor depositado sobre a remuneração do mês, sem JAM). Extrato parcial ou ausente: pendência, com sugestão de intimar a juntada.
- **Base da multa de 40%/20%:** totalidade dos depósitos do contrato (art. 18, § 1º, Lei 8.036/90), mais as diferenças deferidas. Saldo sem origem demonstrada: pendência.
- **Liberação do FGTS já depositado:** não converter em dinheiro; sugerir alvará.
- **Seguro-desemprego convertido (Súm. 389, II):** parcelas pelos meses trabalhados nos 36 anteriores à dispensa (art. 4º, § 2º, Lei 7.998/90); valor pela tabela do ano da dispensa, piso de um salário mínimo; vencimentos mensais a partir de 30 dias da dispensa. Tudo como parâmetro sugerido.
- **Multa por obrigação de fazer** (ex.: baixa na CTPS): não apurar sem intimação prévia e prova do descumprimento.
- **Multas dos arts. 477, § 8º, e 467:** deferidas ou não; no 467, quais parcelas formam a base (só as rescisórias incontroversas, conforme a decisão).
- **Deduções:** só o autorizado ou comprovado a mesmo título; registrar critério (por competência ou global — OJ 415 SDI-1 para horas extras).
- **Prescrição:** registrar o marco aplicado (quinquenal a partir do ajuizamento; bienal).
- **Natureza das verbas para contribuição social** (art. 832, § 3º, CLT): registrar o que a decisão fixou. No modo minuta, se a minuta não indicar a natureza das parcelas, pendência com sugestão de inclusão no dispositivo.
- **Imposto de renda:** RRA (art. 12-A Lei 7.713/88); juros de mora não tributáveis (OJ 400).
- **Correção monetária e juros:** transcrever o critério. Genérico, anterior à Lei 14.905/2024 ou silente a partir de 30/08/2024: pendência. Marco do ajuizamento = distribuição no PJe; outra data citada: alerta. Dano moral: correção desde o arbitramento (Súm. 439) — no modo minuta, a data do arbitramento é a da assinatura prevista.
- **Honorários:** percentual, base (OJ 348 e o critério da planilha, como opções), credor, devedor, suspensão de exigibilidade (justiça gratuita). Periciais: valor, responsável, data de fixação e critério de atualização.
- **Custas:** valor ou percentual e responsável; acórdão que alterou a condenação sem tratar das custas: pendência.

### Horas extras e verbas do mesmo formato

Parâmetros a extrair (cada um com fonte; ausente = pendência):
- **Quantidade mensal fixa.** Se a decisão fixar jornada (ex.: 8h às 19h, seg. a sáb., 1h de intervalo), converter em horas semanais e mensais e mostrar a conta como referência (ex.: 6 h semanais × 4,28 = 25,68 h/mês). Se a decisão mandar apurar "conforme cartões de ponto" ou a jornada variar mês a mês, **fora do escopo do gerador** — alerta.
- **Período** (início, fim, prescrição) e **meses sem labor** (férias gozadas, afastamentos), que o sistema exclui.
- **Adicional** (50%, 100%, o da norma coletiva — neste caso a norma precisa estar nos autos, senão pendência).
- **Divisor** (220, 200, 180 ou a carga mensal — Súm. 431; se omisso, pendência com a carga contratual como sugestão).
- **Base:** salário-base, globalidade salarial (Súm. 264 — inclui adicionais habituais), comissões. Comissionista: só o adicional sobre as comissões (Súm. 340; OJ 397 para o misto).
- **Reflexos deferidos:** RSR e feriados (Súm. 172); aviso, férias + 1/3, 13º e FGTS + 40%. **RSR majorado repercutindo nas demais parcelas:** só para horas extras a partir de 20/03/2023 (IRR Tema 9 — OJ 394 alterada); antes, não. Registrar o que a decisão disse; omissão = pendência.
- **Adicional noturno:** percentual (20% urbano), hora reduzida de 52'30" (art. 73, § 1º), prorrogação da jornada noturna (Súm. 60, II) e se houve reflexos.
- **Intervalo intrajornada:** antes de 11/11/2017, hora integral com adicional e natureza salarial, com reflexos (Súm. 437); a partir de 11/11/2017, só o tempo suprimido, natureza indenizatória, sem reflexos e sem incidências (art. 71, § 4º, CLT, red. Lei 13.467/2017). Registrar o que a decisão fixou; se for omissa quanto ao regime de cada período, pendência.
- **Intervalo interjornada** (art. 66; OJ 355): horas suprimidas com adicional.

### Adicionais de insalubridade e periculosidade

- **Insalubridade:** grau (10%, 20%, 40%), base (salário mínimo — Súm. Vinculante 4 do STF; outra base só se a decisão fixar, e aí fora do escopo do gerador), período (laudo), exclusão das férias gozadas e afastamentos. Reflexos usuais: férias + 1/3, 13º, aviso, FGTS; **não** em RSR (OJ 103 — já remunera o repouso).
- **Periculosidade:** 30% sobre o salário-base, sem acréscimos (art. 193, § 1º; Súm. 191). Lançar sobre o **histórico** do salário-base, mês a mês. Reflexos como na insalubridade (não em RSR).
- **Cumulação:** vedada (IRR Tema 17 TST). Se as duas forem deferidas, alerta sobre a opção do trabalhador.

### Leitura crítica dos documentos

- **Rubricas de contracheque:** confirmar se é vencimento ou desconto (ex.: vale-transporte costuma ser o desconto de 6%).
- **Histórico salarial:** campo "Base de cálculo do FGTS" de cada contracheque, com o 13º em linha própria; históricos separados quando a decisão usar bases diferentes (salário-base, comissões, remuneração). OCR de PDF: avisar que os valores devem ser conferidos com a imagem.
- **Férias gozadas, faltas e afastamentos:** ficha de registro, avisos e recibos de férias (datas exatas de início e fim do gozo — o gerador exclui esses dias). Descartar lançamentos posteriores à ruptura.
- **Extrato do FGTS:** competência, valor depositado; separar depósitos rescisórios e multa já paga.

## Passo 4 — Preencher a ficha (modelo)

```
FICHA DE LIQUIDAÇÃO — Processo nº [número]
Modo: [título | minuta de sentença recebida em dd/mm/aaaa]
Situação: [Em elaboração | Aguardando validação | VALIDADA em dd/mm/aaaa]
Trânsito em julgado: [data e ID | não certificado | não se aplica (minuta)]
Data de liquidação: [data | pendência]
Peças utilizadas: [tabela: peça | ID ou página | uso]

0. IDENTIFICAÇÃO
1. DADOS DO CÁLCULO (campo | valor | status | fonte)
   admissão, demissão, ajuizamento, início/fim do cálculo, marco prescricional,
   carga horária mensal, maior/última remuneração, dias de aviso
2. FÉRIAS, AFASTAMENTOS E FALTAS (período aquisitivo | gozo início–fim | situação | status | fonte)
3. HISTÓRICOS SALARIAIS (um por base: competência | valor | incide FGTS/INSS? | proporcionalizar?)
4. VERBAS (verba | deferida em | tipo para o gerador* | período | quantidade | base | divisor | adicional | FGTS/INSS/IR | status)
   4.1 Reflexos (reflexo | verba-base | período | avos/ocorrências | status)
   + tabelas de valores mensais e textos de observação para o resumo, quando houver
5. FGTS (alíquota, multa, destino, depósitos a deduzir por competência, liberação do saldo)
6. CONTRIBUIÇÃO SOCIAL
7. IMPOSTO DE RENDA
8. CORREÇÃO MONETÁRIA E JUROS (fase | critério | status)
9. HONORÁRIOS E CUSTAS
10. PENDÊNCIAS PARA DECISÃO
   Pn. [pergunta objetiva] — (a) ... (b) ... — Sugestão: ... (só com fundamento claro)
   [modo minuta] Ajuste sugerido na minuta: "[redação]"
11. FORA DO ESCOPO E ALERTAS
```

\* Tipos do gerador: AVISO_PREVIO, FERIAS, MULTA_477, SALDO_SALARIO, DECIMO_TERCEIRO, SALARIO_RETIDO, INFORMADA, HORAS_EXTRAS, VERBA_HISTORICO, REFLEXO, além de multas/indenizações e deduções. Ao preencher, conferir em `references/formato_ficha.md` da skill `gerador-pjc` quais campos cada tipo exige, para que a ficha validada já traga tudo o que o gerador vai pedir.

Campos sem informação geram pendência na seção 10. Nenhum campo em branco sem status.

## Passo 5 — Autoconferência antes de entregar

- Toda verba deferida está na seção 4, 5 ou 11.
- Nenhuma verba lançada deixa de ter fonte na decisão.
- Toda verba da seção 4 tem os campos exigidos pelo tipo do gerador, ou pendência.
- Datas coerentes; divergências registradas com as duas fontes.
- Toda pendência é pergunta objetiva, com opções e, havendo fundamento, sugestão.
- Modo título: obrigações de fazer com status de cumprimento verificado.
- Modo minuta: data de liquidação definida ou pendente; natureza das parcelas (art. 832, § 3º) indicada na minuta ou pendente.

## Passo 6 — Entrega e validação

1. Entregar a ficha como documento editável, título "Ficha de Liquidação — [número do processo]" (no modo minuta, acrescentar "— minuta de sentença"), situação "Aguardando validação".
2. Na resposta, listar só as pendências, numeradas, com a sugestão de cada uma (no modo minuta, com o ajuste de redação sugerido, quando houver).
3. Com as respostas, atualizar a ficha: cada pendência decidida recebe "Decidido em dd/mm/aaaa: (opção)", e os campos afetados são atualizados em todas as seções.
4. Sem pendências abertas, perguntar se pode marcar como validada; com a confirmação, marcar "VALIDADA em dd/mm/aaaa". Só ficha validada segue para o gerador ou o lançamento.

### Particularidades do modo minuta

- Se o juiz alterar a minuta depois da ficha validada, comparar a versão nova com a anterior e atualizar só o que mudou; reabrir a validação dos campos afetados.
- O cálculo gerado acompanha a sentença; a data de liquidação deve coincidir com a data prevista de assinatura (ou o critério que o juiz indicar). Se a assinatura atrasar, basta alterar a data de liquidação no PJe-Calc e liquidar de novo.
- Antes de o cálculo seguir para os autos, conferir se o dispositivo da versão final remete aos cálculos anexos ("conforme planilha anexa, que integra esta decisão") e se os valores do dispositivo, quando houver, batem com o relatório.

## Estilo

Linguagem direta e precisa, sem floreio. Citar dispositivos e súmulas apenas quando sustentarem um parâmetro ou uma pendência. Discordar, com fundamento, quando uma decisão pedida gerar pagamento em duplicidade ou contrariar a decisão.
