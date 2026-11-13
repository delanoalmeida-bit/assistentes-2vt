---
name: "lancamento-pjecalc"
description: "Lança no PJe-Calc 2.16 (web, TRT-16) os parâmetros de uma Ficha de Liquidação validada, via Claude in Chrome, tela a tela, e confere o resultado pelo relatório."
---

# Lançamento no PJe-Calc 2.16 (Claude in Chrome)

## Quando usar

Depois que a skill `ficha-liquidacao-trabalhista` produziu uma ficha marcada como **VALIDADA**. Sem ficha validada, não lançar nada: pedir a validação primeiro.

## Regras de segurança

1. O usuário faz o login no PJe e no PJe-Calc. Nunca digitar senha.
2. Nunca usar "Excluir" (cálculo) nem "Enviar para o PJe". "Liquidar" e "Imprimir" podem ser usados.
3. Combinar com o usuário, antes de começar, o modo de trabalho: (a) pausa antes de cada "Salvar" ou (b) salvar e reler sozinho, com conferência final pelo relatório. Respeitar o modo escolhido.
4. Enquanto o Claude estiver preenchendo, o usuário não deve mexer no cálculo pela própria aba: as abas compartilham a mesma conversa do sistema.
5. Toda divergência entre o que o sistema propõe e a ficha é resolvida pela ficha. Se a ficha não cobrir o ponto, parar e perguntar.

## Conexão

- O Claude só controla abas que ele mesmo abre. Pedir ao usuário o endereço atual do cálculo (qualquer tela) e abri-lo numa aba própria. O `conversationId` muda a cada login e a cada navegação; um endereço recente da mesma sessão costuma funcionar.
- Se a extensão não conectar (lista de navegadores vazia), pedir ao usuário que feche e reabra o navegador e confira a conta logada na extensão.
- Fechar a aba própria ao terminar.

## Técnicas que funcionam

- **Navegação:** menu lateral (links AJAX). Após cada clique, aguardar 2–3 s e capturar a tela.
- **Datas e campos com máscara:** clicar no campo, `ctrl+a`, `Delete` e digitar só os números (`05072024`). Clique triplo não substitui o valor.
- **Campos decimais:** a máscara preenche da direita. Digitar os centavos: `1500` vira 15,00; `3647` vira 36,47. Digitar `15` resulta em 0,15.
- **Combos:** `form_input` funciona para a maioria, mas nem sempre dispara o AJAX. Após mudar um combo, capturar a tela e conferir o que mais mudou.
- **Base de cálculo das verbas:** escolher o histórico no combo **não basta**; é obrigatório clicar em "Adicionar Base" (ícone +) até a base aparecer na tabela abaixo. Sem isso, o salvamento falha com "Campo obrigatório: Histórico Salarial".
- **Grades com muitos valores** (histórico salarial, ocorrências de verba): preencher por JavaScript, localizando cada linha pela competência e o campo pelo `id` (`...:valor`, `...:valorDevido`), disparando `input`, `change` e `blur`. **Depois de salvar, reabrir a grade e reler todos os valores**: já houve perda de duas competências numa gravação.
- **Caixas de seleção e valores** nem sempre aparecem na leitura estrutural da página. Conferir por captura de tela ou por JavaScript (`checked`, `value`).
- **Diálogos "Confirma operação?"** ao mudar valor de verba: confirmar com "Ok".
- **Verificação:** após salvar, procurar "Operação realizada com sucesso" e reabrir a tela pelo menu para confirmar que gravou.

## Ordem e cuidados por tela

### 1. Dados do Cálculo (aba "Parâmetros do Cálculo")
Estado, Município, Admissão, Demissão, Ajuizamento, Data Inicial/Final, Prescrição, Regime, Maior e Última Remuneração, Prazo de Aviso Prévio, Projetar Aviso, Limitar Avos (normalmente desmarcado), Feriados, Carga Horária, Sábado. O campo **Comentários** sai no resumo do relatório: usar para observações da ficha (ex.: multa não apurada).

### 2. Férias
O sistema gera os períodos sozinho e **erra por padrão**: põe o gozo no fim do período concessivo e marca como "Indenizadas" períodos completos não gozados. Corrigir conforme a ficha: gozo real; "Perdidas" para período que o título não deferiu.

### 3. Histórico Salarial
O sistema cria a base "ÚLTIMA REMUNERAÇÃO" (sem FGTS, com contribuição social). Para FGTS de período não depositado, criar base própria: "Novo" → nome → Variável → Incidência FGTS → **desmarcar "Proporcionalizar FGTS"** se as bases já forem as efetivas → competências → valor → "Gerar Ocorrências" → ajustar a grade → Salvar. O 13º entra na base do mês em que foi pago (adiantamento em novembro, parcela final em dezembro).

