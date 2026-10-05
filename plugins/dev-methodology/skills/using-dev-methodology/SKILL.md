---
description: Explica a metodologia de desenvolvimento pessoal do Matheus e a ordem em que as outras skills deste plugin devem ser usadas. É o padrão para QUALQUER tarefa de desenvolvimento (implementar, corrigir, refatorar, revisar, commitar) neste projeto — consulte sempre no início da tarefa, mesmo que o pedido não mencione spec, plano ou TDD explicitamente. Só não se aplica se o Matheus disser explicitamente para não usar a metodologia/o plugin desta vez.
---

# Metodologia de desenvolvimento (dev-methodology)

Metodologia pessoal inspirada no Superpowers (obra/superpowers),
ajustada ao Matheus: full-stack TypeScript (NestJS, React, React
Native), Clean Architecture + DDD, TDD e processo antes de codar. Esta
skill é a **fonte única** das regras de orquestração — as outras skills
e agents apontam para cá em vez de repeti-las.

## Regra padrão: use sempre

- Use em toda tarefa de desenvolvimento, mesmo que o pedido não cite
  spec, plano ou TDD. "Implementa X"/"corrige Y" já é gatilho.
- Única exceção: pedido explícito na conversa ("sem a metodologia
  dessa vez", "vai direto ao código"). Vale só para aquela tarefa.
- "Usar a metodologia" não significa sempre o fluxo completo: o
  tamanho da tarefa define quais etapas rodam (ver abaixo).

## Regras de código (todo desenvolvimento, inline ou subagent)

- **Código em inglês**: identificadores, arquivos, comentários,
  mensagens de erro e nomes de teste. Specs, planos, conversa e
  commits em português. Termos de domínio sem tradução natural podem
  ficar no original, sem misturar idiomas no mesmo nome. Em código
  existente em português, siga a convenção local e sinalize — não
  renomeie fora do escopo.
- **SOLID sempre**: uma responsabilidade por classe/módulo (S);
  estender por abstração em vez de editar (O); implementações
  substituíveis pelo contrato (L); interfaces pequenas (I); depender de
  abstrações `I*`/ports, nunca de concretas (D). Se a tarefa parecer
  exigir violar algum, pare e pergunte.

## Bug relatado? Investigue antes de corrigir

Bug, erro ou comportamento inesperado → skill `debugging-sistematico`
(inline ou agent `investigador-bugs`). Confirme a causa raiz com
evidência; só então corrija entrando no passo 3 (TDD). Sem
brainstorming/plano para bug pontual, a menos que a investigação
revele algo maior.

## Tamanho da tarefa define o fluxo

Antes de qualquer etapa, classifique o pedido e diga em uma linha qual
tamanho escolheu e por quê (ex: "Tratei como **pequena**: 2 tarefas no
mesmo módulo, sem mudança de contrato — se quiser o fluxo completo, me
diga"). O Matheus pode reclassificar a qualquer momento.

| Tamanho | Quando | Fluxo |
|---|---|---|
| **Trivial** | typo, ajuste de string/config, mudança de 1 a poucas linhas óbvias, sem lógica nova | Direto ao código. Sem spec, plano ou pergunta. Rode o teste/lint relacionado e revise você mesmo o diff antes de reportar. |
| **Pequena** | até ~3 tarefas, um módulo, sem decisão arquitetural nova nem mudança de contrato público, nenhuma tarefa `[alta]` | Spec + plano **num único arquivo** (`docs/planos/`), **uma** confirmação com as perguntas juntas. Depois passo 3 normal. Conformidade final inline, checando os critérios de aceite do arquivo. |
| **Grande** | mais de ~3 tarefas, vários módulos, decisão arquitetural, contrato público novo/alterado, ou qualquer tarefa `[alta]` (auth, pagamentos, migração/exclusão de dados, domínio central) | Fluxo completo abaixo: spec e plano em arquivos separados, duas confirmações. |

Na dúvida entre dois tamanhos, escolha o maior. Bug com causa raiz
confirmada normalmente é trivial ou pequeno.

## Ordem do fluxo (tarefa grande)

1. **Spec** → `brainstorming`. Salva em
   `docs/especificacao/AAAA-MM-DD-nome-tarefa.md`, pede confirmação.
2. **Plano** → `writing-plans`. Checklist com tags `[P<n>]`,
   criticidade e arquivos de cada tarefa, salvo em
   `docs/planos/AAAA-MM-DD-nome-tarefa.md`, pede confirmação com a
   rodada única de perguntas (ver "Perguntas: uma rodada só").
3. **Para cada tarefa do plano**:
   a. **Tela/componente de apresentação** (`components/`, `pages/`,
      JSX que só renderiza) → `convencoes-frontend` (inline ou agent
      `implementador-frontend`). Sem TDD nem teste unitário. Se mistura
      lógica com UI, a lógica vai antes para `core` via 3a'.
   a'. **Lógica testável** (domain, application, infra, `core` de
      frontend) → `test-driven-development` (inline ou agent
      `parceiro-tdd`). Nunca implementação antes de teste falhando.
   b. **Code review** → `code-review-gate` (inline ou agent
      `revisor-arquiteto`), sempre com o diff **restrito à tarefa**
      (ver "Diff da tarefa"). Crítico bloqueia a próxima tarefa.
      **Só se for "Diff de UI"** (ver abaixo), entram também os
      revisores especialistas `revisor-acessibilidade` e
      `revisor-responsividade`.
   c. **Commit** → `commit-conventions`, se a resposta da rodada de
      perguntas foi "um commit por tarefa" (ou se o Matheus pedir). Um
      commit atômico por tarefa, escrito pelo orquestrador.
4. **Módulo novo em TypeScript** → `clean-architecture-scaffold`
   (inline ou agent `gerador-modulo`).
5. **Fim do plano** → comparação com a spec (inline ou agent
   `revisor-conformidade`, recomendado). Feature pronta só sem crítico.

## Perguntas: uma rodada só

Todas as decisões de execução vão **junto com a confirmação do plano**,
numa única `AskUserQuestion` (até 4 perguntas), em vez de pausas
espalhadas pelo fluxo:

1. **Plano** — Aprovar / Ajustar (na tarefa pequena, isso aprova spec
   e plano juntos).
2. **Execução** — Subagents (recomendado quando há 2+ tarefas ou diff
   grande: o contexto principal fica limpo) / Inline (mais rápido para
   1-2 tarefas curtas). Vale para TDD, frontend, review e scaffold.
3. **Commit** — Um commit por tarefa / Sem commit (eu commito depois).
   Define também como as worktrees paralelas são integradas.
4. **Conformidade final** (só tarefa grande) — Agent
   `revisor-conformidade` (recomendado) / Inline.

Regras:
- Sempre com a opção recomendada primeiro e o motivo na descrição.
- Pule a pergunta cuja resposta o Matheus já deu nesta conversa
  (ex: "usa subagent pra tudo", "commita cada tarefa").
- Depois dessa rodada, **não pergunte de novo** sobre execução, commit
  ou conformidade — aplique as respostas até o fim do plano. Só volte
  a perguntar se ele pedir para decidir tarefa a tarefa.
- Grupos `[P<n>]` sempre usam agents, qualquer que seja a resposta 2.
- Etapas fora de plano (ex: investigar bug) perguntam inline vs.
  agent na primeira vez que forem necessárias, e a resposta vale para
  o resto da conversa.
- `brainstorming` é sempre inline.

## Diff da tarefa

O review de uma tarefa olha **só** o que ela mudou — nunca `git diff`
puro, que mistura mudanças de outras tarefas ainda não commitadas:

- **Tarefa em worktree** (grupo paralelo): tudo na worktree é da
  tarefa — `git -C <worktree> add -A ':(exclude,glob)**/node_modules'`
  e depois `git -C <worktree> diff --staged`.
- **Tarefa no diretório principal**: `git diff HEAD -- <arquivos da
  tarefa>` (lista vinda do plano/resumo do agent), mais
  `git status --short -- <arquivos>` para ver arquivos novos.

Ao disparar o `revisor-arquiteto` (e os revisores de UI), passe no
prompt o comando exato de diff (ou a worktree + lista de arquivos) —
eles não adivinham o escopo.

## Diff de UI: revisores de acessibilidade e responsividade

Uma tarefa **altera interface de frontend** quando o diff dela cria ou
muda pelo menos um destes arquivos:

- componente/tela: `.tsx`, `.jsx`, `.vue`, `.svelte`, `.html`;
- estilo: `.css`, `.scss`, `.sass`, `.less`, CSS Modules,
  `*.styles.ts`/`*.styled.ts` (styled-components/emotion), `StyleSheet`
  do React Native;
- tema/layout global: `tailwind.config.*`, `globals.css`, tokens de
  tema do design system.

Não conta: teste (`*.test.tsx`, `*.spec.tsx`), story
(`*.stories.tsx`), arquivo de `core` sem JSX, ou `.tsx` cuja mudança é
só em lógica/tipos sem tocar no JSX nem em estilo.

Com diff de UI e execução por **subagents**, dispare no **mesmo turno**
do `revisor-arquiteto`, cada um com o mesmo escopo de diff:

- `revisor-acessibilidade` — semântica, teclado, leitor de tela,
  contraste.
- `revisor-responsividade` — mobile first, overflow, toque, telas
  estreitas e largas.

Regras:
- **Sem diff de UI, não dispare** nenhum dos dois — nem "por garantia".
- Tarefa **trivial** não dispara revisor (a autorrevisão do diff cobre).
- Execução **inline**: o `code-review-gate` inline já cobre as regras
  7 e 10 de `convencoes-frontend`; não dispare os agents.
- Com eles no ar, o `revisor-arquiteto` deixa as regras 7 e 10 para os
  especialistas, sem achado duplicado.
- Crítico de qualquer um dos três bloqueia a próxima tarefa, como no
  `code-review-gate`. Junte os achados dos três numa lista só antes de
  corrigir.
- Os revisores não contam no limite de 4 agents simultâneos de
  "Execução em paralelo" — o limite é para implementação.
- Se a tarefa reduziu acessibilidade por decisão confirmada pelo
  Matheus, diga isso no prompt do `revisor-acessibilidade`.

## Execução em paralelo

Tarefas do mesmo grupo `[P<n>]` rodam ao mesmo tempo, uma `Agent` por
tarefa (`parceiro-tdd` para lógica, `implementador-frontend` para
tela), **todas disparadas no mesmo turno**.

- **Máximo de 4 simultâneas.** Grupo maior → lotes de até 4; o próximo
  lote só sai depois que o anterior foi revisado e integrado.
- Cada agent recebe só a sua tarefa: descrição, critérios de aceite,
  arquivos que pode tocar e qualquer decisão combinada só na conversa
  (ele não vê esta conversa nem os arquivos gitignored de spec/plano).
- Marque cada task em andamento (`TaskUpdate`) ao disparar o agent.
- Revise cada tarefa assim que o agent dela termina, sem esperar o
  grupo. Tarefas dependentes do grupo só começam com **todas** as do
  grupo revisadas sem crítico e integradas.
- Dois agents tocando o mesmo arquivo apesar do plano = achado crítico:
  resolva manualmente e corrija o agrupamento no plano.

### Worktree por tarefa paralela

Grupos com 2+ tarefas rodam cada agent em worktree própria
(`isolation: "worktree"` na chamada `Agent`), para testes, build e diff
não interferirem entre si.

**Pré-condição**: a worktree nasce do `HEAD`, então o que o grupo usa
(tarefas anteriores) precisa estar commitado. Se não estiver — porque o
Matheus não está commitando por tarefa — rode o grupo no diretório
principal, sem worktree, com o diff restrito por arquivos (ver "Diff da
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

1. Revisa pelo diff da worktree (ver "Diff da tarefa").
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

## Modelo por criticidade

Agents herdam o modelo da conversa (`model: inherit`); passe `model` no
`Agent` conforme a tag de criticidade do plano:

- `[baixa]` (mecânica, sem regra de negócio) → `haiku`.
- média (padrão, sem tag) → não passe `model`.
- `[alta]` (auth, pagamentos, migração/exclusão de dados, domínio
  central) → `opus`.

Criticidade incerta = média.

## Contexto que o subagent recebe

- **Automático**: `CLAUDE.md` do projeto (e aninhados).
- **Precisa ler o repo**: padrões que só existem no código.
- **Só se estiver no prompt**: tudo que foi combinado nesta conversa e
  não está em arquivo. Na dúvida, inclua.

## Retorno enxuto dos agents

O resumo do agent entra inteiro no contexto principal. Todos os agents
deste plugin devolvem só o essencial, sem repetir o diff nem colar
saída de ferramenta:

- Implementação: arquivos criados/alterados, testes adicionados (1
  linha cada), resultado final dos testes, pendências.
- Review: `✅ Sem achados.` quando limpo; senão só os achados
  (severidade, `arquivo:linha`, correção sugerida).

## Quando pular etapas

- Tarefa trivial → direto ao ponto (ver "Tamanho da tarefa").
- Spec/plano já dados pelo Matheus → confirme e siga, sem refazer.
- Pedido explícito para pular uma etapa → respeite naquela tarefa.

## Progresso na interface

Plano com mais de uma tarefa → `TaskCreate`/`TaskUpdate`, espelhando o
checklist de `docs/planos/` (detalhes em `writing-plans`).

## Subagents disponíveis

Todos respondem em português do Brasil:

- `parceiro-tdd` — TDD de uma tarefa de lógica.
- `implementador-frontend` — tela/componente de apresentação, sem TDD.
- `revisor-arquiteto` — `code-review-gate` read-only.
- `revisor-acessibilidade` — acessibilidade do diff, só em diff de UI.
- `revisor-responsividade` — responsividade/mobile first do diff, só
  em diff de UI.
- `gerador-modulo` — `clean-architecture-scaffold`.
- `revisor-conformidade` — implementação vs. spec, no fim do plano.
- `investigador-bugs` — causa raiz de bug relatado.

Mensagem de commit não usa subagent: o orquestrador escreve.
