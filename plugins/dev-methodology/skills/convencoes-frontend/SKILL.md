---
description: Convenções de código para frontend (React) — implementação mobile first obrigatória (layout base para telas pequenas, breakpoints maiores só como exceção via min-width), escopo de teste unitário, preferência pelos componentes do design system em vez de elementos HTML crus, tokens de tema em vez de valores fixos, proibição de ternário/condicional dentro do return e de estilo inline, componentização simples, acessibilidade mínima obrigatória, proibição de lógica de negócio em .tsx/useEffect, e restrição de import de use case só em *.registry.ts da infra. Adapta-se ao design system do projeto (antd, tailwind+shadcn, etc). Use ao implementar ou revisar componentes de UI em projetos frontend — a implementação isolada de telas/componentes de apresentação usa o agent implementador-frontend, sem TDD.
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

## 7. Acessibilidade aceitável é obrigatória

Todo componente de apresentação implementado ou revisado sob esta
skill precisa manter um nível mínimo aceitável de acessibilidade — não
é opcional nem "para depois". Isso, na prática, quer dizer:

- **Elemento certo para a função**: `<button>`/componente de botão do
  design system para ações, não `<div onClick>`; `<a>`/link do design
  system para navegação; inputs sempre com `<label>` associado (ou
  `aria-label`/`aria-labelledby` quando não houver label visível).
  Seguir a tabela da regra 6 (componentes do design system em vez de
  HTML cru) já resolve boa parte disso, porque os componentes do
  antd/shadcn trazem semântica e ARIA corretos de fábrica.
- **Navegação por teclado**: qualquer elemento interativo precisa ser
  alcançável e operável via teclado (`Tab`, `Enter`/`Espaço`), sem
  remover o `outline`/foco visível do navegador ou do design system
  sem substituí-lo por um indicador de foco equivalente.
- **Texto alternativo**: `<img>`/`<Image>`/`<Avatar>` com conteúdo
  informativo sempre com `alt` descritivo; imagem puramente decorativa
  usa `alt=""` (não omite o atributo).
- **Não depender só de cor**: estado/erro/sucesso não pode ser
  comunicado só por cor — combine com ícone, texto ou padrão (ex: badge
  colorido acompanhado do texto do status, não só a cor de fundo).
- **Contraste**: use os tokens de tema do design system (regra 2), que
  já são calibrados para contraste adequado; se precisar de uma cor
  fora dos tokens, isso é ainda mais motivo para questionar antes de
  aplicar (ver abaixo).

### Se uma decisão da tarefa prejudicar a acessibilidade, questione antes de implementar

