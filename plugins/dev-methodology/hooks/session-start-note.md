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
pequena junta spec e plano num arquivo com uma confirmação; grande
segue `dev-methodology:brainstorming` → `dev-methodology:writing-plans`
→ (`dev-methodology:test-driven-development` +
`dev-methodology:code-review-gate` + `dev-methodology:commit-conventions`
por tarefa, tarefas `[P<n>]` em paralelo) → revisão de conformidade.

Todas as skills deste plugin são invocadas com o prefixo
`dev-methodology:`. Se uma chamada `Skill` falhar com "Unknown skill",
tente de novo com o prefixo `dev-methodology:` antes de seguir sem ela
— nunca prossiga com o fluxo pulando uma skill que falhou em carregar.
