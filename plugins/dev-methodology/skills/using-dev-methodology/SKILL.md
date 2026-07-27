---
description: Explica a metodologia de desenvolvimento pessoal do Matheus e a ordem em que as outras skills deste plugin devem ser usadas. Consulte sempre que uma tarefa de desenvolvimento nova estiver começando, especialmente quando o pedido for algo como "implementa X", "adiciona a feature Y" ou "corrige Z", ou quando não estiver claro por onde começar.
---

# Metodologia de desenvolvimento (dev-methodology)

Este plugin é uma metodologia pessoal, inspirada no framework Superpowers
(obra/superpowers), mas ajustada ao jeito de trabalhar do Matheus:
full-stack TypeScript (NestJS, React, React Native), Clean Architecture +
DDD, TDD, e disciplina de processo antes de "sair codando".

## Ordem do fluxo

Para qualquer tarefa de desenvolvimento não-trivial, siga esta ordem —
não pule etapas mesmo que o pedido pareça simples:

1. **Spec primeiro** → skill `brainstorming`. Nunca comece a escrever
   código a partir de um pedido vago. Refine o pedido em uma
   especificação curta (objetivo, não-objetivos, restrições, critérios
   de aceite), salve em
   `docs/especificacao/AAAA-MM-DD-nome-tarefa.md` e peça confirmação
   antes de seguir.
2. **Plano** → skill `writing-plans`. Quebre a spec aprovada em tarefas
   pequenas, testáveis e ordenadas. Apresente como checklist e confirme
   antes de executar.
3. **Para cada tarefa do plano**:
   a. **TDD** → skill `test-driven-development`. RED (teste falhando) →
      GREEN (implementação mínima) → REFACTOR. Nunca escreva código de
      implementação antes de existir um teste falhando para ele.
   b. **Code review com gate** → skill `code-review-gate`. Ao terminar
      a tarefa, revise o diff contra o plano e as convenções do
      projeto, classificando problemas por severidade. Problemas
      críticos bloqueiam a próxima tarefa até serem corrigidos.
4. **Módulo novo em projeto TypeScript?** → skill
   `clean-architecture-scaffold`. Use para gerar o esqueleto
   domain/application/infra de um módulo novo, seguindo as convenções
   de nomenclatura (T/I/E) e o padrão de DI com Inversify.
5. **Ao terminar todas as tarefas do plano** → agent
   `spec-compliance-reviewer`. Compare a implementação final contra o
   arquivo de spec salvo em `docs/especificacao/`, item a item
   (objetivo, não-objetivos, restrições, casos de borda, critérios de
   aceite). Só considere a feature pronta sem achados críticos
   pendentes.

## Quando pular etapas

- Correções triviais (typo, ajuste de string, mudança de uma linha)
  não precisam do fluxo completo — vá direto ao ponto.
- Se o Matheus já forneceu uma spec ou plano explícito na conversa,
  não refaça o brainstorming do zero; confirme o que já foi dito e
  siga para o plano ou para o TDD.
- Se o Matheus pedir explicitamente para pular uma etapa ("sem TDD
  dessa vez", "pode ir direto"), respeite o pedido para aquela tarefa.

## Progresso visível na interface

Sempre que houver um plano com mais de uma tarefa, use a ferramenta
`TaskCreate`/`TaskUpdate` do Claude Code para registrar e atualizar o
progresso — não deixe o acompanhamento só no texto da conversa. Isso
garante que o progresso apareça tanto na interface do app quanto no
terminal, em tempo real, tarefa por tarefa (ver detalhes em
`writing-plans`).

## Subagents disponíveis

Este plugin também inclui subagents que aplicam essas skills de forma
isolada (contexto separado, ferramentas restritas):

- `architect-reviewer` — aplica `code-review-gate` como revisor
  read-only.
- `tdd-pairer` — aplica `test-driven-development` para implementar uma
  tarefa específica do plano.
- `module-scaffolder` — aplica `clean-architecture-scaffold` para
  gerar um módulo novo.
- `spec-compliance-reviewer` — compara a implementação final com o
  arquivo de spec em `docs/especificacao/`, ao fim de todas as tarefas
  do plano.

Use os subagents quando quiser manter o contexto da tarefa isolado da
conversa principal (por exemplo, revisar um diff grande sem poluir o
contexto com o código inteiro).
