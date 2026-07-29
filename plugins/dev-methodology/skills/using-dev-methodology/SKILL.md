---
description: Explica a metodologia de desenvolvimento pessoal do Matheus e a ordem em que as outras skills deste plugin devem ser usadas. É o padrão para QUALQUER tarefa de desenvolvimento (implementar, corrigir, refatorar, revisar, commitar) neste projeto — consulte sempre no início da tarefa, mesmo que o pedido não mencione spec, plano ou TDD explicitamente. Só não se aplica se o Matheus disser explicitamente para não usar a metodologia/o plugin desta vez.
---

# Metodologia de desenvolvimento (dev-methodology)

Este plugin é uma metodologia pessoal, inspirada no framework Superpowers
(obra/superpowers), mas ajustada ao jeito de trabalhar do Matheus:
full-stack TypeScript (NestJS, React, React Native), Clean Architecture +
DDD, TDD, e disciplina de processo antes de "sair codando".

## Regra padrão: use sempre

Este plugin é o modo **padrão** de trabalhar em qualquer projeto onde
ele está instalado — não uma opção entre outras. Isso significa:

- **Use por padrão em toda tarefa de desenvolvimento**, mesmo que o
  pedido do Matheus não mencione spec, plano, TDD ou qualquer termo da
  metodologia. Um pedido simples como "implementa X" ou "corrige Y" já
  é gatilho suficiente — não espere ele pedir o processo explicitamente.
- **A única exceção é pedido explícito de não usar**, dito na mesma
  conversa, algo como "sem a metodologia dessa vez", "pode ir direto
  ao código", "não usa o plugin agora", "sem processo, só resolve
  rápido". Nesse caso, siga o pedido para aquela tarefa específica —
  isso não desativa o plugin para o resto da sessão nem para tarefas
  futuras, só para a que foi pedida.
- Não confunda isto com a seção "Quando pular etapas" abaixo: aquilo é
  sobre pular uma etapa específica dentro do fluxo (ex: sem TDD desta
  vez, mas ainda com spec e plano). Este bloco aqui é sobre usar o
  fluxo como um todo por padrão, a menos que o Matheus opte por sair
  dele.
- Na dúvida se o pedido é trivial o suficiente para pular o fluxo
  inteiro, não assuma que sim — trate como tarefa normal e siga a
  metodologia. É mais barato perguntar ou seguir o processo do que
  descobrir depois que faltou spec, teste ou review numa mudança que
  não era tão trivial assim.

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
   pequenas, testáveis e ordenadas. Apresente como checklist, salve em
   `docs/planos/AAAA-MM-DD-nome-tarefa.md` (mesmo nome da spec
   correspondente) e confirme antes de executar.
3. **Para cada tarefa do plano**:
   a. **TDD** → skill `test-driven-development`, aplicada **inline** ou
      pelo agent `parceiro-tdd` isolado — pergunte antes (ver "Pergunte
      antes de decidir inline vs. subagent" abaixo). RED (teste
      falhando) → GREEN (implementação mínima) → REFACTOR. Nunca
      escreva código de implementação antes de existir um teste
      falhando para ele.
   b. **Code review com gate** → skill `code-review-gate`, aplicada
      **inline** ou pelo agent `revisor-arquiteto` isolado — pergunte
      antes, do mesmo jeito. Ao terminar a tarefa, revise o diff
      contra o plano e as convenções do projeto, classificando
      problemas por severidade. Problemas críticos bloqueiam a
      próxima tarefa até serem corrigidos.
   c. **Commit** → skill `commit-conventions`, se o Matheus pedir para
      commitar. Um commit atômico por tarefa, Conventional Commits com
      emoji, escopo = branch atual, mensagem em português.

   Tarefas marcadas como paralelizáveis no plano (mesmo grupo `[P<n>]`
   — ver `writing-plans`) são a exceção à pergunta: dispare
   automaticamente, sem perguntar, uma `Agent`
   `dev-methodology:parceiro-tdd` por tarefa, ao mesmo tempo, em vez
   de uma de cada vez — a marcação `[P<n>]` no plano já é a decisão
   tomada antecipadamente. Exemplo típico: implementar um módulo novo
   com um agente para domain, outro para application e outro para
   infra, todos simultâneos, porque nenhum depende do resultado do
   outro dentro do mesmo disparo. Veja a seção "Execução em paralelo"
   abaixo antes de disparar.
