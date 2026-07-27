# dev-methodology

Metodologia de desenvolvimento pessoal para o Claude Code, inspirada no
[Superpowers](https://github.com/obra/superpowers) (obra), mas ajustada
ao fluxo de trabalho do Matheus: TypeScript full-stack (NestJS, React,
React Native), Clean Architecture + DDD, TDD e disciplina de processo
antes de codar.

## O que tem aqui

- **Skills** (auto-ativadas por descrição):
  - `using-dev-methodology` — explica a ordem do fluxo (meta skill).
  - `brainstorming` — refina um pedido vago em spec antes de codar.
  - `writing-plans` — quebra a spec em tarefas pequenas e testáveis.
  - `test-driven-development` — força RED-GREEN-REFACTOR.
  - `code-review-gate` — revisa cada tarefa com gate de severidade.
  - `clean-architecture-scaffold` — gera módulos domain/application/infra
    com convenções T/I/E e DI via Inversify.
- **Subagents** (contexto isolado, mesmas regras das skills acima):
  - `architect-reviewer` — revisor read-only.
  - `tdd-pairer` — implementa uma tarefa em TDD estrito.
  - `module-scaffolder` — gera o esqueleto de um módulo novo.
  - `spec-compliance-reviewer` — ao fim da implementação, compara o
    resultado com o arquivo de spec salvo em `docs/especificacao/`.
- **Hook**: lembrete no início da sessão apontando para
  `using-dev-methodology`.

## Fluxo

```
brainstorming (spec em docs/especificacao/AAAA-MM-DD-nome-tarefa.md)
  → writing-plans
  → [ para cada tarefa: TDD → code-review-gate ]
  → (opcional) clean-architecture-scaffold
  → spec-compliance-reviewer (compara implementação final x spec)
```

Specs ficam em `docs/especificacao/` no projeto onde a metodologia é
usada, com um `.gitignore` (`*` + `!.gitignore`) para não entrarem no
versionamento do projeto.

## Instalar localmente para testar

```bash
claude --plugin-dir ./plugins/dev-methodology
```

## Instalar via marketplace

Veja o README na raiz do repositório.
