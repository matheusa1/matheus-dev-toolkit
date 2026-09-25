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

## Regras de código (valem para todo desenvolvimento)

Estas duas regras se aplicam a qualquer código escrito ou revisado
com este plugin, inline ou por subagent:

- **Código majoritariamente em inglês.** Identificadores (variáveis,
  funções, classes, tipos, arquivos, pastas), comentários, mensagens
  de erro e nomes de teste ficam em inglês. Specs, planos, conversa e
  mensagens de commit continuam em português (ver `commit-conventions`).
  Exceção: termos de domínio sem tradução natural podem ficar no
  idioma original — mantenha-os consistentes e evite misturar
  idiomas dentro do mesmo nome. Em código existente com nomes em
  português, não renomeie por conta própria fora do escopo da
  tarefa; siga a convenção local e sinalize.
- **Sempre respeitar SOLID.** Uma responsabilidade por classe/módulo
  (S); estender por abstração em vez de editar código existente (O);
  implementações substituíveis pelo contrato que declaram (L);
  interfaces pequenas e focadas, sem forçar dependência de métodos
  não usados (I); depender de abstrações (`I*`/ports), nunca de
  implementações concretas (D). Se uma tarefa parece exigir violar
  algum princípio, pare e pergunte ao Matheus antes de seguir.

## Bug relatado? Investigue antes de corrigir