4. **Módulo novo em projeto TypeScript?** → skill
   `clean-architecture-scaffold`, aplicada **inline** ou pelo agent
   `gerador-modulo` isolado — pergunte antes. Gera o esqueleto
   domain/application/infra de um módulo novo, seguindo as convenções
   de nomenclatura (T/I/E) e o padrão de DI com Inversify.
   - **Tarefa é de frontend (componente de UI)?** → skill
     `convencoes-frontend`, sempre inline, junto com o TDD/code review
     da tarefa (não é uma etapa separada a perguntar) — teste unitário
     restrito à camada core, tokens do antd, sem ternário/condicional
     no `return`, componentes simples, sem estilo inline.
5. **Ao terminar todas as tarefas do plano**: pergunte se a
   comparação final entre a implementação e a spec deve rodar
   **inline** ou pelo agent `revisor-conformidade` isolado (a
   recomendação padrão é o agent, para não poluir o contexto principal
   com o diff inteiro do plano). Compare item a item contra o arquivo
   de spec salvo em `docs/especificacao/` (objetivo, não-objetivos,
   restrições, casos de borda, critérios de aceite) e confira contra o
   arquivo de plano em `docs/planos/` que todas as tarefas previstas
   foram implementadas. Só considere a feature pronta sem achados
   críticos pendentes.

## Pergunte antes de decidir inline vs. subagent

