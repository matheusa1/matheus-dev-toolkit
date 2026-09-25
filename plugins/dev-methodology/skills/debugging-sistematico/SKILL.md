---
description: Investiga um bug ou comportamento inesperado relatado pelo usuário de forma sistemática — reproduzir, coletar evidência, formular e testar hipóteses, isolar a causa raiz — antes de qualquer correção. Use sempre que o Matheus relatar "isso não está funcionando", um erro, um comportamento inesperado, ou pedir para investigar/corrigir um bug, em vez de já sair editando código.
---

# Debugging Sistemático

Objetivo: encontrar a causa raiz real de um problema relatado, com
evidência que a confirme, antes de tocar em qualquer correção. Chutar
uma correção sem confirmar a causa é o erro mais caro em debugging —
essa skill existe para evitar isso.

## Quando usar

- Sempre que o Matheus relatar um bug, erro, exceção, ou comportamento
  diferente do esperado — antes de editar qualquer código.
- Não é para desenvolvimento de feature nova (aí segue o fluxo normal:
  `brainstorming` → `writing-plans`).
- Se o problema já veio com causa raiz clara e confirmada (ex: o
  próprio Matheus já identificou a linha exata e por quê), pode pular
  direto para a correção via `test-driven-development` — não force o
  processo completo quando não há nada a investigar.

## Antes de começar: inline ou subagent?

Inline ou agent `dev-methodology:investigador-bugs`. Recomende o agent
quando a investigação exigir muitos comandos, logs extensos ou várias
hipóteses; inline para bug simples e localizado. Pergunte na primeira vez e
reaproveite a resposta na conversa — regras em `dev-methodology:using-dev-methodology`.

## Processo

1. **Reproduzir.** Colete passos exatos, entrada usada, ambiente,
   mensagem de erro completa (não resumida) e comportamento esperado
   vs. observado. Tente reproduzir localmente (rodando a aplicação,
   um teste, ou um script mínimo). Se não conseguir reproduzir com o
   que foi dado, **pare e peça mais informação** ao Matheus em vez de
   adivinhar a partir de uma descrição incompleta.
2. **Coletar evidência.** Stack trace completo, logs relevantes,
   `git log`/`git blame` do trecho suspeito se for uma regressão,
   resultado de rodar a suíte de testes relacionada. Evidência crua,
   não interpretação ainda.
3. **Formular hipóteses.** Liste as causas plausíveis, ordenadas por
   probabilidade dado a evidência coletada — não pela primeira ideia
   que veio à cabeça. Cada hipótese deve ser testável (dá para
   confirmar ou descartar com uma ação concreta).
4. **Isolar.** Reduza o escopo até a hipótese mais provável:
   - `git bisect` quando for uma regressão e o commit que introduziu
     não é óbvio.
   - Reduza o caso até o menor exemplo que ainda reproduz o problema.
   - Instrumentação temporária (logs/prints, breakpoint) no trecho
     suspeito — não mude comportamento, só observe.
   - Teste uma hipótese de cada vez. Não altere várias coisas ao
     mesmo tempo "para ver se resolve" — isso mascara qual mudança
     resolveu o quê.
5. **Confirmar a causa raiz.** Antes de escrever qualquer correção,
   tenha uma evidência concreta de que a causa identificada é
   realmente a causa — idealmente um teste que falha exatamente pelo
   motivo suspeitado. Remova qualquer instrumentação temporária
   depois de confirmar.
6. **Corrigir.** Siga a skill `dev-methodology:test-driven-development`:
   escreva um teste que reproduz o bug (RED), confirme que falha pelo
   motivo certo, então corrija (GREEN). Isso garante uma correção que
   ataca a causa, não o sintoma, e deixa uma regressão coberta.
7. **Verificar regressão.** Rode a suíte de testes relacionada (não só
   o teste novo) para confirmar que a correção não quebrou nada.
8. **Documentar o achado.** Resuma: causa raiz, por que acontecia,
   correção aplicada, teste de regressão adicionado. Isso vira a base
   da mensagem de commit (`commit-conventions`).

## Regras

- Nunca aplique uma correção sem antes reproduzir e confirmar a causa
  raiz com evidência concreta — "acho que é isso" não é confirmação.
- Não mude múltiplas coisas de uma vez tentando ver se o problema
  some. Isole uma variável por vez.
- Se, depois de esgotar as hipóteses plausíveis, a causa ainda não
  ficou clara, pare: reporte o que já foi descartado e por quê, e
  peça mais contexto ao Matheus em vez de continuar tentando às
  cegas.
- Prefira instrumentação temporária (logs, prints, breakpoints) a
  mudanças permanentes no código até a causa estar confirmada. Reverta
  a instrumentação antes de considerar a investigação concluída.
- A correção em si segue `test-driven-development` — esta skill cobre
  a investigação até a causa raiz confirmada, não substitui o ciclo
  RED-GREEN-REFACTOR na hora de corrigir.
