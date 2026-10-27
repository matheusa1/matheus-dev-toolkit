# matheus-toolkit

Marketplace pessoal de plugins para o Claude Code e para o Codex CLI.

## Plugins

- **dev-methodology** — metodologia de desenvolvimento agnóstica de
  projeto: brainstorm→spec, casos de teste derivados da spec e
  executados no fim, TDD forçado, code review com gate de
  severidade (+ revisores de acessibilidade e responsividade em diff de
  UI), debugging sistemático, execução paralela em worktrees, commits
  em Conventional Commits, scaffolding de Clean Architecture/DDD e
  documentação final da implementação. Ver
  `plugins/dev-methodology/README.md`.

## Instalar (Claude Code)

O marketplace já está publicado em
[`matheusa1/matheus-dev-toolkit`](https://github.com/matheusa1/matheus-dev-toolkit)
(branch `main`).

1. Registre o marketplace (uma vez por máquina):

   ```bash
   /plugin marketplace add matheusa1/matheus-dev-toolkit
   ```

2. Instale o plugin:

   ```bash
   /plugin install dev-methodology@matheus-toolkit
   /reload-plugins
   ```

3. Para deixar ativo em todo projeto sem instalar de novo, declare no
   `~/.claude/settings.json` (todos os projetos) ou no
   `.claude/settings.json` de um projeto:

   ```json
   {
     "extraKnownMarketplaces": {
       "matheus-toolkit": {
         "source": { "source": "github", "repo": "matheusa1/matheus-dev-toolkit" }
       }
     },
     "enabledPlugins": {
       "dev-methodology@matheus-toolkit": true
     }
   }
   ```

## Desenvolver o plugin

### Testar uma mudança local antes de publicar

Dentro de qualquer projeto, aponte para o clone deste repo:

```bash
claude --plugin-dir /caminho/para/matheus-dev-toolkit/plugins/dev-methodology
```

Isso carrega a versão local só nessa sessão, sem passar pelo
marketplace.

### Versionar

O `plugin.json` fixa uma `version` (semver), e o Claude Code usa esse
campo para saber se há atualização: **mudança sem subir a versão não
chega a quem já tem o plugin instalado.** A cada mudança:

- Suba a versão em `plugins/dev-methodology/.claude-plugin/plugin.json`
  **e** em `plugins/dev-methodology/.codex-plugin/plugin.json` (as duas
  sempre iguais): patch para ajuste/correção de regra, minor para
  skill/agent/etapa nova.
- Registre a mudança em `plugins/dev-methodology/CHANGELOG.md`, no
  README do plugin (quando muda o que ele faz) e no corpo do commit,
  citando a versão nova.

### Validar antes de subir

```bash
claude plugin validate .
```

O CI (`.github/workflows/validate.yml`) roda isso em todo pull
request, junto com a checagem dos JSON, das versões Claude Code ×
Codex iguais, da entrada no CHANGELOG e das skills pré-carregadas pelos
agents. Mudou uma regra do fluxo? Rode também as evals do plugin (ver
"Evals" no README do plugin).

### Publicar uma mudança

Mudanças entram na `main` por pull request. Depois do merge, em cada
máquina:

```bash
/plugin marketplace update matheus-toolkit
/reload-plugins
```

## Codex CLI

Este repo também expõe um marketplace pro [Codex CLI](https://developers.openai.com/codex)
(`.agents/plugins/marketplace.json` na raiz + `.codex-plugin/plugin.json`
dentro de cada plugin, ex. `plugins/dev-methodology/.codex-plugin/plugin.json`).

### Instalar

```bash
codex plugin marketplace add matheusa1/matheus-dev-toolkit
codex plugin add dev-methodology@matheus-toolkit
```

### Testar uma mudança local

```bash
codex plugin marketplace add /caminho/para/matheus-dev-toolkit
codex plugin add dev-methodology@matheus-toolkit
```

### Atualizar depois do merge

```bash
codex plugin add dev-methodology@matheus-toolkit
```

### Compatibilidade e limitações

As skills são compartilhadas. No Claude Code, o plugin carrega os agents
nomeados e seu hook de sessão. No Codex, os roteiros em `agents/*.md` são
consultados pelas skills e podem ser repassados a subagentes disponíveis e
autorizados, ou executados inline. A disponibilidade de ferramentas e de
modelos depende do ambiente.

O Codex desktop suporta o hook de sessão de plugins locais após revisão e
confiança explícita na definição do hook. A disponibilidade em outras
superfícies pode variar; sem o hook, invoque `using-dev-methodology`
explicitamente no início da tarefa. Inicie uma nova conversa após instalar.

O caminho de `source.path` do marketplace é relativo à raiz do repositório.
Depois de alterar o plugin, atualize a instalação e reinicie o aplicativo
para carregar a cópia atualizada.