Sempre que uma etapa do fluxo (TDD, code review, scaffold, revisão de
conformidade) puder rodar tanto inline nesta conversa quanto por um
subagent isolado, **pergunte ao Matheus antes de escolher** — não
decida sozinho e não assuma que inline é o padrão. Use `AskUserQuestion`
(ou pergunta direta em texto) com uma recomendação clara e o motivo
(ex: "revisor-arquiteto isolado evita poluir o contexto com o diff
inteiro; prefiro esse — pode ser inline se preferir rapidez").

- Pergunte **por etapa/tarefa**, não uma vez só no início do plano — a
  escolha certa pode mudar tarefa a tarefa (uma tarefa trivial pode ir
  inline, uma tarefa de autenticação pode pedir isolamento).
- **Exceção**: tarefas do mesmo grupo `[P<n>]` (paralelas) não entram
  nessa pergunta — a paralelização já implica agents, dispare direto.
- Brainstorming (`brainstorming`) fica sempre inline — é conversa e
  decisão de design com o Matheus, não há agent equivalente e não faz
  sentido isolar essa etapa.
- Se o Matheus já disse nesta conversa como prefere (ex: "sempre usa
  subagent pra review", "pode ir tudo inline dessa vez"), respeite a
  preferência dada e não repita a pergunta por tarefa.

## Execução em paralelo

Depois que o plano estiver confirmado e as tasks registradas, tarefas
do mesmo grupo `[P<n>]` podem ser implementadas simultaneamente, cada
uma em um agente `parceiro-tdd` separado (via `Agent`, um por tarefa),
em vez de uma de cada vez.

- **Dispare todas as tarefas do grupo no mesmo turno**, uma chamada
  `Agent` por tarefa, para elas rodarem em paralelo de fato — chamadas
  sequenciais em turnos separados não paralelizam.
- Cada agente recebe só a sua tarefa (descrição, critérios de aceite,
  arquivos que deve tocar) — não o plano inteiro. Ele não tem contexto
  desta conversa (ver "O que os subagents herdam automaticamente"
  abaixo) — qualquer decisão combinada só verbalmente precisa ir no
  prompt de disparo.
- Marque cada task como em andamento (`TaskUpdate`) no momento em que
  o agente correspondente é disparado, não todas de uma vez no início.
- **Rode o `code-review-gate` de cada tarefa separadamente**, assim
  que o respectivo agente termina — não espere o grupo inteiro para
  revisar tudo junto.
- Só avance para as tarefas que dependem do grupo (ex: o endpoint que
  depende de application + infra) depois que **todas** as tarefas do
  grupo passaram no code review sem crítico pendente.
- Se, ao ver os diffs, dois agentes do mesmo grupo tocaram no mesmo
  arquivo apesar do plano dizer que não deveriam (import cruzado,
  mesmo arquivo de DI, etc.), trate como achado crítico do code
  review: resolva o conflito manualmente antes de seguir, e ajuste o
  plano/checklist para não repetir o agrupamento errado nas próximas
  tarefas.
- Na dúvida se algo pode rodar em paralelo, não force — dispare
  sequencial. Isso deveria já estar decidido no plano (`writing-plans`),
  não improvisado na hora de disparar os agentes.

## Modelo por criticidade

`revisor-arquiteto`, `revisor-conformidade`, `parceiro-tdd` e
`gerador-modulo` rodam com `model: inherit` por padrão, mas o modelo
pode e deve variar por tarefa: ao disparar via `Agent`, passe o
parâmetro `model` explicitamente conforme a criticidade da tarefa
(avaliada no plano ou no momento do disparo). `redator-commit` é
exceção — sempre roda em `haiku`, independente da criticidade, porque
só redige texto.

- **Baixa** (typo, ajuste de string, mudança cosmética, tarefa
  mecânica sem lógica de negócio) → `haiku`. Mais rápido e barato,
  suficiente para revisão/implementação de baixo risco.
- **Média** (tarefa comum do plano, CRUD, lógica de aplicação sem
  impacto direto em dinheiro/segurança/dados sensíveis) → **não passe
  `model`**, deixe herdar o modelo da conversa (padrão atual).
- **Alta** (autenticação, autorização, pagamentos, migração ou
  exclusão de dados, lógica de domínio central, qualquer coisa que
  seria caro corrigir depois em produção) → `opus`. Mais capaz, vale o
  custo extra quando o risco de um erro passar despercebido é alto.

Se a criticidade da tarefa não estiver clara, trate como **média** —
não force `haiku` para economizar nem `opus` "por segurança" sem
motivo concreto. Marque a criticidade de cada tarefa já no plano
(`writing-plans`), para não precisar decidir isso de novo na hora de
disparar o agente.

## O que os subagents herdam automaticamente

Sempre que uma etapa rodar por subagent (`parceiro-tdd`,
`revisor-arquiteto`, `gerador-modulo`, `revisor-conformidade`,
`redator-commit`), ele segue as regras do projeto — mas não todas pela
mesma via:

- **Automático, sem precisar passar nada**: o `CLAUDE.md` do projeto
  (e qualquer `CLAUDE.md` aninhado) é carregado pelo Claude Code para
  qualquer sessão que rode no diretório do projeto, incluindo a de
  subagents. Convenções documentadas ali chegam sozinhas.
- **Automático, mas exige que o agente vá olhar**: padrões que só
  existem no código (nomenclatura observada, estrutura de pastas, lint
  config) não são "empurrados" para o contexto do agente — ele precisa
  ler o repositório. Por isso os subagents deste plugin têm
  `Read`/`Grep`/`Glob` e as skills que eles carregam (`code-review-gate`,
  `clean-architecture-scaffold`) mandam explicitamente checar contra
  "as convenções do projeto" antes de aprovar ou gerar algo.
- **Não é herdado — precisa ir no prompt**: o histórico desta
  conversa. Um subagent começa sem nenhuma memória do que foi dito
  aqui. Se uma decisão foi combinada só verbalmente comigo e ainda não
  está no `CLAUDE.md` nem no código (ex: "usa Zod em vez de
  class-validator nesse módulo", uma exceção combinada para essa
  tarefa), ela só chega ao agente se for escrita explicitamente no
  prompt de disparo.

Regra prática ao montar o prompt de qualquer `Agent` deste plugin:
pergunte-se "isso está em um arquivo que o agente vai ler sozinho, ou
foi combinado só na conversa?" — se for só conversa, inclua no prompt;
não assuma que o agente vai "simplesmente saber".

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
isolada (contexto separado, ferramentas restritas). Todos respondem
sempre em português do Brasil:

- `revisor-arquiteto` — aplica `code-review-gate` como revisor
  read-only.
- `parceiro-tdd` — aplica `test-driven-development` para implementar uma
  tarefa específica do plano.
- `gerador-modulo` — aplica `clean-architecture-scaffold` para
  gerar um módulo novo.
- `revisor-conformidade` — compara a implementação final com o
  arquivo de spec em `docs/especificacao/`, ao fim de todas as tarefas
  do plano.
- `redator-commit` — roda em Haiku, redige título/descrição de commit
  em português a partir do diff (usado pela skill `commit-conventions`
  para não gastar o modelo principal com isso).

O modelo dos quatro primeiros não é fixo — veja "Modelo por
criticidade" acima para saber quando passar `haiku` ou `opus` em vez
de herdar o padrão.

Use os subagents quando quiser manter o contexto da tarefa isolado da
conversa principal (por exemplo, revisar um diff grande sem poluir o
contexto com o código inteiro).
