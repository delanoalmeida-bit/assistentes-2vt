---
name: "triagem-diaria-minutar-despacho"
description: "Tria os processos que entraram na tarefa Minutar Despacho do PJe (2ª VT de São Luís) no dia anterior. Indica se cabe na CDD, se pede modelo novo, se é urgente ou se é complexo."
---

# Triagem diária da tarefa "Minutar Despacho"

## Para que serve

Na 2ª VT de São Luís (TRT-16), três servidores da Secretaria minutam os despachos simples com base na **Cartilha de Despachos e Decisões (CDD)**. O que não está na CDD vai para a tarefa "Minutar Despacho", onde espera um dos dois assistentes de juiz. A caixa é o maior gargalo da unidade.

Na triagem dos 126 processos mais antigos (nov/2026), 62% cabiam na CDD ou em despacho simples, 21% pediam um modelo novo e só 17% eram complexos. O filtro de entrada falha. Esta triagem diária pega o problema na porta, um dia depois.

Para cada processo que entrou na caixa no período, responda a quatro perguntas:
1. Cabe na CDD ou num modelo avulso aprovado? Se sim, em qual item.
2. É um caso repetitivo que pede um modelo novo?
3. É urgente?
4. É complexo de fato e exige o assistente de juiz?

## Entrada

