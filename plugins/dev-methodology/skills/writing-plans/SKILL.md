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
   - Listar os arquivos que cria ou altera (caminhos ou pastas). Essa
     lista é o que limita o diff do code review à tarefa e o que o
     agent paralelo pode tocar.
2. **Aponte decisões arquiteturais que a tarefa afeta** (nova camada,
   novo módulo, mudança de contrato) para que o code review saiba o
   que checar depois.
   - **Se a tarefa é de frontend e puramente de apresentação**
     (`components/`, `pages/`, JSX que só renderiza, sem lógica
     própria), registre no item que ela vai por `implementador-frontend`
     (ou inline com `convencoes-frontend`), sem teste unitário nem TDD.
     Se mistura lógica com UI, quebre em duas: lógica (`core`,
     `parceiro-tdd`, com teste) e apresentação (`implementador-frontend`),
     a segunda dependendo da primeira.
3. **Marque quais tarefas podem rodar em paralelo.** Duas tarefas só
   podem ser paralelas se, ao mesmo tempo:
   - Nenhuma depende do resultado da outra (não há import, contrato ou
     tipo que uma precise que a outra já tenha criado).
   - Não tocam nos mesmos arquivos nem em arquivos fortemente
     acoplados (ex: o mesmo `module.ts` de DI).
   - Nenhuma altera `package.json` ou lockfile — tarefa que adiciona,
     remove ou atualiza dependência é sempre sequencial (as worktrees
     paralelas compartilham as dependências do diretório principal, e
     dois lockfiles alterados em paralelo conflitam no merge).
   Agrupe essas tarefas com uma tag `[P<n>]` no checklist — tarefas com
   o mesmo `n` podem ser disparadas ao mesmo tempo; tarefas sem tag ou
   com `n` diferente seguem sequenciais. O caso mais comum é um módulo
   novo em Clean Architecture: domain, application e infra costumam
   ser paralelizáveis entre si (cada camada em seu próprio arquivo),
   mas o endpoint/controller normalmente depende do caso de uso e
   segue depois, sequencial.

   Um grupo pode ter mais de 4 tarefas: o orquestrador fatia o disparo
   em lotes de até 4 (`using-dev-methodology`), não é preciso quebrar o
   grupo por causa disso.
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
   - [ ] 1. Criar entidade de domínio `TOrder` + testes unitários — `domain/entities/`
   - [ ] 2. [P1] Implementar caso de uso `CreateOrder` (application) + testes — `application/use-cases/create-order*`
   - [ ] 3. [P1] Implementar repositório TypeORM (infra) + testes de integração — `infra/repositories/`
   - [ ] 4. [alta] Expor endpoint REST no controller + testes e2e (depende de 2 e 3, valida pagamento) — `infra/http/`
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

   - **Tarefa pequena**: o mesmo arquivo já começa com a seção
     `## Spec` escrita pelo `brainstorming`; acrescente o checklist
     abaixo dela em `## Plano`. Não existe arquivo em
     `docs/especificacao/` nesse caso.

7. **Peça confirmação numa rodada única** (`AskUserQuestion`): aprovar
   o plano (e a spec, na tarefa pequena) junto com as decisões de
   execução — subagents ou inline, commit por tarefa, e conformidade
   final (só tarefa grande). Perguntas, opções e regras em
   `dev-methodology:using-dev-methodology` → "Perguntas: uma rodada
   só" (carregue-a se ainda não estiver nesta sessão). Depois dessa
   rodada, execute o plano sem novas perguntas de processo.

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
