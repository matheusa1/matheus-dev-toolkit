# Execução em paralelo

Referência de `using-dev-methodology`, lida só antes de disparar um
grupo `[P<n>]`.

Este roteiro só se aplica quando delegação e worktrees estão disponíveis
e autorizadas. Use as ferramentas equivalentes do harness; os exemplos
`Agent`, `isolation` e `TaskUpdate` abaixo são do Claude Code. Se não
houver worktrees, execute as tarefas sequencialmente.

Tarefas do mesmo grupo `[P<n>]` rodam ao mesmo tempo, uma `Agent` por
tarefa (`parceiro-tdd` para lógica, `implementador-frontend` para
tela), **todas disparadas no mesmo turno**.

- **Máximo de 4 simultâneas.** Grupo maior → lotes de até 4; o próximo
  lote só sai depois que o anterior foi revisado e integrado.
- Cada agent recebe só a sua tarefa: descrição, texto completo dos
  `CAxx` que ela cobre, as regras de negócio e restrições técnicas
  que se aplicam a ela, arquivos que pode tocar e qualquer decisão
  combinada só na conversa (ele não vê esta conversa nem os arquivos
  gitignored de spec/plano).
- Marque cada task em andamento (`TaskUpdate`) ao disparar o agent.
- Revise cada tarefa assim que o agent dela termina, sem esperar o
  grupo. Tarefas dependentes do grupo só começam com **todas** as do
  grupo revisadas sem crítico e integradas.
- Dois agents tocando o mesmo arquivo apesar do plano = achado crítico:
  resolva manualmente e corrija o agrupamento no plano.

## Worktree por tarefa paralela

Grupos com 2+ tarefas rodam cada agent em worktree própria
(`isolation: "worktree"` na chamada `Agent`), para testes, build e diff
não interferirem entre si.

**Pré-condição**: a worktree nasce do `HEAD`, então o que o grupo usa
(tarefas anteriores) precisa estar commitado. Se não estiver — porque o
Matheus não está commitando por tarefa — execute as tarefas em sequência
no diretório principal, com o diff restrito por arquivos (ver "Diff da
tarefa"). Não crie commit temporário por conta própria.

**Antes de disparar**, detecte uma vez o gerenciador de pacotes e
monte o bloco de preparo que vai no prompt de cada agent:

| Detecção | Preparo na worktree |
|---|---|
| `bun.lock` / `bun.lockb` | `bun install --frozen-lockfile` |
| `yarn.lock` + `.yarnrc.yml` sem `nodeLinker: node-modules` (PnP) | `yarn install --immutable` |
| `yarn.lock` + `.yarnrc.yml` com `nodeLinker: node-modules` | `ln -s <raiz-principal>/node_modules node_modules` |
| `yarn.lock` sem `.yarnrc.yml` (Classic) | `ln -s <raiz-principal>/node_modules node_modules` |
| outro (`package-lock.json`, `pnpm-lock.yaml`) | `npm ci` / `pnpm install --frozen-lockfile` |

Em monorepo com `node_modules` aninhados, prefira o install ao symlink.
Some ao preparo: `cp <raiz-principal>/.env* . 2>/dev/null || true`.
`<raiz-principal>` é o caminho absoluto do diretório principal
(`git rev-parse --show-toplevel` antes de disparar).

**O agent**: roda o preparo, implementa, roda só os testes da tarefa,
**não commita**, e informa no resumo o caminho da worktree
(`pwd`) e a branch (`git branch --show-current`).

**Depois de cada agent**, o orquestrador:

1. Revisa pelo diff da worktree (ver "Diff da tarefa" em `regras-de-codigo`).
2. Integra no diretório principal, na ordem do plano:
   - Commitando por tarefa: commit **na worktree** com a mensagem de
     `commit-conventions` (escopo pela branch **principal**, não a da
     worktree), depois `git cherry-pick <sha>` no principal.
   - Sem commit: `git -C <worktree> diff --staged --binary | git apply`
     no principal.
3. Remove: `git worktree remove --force <worktree>` e
   `git branch -D <branch-da-worktree>`.

Depois de integrar o grupo inteiro, rode a suíte relacionada uma vez no
diretório principal.
