---
description: Revisa o código de uma tarefa recém-concluída contra o plano e as convenções do projeto, classificando problemas por severidade e bloqueando avanço em caso de problema crítico. Use ao final de cada tarefa do plano, antes de marcá-la como concluída ou seguir para a próxima.
---

# Code Review Gate

Objetivo: revisar o diff da tarefa recém-implementada e decidir se é
seguro seguir em frente.

## Antes de começar: inline ou subagent?

Inline ou agent `dev-methodology:revisor-arquiteto` (recomendado: evita
trazer o diff para o contexto principal). Decidido na rodada única de perguntas junto com o plano —
regras em `dev-methodology:using-dev-methodology`. Em diff de UI com
subagents, `revisor-acessibilidade` e `revisor-responsividade` rodam em
paralelo ao `revisor-arquiteto` (ver "Diff de UI" na mesma skill).

## Processo

1. Veja **só o diff desta tarefa** — nunca `git diff` puro, que inclui
   mudanças de outras tarefas não commitadas (ex: agents paralelos):
   - Em worktree: `git -C <worktree> add -A ':(exclude,glob)**/node_modules'`
     e `git -C <worktree> diff --staged`.
   - No diretório principal: `git diff HEAD -- <arquivos da tarefa>` e
     `git status --short -- <arquivos>` para arquivos novos.
   Se não souber quais arquivos são da tarefa, pergunte a quem pediu a
   revisão em vez de revisar o diff inteiro.
2. Revise contra:
   - **O plano**: a tarefa entrega o que foi prometido, nem mais nem
     menos?
   - **Testes**: existe teste cobrindo o comportamento novo? Ele
     passou de fato (RED antes, GREEN depois)?
   - **Arquitetura**: camadas respeitadas (domain não importa infra,
     application não conhece detalhes de framework), convenções de
     nomenclatura (`T`/`I`/`E` em TypeScript), DI correta (bindings
     Inversify no módulo certo).
   - **Segurança básica**: segredos expostos, entrada não validada,
     SQL/queries não parametrizadas.
   - **Legibilidade**: nomes claros, sem duplicação óbvia.
   - **Idioma**: identificadores, comentários e nomes de teste em
     inglês (specs, planos e commits seguem em português). Nome em
     português fora do padrão local é 🟡 aviso.
   - **SOLID**: classe/módulo com mais de uma responsabilidade,
     dependência de implementação concreta em vez de `I*`, interface
     inchada, subtipo que quebra o contrato do pai, ou alteração de
     código existente onde bastava estender. Violação clara é 🔴
     crítico quando compromete a arquitetura; caso contrário 🟡.
   - **Só se o diff tiver `.tsx`/`.jsx`** (UI): carregue a skill
     `dev-methodology:convencoes-frontend` e revise contra ela. Diff
     sem arquivo de UI não carrega essa skill. Redução de
     acessibilidade sem justificativa registrada é pelo menos 🟡, e 🔴
     se elimina acesso por teclado ou leitor de tela num fluxo
     essencial.
3. **Classifique cada achado por severidade:**
   - 🔴 **Crítico** — quebra a arquitetura, falta teste para lógica de
     negócio, bug real, segredo exposto. **Bloqueia** a próxima
     tarefa até ser corrigido.
   - 🟡 **Aviso** — deveria ser corrigido, mas não bloqueia (ex:
     nomenclatura inconsistente, duplicação pequena).
   - 🟢 **Sugestão** — melhoria opcional.
4. Apresente só os achados, agrupados por severidade, cada um com
   `arquivo:linha` e a correção sugerida em uma ou duas linhas — sem
   repetir o diff nem descrever o que está correto. Diff limpo:
   responda apenas `✅ Sem achados.`
5. Se houver crítico: pare, corrija (voltando ao TDD se for lógica
   faltando), revise de novo. Só considere a tarefa concluída sem
   crítico pendente.

## Regras

- Não invente problemas para parecer minucioso — se o diff está limpo,
  diga isso claramente e siga em frente.
- Seja específico: aponte arquivo e trecho, não faça observações
  genéricas tipo "melhorar tratamento de erros" sem dizer onde.
- Esta skill é sobre o diff da tarefa atual, não uma auditoria do
  projeto inteiro — não expanda escopo sem pedir.
