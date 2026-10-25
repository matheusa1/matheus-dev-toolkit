---
description: Gera a documentação final de uma implementação concluída — um arquivo markdown no formato padrão do Matheus (ticket, detalhes do back e do web, contratos, rotas, impacto), escrito a partir do diff real da branch. Etapa obrigatória no fim de toda implementação do fluxo de `using-dev-methodology` (tarefa pequena, grande ou bug), depois da conformidade e dos casos de teste executados. Use também quando o Matheus pedir "documentação final", "documenta a implementação" ou "gera a doc do que foi feito".
---

# Documentação da implementação

Objetivo: um documento para quem **revisa, testa ou mantém** a entrega
saber o que mudou — contratos, rotas, comportamento de tela e impacto.
Não é relato do processo: não cite spec, plano, TDD, agents, reviews
nem a conversa.

O formato de referência está em [`exemplo.md`](exemplo.md) (domínio
fictício). Leia antes de escrever o primeiro documento da conversa.

## Quando gerar

- **Pedido explícito**, em qualquer momento → gere.
- **Dentro do fluxo** → sempre, como última etapa, sem perguntar,
  conforme "Documentação final" em `using-dev-methodology` (tarefa
  trivial só sob pedido). Só pule com pedido explícito para não gerar.
- Implementação ainda com crítico aberto no review ou na conformidade
  → avise e gere só depois de resolvido (ou se ele insistir, marcando
  o que está pendente).

## Fontes

A ordem é de confiança. Quando duas fontes divergem, vale a de cima.

1. **Código**: o diff completo da entrega, não só o último commit,
   com os comandos de "Diff da branch" em `regras-de-codigo`.
   - Leia os arquivos alterados quando o diff sozinho não mostra o
     contrato inteiro (tipo, DTO, validação, mensagens de erro).
2. **Commits**: `git log --oneline <base>..HEAD`.
3. **Spec e plano** (`docs/especificacao/`, `docs/planos/`), se
   existirem: só para o contexto — título, problema, porquê. Se o
   plano diz uma coisa e o código faz outra, o documento segue o
   código; avise o Matheus da divergência no chat, não no documento.
4. **Conversa**: causa raiz confirmada (`debugging-sistematico`) e
   decisões combinadas.

**Nunca invente.** Rota, método, campo, tipo, status HTTP, mensagem de
erro e texto de tela são copiados do código. O que não dá para
confirmar vira `> ⚠️ **A confirmar:** <o quê>` no ponto exato e entra
na lista de pendências da resposta.

## Ticket e título

- Ticket: identificador da branch, com a mesma regra de escopo de
  `commit-conventions` (sem o prefixo `fix/`, `feat/`...). Branch sem
  ticket → use um nome curto da entrega.
- Título: `<TICKET> – <descrição>`. A descrição vem do título do
  ticket na spec/conversa; se não houver, descreva o problema
  resolvido (não a solução) em uma frase.
- Link do Jira: reaproveite a URL base de documentos anteriores em
  `docs/implementacao/` ou do `CLAUDE.md`. Não achou → pergunte uma
  vez; sem resposta, omita a linha.

## Onde salvar

`docs/implementacao/AAAA-MM-DD-<ticket-ou-nome>.md`, data de hoje.

- Se a pasta não existe, crie com um `docs/implementacao/.gitignore`
  contendo **exatamente** uma linha `*` — sem `!.gitignore` nem outra
  exceção (mesma regra de `docs/especificacao/` em `brainstorming`).
- Mesmo arquivo já existe (documento regerado) → sobrescreva.

## Estrutura

Seções sem conteúdo **somem** (tarefa só de front não tem "Back"; sem
rota nova não há "Rotas novas"). A ordem é fixa:

