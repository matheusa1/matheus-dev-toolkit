---
description: Convenções de código para frontend (React) — escopo de teste unitário, preferência pelos componentes do design system em vez de elementos HTML crus, tokens de tema em vez de valores fixos, proibição de ternário/condicional dentro do return e de estilo inline, e componentização simples. Adapta-se ao design system do projeto (antd, tailwind+shadcn, etc). Use ao implementar ou revisar componentes de UI em projetos frontend — a implementação isolada de telas/componentes de apresentação usa o agent implementador-frontend, sem TDD.
---

# Convenções de frontend

Objetivo: manter componentes de apresentação simples, testáveis onde
importa e consistentes com o design system do projeto.

## 0. Detecte o design system do projeto primeiro

Antes de aplicar as regras 2 e 6 (tokens e componentes), identifique
qual design system o projeto usa — não assuma antd por padrão.

- Olhe `package.json`: `antd` presente → convenções antd. `tailwindcss`
  + `shadcn`/`@radix-ui`/componentes em `components/ui/` → convenções
  tailwind+shadcn.
- Projetos de trabalho (ex: repositórios da empresa) tendem a usar
  antd; projetos pessoais tendem a usar tailwind+shadcn — mas confirme
  sempre pelo `package.json`/imports reais do projeto, nunca por
  suposição de contexto.
- Se nenhum dos dois for detectado, pergunte ou siga o padrão que já
  aparece no código existente do projeto.

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
  vive em `core` — o ciclo RED-GREEN-REFACTOR continua valendo ali,
  aplicado pelo agent `parceiro-tdd`. A implementação da camada de
  apresentação em si (o que esta skill cobre) é feita pelo agent
  `implementador-frontend`, sem teste e sem ciclo TDD.

## 2. Tokens do tema, nunca valores fixos

Cores, espaçamentos, tamanhos de fonte, border-radius, etc. vêm sempre
dos tokens do tema do design system em uso, nunca hardcoded
(`#1677ff`, `16px`, `'red'`).

- **antd**: `theme.useToken()`, `token.colorPrimary`, `token.marginMD`,
  etc.
- **tailwind + shadcn**: classes utilitárias/tokens do tema
  (`bg-primary`, `text-muted-foreground`, `p-4`, `rounded-md`) e
  variáveis CSS definidas em `globals.css`/`tailwind.config` (ex:
  `--primary`, `--radius`), nunca valores arbitrários fora da escala
  (`className="p-[13px]"`, cor hex direto na classe).
- Antes de escrever um valor, pergunte-se: "existe um token/classe do
  design system para isso?" Cores, espaçamentos, tipografia e
  border-radius quase sempre têm.
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
estilização do projeto: styled-components, CSS Modules, classes do
antd + tokens via `theme.useToken()`, ou classes utilitárias do
tailwind combinadas com os tokens de tema do shadcn.

- Estilo inline não usa os tokens do design system (contradiz a regra
  2), não é reaproveitável e dificulta manutenção de tema (ex: dark
  mode).
- Se a única forma de aplicar um valor dinâmico parecer ser `style`
  inline, prefira variável CSS custom property atualizada via classe
  (ou `cn()`/`clsx` condicional no caso de tailwind), ou o mecanismo de
  estilização dinâmica do próprio design system.

## 6. Prefira sempre os componentes do design system a elementos HTML crus

Antes de escrever `<div>`, `<span>`, `<p>`, `<h1>` ou qualquer elemento
HTML solto, pergunte-se: **"existe um componente do design system que
faz isso?"** Quase sempre existe — e ele já traz tokens, tema (dark
mode), acessibilidade e espaçamento consistentes de graça. Use a
detecção da regra 0 para saber qual tabela aplicar.

### antd

| Em vez de | Use |
| --- | --- |
| `<div>` com `display: flex` / `gap` | `<Flex>` (`align`, `justify`, `gap`, `vertical`) |
| `<div>` só para espaçar filhos | `<Space>` (`direction`, `size`) |
| `<span>` / `<p>` / `<h1>` com texto | `<Typography.Text>` / `<Typography.Paragraph>` / `<Typography.Title>` |
| `<div>` com grid de colunas | `<Row>` + `<Col>` |
| `<div>` com borda/fundo de cartão | `<Card>` |
| `<div>` como separador | `<Divider>` |
| `<span>` com fundo colorido de rótulo | `<Tag>` ou `<Badge>` |
| `<img>` | `<Image>` (ou `<Avatar>` para foto/ícone circular) |
| `<button>` / `<a>` | `<Button>` (`type="link"` quando for link) |

### tailwind + shadcn

| Em vez de | Use |
| --- | --- |
| `<div>` com `display: flex` / `gap` | `<div className="flex gap-*">` (tailwind cobre isso nativamente — não existe componente shadcn dedicado) |
| `<span>` / `<p>` / `<h1>` com texto | componentes de `components/ui/typography` se o projeto tiver, senão elemento HTML com classes de tema (`text-muted-foreground`, etc.) |
| `<div>` com grid de colunas | `<div className="grid grid-cols-*">` |
| `<div>` com borda/fundo de cartão | `<Card>` / `<CardHeader>` / `<CardContent>` (shadcn) |
| `<div>` como separador | `<Separator>` (shadcn) |
| `<span>` com fundo colorido de rótulo | `<Badge>` (shadcn) |
| `<img>` | `<Avatar>` (shadcn) quando for foto/ícone circular; caso contrário `<img>` com classes de tema é aceitável — tailwind não força um wrapper |
| `<button>` / `<a>` | `<Button>` (shadcn, `variant="link"` quando for link) |
| dialog/modal, tooltip, dropdown, select | componente shadcn correspondente (`<Dialog>`, `<Tooltip>`, `<DropdownMenu>`, `<Select>`) em vez de HTML/lib crua |

- No stack tailwind+shadcn, `<div>`/`<span>` com classes utilitárias
  **não** é uma violação por si só — tailwind é utility-first e não tem
  componente para todo elemento de layout, diferente do antd. A regra
  6 se aplica principalmente quando existe um componente shadcn
  equivalente (Card, Button, Badge, Dialog, etc.) e o código usa HTML
  cru + estilização manual em vez dele.
- Um `<div>` cru só se justifica quando **nenhum** componente do design
  system cobre o caso (um wrapper de posicionamento absoluto, um
  overlay específico, ou — no caso tailwind — layout puro sem
  componente correspondente). Nesse caso, em projetos antd, deixe
  claro no código/review que foi uma escolha consciente, não descuido.
- Isso vale junto com a regra 5: trocar `<div style={{ display: 'flex',
  gap: 8 }}>` por `<Flex gap="small">` (antd) ou por
  `<div className="flex gap-2">` (tailwind) resolve estilo inline **e**
  uso de valor fixo de uma vez.
- Regra prática para o code review: em projeto antd, se o diff
  introduziu `<div>` ou `<span>` novos onde a tabela antd tem
  equivalente, isso é um achado — pelo menos 🟡 aviso. Em projeto
  tailwind+shadcn, o achado só vale quando existe componente shadcn
  equivalente disponível e não usado (Card, Button, Badge, Dialog,
  Separator, etc.) — `<div>` com classes utilitárias de layout é
  normal.
