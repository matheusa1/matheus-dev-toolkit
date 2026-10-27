---
name: brainstorming
description: Refina um pedido de feature vago ou high-level em uma especificação clara antes de qualquer código ser escrito. Use no início de qualquer tarefa de desenvolvimento nova, quando o pedido for ambíguo, quando faltarem critérios de aceite, ou quando o Matheus disser algo como "quero implementar X" sem detalhar como.
---

# Brainstorming → Spec

Objetivo: transformar uma ideia em uma especificação curta e concreta
ANTES de escrever qualquer código. Não pule direto para a implementação.

## Processo

1. **Entenda o pedido tal como foi feito.** Não assuma detalhes que não
   foram ditos. Se o pedido já tem constraints claras, não pergunte de
   novo — apenas confirme seu entendimento.
2. **Faça perguntas objetivas, uma de cada vez (ou em lote curto)**,
   focadas no que muda a decisão de design:
   - Quem usa e para quê (a história de usuário)?
   - Qual é o objetivo real (o problema que isso resolve)?
   - Quais comportamentos e casos de borda precisam acontecer
     (viram os critérios de aceitação)?
   - Que regras de negócio valem (status, permissão, cálculo)?
   - O que está fora do escopo?
3. **Escreva a spec sempre no formato abaixo.** Ele existe para que os
   casos de teste possam ser derivados depois direto dos critérios de
   aceitação, um ou mais por `CAxx`. Modelo completo, com domínio
   fictício, em [`exemplo.md`](exemplo.md) — use a estrutura, não o
   domínio.

   ```markdown
   # <Título da funcionalidade>

   Como <papel do usuário>,
   quero <ação ou capacidade>,
   para <benefício ou motivo>.

   ## Objetivo
   <1 parágrafo: o que será disponibilizado e o problema que resolve>

   ## Critérios de aceitação

   ### CA01 — <Título curto do comportamento>
   Dado que <contexto/estado inicial>,
   quando <ação ou evento>,
   então o sistema deve <resultado observável>.

   ## Regras de negócio
   - <regra que vale em toda a funcionalidade>

   ## Fora do escopo
   - <o que não será feito nesta entrega>

   ## Resultado esperado
   Ao final, o usuário deverá conseguir <estado final verificável>.
   ```

   Regras do formato:
   - Seções sempre nessa ordem e com esses nomes. Sem item para uma
     seção, escreva "Nenhuma." em vez de omiti-la.
   - Cada CA descreve **um** comportamento observável, em
     Dado/quando/então, sem detalhe de implementação (nada de nome de
     classe, tabela ou endpoint). Vários resultados no mesmo `então`
     viram lista; desdobramentos (confirmar/cancelar) viram pares
     `Quando…/então…` extras dentro do mesmo CA.
   - Casos de borda, validações e tratamento de erro são CAs próprios,
     não uma seção à parte.
   - Na primeira versão, numeração `CA01`, `CA02`… sequencial, sem
     buracos. Depois da spec aprovada, os números não mudam (testes e
     casos de teste referenciam): CA novo pega o próximo número livre;
     CA removido sai sem renumerar os demais, e o buraco fica.
   - Regras de negócio são invariantes que valem para vários CAs
     (status, permissão, cálculo); comportamento de um fluxo só vai no
     CA dele.
   - Restrições técnicas (stack, performance, compatibilidade) não
     entram na spec: registre-as no plano (`writing-plans`).

4. **Salve a spec em arquivo**, não só na conversa:
   `docs/especificacao/AAAA-MM-DD-nome-tarefa.md`, usando a data atual
   e um nome curto em kebab-case para a tarefa (ex:
   `docs/especificacao/2026-07-27-login-social.md`).
   - Se `docs/especificacao/` ainda não existe no projeto, crie-a e
     adicione um `docs/especificacao/.gitignore` com este conteúdo,
     para as specs ficarem no disco mas fora do versionamento:

     ```gitignore
     *
     ```

     O conteúdo é exatamente essa única linha `*` — **não** adicione
     `!.gitignore` nem qualquer outra exceção: o próprio `.gitignore`
     também deve ficar fora do versionamento, junto com as specs.
   - Este arquivo é a referência que o `revisor-conformidade` vai
     usar no fim da implementação para conferir se o que foi
     construído bate com o que foi especificado — por isso ele precisa
     existir em disco, não só ter sido dito na conversa.

5. **Pare e peça confirmação** da spec. Não implemente nada nesta
   etapa.
6. **Gere os casos de teste** com a skill `casos-de-teste` logo depois
   da confirmação, antes do plano, e então siga para `writing-plans`.

## Tarefa pequena: spec dentro do plano

Se a tarefa foi classificada como **pequena** (ver "Tamanho da
tarefa" em `using-dev-methodology`), não crie arquivo em
`docs/especificacao/` nem peça confirmação separada:

- Faça só as perguntas indispensáveis (muitas vezes nenhuma).
- Escreva a spec como seção `## Spec` no topo do arquivo de plano em
  `docs/planos/AAAA-MM-DD-nome-tarefa.md`, no mesmo formato (história,
  Objetivo, CAs, Regras de negócio, Fora do escopo, Resultado
  esperado) um nível de título abaixo (`###` para as seções, `####`
  para cada CA). Pode ser enxuta, mas os CAs continuam em
  Dado/quando/então.
- Gere os casos de teste (`casos-de-teste`, arquivo próprio em
  `docs/casos-teste/`) e siga direto para `writing-plans`, que
  acrescenta o checklist no mesmo arquivo e faz **uma** confirmação
  para spec + casos de teste + plano.

## Regras

- Não infira requisitos não-ditos e apresente como se fossem certos —
  marque como suposição e confirme.
- Prefira poucas perguntas de alto impacto a um questionário longo.
- Se o pedido já é uma spec completa (o Matheus já detalhou tudo),
  resuma de volta em 3-4 linhas para confirmar entendimento, salve o
  arquivo da mesma forma (convertido para o formato acima, se ele veio
  em outro), gere os casos de teste (`casos-de-teste`) e só então siga
  para o plano, sem reabrir perguntas já respondidas.
- Se a spec mudar depois de confirmada (novo requisito descoberto
  durante o plano ou a implementação), atualize o mesmo arquivo em vez
  de criar um segundo — a spec em disco deve refletir a versão vigente.