- **Preferencial:** o arquivo `.md` gerado pelo botão "Entradas de ontem: Minutar Despacho" (repositório relatorio-caixas-pje). Use o bloco ```json, que traz `processos[]` com cnj, idProcesso, classe, fase, entradaNaTarefa, digitoFinal, assistentePeloDigito, partes, entes públicos, recuperação judicial ou falência, sindicato, prioridades, comentarioNoPJe, segredoDeJustica, lotes e assuntos.
- **Alternativa:** uma lista de números de processo colada pelo usuário. Nesse caso, o assistente sai do dígito final: o 7º dígito do número sequencial (0000004 → 4). Finais 0–4 vão para **Fábio Henrique**; finais 5–9, para **Alexsandro**.
- Se nada for anexado, peça o arquivo. Não invente a lista.

## Fontes de consulta

- **CDD:** o .docx da cartilha nos arquivos do Projeto ou anexado. O sumário serve de catálogo. Cite sempre o item exato, no formato já usado pela equipe:
  - `CDD Conhecimento 5.5`
  - `CDD Liquidação Modelo 5` (remessa aos cálculos)
  - `CDD Liquidação Hom. Modelo 1` (homologação)
  - `CDD Execução 11.2`
  - `CDD Execução Modelo 5` (sentenças de arquivamento)

  A CDD muda com frequência. Use sempre a versão do arquivo, nunca a memória.
- **Modelos avulsos e modelos novos aprovados:** o arquivo `modelos-avulsos.md` do Projeto, se existir. Cite como `Avulso: <nome>`.
- **Histórico:** a planilha "Triagem diária – Minutar Despacho" no Google Drive (ver Saída). Ela serve para detectar repetição entre os dias.
- **Calibração:** a triagem piloto (PDF nos arquivos do Projeto). Ela mostra o nível de detalhe e os critérios já validados pelo usuário.

## Como ler cada processo

1. Abra o processo no PJe pelo conector, usando o número. Leia os **movimentos e documentos juntados depois do último ato do magistrado**: a petição nova, a certidão, o decurso de prazo, o retorno do TRT.
2. Se o título da peça não basta, leia o texto. Se o texto não estiver disponível, classifique pelo título e anote "classificado pelo título; conferir".
3. **Segredo de justiça** ou processo sem acesso: grupo "—", ato "triagem manual". Não deduza nada.
4. Se o conector do PJe não estiver disponível, diga isso e pare. Não classifique só pelos metadados do arquivo, porque eles não dizem por que o processo está concluso.
5. Trabalhe em lotes de até 25 processos. Se houver mais, avise quantos faltam.

## Classificação (um grupo por processo)

**A. Cabe na CDD, em modelo avulso ou em despacho simples.** Vai para a Secretaria.

São atos de impulso. Exemplos:
- vista ou ciência às partes;
- intimar para indicar meios, sob pena de arquivo provisório (art. 11-A);
- homologar cálculos não impugnados;
- remeter ao calculista;
- liberar valores e expedir alvará;
- devolver saldo à executada;
- homologar acordo em execução;
- ciência do retorno do TRT e prosseguimento;
- intimar ente público (535 CPC, RPV);
- habilitação de crédito no juízo falimentar;
- certidões de imóveis pelo próprio autor.

Indique o item da CDD. Se o modelo precisa de ajuste, escreva "(adaptado)" e diga o quê.

**B. Repetitivo sem modelo.** O assistente faz o modelo uma vez e a Secretaria aplica em bloco.

Padrões já identificados, com o nome a usar na coluna Situação-padrão:
- `pesquisas-patrimoniais`: pedido genérico de bateria de convênios (SISBAJUD teimosinha, RENAJUD, INFOJUD, CNIB, CCS, SERASAJUD, SNIPER, CENSEC). Depende de uma diretriz do Juízo sobre o que se defere de ofício.
- `cumsen-correios-parecer-calculista`: acolhe o parecer do calculista e expede RPV.
- `idpj-instauracao`: instauração de IDPJ e citação dos sócios (art. 855-A CLT).
- `renajud-positivo`: restrição, mandado de penhora e avaliação.
- `alvara-seguro-desemprego-fora-prazo`
- `seguro-garantia-deposito-recursal`
- `patio-detran-art-328-ctb`
- `saldo-remanescente-arquivado`: pedido do mesmo escritório em processos arquivados (Bradesco, Unisys).

Um padrão novo entra no grupo B quando:
- aparece em **2 ou mais processos do mesmo dia** (ou do mesmo lote do arquivo), ou
- soma **3 ou mais ocorrências** no histórico da planilha.

Na primeira ocorrência, classifique como A (despacho simples) ou C, conforme o caso. Registre a situação-padrão mesmo assim, para a contagem.

**C. Complexo de fato.** Fica com o assistente do dígito.

É o que exige decisão com fundamentação de mérito ou de valoração. Exemplos:
- impugnação à penhora ou alegação de impenhorabilidade;
- embargos à execução ou impugnação aos cálculos com teses;
- exceção de pré-executividade;
- decisão de IDPJ já instruído;
- fraude à execução;
- embargos de terceiro ou pedido de terceiro sobre a constrição;
- alcance da recuperação judicial (stay, juízo universal);
- tutela cautelar;
- chamamento do feito à ordem;
- critério de liquidação controvertido;
- reunião de execuções;
- penhora de salário concorrente com outros juízos.

Se houver skill de execução aplicável, indique: `minutador-de-incidentes-de-execucao`, `analista-de-embargos-e-impugnacoes-execucao` ou `minutador-de-idpj-e-redirecionamento-execucao`. O assistente passa a revisar uma minuta em vez de redigir do zero.

**D. Conclusão desnecessária.** O ato já está determinado e só falta a Secretaria cumprir. Exemplos:
- pesquisa já autorizada e não feita;
- suspensão em curso, sem petição nova;
- ofício a reiterar.

O processo volta para cumprimento, sem despacho novo.

Na dúvida entre A e C, escolha **C** e explique o motivo na observação. Errar para o lado do assistente custa menos que um despacho errado.

## Urgência (marcação independente do grupo)

Marque **URGENTE** e diga o motivo e a data-limite quando houver:
- tutela de urgência ou cautelar pendente de apreciação;
- prazo que vence em até 10 dias e faz o pedido perder o objeto: vencimento de acordo, leilão marcado, prazo do art. 328 CTB, prescrição;
- verba de natureza alimentar bloqueada ou pedido de desbloqueio de salário ou aposentadoria;
- liberação de valores a credor com prioridade forte: idoso acima de 80, doença grave, deficiência;
- pedido de celeridade reiterado, ou pedido parado há meses e cobrado nos autos;
- ofício ou cobrança do TRT, da Corregedoria, de outro juízo ou de outro órgão com prazo.

A prioridade legal comum (idoso, por exemplo) **não** torna o caso urgente. Ela vai só na observação. Das 272 prioridades da caixa, só umas 15 são fortes.

## Saída

1. **Resumo no chat**, nesta ordem:
   - o período e o total;
   - a contagem por grupo;
   - os **urgentes primeiro**, com o motivo;
   - a tabela completa, ordenada por grupo e, dentro do grupo, por assistente. Colunas: Processo | Classe | Fase | Assistente (dígito) | Grupo | Urgente | O que está pendente | Ato sugerido (modelo) | Observação;
   - a seção "Modelos a criar": cada situação-padrão que atingiu o critério do grupo B, com a contagem e os processos;
   - a seção "Retorno ao Escaninho": os processos A e D, para lembrar quem tria que eles não precisavam vir para a tarefa.
2. **Planilha de histórico.** Use o Google Sheets, com o conector, na planilha "Triagem diária – Minutar Despacho". Se ela não existir, crie-a com a aba "Triagem" e o cabeçalho abaixo. Acrescente uma linha por processo. Nunca apague linhas antigas.

   Colunas: Data da triagem | Processo | Classe | Fase | Entrada na caixa | Assistente (dígito) | Grupo | Urgente | O que está pendente | Ato sugerido (modelo) | Situação-padrão | Observação | Status

   O Status começa como "A fazer". Antes de gravar, confira se o processo já tem linha com a mesma data de entrada, para evitar duplicata. Sem conector do Google, entregue as linhas em CSV no fim e avise.
3. **Às sextas-feiras** (ou quando pedirem), acrescente indicadores:
   - entradas da semana por grupo;
   - % de A+D, que indica o tamanho da falha do filtro de entrada;
   - as situações-padrão mais frequentes, para orientar a revisão da CDD.

## Regras

- Não minute por padrão. Indique o modelo. Gere a minuta só se o usuário pedir, e só para os processos que ele indicar.
- Cada classificação tem que se apoiar no que foi lido no processo. Se não leu, diga. Não especule sobre o conteúdo de peças não lidas.
- O assistente vem sempre do dígito final, mesmo que o PJe mostre outro responsável. Se houver divergência, aponte na observação ("PJe: <nome>").
- Ente público: observe as prerrogativas (prazos, RPV ou precatório, nada de SISBAJUD contra a Fazenda). Recuperação judicial ou falência: verifique o juízo universal antes de sugerir constrição.
- Linguagem direta. A tabela é instrumento de trabalho, não relatório.