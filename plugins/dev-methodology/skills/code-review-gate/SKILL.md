---
name: code-review-gate
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

1. Veja **só o diff desta tarefa**, com os comandos de "Diff da
   tarefa" em `regras-de-codigo` — nunca `git diff` puro.
   Se não souber quais arquivos são da tarefa, pergunte a quem pediu a
   revisão em vez de revisar o diff inteiro.
2. Revise contra:
   - **O plano**: a tarefa entrega o que foi prometido, nem mais nem
     menos?
   - **Testes**: existe teste cobrindo o comportamento novo? Ele
     passou de fato (RED antes, GREEN depois)? Tarefa só de
     apresentação (`implementador-frontend`) não tem teste unitário
     por regra — não aponte falta de teste nela.
   - **Arquitetura**: camadas respeitadas (domain não importa infra,
     application não conhece detalhes de framework), convenções de
     nomenclatura (`T`/`I`/`E` em TypeScript), DI correta (bindings
     Inversify no módulo certo). `application`/`domain` não instanciam
     logger, cliente de telemetria nem qualquer classe de framework
     (ex: `new Logger(...)` do NestJS): log e telemetria entram como
     dependência injetada pelo container (porta `Pick<...>` ou `I*`).
     🟡 aviso; 🔴 se o use case passa a depender do framework para
     funcionar.
   - **Imports**: se o projeto define path aliases (`paths` no
     tsconfig), import que sai do módulo atual usa o alias, nunca
     `../../..`. Relativo só dentro do próprio módulo. Arquivo legado
     com relativo não é justificativa. 🟡 aviso.
   - **Segurança básica**: segredos expostos, entrada não validada,
     SQL/queries não parametrizadas.
   - **Legibilidade**: nomes claros, sem duplicação óbvia.
   - **Regras de código** (`regras-de-codigo`): idioma, SOLID,
     vizinho legado e tamanho (150 linhas por arquivo, 20 por função),
     com a severidade da tabela de lá.
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
