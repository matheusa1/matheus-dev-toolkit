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
   pequenas, testáveis e ordenadas. Apresente como checklist e confirme
   antes de executar.
3. **Para cada tarefa do plano**:
   a. **TDD** → skill `test-driven-development`. RED (teste falhando) →
      GREEN (implementação mínima) → REFACTOR. Nunca escreva código de
      implementação antes de existir um teste falhando para ele.
   b. **Code review com gate** → skill `code-review-gate`. Ao terminar
      a tarefa, revise o diff contra o plano e as convenções do
      projeto, classificando problemas por severidade. Problemas
      críticos bloqueiam a próxima tarefa até serem corrigidos.
   c. **Commit** → skill `commit-conventions`, se o Matheus pedir para
      commitar. Um commit atômico por tarefa, Conventional Commits com
      emoji, escopo = branch atual, mensagem em português.

   Tarefas marcadas como paralelizáveis no plano (mesmo grupo `[P<n>]`
   — ver `writing-plans`) podem ser disparadas ao mesmo tempo, uma
   `Agent` `dev-methodology:parceiro-tdd` por tarefa, em vez de uma de
   cada vez. Exemplo típico: implementar um módulo novo com um agente
   para domain, outro para application e outro para infra, todos
   simultâneos, porque nenhum depende do resultado do outro dentro do
   mesmo disparo. Veja a seção "Execução em paralelo" abaixo antes de
   disparar.
4. **Módulo novo em projeto TypeScript?** → skill
   `clean-architecture-scaffold`. Use para gerar o esqueleto
   domain/application/infra de um módulo novo, seguindo as convenções
   de nomenclatura (T/I/E) e o padrão de DI com Inversify.
5. **Ao terminar todas as tarefas do plano** → agent
   `revisor-conformidade`. Compare a implementação final contra o
   arquivo de spec salvo em `docs/especificacao/`, item a item
   (objetivo, não-objetivos, restrições, casos de borda, critérios de
   aceite). Só considere a feature pronta sem achados críticos
   pendentes.

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
  desta conversa.
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