### 4. Verbas
Usar "Expresso" e marcar as verbas da ficha. Depois, abrir cada uma (primeiro ícone) e conferir. **Padrões perigosos já vistos:**
- 13º SALÁRIO vem com período desde a admissão e ocorrência "Dezembro": restringir o período ao ano deferido, ou o sistema paga 13º de anos já quitados.
- FÉRIAS + 1/3: restringir o período ao período aquisitivo deferido.
- DEVOLUÇÃO DE DESCONTOS INDEVIDOS vem com ocorrência "Mensal": para valor único, trocar para "Desligamento", ou o valor se repete todo mês.
- VALE TRANSPORTE vem calculado por tarifa × 2 × dias úteis: para valores mensais da ficha, mudar para "Informado", desmarcar as exclusões e preencher a grade de ocorrências (segundo ícone).
- SALDO DE SALÁRIO, 13º e outras com base em histórico: "Adicionar Base" obrigatório; ajustar divisor e quantidade.
- Conferir as incidências (IRPF, Contribuição Social, FGTS) de cada verba contra a ficha.

**Regerar ocorrências:** alterar parâmetros de uma verba **não** atualiza as ocorrências já geradas. Depois de ajustar todas, selecionar todas e "Regerar" com **"Sobrescrever"** — mas só antes de editar grades manualmente. Depois de editar grades (ex.: vale-transporte), qualquer nova regeração deve usar **"Manter alterações"**.

### 5. FGTS
Destino (Pagar/Recolher), Multa (marcar; 20% ou 40%), Incidência da multa (para incluir depósitos existentes: "Sobre devido + saldo e/ou saque" e informar o saldo em "Saldo e/ou Saque", sem marcar "Deduzir do FGTS"). **"Excluir da Base da Multa o FGTS sobre Aviso Prévio" vem marcado por padrão**: desmarcar se a ficha mandar a multa sobre todos os depósitos.

### 6. Seguro-desemprego
Tela própria: Apurar, Tipo de Solicitação, Valor Calculado, base (Maior Remuneração ou Histórico). O sistema calcula parcelas e piso, mas vence todas as parcelas no mês da ruptura.

### 7. Contribuição Social e Imposto de Renda
Conferir os padrões (20% empresa, SAT 3%, terceiros; salários pagos desmarcado; IR com RRA). Salvar mesmo sem alteração.

### 8. Honorários
"Novo" → Tipo "Honorários de Sucumbência" → Devedor → Calculado → Alíquota (digitar centavos) → Base para Apuração → Credor (lista de advogados do processo).

### 9. Custas Judiciais
Conhecimento do reclamado: Calculada 2% ou Informada (vencimento + valor). Liquidação: conforme a ficha.

### 10. Correção, Juros e Multa
O padrão vem com IPCA-E e **juros na fase pré-judicial marcados (TRD)**, mais "Sem Juros" a partir do ajuizamento. Ajustar conforme o título: "Combinar com Outro Índice" (ex.: SELIC (Receita Federal) a partir do ajuizamento; IPCA a partir de 30/08/2024) e "Combinar com Outra Tabela de Juros" (ex.: Taxa Legal a partir de 30/08/2024), sempre com "Adicionar" após escolher índice e data.

## Liquidação e conferência

1. Operações → Liquidar. Ler as pendências: erros impedem; alertas devem ser explicados (ex.: base de FGTS sem valor em meses não deferidos é esperado).
2. Operações → Imprimir. A geração do relatório pela aba do Claude pode falhar (erro 503 ou abertura fora da aba). Nesse caso, pedir ao usuário que gere o PDF e anexe.
3. Conferir o relatório contra a ficha, item por item: dias de aviso, avos de 13º e férias, bases, valores fixos e suas competências, cada competência de grades manuais, FGTS e base da multa, critério de correção e juros (página "Critério de Cálculo"), contribuição social, IR, honorários, custas e comentários no resumo.
4. Corrigir divergências, liquidar de novo e pedir novo relatório.
5. Registrar na ficha o resultado final e as decisões tomadas durante o lançamento.

## Ao final

Relatar ao usuário, em poucas linhas: total devido e sua composição; padrões do sistema alterados e por quê; pontos que dependem de decisão; e o cuidado de usar "Manter alterações" em futuras regerações, se houver grades editadas.