# PROJ-123 – Extrato de despesas exibe lançamento divergente ao editar nota de despesas agrupadas por pedido de compra

Jira: https://empresa.atlassian.net/browse/PROJ-123

## Detalhes da implementação

### Back

#### Retorno de `/expenses/statement`

O retorno da rota ganhou uma estrutura com as notas originais que foram
agrupadas na linha do extrato.

- As linhas de despesa de fornecedor, agrupadas por pedido de compra,
  agora sempre trazem `originalInvoices`. Antes isso só vinha com
  `expandRows=true`. As opções `includeOriginalInvoices` e
  `TFormatSupplierStatementOptions` foram removidas.
- Novo campo `purchaseOrderId` na linha, com o id do pedido de compra. É
  ele que o front usa para chamar as duas rotas novas.
- Cada item de `originalInvoices` (`buildOriginalInvoices.use.case.ts`)
  ganhou dois campos:
  - `totalValue`: valor da nota, calculado sobre o campo de valor do
    extrato (`grossValue` nas despesas de serviço);
  - `allocatedValue`: soma do que já foi rateado. Quando há rateio por
    projeto, soma os projetos; senão, soma os centros de custo.

```typescript
type TStatementOriginalInvoice = {
  invoiceId?: string;           // id da nota (é este que deve ir para a edição)
  invoiceNumber?: number;       // número da nota fiscal
  invoiceSeries?: string;       // série
  totalValue?: number;          // valor bruto da nota (mesma base do totalValue da linha)
  allocatedValue?: number;      // valor alocado após o filtro de centro de custo/projeto
  category?: { id: string; ... };
  period?: string;
  costCenter?: { id: string; name: string; ... };
  isExcludedFromMetrics?: number;
  allocations?: Array<{ costCenter?; category?; period?; allocatedValue?; projects?: Array<{ id; name; allocatedValue }> }>;
};

// linha do extrato
type TStatement = { ...camposAtuais; purchaseOrderId?: string; originalInvoices?: TStatementOriginalInvoice[] };
```

#### Rotas novas

Duas rotas novas, ambas para atualizar em lote todas as notas de um
pedido de compra.

##### Ratear todas as notas de um pedido

`PUT /api/v1/invoice/purchase-order/:purchaseOrderId/allocation`

1. Busca todas as notas do pedido com o novo `getByPurchaseOrder` do
   gateway, que já traz o pedido e os rateios de centro de custo e
   projeto.
2. Se o pedido não tiver notas, retorna 404.
3. Valida se o usuário tem acesso à conta do pedido e se o rateio é
   válido, com o `ValidateInputUseCase` que já existia.
4. Numa única transação, aplica o mesmo rateio a cada nota via
   `saveByInvoice`. Se qualquer uma falhar, nada é gravado.

**Parâmetros**

- `:purchaseOrderId` é o id do pedido de compra, não o id de uma nota.
- Body (`TUpdateAllocationByPurchaseOrder`):

```json
{
  "allocation": [
    {
      "percentage": 30,
      "period": "2026-01",
      "costCenterId": "<uuid>",
      "category": { "id": "<uuid>", "accountId": "<uuid>" },
      "projects": [
        { "projectId": "<uuid>", "percentage": 15 }
      ]
    }
  ]
}
```

| Campo | Obrigatório | Regra |
|---|---|---|
| `allocation` | sim | array, pode ser vazio (`[]` limpa o rateio) |
| `allocation[].percentage` | sim | 0 a 100, até 2 casas decimais |
| `allocation[].period` | não | competência |
| `allocation[].costCenterId` | não | UUID |
| `allocation[].category` | não | `{ id, accountId }`, ambos UUID e obrigatórios se `category` vier |
| `allocation[].projects[]` | não | `{ projectId (UUID), percentage (0–100) }` |

- Resposta: `200` → `true`. Erros: `404` "Pedido de compra não
  encontrado"; `400` com a mensagem de validação ou "Erro ao ratear as
  notas do pedido de compra. Detalhes: ...".

##### Ocultar/exibir nas métricas todas as notas de um pedido

`PUT /api/v1/invoice/purchase-order/:purchaseOrderId/hide`

- Mesmo fluxo: busca as notas, valida o acesso à conta e atualiza
  `isExcludedFromMetrics` de todas numa transação.
- Para isso, o `updateMetricsExclusion` do gateway passou a aceitar um
  `queryRunner` opcional. A rota antiga `PUT /hide` continua funcionando
  igual.

**Parâmetros**

- `:purchaseOrderId` é o id do pedido de compra, não o id de uma nota.
- Body (`THideByPurchaseOrder`):

```json
{ "hide": true }
```

- `hide` é boolean e obrigatório: `true` oculta, `false` volta a exibir.
- Resposta: `200` → `true`. Erros: `404` "Pedido de compra não
  encontrado"; `400` "Erro ao ocultar as notas do pedido de compra.
  Detalhes: ...".

#### Mudança de comportamento em rota existente

`PUT /api/v1/invoice/:id`

- Quando a nota foi importada do ERP (`originType === ERP`), a rota
  agora usa o novo `UpdateErpInvoiceUseCase` e só altera duas coisas:
  - `allocation`: o rateio, se vier no body;
  - `purchaseOrder.description`: a observação do pedido, via o novo
    `updateDescription` no módulo `purchaseOrder`.
- Todos os outros campos do body são ignorados sem erro para notas do
  ERP. O body continua sendo o `TCreateInvoiceStructure` de sempre.
- Para notas de outras origens, nada mudou.

### Web

#### Correção da edição (origem do bug)

