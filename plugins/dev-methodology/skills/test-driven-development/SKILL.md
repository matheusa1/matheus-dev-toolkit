---
description: Força o ciclo RED-GREEN-REFACTOR ao implementar qualquer lógica de negócio nova. Use sempre que for implementar uma tarefa do plano, corrigir um bug com lógica testável, ou escrever qualquer função/caso de uso novo.
---

# Test-Driven Development (RED-GREEN-REFACTOR)

Regra central: **nunca escreva código de implementação antes de existir
um teste que falhe por causa da ausência desse código.**

## Antes de começar: inline ou subagent?

Inline ou agent `dev-methodology:parceiro-tdd`. Decidido na rodada única de
perguntas junto com o plano; grupos `[P<n>]` vão direto para agents — regras em
`dev-methodology:using-dev-methodology`.

## Ciclo

1. **RED** — Escreva o teste que descreve o comportamento esperado.
   Rode **só o arquivo de teste da tarefa** e confirme que falha pelo
   motivo certo (não por erro de sintaxe ou import quebrado).
2. **GREEN** — Escreva a implementação mínima necessária para o teste
   passar. Nada de generalizar além do que o teste pede. Rode de novo
   só esse arquivo.
3. **REFACTOR** — Com os testes verdes, limpe o código (nomes,
   duplicação, estrutura) sem mudar comportamento e rode o arquivo de
   novo.
4. Repita para o próximo pedaço de comportamento.
5. Ao fechar a tarefa, rode uma vez a suíte relacionada (o módulo/pasta
   afetado) para pegar regressão.

Rode os testes no modo silencioso do runner (ex: `--silent`,
reporter `dot`) e, quando a saída for longa, filtre só as falhas —
saída inteira de teste gasta contexto sem ajudar.

## Se você perceber que escreveu implementação antes do teste

Pare. Descarte (ou comente) a implementação, escreva o teste primeiro,
veja-o falhar, e só então restaure a implementação. Isso não é
burocracia — é a garantia de que o teste realmente testa algo.

## Convenções

- Um teste por comportamento/caso de borda, não um teste gigante
  cobrindo tudo.
- Nomeie o teste pelo comportamento esperado, não pelo nome do método
  (`should reject an order without items`, não `testCreateOrder2`).
  Código e nomes de teste em inglês, e a implementação deve respeitar
  SOLID (ver `using-dev-methodology`, "Regras de código").
- Em projetos TypeScript/NestJS: teste unitário para domain/application
  (mocks para os ports/interfaces `I*`), teste de integração para
  infra (banco real ou testcontainer), teste e2e para os endpoints.
- Em projetos frontend: esta skill (e o agent `parceiro-tdd`) se aplica
  só à camada `core` (lógica de negócio, hooks com lógica, services,
  utils). Componentes de apresentação não recebem teste unitário e não
  passam por TDD — essas tarefas vão para a skill
  `convencoes-frontend`/agent `implementador-frontend` em vez desta.
- Não pule o passo RED "porque já sei que vai passar" — o objetivo é
  confirmar que o teste falha do jeito certo antes de confiar nele.

## Quando não aplicar TDD estrito

Para spikes exploratórios, scripts descartáveis, ou quando o Matheus
pedir explicitamente para pular, siga sem o ciclo — mas diga isso
explicitamente em vez de aplicar TDD parcialmente sem avisar.
