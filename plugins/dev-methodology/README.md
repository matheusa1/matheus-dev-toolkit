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
  - `convencoes-frontend` — componentes do design system (antd ou
    tailwind+shadcn, detectado por projeto) em vez de `<div>`/`<span>`
    crus, teste unitário restrito à camada core, tokens de tema em vez
    de valores fixos, sem ternário/condicional no `return`,
    componentes simples, sem estilo inline.
  - `commit-conventions` — Conventional Commits + emoji, escopo =
    branch, mensagem em português, sem trailer de co-autoria.
  - `debugging-sistematico` — investiga um bug relatado (reproduzir,
    coletar evidência, testar hipóteses, isolar causa raiz) antes de
    qualquer correção.
- **Subagents** (contexto isolado, mesmas regras das skills acima,
  sempre respondem em português do Brasil):
  - `revisor-arquiteto` — revisor read-only.
  - `parceiro-tdd` — implementa uma tarefa em TDD estrito.
  - `implementador-frontend` — implementa uma tela/componente de
    apresentação frontend sem teste e sem TDD, seguindo
    `convencoes-frontend`. Roda no lugar do `parceiro-tdd` para
    tarefas puramente de UI.
  - `gerador-modulo` — gera o esqueleto de um módulo novo.
  - `revisor-conformidade` — ao fim da implementação, compara o
    resultado com o arquivo de spec salvo em `docs/especificacao/` e
    o plano salvo em `docs/planos/`.
  - `investigador-bugs` — investiga um bug relatado até a causa raiz
    confirmada, sem sair corrigindo por tentativa e erro.
  - `redator-commit` — roda em Haiku, redige o texto do commit
    (título/descrição) sem gastar o modelo principal.
- **Hook**: lembrete no início da sessão apontando para
  `using-dev-methodology`.
- **Modelo por criticidade**: o modelo de `revisor-arquiteto`,
  `parceiro-tdd`, `implementador-frontend`, `gerador-modulo`,
  `revisor-conformidade` e `investigador-bugs` não é fixo — varia entre
  `haiku` (baixa), padrão da conversa (média) e `opus` (alta), conforme
  a criticidade marcada na tarefa do plano. Ver "Modelo por
  criticidade" em `using-dev-methodology`.

## Fluxo

```
brainstorming (spec em docs/especificacao/AAAA-MM-DD-nome-tarefa.md)
  → writing-plans (plano em docs/planos/AAAA-MM-DD-nome-tarefa.md, marca tarefas independentes com [P<n>])
  → [ para cada tarefa (ou grupo [P<n>] em paralelo): TDD (lógica) ou convencoes-frontend sem teste (tela/UI) → code-review-gate → commit-conventions ]
  → (opcional) clean-architecture-scaffold
  → revisor-conformidade (compara implementação final x spec e x plano)
```

Para um **bug relatado** (em vez de feature nova), o fluxo entra por
`debugging-sistematico` em vez de `brainstorming`:

```
debugging-sistematico (reproduzir → evidência → hipóteses → isolar → causa raiz confirmada)
  → TDD (teste que reproduz o bug → correção) → code-review-gate → commit-conventions
```

Tarefas do mesmo grupo `[P<n>]` no plano — ex: domain/application/infra
de um módulo novo, quando não dependem uma da outra nem tocam nos
mesmos arquivos — podem ser disparadas ao mesmo tempo, um agente por
tarefa (`parceiro-tdd` para lógica, `implementador-frontend` para
tela/apresentação). Veja "Execução em paralelo" em
`using-dev-methodology`.

Specs ficam em `docs/especificacao/` e planos em `docs/planos/` no
projeto onde a metodologia é usada, cada um com seu próprio
`.gitignore` (`*` + `!.gitignore`) para não entrarem no versionamento
do projeto.

## Instalar localmente para testar

```bash
claude --plugin-dir ./plugins/dev-methodology
```

## Instalar via marketplace

Veja o README na raiz do repositório.
