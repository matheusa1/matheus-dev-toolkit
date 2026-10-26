# Changelog

Versões do plugin `dev-methodology` (semver). A versão vale para as
duas manifests (`.claude-plugin/plugin.json` e
`.codex-plugin/plugin.json`), que sobem sempre juntas. Atualize este
arquivo no mesmo commit que muda a versão.

## 0.22.0 — 2026-10-26

- Título e descrição do MR/PR gerados a partir da documentação final
  (`documentacao-implementacao`), sem "Generated with Claude Code",
  link de sessão, `Co-Authored-By` nem outra atribuição.

## 0.21.0 — 2026-10-25

- Documentação final (`documentacao-implementacao`) obrigatória no fim
  de toda tarefa pequena, grande e bug, sem oferta nem pergunta; a
  trivial só gera sob pedido. Sai da rodada única de perguntas.
- Eval de bug confere que a correção termina com a documentação final.

## 0.20.0 — 2026-10-22

- Spec sempre no formato história de usuário (Como/quero/para),
  Objetivo, critérios de aceitação `CAxx` em Dado/quando/então, Regras
  de negócio, Fora do escopo e Resultado esperado.
- Skill `casos-de-teste`: gera os CTs (formato Xray manual) a partir da
  spec, sem viés de implementação, com CTs de endpoint quando há API.
- Agent `executor-casos-teste`: executa os CTs no fim e marca as
  divergências.
- Plano, TDD e conformidade rastreiam `CAxx`; testes e2e derivados dos
  CTs de endpoint, com o `CTxx` no nome.
- Skill `regras-de-codigo`: fonte única de idioma, SOLID, vizinho
  legado, limites de tamanho e comandos de diff, pré-carregada nos
  agents.
- `using-dev-methodology` enxuta: diff de UI e execução paralela em
  arquivos de referência lidos só quando necessários.
- Hook `SessionStart` também roda depois de compactar o contexto.
- CI valida o plugin, os JSON e a igualdade das versões; cenários de
  `claude plugin eval` em `evals/`.

## 0.19.0 — 2026-10-20

- Arquivo com no máximo 150 linhas e função com no máximo 20.

## 0.18.2 — 2026-10-13

- Acessibilidade cobre gráficos, leitura por leitor de tela e
  contraste por estado.

## 0.18.1 — 2026-10-13

- Review barra framework em `application`, import relativo entre
  módulos e vizinho legado como convenção.

## 0.18.0 — 2026-10-13

- Skill `documentacao-implementacao` (documentação final da entrega).

## 0.17.0 — 2026-10-05

- Agents `revisor-acessibilidade` e `revisor-responsividade`.

## 0.16.1 — 2026-09-30

- `.gitignore` de specs e planos contém só `*`.

## 0.16.0 — 2026-09-25

- Fluxo por tamanho de tarefa, rodada única de perguntas e worktrees
  paralelas.

## 0.15.0 — 2026-09-25

- Regras de inglês e SOLID; escopo dos commits corrigido.

## 0.14.0 — 2026-09-23

- Orquestrador redige o commit; paralelismo limitado a 4 tarefas.

## 0.13.0 — 2026-08-06 e anteriores

- 0.11.0: agent `implementador-frontend`, sem TDD.
- 0.10.0: `convencoes-frontend` agnóstica de design system.
- 0.9.0: skill `debugging-sistematico` e agent `investigador-bugs`.
- 0.7.0: planos salvos em arquivo.
- 0.3.1: execução paralela, `commit-conventions` e uso padrão.
- 0.1.0: versão inicial.
