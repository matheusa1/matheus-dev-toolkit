---
description: Transforma uma especificação já aprovada em um plano de implementação dividido em tarefas pequenas, ordenadas e testáveis. Use depois da skill brainstorming e antes de escrever qualquer código de implementação.
---

# Writing Plans

Objetivo: quebrar uma spec aprovada em tarefas pequenas o suficiente
para cada uma ser implementada com TDD (um ciclo RED-GREEN-REFACTOR
por tarefa, ou poucos ciclos).

## Processo

1. **Liste as tarefas em ordem de dependência.** Cada tarefa deve:
   - Ter um resultado verificável (um teste que passa, um endpoint que
     responde, um componente que renderiza).
   - Ser pequena o suficiente para revisar em poucos minutos.
   - Declarar suas dependências (quais tarefas anteriores ela precisa).
2. **Aponte decisões arquiteturais que a tarefa afeta** (nova camada,
   novo módulo, mudança de contrato) para que o code review saiba o
   que checar depois.
   - **Se a tarefa é de frontend e puramente de apresentação**
     (`components/`, `pages/`, JSX que só renderiza, sem lógica
     própria), registre no próprio item do plano que ela vai pelo agent
     `dev-methodology:implementador-frontend` (ou inline com a skill
     `dev-methodology:convencoes-frontend`) em vez de
     `parceiro-tdd`/`test-driven-development` — sem teste unitário e
     sem ciclo RED-GREEN-REFACTOR para essa tarefa, só as convenções de
     componentes do design system do projeto (antd ou tailwind+shadcn,
     a skill detecta qual), tokens de tema em vez de valores fixos, sem
     ternário/condicional no `return`, sem estilo inline. Se a tarefa
     mistura lógica com UI, quebre-a em duas: uma de lógica (`core`,
     `parceiro-tdd`, com teste) e uma de apresentação
     (`implementador-frontend`, sem teste), com a segunda dependendo da
     primeira.
3. **Marque quais tarefas podem rodar em paralelo.** Duas tarefas só
   podem ser paralelas se, ao mesmo tempo:
   - Nenhuma depende do resultado da outra (não há import, contrato ou
     tipo que uma precise que a outra já tenha criado).
   - Não tocam nos mesmos arquivos nem em arquivos fortemente
     acoplados (ex: o mesmo `module.ts` de DI).
   Agrupe essas tarefas com uma tag `[P<n>]` no checklist — tarefas com
   o mesmo `n` podem ser disparadas ao mesmo tempo; tarefas sem tag ou
   com `n` diferente seguem sequenciais. O caso mais comum é um módulo
   novo em Clean Architecture: domain, application e infra costumam
   ser paralelizáveis entre si (cada camada em seu próprio arquivo),
   mas o endpoint/controller normalmente depende do caso de uso e
   segue depois, sequencial.

   **Máximo de 4 tarefas por disparo simultâneo.** Um grupo `[P<n>]`
   pode ter quantas tarefas fizerem sentido logicamente, mas na hora de
   executar (`using-dev-methodology` → "Execução em paralelo") nunca
   mais de 4 rodam ao mesmo tempo — grupos maiores são disparados em
   lotes de até 4. Não é preciso quebrar o grupo em `[P<n>]` diferentes
   só por causa desse limite; é o orquestrador que fatia o disparo na
   hora de executar.
4. **Marque a criticidade de cada tarefa**: `[baixa]`, `[média]`
   (padrão, pode omitir a tag) ou `[alta]`. Alta é para autenticação,
   autorização, pagamentos, migração/exclusão de dados ou lógica de
   domínio central; baixa é para tarefa mecânica sem lógica de negócio
   (ex: ajuste de string, tipagem). Essa tag é o que a skill
   `using-dev-methodology` ("Modelo por criticidade") usa para decidir
   se o `Agent` de implementação/revisão da tarefa roda em `haiku`,
   herda o modelo padrão, ou roda em `opus`.
5. **Apresente como checklist markdown**, por exemplo:

   ```markdown
   - [ ] 1. Criar entidade de domínio `TPedido` + testes unitários
   - [ ] 2. [P1] Implementar caso de uso `CriarPedido` (application) + testes
   - [ ] 3. [P1] Implementar repositório TypeORM (infra) + testes de integração
   - [ ] 4. [alta] Expor endpoint REST no controller + testes e2e (depende de 2 e 3, valida pagamento)
   ```

   Aqui as tarefas 2 e 3 dependem só da 1 (entidade já existe) e não
   compartilham arquivo entre si, então podem ser disparadas juntas
   (`[P1]`), ambas com criticidade média (sem tag). A tarefa 4 depende
   das duas, fica fora do grupo paralelo, e é `[alta]` porque valida
   pagamento — o agente que a implementar/revisar deve rodar em
   `opus`.

