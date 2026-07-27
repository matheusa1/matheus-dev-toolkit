# matheus-toolkit

Marketplace pessoal de plugins para o Claude Code.

## Plugins

- **dev-methodology** — metodologia de desenvolvimento agnóstica de
  projeto (brainstorm→spec, TDD, code review com gate, scaffolding de
  Clean Architecture/DDD). Ver `plugins/dev-methodology/README.md`.

## Como usar

### 1. Testar localmente, sem subir pro GitHub ainda

Dentro de qualquer projeto:

```bash
claude --plugin-dir /caminho/para/matheus-dev-toolkit/plugins/dev-methodology
```

Isso carrega o plugin só para essa sessão, sem precisar de marketplace.

### 2. Publicar como marketplace pessoal (recomendado)

1. Crie um repositório no GitHub (público ou privado) e suba esta
   pasta inteira (`matheus-dev-toolkit/`) como o conteúdo do repo.

   ```bash
   cd matheus-dev-toolkit
   git init
   git add .
   git commit -m "dev-methodology plugin v0.1.0"
   git branch -M main
   git remote add origin git@github.com:<seu-usuario>/<repo>.git
   git push -u origin main
   ```

2. Em qualquer máquina/projeto, registre o marketplace:

   ```bash
   /plugin marketplace add <seu-usuario>/<repo>
   ```

3. Instale o plugin:

   ```bash
   /plugin install dev-methodology@matheus-toolkit
   /reload-plugins
   ```

4. Para usar em todo projeto por padrão sem reinstalar toda vez, você
   pode declarar no `.claude/settings.json` de cada projeto (ou no seu
   `~/.claude/settings.json` para todos os projetos):

   ```json
   {
     "extraKnownMarketplaces": {
       "matheus-toolkit": {
         "source": { "source": "github", "repo": "<seu-usuario>/<repo>" }
       }
     },
     "enabledPlugins": {
       "dev-methodology@matheus-toolkit": true
     }
   }
   ```

### Atualizar depois de mudar algo

```bash
git add . && git commit -m "ajuste na skill X" && git push
/plugin marketplace update matheus-toolkit
/reload-plugins
```

Como o `plugin.json` não fixa uma `version`, cada commit novo já conta
como uma versão nova — não precisa bumpar nada manualmente.

## Validar antes de subir

```bash
claude plugin validate .
```