```markdown
# <TICKET> – <descrição>

Jira: <url>

## Detalhes da implementação

<1-2 frases do que a entrega faz, só se ajudar a ler o resto>

### Back

#### Retorno de `<rota>`          ← contrato de resposta alterado
#### Rotas novas                    ← uma subseção ##### por rota
#### Mudança de comportamento em rota existente
#### <outros>                       ← migração, job, evento, config

### Web

#### Correção (origem do bug)       ← só em bug: antes x agora
#### <ação/tela nova>               ← uma subseção por fluxo de tela
#### Camada `@core`                 ← tabela Módulo | Item | Responsabilidade
#### Outros ajustes

## Impacto

| Área | Impacto |
|---|---|
```

Projeto que não é back + web (ex: mobile, lib, só back): troque os
blocos `### Back`/`### Web` pelas partes reais da entrega, mantendo o
resto.

## Como escrever cada parte

**Contrato alterado** (retorno, DTO, tipo público):
- Bloco `typescript` só com os tipos novos ou alterados, um
  comentário curto por campo novo; o que não mudou vira
  `...camposAtuais`.
- Em lista: campos novos, campos que passaram a vir sempre, opções
  removidas.

**Rota nova**, nesta ordem:
1. `MÉTODO /caminho/completo` em código, numa linha própria.
2. Fluxo numerado do que a rota faz (busca, validação, transação,
   o que acontece em falha). Rota trivial → uma frase basta.
3. **Parâmetros**: o que é cada parâmetro de path (principalmente
   quando um id pode ser confundido com outro), body com o nome do
   tipo e exemplo `json` com `<uuid>`/valores fictícios, e tabela
   `Campo | Obrigatório | Regra` quando o body tem 3+ campos.
4. Resposta de sucesso e erros, com status e mensagem exatos.

**Mudança em rota existente**: `MÉTODO /caminho`, em que condição o
comportamento muda, o que passou a fazer, o que é ignorado e o que
continua igual.

**Web**:
- Bug: comece pela causa ("Antes, ... Agora ...") e depois liste o
  comportamento por cenário (ex: linha com um item × vários itens).
- Ação nova: onde aparece e quando, passos numerados do que
  acontece, textos de tela e confirmações entre aspas, rotas chamadas.
- Camada `@core` (ou equivalente): tabela com cada tipo, use case,
  gateway ou enum novo.
- Outros ajustes: tudo que muda algo visível ou compartilhado (CSS
  global, tooltip, limite de campo, refactor que outro fluxo usa).

**Prints**: o agente não captura tela. Onde a UI nova ou alterada fica
mais clara com imagem, deixe um marcador numa linha própria:

```markdown
> 📷 **Print:** <o que a imagem deve mostrar>
```

**Impacto** (sempre presente): uma linha por área afetada, cobrindo:
- o que a entrega corrige ou habilita;
- ações irreversíveis ou em lote, e se há confirmação/desfazer;
- mudanças sutis de comportamento (default, condição, `=== 0` →
  indefinido);
- efeitos colaterais fora da tela da tarefa (CSS global, código
  compartilhado, rota antiga);
- compatibilidade com versões anteriores da API/tela;
- migração ou passo manual de deploy, se houver.

## Regras de escrita

- Português do Brasil. Identificadores, rotas, campos, tipos e
  arquivos em `código`, com o nome original.
- Frases curtas e diretas, voz ativa. Mudança de comportamento sempre
  com "antes" e "agora".
- Lista para itens soltos; tabela quando 3+ itens têm os mesmos
  atributos.
- Markdown simples (títulos, listas, tabelas, blocos de código com
  linguagem, citação), sem HTML nem nota de rodapé — o documento é
  colado em editores como o AFFiNE.
- Sem segredo, token, valor de `.env`, host interno ou dado real de
  cliente/usuário, nem nos exemplos de body.
- Não liste testes, commits nem arquivos alterados: o PR já mostra.

## Antes de responder

- [ ] Toda rota, campo e mensagem confere com o código.
- [ ] Seções vazias removidas; nenhuma menção a spec/plano/agents.
- [ ] Impacto cobre riscos e efeitos colaterais vistos no diff.
- [ ] Marcadores de print onde a UI mudou.

No chat, responda só com: caminho do arquivo, 1-2 linhas do que o
documento cobre, a lista de prints a inserir e a de itens
`A confirmar` (se houver). Não cole o documento inteiro.
