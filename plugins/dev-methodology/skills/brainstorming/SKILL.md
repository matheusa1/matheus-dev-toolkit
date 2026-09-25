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

4. **Salve a spec em arquivo**, não só na conversa:
   `docs/especificacao/AAAA-MM-DD-nome-tarefa.md`, usando a data atual
   e um nome curto em kebab-case para a tarefa (ex:
   `docs/especificacao/2026-07-27-login-social.md`).
   - Se `docs/especificacao/` ainda não existe no projeto, crie-a e
     adicione um `docs/especificacao/.gitignore` com este conteúdo,
     para as specs ficarem no disco mas fora do versionamento:

     ```gitignore
     *
     !.gitignore
     ```
   - Este arquivo é a referência que o `revisor-conformidade` vai
     usar no fim da implementação para conferir se o que foi
     construído bate com o que foi especificado — por isso ele precisa
     existir em disco, não só ter sido dito na conversa.

5. **Pare e peça confirmação** antes de seguir para o plano
   (`writing-plans`). Não implemente nada nesta etapa.

## Tarefa pequena: spec dentro do plano

Se a tarefa foi classificada como **pequena** (ver "Tamanho da
tarefa" em `using-dev-methodology`), não crie arquivo em
`docs/especificacao/` nem peça confirmação separada:

- Faça só as perguntas indispensáveis (muitas vezes nenhuma).
- Escreva a spec como seção `## Spec` (com os mesmos cinco blocos,
  cada um em 1-3 linhas) no topo do arquivo de plano em
  `docs/planos/AAAA-MM-DD-nome-tarefa.md`.
- Siga direto para `writing-plans`, que acrescenta o checklist no mesmo
  arquivo e faz **uma** confirmação para spec + plano.

## Regras

- Não infira requisitos não-ditos e apresente como se fossem certos —
  marque como suposição e confirme.
- Prefira poucas perguntas de alto impacto a um questionário longo.
- Se o pedido já é uma spec completa (o Matheus já detalhou tudo),
  resuma de volta em 3-4 linhas para confirmar entendimento, salve o
  arquivo da mesma forma e siga direto para o plano, sem reabrir
  perguntas já respondidas.
- Se a spec mudar depois de confirmada (novo requisito descoberto
  durante o plano ou a implementação), atualize o mesmo arquivo em vez
  de criar um segundo — a spec em disco deve refletir a versão vigente.
