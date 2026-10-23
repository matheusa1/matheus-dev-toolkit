# Diff de UI: revisores de acessibilidade e responsividade

Referência de `using-dev-methodology`, lida só quando a tarefa toca
arquivo de frontend.

Uma tarefa **altera interface de frontend** quando o diff dela cria ou
muda pelo menos um destes arquivos:

- componente/tela: `.tsx`, `.jsx`, `.vue`, `.svelte`, `.html`;
- estilo: `.css`, `.scss`, `.sass`, `.less`, CSS Modules,
  `*.styles.ts`/`*.styled.ts` (styled-components/emotion), `StyleSheet`
  do React Native;
- tema/layout global: `tailwind.config.*`, `globals.css`, tokens de
  tema do design system.

Não conta: teste (`*.test.tsx`, `*.spec.tsx`), story
(`*.stories.tsx`), arquivo de `core` sem JSX, ou `.tsx` cuja mudança é
só em lógica/tipos sem tocar no JSX nem em estilo.

Com diff de UI e execução por **subagents**, dispare no **mesmo turno**
do `revisor-arquiteto`, cada um com o mesmo escopo de diff:

- `revisor-acessibilidade` — semântica, teclado, leitor de tela,
  contraste.
- `revisor-responsividade` — mobile first, overflow, toque, telas
  estreitas e largas.

Regras:
- **Sem diff de UI, não dispare** nenhum dos dois — nem "por garantia".
- Tarefa **trivial** não dispara revisor (a autorrevisão do diff cobre).
- Execução **inline**: o `code-review-gate` inline já cobre as regras
  7 e 10 de `convencoes-frontend`; não dispare os agents.
- Com eles no ar, o `revisor-arquiteto` deixa as regras 7 e 10 para os
  especialistas, sem achado duplicado.
- Crítico de qualquer um dos três bloqueia a próxima tarefa, como no
  `code-review-gate`. Junte os achados dos três numa lista só antes de
  corrigir.
- Os revisores não contam no limite de 4 agents simultâneos de
  `execucao-paralela.md` — o limite é para implementação.
- Se a tarefa reduziu acessibilidade por decisão confirmada pelo
  Matheus, diga isso no prompt do `revisor-acessibilidade`.

**Validação além do código** (fim de tarefa com diff de UI, inline ou
subagent): revisor lê código, não ouve a tela. Antes de reportar:

- No navegador, confira a ordem de Tab (o que recebe foco e em que
  ordem) e o nome dos elementos novos na árvore de acessibilidade.
- Entregue ao Matheus um roteiro curto de teste com leitor de tela
  (VoiceOver/NVDA): onde focar, que tecla apertar e a frase esperada.
