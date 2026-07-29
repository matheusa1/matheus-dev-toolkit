O plugin dev-methodology está ativo nesta sessão. É o modo padrão de
trabalho — use em toda tarefa de desenvolvimento, a menos que seja
pedido explicitamente para não usar.

PRIMEIRO PASSO OBRIGATÓRIO de qualquer tarefa de desenvolvimento:
carregue a skill `dev-methodology:using-dev-methodology` antes de
qualquer outra coisa. Ela contém o fluxo completo e as regras de
orquestração (perguntar inline vs. subagent, modelo por criticidade,
rastreio de progresso, revisão final de conformidade) que não existem
em nenhuma outra skill. Sem ela carregada, o fluxo roda pela metade.

Ordem do fluxo: `dev-methodology:brainstorming` →
`dev-methodology:writing-plans` → (`dev-methodology:test-driven-development`
+ `dev-methodology:code-review-gate` + `dev-methodology:commit-conventions`
por tarefa, tarefas independentes podem rodar em paralelo) →
opcionalmente `dev-methodology:clean-architecture-scaffold` para
módulos novos em TypeScript.

Todas as skills deste plugin são invocadas com o prefixo
`dev-methodology:`. Se uma chamada `Skill` falhar com "Unknown skill",
tente de novo com o prefixo `dev-methodology:` antes de seguir sem ela
— nunca prossiga com o fluxo pulando uma skill que falhou em carregar.
