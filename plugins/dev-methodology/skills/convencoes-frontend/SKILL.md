---
description: Convenções de código para frontend (React/antd) — escopo de teste unitário, tokens do antd em vez de valores fixos, proibição de ternário/condicional dentro do return e de estilo inline, e componentização simples. Use ao implementar ou revisar componentes de UI em projetos frontend.
---

# Convenções de frontend

Objetivo: manter componentes de apresentação simples, testáveis onde
importa e consistentes com o design system do projeto.

## 1. Teste unitário só na camada core

Componentes de apresentação (a camada de UI que só renderiza —
`components/`, `pages/`, JSX em geral) **não têm teste unitário**.
Teste unitário se limita à camada `core` (lógica de negócio, hooks
customizados com lógica, services, utils, reducers, use cases).

- Se um componente de apresentação tem lógica complexa o suficiente
  para "merecer" teste, isso é sinal de que essa lógica deveria estar
  extraída para um hook ou função em `core`, testado lá — não que o
  componente deveria ganhar um teste de UI.
- Fluxos de UI, quando precisarem de cobertura, usam teste de
  integração/e2e (ex: Testing Library com foco em comportamento
  observável pelo usuário, Cypress/Playwright), não teste unitário do
  componente isolado.
- Isso não dispensa TDD (`test-driven-development`) para a lógica que
  vive em `core` — o ciclo RED-GREEN-REFACTOR continua valendo ali.

## 2. Tokens do antd, nunca valores fixos

Em projetos que usam antd, cores, espaçamentos, tamanhos de fonte,
border-radius, etc. vêm sempre dos tokens do tema (`theme.useToken()`,
`token.colorPrimary`, `token.marginMD`, etc.), nunca hardcoded
(`#1677ff`, `16px`, `'red'`).

- Antes de escrever um valor, pergunte-se: "existe um token do antd
  para isso?" Cores, espaçamentos, tipografia e border-radius quase
  sempre têm.
- Se o valor realmente não existe como token (caso raro), documente
  brevemente o motivo em vez de simplesmente hardcodar sem explicação.

## 3. Sem ternário ou condicional dentro do `return`

O `return` (ou JSX) de um componente não contém `? :`, `&&` condicional
nem qualquer lógica de decisão inline para renderizar algo diferente.

- Se um item pode variar (ex: badge de status, ícone condicional,
  texto que muda conforme uma prop), extraia um componente próprio
  para esse item, que decide sozinho o que renderizar.
- O componente pai só compõe: chama os componentes filhos, sem `if`,
  ternário ou `&&` decidindo o que aparece na árvore.
- Early return no topo da função (antes do JSX principal, ex.
  `if (loading) return <Spinner />`) é aceitável — a regra é sobre o
  `return`/JSX final não conter ramificação, não sobre proibir todo
  `if` no componente.

## 4. Componentes simples, não complexos

Evite componentes grandes fazendo muita coisa. Quebre em componentes
menores e mais específicos sempre que possível.

- Um componente deveria ser fácil de entender lendo de cima a baixo,
  sem precisar pular entre múltiplos blocos de lógica condicional.
- Se o componente está crescendo (muitas props, muitos estados, muita
  lógica de renderização), é sinal de dividir em componentes filhos
  menores, cada um com uma responsabilidade única.
- Isso anda junto com a regra 3: eliminar ternário/condicional do
  `return` naturalmente empurra para mais componentização.

## 5. Nunca use estilo inline

Sem `style={{ ... }}` em elementos JSX. Use os mecanismos de
estilização do projeto (styled-components, CSS Modules, classes do
antd, tokens via `theme.useToken()` combinados com CSS/classe).

- Estilo inline não usa tokens do antd (contradiz a regra 2), não é
  reaproveitável e dificulta manutenção de tema (ex: dark mode).
- Se a única forma de aplicar um valor dinâmico parecer ser `style`
  inline, prefira variável CSS custom property atualizada via classe,
  ou o mecanismo de estilização dinâmica do próprio design system.