Se o pedido é um bug, erro ou comportamento inesperado relatado pelo
Matheus (não uma feature nova), o fluxo abaixo não se aplica direto —
use primeiro a skill `debugging-sistematico`, aplicada **inline** ou
pelo agent `investigador-bugs` isolado (pergunte antes, mesma lógica
de "Pergunte antes de decidir inline vs. subagent"). Reproduza, colete
evidência, teste hipóteses e confirme a causa raiz antes de escrever
qualquer correção. Só depois da causa raiz confirmada entre no fluxo
normal a partir do passo 3a (TDD) para a correção em si — não é
preciso brainstorming/plano para um bug pontual, a menos que a
investigação revele que o problema é maior do que um bug isolado.

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
3. **Para cada tarefa do plano**, decida primeiro se ela é de tela/
   apresentação frontend ou de lógica testável:
   a. **Tarefa de tela/componente de apresentação frontend**
      (`components/`, `pages/`, JSX que só renderiza, sem lógica
      própria) → skill `convencoes-frontend`, aplicada **inline** ou
      pelo agent `implementador-frontend` isolado — pergunte antes (ver
      "Pergunte antes de decidir inline vs. subagent" abaixo). Sem
      ciclo RED-GREEN-REFACTOR e sem teste unitário para essa tarefa.
      Se a tarefa mistura lógica com UI, extraia a lógica para `core`
      e trate-a pelo passo 3a' (TDD) antes de implementar a
      apresentação por cima.
   a'. **Qualquer outra tarefa** (lógica testável: domain, application,
      infra, hooks/services/utils de `core`) → skill
      `test-driven-development`, aplicada **inline** ou pelo agent
      `parceiro-tdd` isolado — pergunte antes (ver "Pergunte antes de
      decidir inline vs. subagent" abaixo). RED (teste falhando) →
      GREEN (implementação mínima) → REFACTOR. Nunca escreva código de
      implementação antes de existir um teste falhando para ele.
   b. **Code review com gate** → skill `code-review-gate`, aplicada
      **inline** ou pelo agent `revisor-arquiteto` isolado — pergunte
      antes, do mesmo jeito. Ao terminar a tarefa, revise o diff
      contra o plano e as convenções do projeto, classificando
      problemas por severidade. Problemas críticos bloqueiam a
      próxima tarefa até serem corrigidos.
   c. **Commit** → skill `commit-conventions`, se o Matheus pedir para
      commitar. Um commit atômico por tarefa, Conventional Commits com
      emoji, escopo = tarefa da branch sem prefixo de tipo, mensagem em português.

   Tarefas marcadas como paralelizáveis no plano (mesmo grupo `[P<n>]`
   — ver `writing-plans`) são a exceção à pergunta: dispare
   automaticamente, sem perguntar, uma `Agent` por tarefa (
   `dev-methodology:parceiro-tdd` para as de lógica,
   `dev-methodology:implementador-frontend` para as de
   tela/apresentação), ao mesmo tempo, em vez de uma de cada vez — a
   marcação `[P<n>]` no plano já é a decisão tomada antecipadamente.
   Exemplo típico: implementar um módulo novo com um agente para
   domain, outro para application e outro para infra, todos
   simultâneos, porque nenhum depende do resultado do outro dentro do
   mesmo disparo. Veja a seção "Execução em paralelo" abaixo antes de
   disparar.
4. **Módulo novo em projeto TypeScript?** → skill
   `clean-architecture-scaffold`, aplicada **inline** ou pelo agent
   `gerador-modulo` isolado — pergunte antes. Gera o esqueleto
   domain/application/infra de um módulo novo, seguindo as convenções
   de nomenclatura (T/I/E) e o padrão de DI com Inversify.
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

## Pergunte uma vez: inline vs. subagent

Sempre que uma etapa do fluxo (TDD, code review, scaffold, revisão de
conformidade) puder rodar tanto inline nesta conversa quanto por um
subagent isolado, **é obrigatório perguntar ao Matheus** — não decida
sozinho e não assuma que inline é o padrão. Use `AskUserQuestion` (ou
pergunta direta em texto) com uma recomendação clara e o motivo (ex:
"revisor-arquiteto isolado evita poluir o contexto com o diff inteiro;
prefiro esse — pode ser inline se preferir rapidez").

- Pergunte **uma única vez por conversa**, na primeira oportunidade em
  que a decisão for necessária (ex: antes da primeira tarefa do plano,
  ou antes da primeira etapa aplicável se não houver plano formal) —
  não é preciso perguntar de novo a cada tarefa/etapa seguinte.
- Depois de obter a resposta, aplique essa preferência a todas as
  etapas seguintes da mesma conversa (TDD, code review, scaffold,
  investigação de bug, revisão de conformidade) sem repetir a
  pergunta.
- **Exceção**: tarefas do mesmo grupo `[P<n>]` (paralelas) não entram
  nessa pergunta — a paralelização já implica agents, dispare direto.
- Brainstorming (`brainstorming`) fica sempre inline — é conversa e
  decisão de design com o Matheus, não há agent equivalente e não faz
  sentido isolar essa etapa.
- Se o Matheus já disse nesta conversa como prefere (ex: "sempre usa
  subagent pra review", "pode ir tudo inline dessa vez"), respeite a
  preferência dada e não repita a pergunta.
- Se o Matheus pedir explicitamente para variar por tarefa (ex:
  "prefiro decidir tarefa a tarefa"), siga esse pedido e volte a
  perguntar a cada etapa — a regra de "uma vez só" é o padrão, não uma
  proibição.

## Execução em paralelo

Depois que o plano estiver confirmado e as tasks registradas, tarefas
do mesmo grupo `[P<n>]` podem ser implementadas simultaneamente, cada
uma em um agente separado (via `Agent`, um por tarefa) — `parceiro-tdd`
para tarefas de lógica, `implementador-frontend` para tarefas de
tela/apresentação — em vez de uma de cada vez.

- **Dispare todas as tarefas do grupo no mesmo turno**, uma chamada
  `Agent` por tarefa, para elas rodarem em paralelo de fato — chamadas
  sequenciais em turnos separados não paralelizam.
- **Máximo de 4 tarefas simultâneas.** Nunca dispare mais de 4 chamadas
  `Agent` no mesmo turno, mesmo que o grupo `[P<n>]` do plano tenha mais
  itens. Se o grupo tiver 5 ou mais tarefas, divida em lotes de até 4:
  dispare o primeiro lote, espere todas as tarefas do lote terminarem
  (implementação + `code-review-gate` de cada uma), e só então dispare
  o próximo lote. Isso vale mesmo que todas as tarefas do grupo sejam,
  em tese, independentes entre si — o limite é sobre custo/atenção de
  revisão simultânea, não sobre dependência.
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

`revisor-arquiteto`, `revisor-conformidade`, `parceiro-tdd`,
`implementador-frontend`, `gerador-modulo` e `investigador-bugs` rodam
com `model: inherit` por padrão, mas o modelo
pode e deve variar por tarefa: ao disparar via `Agent`, passe o
parâmetro `model` explicitamente conforme a criticidade da tarefa
(avaliada no plano ou no momento do disparo).

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
`implementador-frontend`, `revisor-arquiteto`, `gerador-modulo`,
`revisor-conformidade`, `investigador-bugs`), ele
segue as regras do projeto
— mas não todas pela mesma via:

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
  tarefa específica do plano (lógica testável: domain, application,
  infra, `core` de frontend).
- `implementador-frontend` — aplica `convencoes-frontend` para
  implementar uma tela/componente de apresentação frontend, sem teste
  e sem ciclo de TDD. Use no lugar do `parceiro-tdd` quando a tarefa
  for puramente de UI (`components/`, `pages/`, JSX que só renderiza).
- `gerador-modulo` — aplica `clean-architecture-scaffold` para
  gerar um módulo novo.
- `revisor-conformidade` — compara a implementação final com o
  arquivo de spec em `docs/especificacao/`, ao fim de todas as tarefas
  do plano.
- `investigador-bugs` — aplica `debugging-sistematico` para investigar
  um bug relatado até a causa raiz confirmada, antes de qualquer
  correção.

O modelo desses subagents não é fixo — veja "Modelo por
criticidade" acima para saber quando passar `haiku` ou `opus` em vez
de herdar o padrão. A mensagem de commit (`commit-conventions`) não
usa subagent — é escrita pelo orquestrador da conversa, que já tem o
contexto da tarefa.

Use os subagents quando quiser manter o contexto da tarefa isolado da
conversa principal (por exemplo, revisar um diff grande sem poluir o
contexto com o código inteiro).
