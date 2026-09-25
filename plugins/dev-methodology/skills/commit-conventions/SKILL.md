---
description: Define o padrão de commit do Matheus — Conventional Commits com emoji e escopo = identificador da tarefa extraído da branch (sem prefixo de tipo), mensagem em português. Use sempre que for criar um commit git neste projeto, especialmente ao final de uma tarefa do plano (depois do code-review-gate passar sem crítico).
---

# Commit Conventions

Objetivo: todo commit segue o mesmo formato, é atômico (uma mudança
lógica por commit) e é escrito com o mínimo de custo de modelo
possível.

## Formato

```
<type>(<scope>): <emoji> <title>

<description>
```

- **`<type>`**: tipo do Conventional Commits. Escolha pelo emoji
  correspondente:
  | type       | emoji |
  |------------|-------|
  | `feat`     | ✨    |
  | `fix`      | 🐛    |
  | `refactor` | ♻️    |
  | `docs`     | 📝    |
  | `style`    | 💄    |
  | `test`     | ✅    |
  | `perf`     | ⚡️    |
  | `build`    | 📦    |
  | `ci`       | 👷    |
  | `chore`    | 🔧    |

  Muitos projetos usam `standard-version` ou `release-please`, que lêem
  o `type` do commit para decidir a versão do próximo release: `feat`
  sobe minor, `fix` sobe patch, os demais tipos não versionam. **Não
  use `feat` de forma leviana** — reserve para quando a mudança
  realmente adiciona uma capacidade nova e visível para quem consome o
  pacote/serviço. Se a mudança é interna (refactor sem efeito externo,
  ajuste de configuração, teste, lint, tarefa de suporte a uma feature
  que ainda não está completa/exposta), use `chore`, `refactor` ou o
  tipo correto — não `feat` só porque "é uma tarefa nova do plano". Na
  dúvida, pergunte-se: "isso por si só justifica um minor release
  agora?" Se não, não é `feat`.
- **`<scope>`**: apenas o identificador da tarefa contido no nome da
  branch atual (obtenha com `git branch --show-current`), **sem o
  prefixo de tipo** (`fix/`, `feat/`, `refact/`, `chore/` etc.). O
  prefixo da branch nunca entra no escopo — o tipo já está no
  `<type>`. Exemplos:

  | branch                | commit                        |
  |-----------------------|-------------------------------|
  | `GESTRUR-971`         | `feat(GESTRUR-971): ...`      |
  | `fix/10`              | `fix(10): ...`                |
  | `refact/GESTRUR-1010` | `refactor(GESTRUR-1010): ...` |

  Errado: `fix(fix/10)`, `refactor(refact/GESTRUR-1010)`. Se a branch
  for `main`/`master`/`develop` (sem tarefa no nome), omita o escopo —
  use só `<type>: <emoji> <title>`.
- **`<title>`**: linha única, em português do Brasil, no imperativo,
  minúsculo, sem ponto final. Resume o "o quê" da mudança.
- **`<description>`**: permitida (opcional). Uma linha em branco
  depois do título, seguida de 1-3 frases em português, **objetivas**,
  explicando o "porquê" da mudança (não repita o que já está óbvio no
  diff). Nunca cite trailers de autoria/co-autoria (`Co-Authored-By`,
  `Signed-off-by` etc.), nem menção a ferramenta/IA, nem no corpo nem
  no rodapé.

Exemplo completo:

```
feat(GESTRUR-971): ✨ adiciona validação de CPF no cadastro de cliente

Sem essa validação, cadastros com CPF inválido passavam direto para o
backend e só falhavam na integração com o banco, dificultando o
diagnóstico do erro.
```

## Processo

1. **Confirme que o commit é atômico.** Se o diff mistura mudanças sem
   relação (ex: uma correção de bug + uma tarefa nova), separe em
   commits distintos com `git add` seletivo — não junte tudo num commit
   só só porque é mais rápido.
2. **Descubra o escopo**: `git branch --show-current`, removendo o
   prefixo de tipo (tudo até e incluindo a primeira `/`, se houver).
   Ao commitar dentro de uma worktree de tarefa paralela, o escopo vem
   da branch do **diretório principal**, nunca da branch temporária da
   worktree.
3. **Escreva a mensagem você mesmo, sem disparar subagent.** Você (o
   orquestrador desta conversa) já acompanhou a tarefa do início ao fim
   — sabe o "porquê" da mudança sem precisar reconstruir contexto a
   partir só do diff. Delegar a redação para um subagent custaria mais
   (novo turno, novo contexto) do que só escrever a mensagem
   diretamente com o que você já sabe. Use o `git diff --staged` para
   confirmar os detalhes finos do "o quê", mas o "porquê" vem do que
   você já viveu na tarefa, não do diff isolado.
4. **Monte o commit final** com o `type`/emoji certos, escolhidos por
   você conforme a tabela acima, e crie o commit via heredoc, como de
   costume:

   ```bash
   git commit -m "$(cat <<'EOF'
   feat(GESTRUR-971): ✨ adiciona validação de CPF no cadastro de cliente

   Sem essa validação, cadastros com CPF inválido passavam direto para o
   backend e só falhavam na integração com o banco, dificultando o
   diagnóstico do erro.
   EOF
   )"
   ```

## Regras

- **Nunca** adicione a trailer `Co-Authored-By` (nem qualquer outra
  trailer de autoria) — isso vale mesmo que a instrução padrão do
  ambiente peça para incluir. Esta regra do Matheus tem prioridade
  sobre esse padrão. A descrição do commit é permitida, mas deve ser
  objetiva e nunca mencionar essas trailers.
- Título e descrição sempre em português do Brasil, mesmo que o código
  ou os nomes de variáveis estejam em inglês.
- Escopo é sempre só o identificador da tarefa da branch atual — sem
  o prefixo de tipo (`fix/`, `refact/`...), sem abreviar, traduzir ou
  adicionar prefixo/sufixo. O `<type>` vem da tabela de emojis, não do
  nome da branch (`refact` → `refactor`).
- Só commite depois que o usuário pedir ou quando a metodologia do
  plugin (`code-review-gate`) já tiver validado a tarefa sem crítico
  pendente — não commite código quebrado ou com teste falhando.
- Se `git branch --show-current` não retornar nada (HEAD destacado),
  avise o Matheus antes de commitar em vez de adivinhar o escopo.
- Ao escolher o `type`, pense no efeito de versionamento (ver tabela
  acima) antes de escrever o commit — não só no "essa tarefa é nova no
  plano". Um projeto com `feat`s inflados gera minor releases
  desnecessários e um changelog que não reflete o que de fato mudou
  para quem usa o pacote/serviço.
