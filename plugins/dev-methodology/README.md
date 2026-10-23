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

O tamanho da tarefa define o fluxo: **trivial** vai direto ao código;
**pequena** junta spec e plano num único arquivo com uma confirmação;
**grande** segue o fluxo completo. Aprovação do plano, inline vs.
subagent, commit por tarefa e revisão de conformidade são perguntados
juntos, numa rodada única, e não se repetem durante a execução.

## O que tem aqui

- **Skills** (auto-ativadas por descrição):
  - `using-dev-methodology` — explica a ordem do fluxo (meta skill).
  - `brainstorming` — refina um pedido vago em spec antes de codar,
    sempre no formato história de usuário + critérios de aceitação
    `CAxx` em Dado/quando/então (base para casos de teste). Modelo em
    `exemplo.md`, com domínio fictício.
  - `casos-de-teste` — logo após a spec, gera os casos de teste
    (formato Xray manual: CTxx com pré-condição, requisitos CA e
    passos Ação | Dados | Resultado esperado) só a partir da spec, sem
    viés de implementação, com CTs de endpoint quando há API. Salvos em
    `docs/casos-teste/`. Modelo em `exemplo.md`, com domínio fictício.
  - `writing-plans` — quebra a spec em tarefas pequenas e testáveis.
  - `test-driven-development` — força RED-GREEN-REFACTOR.
  - `code-review-gate` — revisa cada tarefa com gate de severidade.
  - `clean-architecture-scaffold` — gera módulos domain/application/infra
    com convenções T/I/E e DI via Inversify.
  - `convencoes-frontend` — componentes do design system (antd ou
    tailwind+shadcn, detectado por projeto) em vez de `<div>`/`<span>`
    crus, teste unitário restrito à camada core, tokens de tema em vez
    de valores fixos, sem ternário/condicional no `return`,
    componentes simples, sem estilo inline, e acessibilidade mínima
    obrigatória (questiona antes de implementar algo que prejudique
    acessibilidade).
  - `commit-conventions` — Conventional Commits + emoji, escopo =
    tarefa da branch (sem prefixo `fix/`, `refact/`...), mensagem em português, sem trailer de co-autoria.
  - `debugging-sistematico` — investiga um bug relatado (reproduzir,
    coletar evidência, testar hipóteses, isolar causa raiz) antes de
    qualquer correção.
  - `documentacao-implementacao` — gera, quando o Matheus aceita ou
    pede, a documentação final da entrega em markdown (ticket,
    contratos, rotas novas e alteradas, mudanças de tela, impacto) a
    partir do diff real da branch, salva em `docs/implementacao/`.
    Formato de referência em `exemplo.md`, com domínio fictício.
  - `regras-de-codigo` — fonte única das regras de código e dos
    comandos de diff, pré-carregada nos agents (ver abaixo).
- **Regras de código** (skill `regras-de-codigo`, valem para todo
  desenvolvimento): código majoritariamente em inglês (specs, planos e
  commits seguem em português), sempre respeitando SOLID, e vizinho
  legado não é convenção: com dois padrões no repo, vale o documentado
  no `CLAUDE.md` ou o que respeita camadas/SOLID, com a divergência
  sinalizada. Arquivo com no máximo 150 linhas e função (inclusive
  componente) com no máximo 20, conferidos no `code-review-gate`:
  excedente em código novo bloqueia a tarefa. Os testes e2e de
  endpoint saem dos CTs de endpoint, com o `CTxx` no nome, e ficam
  como regressão.
- **Subagents** (contexto isolado, mesmas regras das skills acima,
  sempre respondem em português do Brasil):
  - `revisor-arquiteto` — revisor read-only.
  - `revisor-acessibilidade` — revisor read-only de acessibilidade
    (semântica, teclado, leitor de tela, contraste por estado,
    gráficos). Só disparado em tarefa que altera interface de
    frontend, junto com o `revisor-arquiteto`; limitação global (tema,
    `#root` do React) sai como pendência, sem bloquear a tarefa. Toda
    tarefa com diff de UI termina com conferência de Tab e da árvore de
    acessibilidade no navegador e um roteiro curto de teste com leitor
    de tela para o Matheus.
  - `revisor-responsividade` — revisor read-only de responsividade
    (mobile first, overflow, toque, telas estreitas e largas). Só
    disparado em tarefa que altera interface de frontend, junto com o
    `revisor-arquiteto`.
  - `parceiro-tdd` — implementa uma tarefa em TDD estrito.
  - `implementador-frontend` — implementa uma tela/componente de
    apresentação frontend sem teste e sem TDD, seguindo
    `convencoes-frontend`. Roda no lugar do `parceiro-tdd` para
    tarefas puramente de UI.
  - `gerador-modulo` — gera o esqueleto de um módulo novo.
  - `revisor-conformidade` — ao fim da implementação, compara o
    resultado com o arquivo de spec salvo em `docs/especificacao/` e
    o plano salvo em `docs/planos/`.
  - `executor-casos-teste` — no fim, depois da conformidade, executa
    os casos de teste de `docs/casos-teste/` contra a aplicação
    rodando (endpoints via HTTP, telas via navegador) e marca
    divergências no próprio arquivo.
  - `investigador-bugs` — investiga um bug relatado até a causa raiz
    confirmada, sem sair corrigindo por tentativa e erro.
