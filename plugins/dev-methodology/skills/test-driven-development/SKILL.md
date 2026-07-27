---
description: Força o ciclo RED-GREEN-REFACTOR ao implementar qualquer lógica de negócio nova. Use sempre que for implementar uma tarefa do plano, corrigir um bug com lógica testável, ou escrever qualquer função/caso de uso novo.
---

# Test-Driven Development (RED-GREEN-REFACTOR)

Regra central: **nunca escreva código de implementação antes de existir
um teste que falhe por causa da ausência desse código.**

## Ciclo

1. **RED** — Escreva o teste que descreve o comportamento esperado.
   Rode a suíte e confirme que ele falha, e que falha pelo motivo
   certo (não por erro de sintaxe ou import quebrado).
2. **GREEN** — Escreva a implementação mínima necessária para o teste
   passar. Nada de generalizar além do que o teste pede.
3. **REFACTOR** — Com os testes verdes, limpe o código (nomes,
   duplicação, estrutura) sem mudar comportamento. Rode os testes de
   novo depois de refatorar.
4. Repita para o próximo pedaço de comportamento.

## Se você perceber que escreveu implementação antes do teste

Pare. Descarte (ou comente) a implementação, escreva o teste primeiro,
veja-o falhar, e só então restaure a implementação. Isso não é
burocracia — é a garantia de que o teste realmente testa algo.

## Convenções

- Um teste por comportamento/caso de borda, não um teste gigante
  cobrindo tudo.
- Nomeie o teste pelo comportamento esperado, não pelo nome do método
  (`deve rejeitar pedido sem itens`, não `testCriarPedido2`).
- Em projetos TypeScript/NestJS: teste unitário para domain/application
  (mocks para os ports/interfaces `I*`), teste de integração para
  infra (banco real ou testcontainer), teste e2e para os endpoints.
- Não pule o passo RED "porque já sei que vai passar" — o objetivo é
  confirmar que o teste falha do jeito certo antes de confiar nele.

## Quando não aplicar TDD estrito

Para spikes exploratórios, scripts descartáveis, ou quando o Matheus
pedir explicitamente para pular, siga sem o ciclo — mas diga isso
explicitamente em vez de aplicar TDD parcialmente sem avisar.