Se, ao implementar a tarefa como descrita, você perceber que o
resultado vai prejudicar a acessibilidade (ex: pedido explícito para
remover o foco visível, usar `<div>` clicável em vez de botão, omitir
`alt`/label, usar só cor para indicar estado, ou aplicar uma cor fora
dos tokens que reduz o contraste), **não implemente isso em silêncio
nem "corrija" por conta própria** — pare e pergunte se o objetivo é
mesmo abrir mão da acessibilidade ali (ex: "isso remove o indicador de
foco do teclado para todos os usuários desse componente — é essa a
intenção, ou posso manter/adaptar o foco visível?"). Só prossiga do
jeito que reduz acessibilidade se a resposta confirmar que é
intencional; caso contrário, implemente a alternativa acessível.

## 8. Sem lógica de negócio em `.tsx`, nem dentro de `useEffect`

Arquivo `.tsx` (componente de apresentação) não contém lógica de
negócio — cálculo, transformação de dado, regra de decisão — nem
lógica dentro de `useEffect`. Isso é verificado automaticamente pelo
`danger:check` do projeto.

- **Cálculo/transformação**: se o componente precisa de um valor
  derivado (ex: `const remaining = container.scrollHeight -
  container.scrollTop - container.clientHeight`), essa conta não vive
  solta no `.tsx` — extraia para uma função em `@core` (ou, no mínimo,
  um hook dedicado que a encapsula) e o componente só consome o
  resultado.
- **`useEffect` sem lógica dentro**: o corpo do `useEffect` não decide,
  calcula nem orquestra nada por conta própria. Extraia o
  comportamento para um `useCallback` (ou função de `@core`) e o
  `useEffect` só chama essa função — ele deve ser praticamente uma
  linha de disparo, não o lugar onde a lógica acontece.
- Isso é uma extensão da regra 1 (teste unitário só na camada core):
  se há lógica o bastante para justificar mover para `@core`, ela
  também passa a ser testável/testada lá, seguindo TDD via
  `parceiro-tdd`.
- Ao encontrar isso durante implementação (agent
  `implementador-frontend`) ou revisão, não “resolva” escondendo a
  lógica em outro lugar do mesmo `.tsx` — mova de fato para `@core` e
  deixe explícito no resumo o que foi extraído.

## 9. Use case só é importado em `*.registry.ts` da camada infra

Componentes, hooks e helpers de `@presentation` não importam use case
diretamente. Import de use case só é permitido em arquivos
`*.registry.ts` da camada infra — é lá que o use case é resolvido e
exposto (ex: via injeção/factory) para o resto do app consumir.

- Se um componente, hook (`useX.hooks.ts`) ou helper precisa do
  comportamento de um use case, ele deve obtê-lo através do que o
  `*.registry.ts` expõe (ex: uma factory/hook de infra já registrado),
  nunca com `import { AlgumUseCase } from '.../application/...'` direto
  no arquivo de apresentação.
- Isso vale mesmo quando o use case está sendo usado só para um
  cálculo simples dentro de um helper (`helper.ts`) — o import
  continua proibido fora de `*.registry.ts`, independente de quão
  pequeno for o uso.
- Ao implementar ou revisar, se a tarefa parecer exigir importar um
  use case direto em `@presentation`, isso é sinal de que falta um
  registro em `*.registry.ts` (infra) para expor esse caso de uso — a
  correção é criar/usar esse registro, não contornar a regra com
  import direto.

## 10. Implementação é sempre mobile first

Todo componente/tela é construído partindo do layout de tela pequena
como padrão, e telas maiores são tratadas como exceção/ajuste sobre
essa base — nunca o contrário. Isso evita retrabalho de
responsividade depois: a responsividade é parte da implementação
inicial, não um passo posterior.

- **Estilo base = mobile.** As classes/propriedades sem prefixo de
  breakpoint (tailwind) ou os valores padrão de um token/prop
  responsivo (antd) descrevem o layout de tela pequena. Ajustes para
  telas maiores entram como incremento sobre essa base, nunca como
  reset de um layout desktop pensado primeiro.
- **tailwind + shadcn**: use os prefixos de breakpoint (`sm:`, `md:`,
  `lg:`, `xl:`) sempre para adicionar/alterar comportamento em telas
  *maiores* que a base (`min-width`, que é o comportamento nativo do
  tailwind). Não use `max-w-*`/media query desktop-first como
  substituto disso — ex: escreva `className="flex flex-col md:flex-row
  gap-2 md:gap-4"` (coluna no mobile, linha a partir de `md`), não o
  inverso com override para baixo.
- **antd**: use os breakpoints do grid (`<Row>`/`<Col>` com props
  `xs`/`sm`/`md`/`lg`/`xl`/`xxl`, ou `Grid.useBreakpoint()`) definindo
  primeiro o valor de `xs` (mobile) e adicionando os breakpoints
  maiores só onde o layout realmente precisa mudar. Componentes como
  `<Flex>` que mudam de direção (`vertical` no mobile, horizontal no
  desktop) seguem a mesma lógica: vertical é o padrão, horizontal é o
  ajuste condicionado a breakpoint maior.
- **Toque antes de mouse**: áreas clicáveis/tocáveis (botões, itens de
  lista, controles) devem ter tamanho e espaçamento adequados a toque
  (dedo, não cursor preciso) por padrão; estados como `:hover` são
  complementares, nunca a única forma de revelar uma ação essencial,
  já que não existem em touch.
- **Sem overflow horizontal no mobile**: tabelas, grids de cartões,
  linhas com muitos itens lado a lado etc. precisam de uma solução
  pensada para telas estreitas desde o início (empilhar, virar lista,
  scroll horizontal controlado com indicação visual, componente
  responsivo do design system), não "funciona no desktop e depois se
  vê" — não implemente a versão desktop e adie a versão mobile para
  depois.
- Isso não substitui as regras 2 e 6 (tokens e componentes do design
  system) — os breakpoints e ajustes responsivos também usam os
  tokens/props do design system (regra 0 detecta qual), nunca valores
  fixos de media query hardcoded fora da escala do projeto.
- Ao implementar (agent `implementador-frontend`) ou revisar, se a
  tarefa/design de referência só descrever o layout desktop, não
  implemente só essa versão e "lembre depois" do mobile — construa a
  base mobile primeiro e trate o desktop como o ajuste sobre ela; se
  faltar informação sobre o comportamento em tela pequena, pergunte
  antes de assumir.