- **Hook**: lembrete no início da sessão (e depois de compactar o
  contexto) apontando para `using-dev-methodology`.
- **Modelo por criticidade**: o modelo de `revisor-arquiteto`,
  `revisor-acessibilidade`, `revisor-responsividade`, `parceiro-tdd`, `implementador-frontend`, `gerador-modulo`,
  `revisor-conformidade`, `executor-casos-teste` e `investigador-bugs` não é fixo — varia entre
  `haiku` (baixa), padrão da conversa (média) e `opus` (alta), conforme
  a criticidade marcada na tarefa do plano. Ver "Modelo por
  criticidade" em `using-dev-methodology`.

## Fluxo

```
brainstorming (spec em docs/especificacao/AAAA-MM-DD-nome-tarefa.md)
  → casos-de-teste (CTs em docs/casos-teste/AAAA-MM-DD-nome-tarefa.md, só a partir da spec)
  → writing-plans (plano em docs/planos/AAAA-MM-DD-nome-tarefa.md, marca tarefas independentes com [P<n>])
  → [ para cada tarefa (ou grupo [P<n>] em paralelo): TDD (lógica) ou convencoes-frontend sem teste (tela/UI) → code-review-gate (+ revisores de acessibilidade e responsividade se o diff altera UI) → commit-conventions ]
  → (opcional) clean-architecture-scaffold
  → revisor-conformidade (compara implementação final x spec e x plano)
  → executor-casos-teste (executa os CTs na aplicação rodando)
  → (opcional, se aceito) documentacao-implementacao (doc final em docs/implementacao/AAAA-MM-DD-ticket.md)
```

A documentação final nunca é gerada sem aceite: na tarefa pequena ela é
a 4ª pergunta da rodada única; na grande e em bug, é oferecida em uma
linha no relatório final; na trivial, só sob pedido.

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
tela/apresentação), cada um na própria git worktree para testes, build
e diff não interferirem entre si. O preparo de dependências da
worktree é detectado pelo lockfile (Bun, Yarn Berry/PnP, Yarn Classic
com symlink de `node_modules`), e o code review de cada tarefa olha só
o diff dela. Veja "Execução em paralelo" em `using-dev-methodology`.

Specs ficam em `docs/especificacao/`, casos de teste em
`docs/casos-teste/`, planos em `docs/planos/` e
documentações finais em `docs/implementacao/` no projeto onde a
metodologia é usada, cada um com seu próprio
`.gitignore` contendo só `*` (sem `!.gitignore`), para que nem os
arquivos nem o próprio `.gitignore` entrem no versionamento do projeto.

## Evals

`evals/` tem cenários de `claude plugin eval` que conferem o fluxo
(endpoint novo gera spec, casos de teste e plano no formato certo;
tarefa trivial vai direto; bug não gera spec nem plano). Rode a partir
desta pasta:

```bash
claude plugin eval . --allow-tools Write Edit
```

Os cenários não usam `Bash`: sem sandbox (bubblewrap) a ferramenta é
recusada. Mude uma regra do fluxo → rode as evals antes do PR.

## Versões

Histórico em [`CHANGELOG.md`](CHANGELOG.md), atualizado no mesmo commit
que muda a versão. O CI (`.github/workflows/validate.yml` na raiz)
valida o plugin, os JSON, a igualdade das versões Claude Code × Codex
e a entrada do CHANGELOG.

## Instalar

Publicado no marketplace `matheus-toolkit`
([`matheusa1/matheus-dev-toolkit`](https://github.com/matheusa1/matheus-dev-toolkit)):

```bash
/plugin marketplace add matheusa1/matheus-dev-toolkit
/plugin install dev-methodology@matheus-toolkit
```

Ativação em todo projeto, Codex CLI, teste local com `--plugin-dir` e
como versionar/publicar uma mudança: veja o README na raiz do
repositório.
