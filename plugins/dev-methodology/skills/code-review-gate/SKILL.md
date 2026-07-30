---
description: Revisa o código de uma tarefa recém-concluída contra o plano e as convenções do projeto, classificando problemas por severidade e bloqueando avanço em caso de problema crítico. Use ao final de cada tarefa do plano, antes de marcá-la como concluída ou seguir para a próxima.
---

# Code Review Gate

Objetivo: revisar o diff da tarefa recém-implementada e decidir se é
seguro seguir em frente.

## Antes de começar: inline ou subagent?

Esta revisão pode rodar inline nesta conversa ou pelo agent
`dev-methodology:revisor-arquiteto` isolado. Se essa decisão ainda não
foi tomada nesta conversa, **é obrigatório perguntar ao Matheus** —
não assuma inline. A recomendação padrão é o agent isolado, que evita
poluir o contexto principal com o diff inteiro. Se já foi perguntado e
respondido antes (mesmo para outra tarefa), reaproveite essa resposta
sem perguntar de novo. Exceção: tarefas do mesmo grupo `[P<n>]` do
plano. Detalhes em `dev-methodology:using-dev-methodology`.

## Processo

1. Rode `git diff` (ou `git diff --staged`) para ver exatamente o que
   mudou nesta tarefa. Foque só nos arquivos modificados.
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
   - **Se o diff é de frontend** (componentes de UI): aplique também a
     skill `dev-methodology:convencoes-frontend` — componentes do
     design system do projeto (antd ou tailwind+shadcn, a skill
     detecta qual) em vez de `<div>`/`<span>` crus, teste unitário
     restrito à camada core, tokens de tema em vez de valores fixos,
     sem ternário/condicional no `return`, componentes simples, sem
     estilo inline.
3. **Classifique cada achado por severidade:**
   - 🔴 **Crítico** — quebra a arquitetura, falta teste para lógica de
     negócio, bug real, segredo exposto. **Bloqueia** a próxima
     tarefa até ser corrigido.
   - 🟡 **Aviso** — deveria ser corrigido, mas não bloqueia (ex:
     nomenclatura inconsistente, duplicação pequena).
   - 🟢 **Sugestão** — melhoria opcional.
4. Apresente os achados agrupados por severidade, com o arquivo/linha e
   uma sugestão concreta de correção para cada um.
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