6. **Salve o plano em arquivo**, não só na conversa:
   `docs/planos/AAAA-MM-DD-nome-tarefa.md`, usando a data atual e o
   mesmo nome curto em kebab-case da spec correspondente (ex:
   `docs/planos/2026-07-27-login-social.md`), com o checklist markdown
   do passo 5 (incluindo tags `[P<n>]` e criticidade).
   - Se `docs/planos/` ainda não existe no projeto, crie-a e adicione
     um `docs/planos/.gitignore` com este conteúdo, para os planos
     ficarem no disco mas fora do versionamento:

     ```gitignore
     *
     !.gitignore
     ```
   - Este arquivo é a fonte de verdade do plano durante toda a
     implementação — as tasks do `TaskCreate`/`TaskUpdate` espelham
     esse checklist, mas o arquivo é o que sobrevive a uma
     compactação de contexto ou a uma nova sessão.

7. **Pare e peça confirmação** do plano antes de começar a implementar.

## Antes de executar o plano: pergunte inline vs. subagent, uma vez

Com o plano confirmado, cada tarefa pode ser implementada e revisada
**inline** nesta conversa ou por um subagent isolado (`parceiro-tdd`
para tarefas de lógica, `implementador-frontend` para tarefas de
tela/apresentação, `revisor-arquiteto` para o code review). **É
obrigatório perguntar ao Matheus**, mas só **uma vez**, antes de
começar a primeira tarefa do plano — não decida sozinho e não assuma
que inline é o padrão. Apresente uma recomendação com o motivo (ex:
"revisor-arquiteto isolado evita poluir o contexto com o diff
inteiro").

- Reaproveite a resposta para todas as tarefas seguintes do plano
  (TDD e code review) sem perguntar de novo tarefa a tarefa.
- Exceção: tarefas do mesmo grupo `[P<n>]` já implicam agents em
  paralelo — dispare direto, sem perguntar.
- Se o Matheus já disse nesta conversa como prefere, respeite e não
  repita a pergunta.
- Ao terminar **todas** as tarefas, pergunte também se a comparação
  final com a spec roda inline ou pelo agent
  `dev-methodology:revisor-conformidade`
  (recomendação padrão: o agent) — essa é uma pergunta separada, feita
  uma única vez ao final.

O detalhamento completo está em `dev-methodology:using-dev-methodology`
— se essa skill ainda não foi carregada nesta sessão, carregue-a antes
de começar a implementar.

## Regras

- Não junte múltiplas responsabilidades em uma tarefa só (ex: domínio +
  infra + endpoint tudo junto) — quebre por camada quando fizer
  sentido para a arquitetura do projeto.
- Se o plano mudar durante a implementação (descoberta de algo novo),
  atualize o checklist explicitamente antes de continuar, não
  silenciosamente — no arquivo em `docs/planos/` e nas tasks, não só
  na conversa.
- Marque cada tarefa como concluída somente depois que o code review
  da tarefa (`code-review-gate`) não tiver mais problemas críticos.
- Na dúvida se duas tarefas podem ser paralelas, não marque — trate
  como sequencial. Conflito de merge custa mais caro que rodar em
  série.

## Use a interface do Claude Code para rastrear o progresso

Assim que o plano for confirmado, registre as tarefas com a ferramenta
`TaskCreate` (não só no markdown da conversa). Isso faz o progresso
aparecer tanto na interface do app quanto no terminal, permitindo que
o Matheus acompanhe em tempo real sem precisar reler a conversa.

- Crie uma task por item do checklist, na mesma ordem/dependência do
  plano.
- Ao começar uma tarefa, marque-a como em andamento antes de escrever
  qualquer código.
- Ao terminar uma tarefa (TDD completo + code review sem críticos),
  marque-a como concluída imediatamente — não acumule várias tarefas
  prontas para marcar todas de uma vez no final.
- Se o plano mudar durante a execução (nova tarefa, tarefa quebrada em
  duas, tarefa cancelada), atualize as tasks correspondentes junto com
  o checklist markdown **e** o arquivo em `docs/planos/`, para as três
  fontes não ficarem divergentes.
