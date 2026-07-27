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
4. **Apresente como checklist markdown**, por exemplo:

   ```markdown
   - [ ] 1. Criar entidade de domínio `TPedido` + testes unitários
   - [ ] 2. [P1] Implementar caso de uso `CriarPedido` (application) + testes
   - [ ] 3. [P1] Implementar repositório TypeORM (infra) + testes de integração
   - [ ] 4. Expor endpoint REST no controller + testes e2e (depende de 2 e 3)
   ```

   Aqui as tarefas 2 e 3 dependem só da 1 (entidade já existe) e não
   compartilham arquivo entre si, então podem ser disparadas juntas
   (`[P1]`). A tarefa 4 depende das duas e por isso fica fora do grupo,
   rodando depois.

5. **Pare e peça confirmação** do plano antes de começar a implementar.

## Regras

- Não junte múltiplas responsabilidades em uma tarefa só (ex: domínio +
  infra + endpoint tudo junto) — quebre por camada quando fizer
  sentido para a arquitetura do projeto.
- Se o plano mudar durante a implementação (descoberta de algo novo),
  atualize o checklist explicitamente antes de continuar, não
  silenciosamente.
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
  o checklist markdown, para as duas fontes não ficarem divergentes.
