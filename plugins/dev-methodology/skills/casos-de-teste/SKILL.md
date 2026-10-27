---
name: casos-de-teste
description: Gera os casos de teste (formato Xray manual, CTxx com pré-condição, requisitos CA e passos Ação | Dados | Resultado esperado) a partir da especificação aprovada, sem viés de implementação, incluindo testes de endpoint quando a entrega tem API. Use logo depois que a spec do brainstorming for salva, antes do plano, ou quando o Matheus pedir casos de teste de uma spec.
---

# Casos de teste a partir da spec

Objetivo: derivar dos critérios de aceitação (`CAxx`) da spec os casos
de teste (`CTxx`) que vão ser executados no fim da implementação e da
revisão (agent `executor-casos-teste`). Roda logo depois da spec,
**antes** do plano e de qualquer código.

O formato de referência está em [`exemplo.md`](exemplo.md) (domínio
fictício) — use a estrutura, não o domínio.

## Sem viés de implementação

- A **única** fonte é a spec (e o contrato público de API, se ela ou a
  conversa o definirem). Não leia código, plano nem estrutura do
  projeto para escrever os casos.
- Teste caixa-preta: descreva o que a pessoa usuária (ou o cliente da
  API) faz e vê. Nada de classe, função, tabela, coluna, fila ou
  detalhe interno.
- O resultado esperado sai do `então` do CA e das regras de negócio,
  não de como você imagina que vai ser implementado. Texto exato de
  tela/mensagem só se a spec o definir; senão descreva o efeito
  ("mensagem informando que o campo é obrigatório").

## Processo

1. Leia a spec salva (`docs/especificacao/…` ou a seção `## Spec` do
   plano, na tarefa pequena).
2. Agrupe CAs que se testam no mesmo roteiro em um CT (ex: exibir +
   selecionar). Cada CA precisa estar em **pelo menos um** CT; um CA
   pode estar em vários.
3. Cubra, além do caminho feliz: validações, valores-limite, erro,
   cancelamento, permissão e cada regra de negócio (ex: status que
   bloqueia edição). Regra de negócio sem CA vira passo no CT do CA
   mais próximo.
4. **Entrega com API** (endpoint novo ou alterado): além dos CTs de
   tela, escreva CTs de endpoint cobrindo os mesmos CAs pelo contrato,
   um por rota/método que muda estado; rota de consulta pode entrar
   como passo de verificação no CT da rota que ela confere. Rota de
   consulta com CA próprio (filtro, paginação, permissão) ou entrega
   só com rotas de consulta → um CT dedicado por rota de consulta:
   - Ação: `MÉTODO /rota` (ex: `POST /service-orders/{id}/attachments`).
   - Dados: parâmetros, corpo e autenticação usados.
   - Resultado esperado: status HTTP e o que o corpo da resposta deve
     ter (campos e valores observáveis), e o efeito visível numa
     consulta posterior (ex: `GET` seguinte já traz o item).
   - Inclua sempre sucesso, validação (400/422) e cada regra de
     negócio que bloqueia a operação. Inclua sem autenticação (401),
     sem permissão (403) e recurso inexistente (404) quando a rota os
     tiver (rota pública não tem 401; rota sem recurso por id não tem
     404).
   - Rota ainda não definida na spec → use `<rota a definir>`; o
     `writing-plans` substitui quando fixar o contrato.
   Entrega só de API (sem tela) → só CTs de endpoint.
5. Escreva o arquivo no formato abaixo e salve em
   `docs/casos-teste/AAAA-MM-DD-nome-tarefa.md`, mesmo nome da spec.
   Se `docs/casos-teste/` não existe, crie-a com um `.gitignore`
   contendo exatamente a linha `*` (mesma regra de
   `docs/especificacao/` em `brainstorming`).
6. Não peça confirmação separada: siga para `writing-plans` e cite o
   arquivo de casos de teste na rodada única de confirmação do plano.

## Formato

```markdown
# Casos de teste Xray: <título da história>

História: <título> (chave Jira a preencher). <onde fica: menu, tela
ou API>. Tipo de teste: Manual. Cada caso tem Pré-condição e passos no
formato Ação | Dados | Resultado esperado.

## Cobertura

| CA | Casos |
|---|---|
| CA01 | CT01 |

## CT01 — <título do roteiro>

**Pré-condição:**  
<perfil/permissão do usuário, dados que precisam existir, estado da
tela>

**Requisito CA01 — <título do CA>**  
<Dado/quando/então copiado da spec, sem alterar>

| # | Ação | Dados | Resultado esperado |
|---|---|---|---|
| 1 | <ação da pessoa usuária> | <valor usado, ou vazio> | <o que deve ser visto> |
```

Regras do formato:
- `CT01`, `CT02`… sequenciais; tabela de Cobertura com **todos** os CAs
  da spec, em ordem.
- Um passo = uma ação e um resultado verificável. Dados concretos
  (`1.500,00`, `31/02/2026`), não "um valor qualquer".
- Pré-condição completa o bastante para outra pessoa (ou agent)
  executar sem perguntar nada.
- Não escreva blocos `> **Divergência:**` aqui: eles são acrescentados
  pelo `executor-casos-teste` quando o comportamento entregue difere.
- Spec mudou depois → atualize este arquivo junto (CA novo ganha CT ou
  passo; Cobertura refeita).
