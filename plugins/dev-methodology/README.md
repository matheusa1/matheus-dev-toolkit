# dev-methodology

Metodologia de desenvolvimento pessoal para o Claude Code, inspirada no
[Superpowers](https://github.com/obra/superpowers) (obra), mas ajustada
ao fluxo de trabalho do Matheus: TypeScript full-stack (NestJS, React,
React Native), Clean Architecture + DDD, TDD e disciplina de processo
antes de codar.

**Este é o modo padrão de desenvolver em qualquer projeto onde o
plugin está instalado** — use em toda tarefa (implementar, corrigir,
refatorar, revisar, commitar), mesmo que o pedido não mencione spec,
plano ou TDD. Só não use se o Matheus pedir explicitamente para pular
a metodologia naquela tarefa específica. Ver `using-dev-methodology`.

## O que tem aqui

- **Skills** (auto-ativadas por descrição):
  - `using-dev-methodology` — explica a ordem do fluxo (meta skill).
  - `brainstorming` — refina um pedido vago em spec antes de codar.
  - `writing-plans` — quebra a spec em tarefas pequenas e testáveis.
  - `test-driven-development` — força RED-GREEN-REFACTOR.
  - `code-review-gate` — revisa cada tarefa com gate de severidade.
  - `clean-architecture-scaffold` — gera módulos domain/application/infra
    com convenções T/I/E e DI via Inversify.
  - `commit-conventions` — Conventional Commits + emoji, escopo =
    branch, mensagem em português, sem trailer de co-autoria.
- **Subagents** (contexto isolado, mesmas regras das skills acima,
  sempre respondem em português do Brasil):
  - `revisor-arquiteto` — revisor read-only.
  - `parceiro-tdd` — implementa uma tarefa em TDD estrito.
  - `gerador-modulo` — gera o esqueleto de um módulo novo.
  - `revisor-conformidade` — ao fim da implementação, compara o
    resultado com o arquivo de spec salvo em `docs/especificacao/`.
  - `redator-commit` — roda em Haiku, redige o texto do commit
    (título/descrição) sem gastar o modelo principal.
- **Hook**: lembrete no início da sessão apontando para
  `using-dev-methodology`.
- **Modelo por criticidade**: o modelo de `revisor-arquiteto`,
  `parceiro-tdd`, `gerador-modulo` e `revisor-conformidade` não é
  fixo — varia entre `haiku` (baixa), padrão da conversa (média) e
  `opus` (alta), conforme a criticidade marcada na tarefa do plano.
  Ver "Modelo por criticidade" em `using-dev-methodology`.

## Fluxo

```
brainstorming (spec em docs/especificacao/AAAA-MM-DD-nome-tarefa.md)
  → writing-plans (marca tarefas independentes com [P<n>])
  → [ para cada tarefa (ou grupo [P<n>] em paralelo): TDD → code-review-gate → commit-conventions ]
  → (opcional) clean-architecture-scaffold
  → revisor-conformidade (compara implementação final x spec)
```

Tarefas do mesmo grupo `[P<n>]` no plano — ex: domain/application/infra
de um módulo novo, quando não dependem uma da outra nem tocam nos
mesmos arquivos — podem ser disparadas ao mesmo tempo, um agente
`parceiro-tdd` por tarefa. Veja "Execução em paralelo" em
`using-dev-methodology`.

Specs ficam em `docs/especificacao/` no projeto onde a metodologia é
usada, com um `.gitignore` (`*` + `!.gitignore`) para não entrarem no
versionamento do projeto.

## Instalar localmente para testar

```bash
claude --plugin-dir ./plugins/dev-methodology
```

## Instalar via marketplace

Veja o README na raiz do repositório.