Antes, ao editar ou ocultar uma linha agrupada por pedido de compra, o
front usava o `invoiceId ?? id` da linha. Esse id apontava para uma única
nota do agrupamento, e não necessariamente para a nota que o usuário
queria alterar. Agora o id é resolvido pelo novo
`ResolveStatementOriginalInvoicesUseCase`:

- Linha com uma única nota: editar e ocultar usam o `invoiceId` da
  própria nota (`getEditInvoiceId` / `getExclusionParams`).
- Linha com mais de uma nota: os botões de editar e ocultar da linha não
  agem mais direto. Eles expandem a linha para o usuário escolher a nota,
  com os tooltips "Escolha a nota do pedido para editar/ocultar".
- Painel "Notas do pedido": cada nota tem o seu olho e o seu lápis, que
  enviam o `invoiceId` dela para a rota de edição ou para a rota
  `PUT /hide` que já existia.
- Coluna de valor: linhas com várias notas mostram "N notas" abaixo do
  valor.

#### Ações em lote no painel "Notas do pedido"

Os botões aparecem no cabeçalho do painel só quando a linha tem
`purchaseOrderId` e mais de uma nota.

> 📷 **Print:** cabeçalho do painel "Notas do pedido" com os botões "Ratear todas" e "Ocultar todas"

##### Ratear todas

1. Ao abrir o modal, busca todas as notas do pedido em paralelo
   (`getById`).
2. Compara os rateios atuais com o `ResolveSharedAllocationUseCase`. A
   comparação usa centro de custo, categoria, competência, percentual
   arredondado em 2 casas e projetos, e ignora a ordem.
3. Se todas as notas têm o mesmo rateio, o formulário já vem preenchido
   com ele. Se os rateios forem diferentes, o formulário abre em branco
   com um alerta: a ação não mescla, ela substitui o rateio de cada nota.
4. O formulário trabalha só com percentual, com o campo de valor oculto
   pela nova prop `hideValueInput`, porque cada nota tem um valor bruto
   diferente.
5. Envia para `PUT .../purchase-order/:purchaseOrderId/allocation`. Se o
   usuário salvar sem nenhum rateio, o front pede a confirmação "Remover
   o rateio de todas as notas?" antes de mandar `allocation: []`.
6. Em caso de sucesso, recarrega o extrato.

> 📷 **Print:** modal "Ratear todas" com o alerta de rateios diferentes

##### Ocultar todas / Exibir todas

- O rótulo é decidido por `getBulkExclusion`: mostra "Exibir todas" só
  quando todas as notas já estão ocultas. Nos demais casos, mostra
  "Ocultar todas".
- Pede confirmação (popconfirm), envia
  `PUT .../purchase-order/:purchaseOrderId/hide` com
  `{ "hide": true | false }` e recarrega o extrato.

#### Camada `@core`

| Módulo | Item | Responsabilidade |
|---|---|---|
| `expenseStatement` | `TStatementOriginalInvoice` + campos `originalInvoices` e `purchaseOrderId` na linha | Tipagem do novo retorno de `/expenses/statement` |
| `expenseStatement` | `ResolveStatementOriginalInvoicesUseCase` | Regras da linha agrupada: contagem, id de edição, parâmetros de ocultar, ações em lote e labels |
| `invoice` | `updatePurchaseOrderAllocation` / `updatePurchaseOrderVisibility` (gateway + use cases) | Chamam as duas rotas novas e dão erro se o `purchaseOrderId` não vier |
| `invoice` | `ResolveSharedAllocationUseCase` | Verifica se as notas têm o mesmo rateio e devolve o rateio comum |
| `invoice` | `ConvertAllocationsToFormUseCase` / `BuildAllocationPayloadUseCase` | Conversão API → form e form → payload. Foram extraídos do `useSupplierExpenseForm` e agora são reutilizados no modal |
| `invoice` | `EInvoiceOriginType` (`USER = 1`, `ERP = 2`) | Substitui o número mágico `2` na checagem de nota do ERP |

#### Outros ajustes

- Formulário de despesa de fornecedor: o `useSupplierExpenseForm` passou
  a usar os use cases de conversão de rateio. O comportamento continua o
  mesmo.
- Observação em notas do ERP: limite de 250 caracteres (nas demais
  continua 255). O ajuste acompanha a mudança do back, em que a rota de
  edição de nota do ERP só altera o rateio e a
  `purchaseOrder.description`.
- CSS global corrigido: a regra `.ant-card-head { padding: 0 !important }`
  do formulário de despesa vazava para todos os cards do sistema. Agora
  vale só dentro de `.form-expense-card`.
- Tooltips do olho: passam a descrever a ação ("Ocultar do cálculo…" /
  "Incluir no cálculo…") em vez do estado atual.
- Botão de editar: ganhou tooltip, `aria-label` e destaque de cor. O
  título do painel expandido ficou maior.

## Impacto

| Área | Impacto |
|---|---|
| Edição de despesa agrupada por pedido | Corrige o bug do ticket: a nota editada ou ocultada é sempre a que o usuário escolheu. |
| Operações em lote | "Ratear todas" e "Ocultar todas" sobrescrevem todas as notas do pedido, inclusive as ocultas. Há confirmação, mas não há desfazer (no back é tudo ou nada, numa transação). |
| Linhas com uma nota | Mudança sutil: o olho considera "incluso" quando `isExcludedFromMetrics` vem indefinido. Antes exigia `=== 0`. |
| Outras telas | A correção do CSS pode alterar o visual de cards que dependiam, sem intenção, do padding zerado. Vale uma conferência visual. |
| Compatibilidade | Se a API não devolver `originalInvoices`, a tela se comporta como antes. |
