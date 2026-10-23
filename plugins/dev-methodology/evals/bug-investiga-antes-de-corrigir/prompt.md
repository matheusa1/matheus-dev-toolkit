---
max_turns: 25
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Primeiro crie `src/total.ts` com:

```ts
export function total(prices: number[]): number {
  let sum = 0;
  for (let i = 1; i < prices.length; i++) sum += prices[i];
  return sum;
}
```

Depois disso: o total do carrinho está vindo menor do que deveria.
Pode resolver?
