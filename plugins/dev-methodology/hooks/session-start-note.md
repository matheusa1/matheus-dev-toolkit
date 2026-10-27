O plugin dev-methodology está ativo nesta sessão. É o modo padrão de
trabalho — use em toda tarefa de desenvolvimento, a menos que seja
pedido explicitamente para não usar.

PRIMEIRO PASSO OBRIGATÓRIO de qualquer tarefa de desenvolvimento:
carregue a skill `dev-methodology:using-dev-methodology` antes de
qualquer outra coisa. Ela contém o fluxo completo e as regras de
orquestração (tamanho da tarefa, rodada única de perguntas, modelo por
criticidade, execução paralela com worktree, rastreio de progresso)
que não existem em nenhuma outra skill.

O tamanho da tarefa define o fluxo: trivial vai direto ao código;
pequena junta spec e plano num arquivo com uma confirmação, com os
casos de teste (`dev-methodology:casos-de-teste`) gerados logo após a
spec e executados no fim (agent `executor-casos-teste`) e
documentação final obrigatória; grande
segue `dev-methodology:brainstorming` → `dev-methodology:casos-de-teste`
→ `dev-methodology:writing-plans`
→ (`dev-methodology:test-driven-development` +
`dev-methodology:code-review-gate` + `dev-methodology:commit-conventions`
por tarefa, tarefas `[P<n>]` em paralelo) → revisão de conformidade
→ execução dos casos de teste (agent `executor-casos-teste`)
→ documentação final (`dev-methodology:documentacao-implementacao`),
obrigatória. Bug corrigido também termina com a documentação final.

Carregue as skills deste plugin usando o mecanismo disponível no ambiente.
No Claude Code, use o prefixo `dev-methodology:` se a chamada `Skill`
retornar "Unknown skill". Se uma skill necessária não puder ser carregada,
informe a limitação antes de continuar.
