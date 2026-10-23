---
description: Regras de código que valem para todo desenvolvimento do Matheus (idioma, SOLID, vizinho legado, limite de 150 linhas por arquivo e 20 por função) com a severidade de cada uma no review, e os comandos para obter o diff de uma tarefa ou da branch. Use antes de escrever, refatorar ou revisar qualquer código, inline ou em subagent.
---

# Regras de código

Fonte única destas regras: skills e agents apontam para cá em vez de
repeti-las. Os agents de implementação e review já carregam esta skill.

## Regras

- **Código em inglês**: identificadores, arquivos, comentários,
  mensagens de erro e nomes de teste. Specs, planos, conversa e
  commits em português. Termos de domínio sem tradução natural podem
  ficar no original, sem misturar idiomas no mesmo nome. Em código
  existente em português, siga a convenção local e sinalize — não
  renomeie fora do escopo.
- **SOLID sempre**: uma responsabilidade por classe/módulo (S);
  estender por abstração em vez de editar (O); implementações
  substituíveis pelo contrato (L); interfaces pequenas (I); depender de
  abstrações `I*`/ports, nunca de concretas (D). Se a tarefa parecer
  exigir violar algum, pare e pergunte.
- **Vizinho legado não é convenção.** Se o repo tem dois padrões para
  a mesma coisa (ex: logger instanciado vs. telemetria injetada; import
  relativo vs. path alias), siga o que está documentado no `CLAUDE.md`
  do projeto ou, sem documentação, o que respeita as camadas/SOLID —
  não o arquivo vizinho só por estar ao lado. Sinalize a divergência
  no relatório em vez de escolher em silêncio.
- **Arquivo com no máximo 150 linhas, função com no máximo 20.** Conta
  a função inteira, da assinatura ao fechamento, inclusive método e
  componente React. Passou do limite: extraia função, componente ou
  arquivo com uma responsabilidade (anda junto com o S do SOLID).
  Ficam de fora arquivos de teste, gerados, migrations, config e
  documentação (`.md`); num `describe`/`it` longo, prefira helper ou
  fixture. Arquivo legado já acima do limite: não refatore fora do
  escopo, mas não o faça crescer — o que você adicionar vai para um
  arquivo novo — e sinalize.

## Severidade no review

| Regra | Severidade |
|---|---|
| Nome em português fora do padrão local | 🟡 aviso |
| Violação clara de SOLID que compromete a arquitetura | 🔴 crítico; demais casos 🟡 |
| Vizinho legado seguido contra o documentado, sem sinalizar | 🟡 aviso |
| Arquivo ou função **criado** pelo diff acima do limite | 🔴 crítico |
| Legado que o diff fez crescer além do limite | 🟡 aviso, com a extração sugerida |

Meça o tamanho com `wc -l` nos arquivos do diff e olhando as funções
que o diff cria ou altera.

## Diff da tarefa

O review de uma tarefa olha **só** o que ela mudou — nunca `git diff`
puro, que mistura mudanças de outras tarefas ainda não commitadas:

- **Tarefa em worktree** (grupo paralelo): tudo na worktree é da
  tarefa — `git -C <worktree> add -A ':(exclude,glob)**/node_modules'`
  e depois `git -C <worktree> diff --staged`.
- **Tarefa no diretório principal**: `git diff HEAD -- <arquivos da
  tarefa>` (lista vinda do plano/resumo do agent), mais
  `git status --short -- <arquivos>` para ver arquivos novos.

Quem dispara um revisor passa no prompt o comando exato de diff (ou a
worktree + lista de arquivos). Revisor sem escopo no prompt para e
pede, em vez de revisar o diff inteiro.

## Diff da branch

Conformidade e documentação final olham a entrega inteira, não só o
último commit:

- Base: `git merge-base HEAD origin/<branch-base>`; branch-base é a de
  onde a branch saiu (`develop`, `main`...). Se não for óbvio,
  pergunte.
- `git diff <base>...HEAD` + `git diff HEAD` (não commitado) +
  `git status --short` (arquivos novos); commits em
  `git log --oneline <base>..HEAD`.
