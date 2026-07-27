---
description: Refina um pedido de feature vago ou high-level em uma especificação clara antes de qualquer código ser escrito. Use no início de qualquer tarefa de desenvolvimento nova, quando o pedido for ambíguo, quando faltarem critérios de aceite, ou quando o Matheus disser algo como "quero implementar X" sem detalhar como.
---

# Brainstorming → Spec

Objetivo: transformar uma ideia em uma especificação curta e concreta
ANTES de escrever qualquer código. Não pule direto para a implementação.

## Processo

1. **Entenda o pedido tal como foi feito.** Não assuma detalhes que não
   foram ditos. Se o pedido já tem constraints claras, não pergunte de
   novo — apenas confirme seu entendimento.
2. **Faça perguntas objetivas, uma de cada vez (ou em lote curto)**,
   focadas no que muda a decisão de design:
   - Qual é o objetivo real (o problema que isso resolve)?
   - O que está fora de escopo (não-objetivos)?
   - Há restrições técnicas (stack, performance, compatibilidade)?
   - Quais são os casos de borda que importam?
   - Como saberemos que está pronto (critérios de aceite)?
3. **Escreva a spec** em formato curto:

   ```markdown
   ## Objetivo
   ...
   ## Não-objetivos
   ...
   ## Restrições
   ...
   ## Casos de borda
   ...
   ## Critérios de aceite
   ...
   ```

4. **Pare e peça confirmação** antes de seguir para o plano
   (`writing-plans`). Não implemente nada nesta etapa.

## Regras

- Não infira requisitos não-ditos e apresente como se fossem certos —
  marque como suposição e confirme.
- Prefira poucas perguntas de alto impacto a um questionário longo.
- Se o pedido já é uma spec completa (o Matheus já detalhou tudo),
  resuma de volta em 3-4 linhas para confirmar entendimento e siga
  direto para o plano, sem reabrir perguntas já respondidas.
