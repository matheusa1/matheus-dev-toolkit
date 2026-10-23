# Casos de teste Xray: Anexos da ordem de serviço

História: Anexos da ordem de serviço (chave Jira a preencher). Na web,
fica na aba "Anexos" da ordem de serviço; na API, nas rotas de anexos
da ordem. Tipo de teste: Manual. Cada caso tem Pré-condição e passos no
formato Ação | Dados | Resultado esperado.

## Cobertura

| CA | Casos |
|---|---|
| CA01 | CT01 |
| CA02 | CT01, CT04 |
| CA03 | CT02, CT04 |
| CA04 | CT03, CT05 |
| CA05 | CT03, CT05 |

## CT01 — Exibir os anexos e enviar um arquivo

**Pré-condição:**  
Técnico autenticado com acesso à ordem de serviço; ordem aberta com um
anexo PDF de 2 MB já enviado; arquivo `foto.jpg` de 3 MB disponível

**Requisito CA01 — Exibir os anexos da ordem**  
Dado que o técnico acessou uma ordem de serviço,  
quando a área de anexos for carregada,  
então o sistema deve exibir:

- Lista de anexos já enviados, com nome, tamanho e data de envio;
- Ação para enviar um novo anexo;
- Ação para remover um anexo;
- Espaço total utilizado pelos anexos da ordem.

**Requisito CA02 — Enviar anexo**  
Dado que o técnico está na área de anexos,  
quando selecionar um arquivo e confirmar o envio,  
então o sistema deve salvar o arquivo, incluí-lo na lista e
recalcular o espaço utilizado.

| # | Ação | Dados | Resultado esperado |
|---|---|---|---|
| 1 | Abrir a ordem de serviço e acessar a área de anexos |  | Lista com o PDF (nome, 2 MB, data de envio), ação de enviar, ação de remover no item e espaço utilizado "2 MB" |
| 2 | Enviar um novo anexo | `foto.jpg` (3 MB) | Arquivo aparece na lista com nome, tamanho e data de hoje |
| 3 | Verificar o espaço utilizado |  | Exibe "5 MB" |
| 4 | Sair da ordem e abrir de novo |  | Os dois anexos continuam na lista e o espaço segue "5 MB" |

## CT02 — Validar tipo e tamanho do arquivo

**Pré-condição:**  
Técnico autenticado com acesso a duas ordens de serviço abertas: a
ordem A, com 45 MB em anexos, e a ordem B, com 10 MB (passo 2); arquivos
`planilha.xlsx` (1 MB), `video.jpg` (11 MB) e `foto.jpg` (6 MB)
disponíveis

**Requisito CA03 — Validar o arquivo enviado**  
Dado que o técnico selecionou um arquivo,  
quando tentar enviá-lo,  
então o sistema deve validar que:

- O tipo do arquivo é imagem ou PDF;
- O tamanho do arquivo não passa de 10 MB;
- O espaço total da ordem não passa de 50 MB após o envio.

Quando alguma validação falhar,  
então o sistema deve impedir o envio e exibir uma mensagem informando
o motivo.

| # | Ação | Dados | Resultado esperado |
|---|---|---|---|
| 1 | Na ordem A, enviar um arquivo que não é imagem nem PDF | `planilha.xlsx` | Envio impedido; mensagem informando que só imagem ou PDF são aceitos |
| 2 | Na ordem B, enviar uma imagem acima de 10 MB | `video.jpg` (11 MB) | Envio impedido; mensagem informando o limite de 10 MB (o total de 21 MB não estoura os 50 MB); espaço segue "10 MB" |
| 3 | Na ordem A, enviar uma imagem que faz o total passar de 50 MB | `foto.jpg` (6 MB) | Envio impedido; mensagem informando que o espaço da ordem seria excedido |
| 4 | Verificar a lista e o espaço utilizado da ordem A |  | Nenhum arquivo novo na lista; espaço segue "45 MB" |

## CT03 — Remover anexo, cancelar e falha na operação

**Pré-condição:**  
Técnico autenticado com acesso à ordem de serviço; ordem aberta com
dois anexos de 2 MB; opção de simular falha de rede (DevTools >
Network > Offline)

**Requisito CA04 — Remover anexo**  
Dado que a ordem possui um ou mais anexos,  
quando o técnico selecionar a opção Remover,  
então o sistema deve solicitar a confirmação da remoção.  
Quando o técnico confirmar,  
então o sistema deve remover o anexo e recalcular o espaço utilizado.  
Quando o técnico cancelar,  
então o anexo deve permanecer inalterado.

**Requisito CA05 — Tratamento de erros**  
Dado que ocorra uma falha ao enviar ou remover um anexo,  
quando a operação for concluída,  
então o sistema deve informar que não foi possível realizar a ação e
não deve apresentar o anexo como salvo ou removido.

| # | Ação | Dados | Resultado esperado |
|---|---|---|---|
| 1 | Selecionar Remover no primeiro anexo |  | Sistema pede confirmação da remoção |
| 2 | Cancelar |  | Os dois anexos continuam na lista; espaço "4 MB" |
| 3 | Selecionar Remover no primeiro anexo e confirmar |  | Anexo sai da lista; espaço "2 MB" |
| 4 | Ativar o modo offline e remover o anexo restante, confirmando |  | Mensagem informando que não foi possível remover; anexo continua na lista |
| 5 | Desativar o offline e recarregar a ordem |  | Anexo restante continua na lista; espaço "2 MB" |
| 6 | Encerrar a ordem e acessar a área de anexos |  | Ações de enviar e remover indisponíveis |

## CT04 — API: enviar anexo

**Pré-condição:**  
Token de um técnico com acesso à ordem `OS-1` (aberta, 45 MB em
anexos); token de um técnico sem acesso à `OS-1`; ordem `OS-2`
encerrada; ordem `OS-3` aberta, com 10 MB em anexos, à qual o mesmo
técnico tem acesso (passos 9 e 11)

**Requisito CA02 — Enviar anexo**  
Dado que o técnico está na área de anexos,  
quando selecionar um arquivo e confirmar o envio,  
então o sistema deve salvar o arquivo, incluí-lo na lista e
recalcular o espaço utilizado.

**Requisito CA03 — Validar o arquivo enviado**  
Dado que o técnico selecionou um arquivo,  
quando tentar enviá-lo,  
então o sistema deve validar que:

- O tipo do arquivo é imagem ou PDF;
- O tamanho do arquivo não passa de 10 MB;
- O espaço total da ordem não passa de 50 MB após o envio.

Quando alguma validação falhar,  
então o sistema deve impedir o envio e exibir uma mensagem informando
o motivo.

| # | Ação | Dados | Resultado esperado |
|---|---|---|---|
| 1 | `POST /service-orders/{id}/attachments` | `id=OS-1`, `foto.jpg` (3 MB), token com acesso | 201; corpo com id, nome, tamanho e data de envio do anexo |
| 2 | `GET /service-orders/{id}/attachments` | `id=OS-1`, token com acesso | 200; lista inclui o anexo do passo 1 e o espaço utilizado é 48 MB |
| 3 | `POST /service-orders/{id}/attachments` | `id=OS-1`, `planilha.xlsx` | 422; mensagem informando que só imagem ou PDF são aceitos |
| 4 | `POST /service-orders/{id}/attachments` | `id=OS-1`, `foto.jpg` (3 MB) | 422; mensagem informando que o espaço da ordem seria excedido |
| 5 | `POST /service-orders/{id}/attachments` | `id=OS-1`, sem token | 401 |
| 6 | `POST /service-orders/{id}/attachments` | `id=OS-1`, token sem acesso | 403 |
| 7 | `POST /service-orders/{id}/attachments` | `id=OS-2` (encerrada), token com acesso | 422; mensagem informando que a ordem está encerrada |
| 8 | `POST /service-orders/{id}/attachments` | `id` inexistente | 404 |
| 9 | `POST /service-orders/{id}/attachments` | `id=OS-3`, `video.jpg` (11 MB), token com acesso | 422; mensagem informando o limite de 10 MB (o total de 21 MB não estoura os 50 MB) |
| 10 | `GET /service-orders/{id}/attachments` | `id=OS-1`, token com acesso | 200; mesma lista do passo 2 (nada dos passos 3 a 8 foi salvo) e espaço utilizado 48 MB |
| 11 | `GET /service-orders/{id}/attachments` | `id=OS-3`, token com acesso | 200; `video.jpg` não aparece e o espaço utilizado segue 10 MB |

## CT05 — API: remover anexo

**Pré-condição:**  
Token de um técnico com acesso à ordem `OS-1` (aberta, com os anexos
`A-1` e `A-2` de 2 MB); token de um técnico sem acesso à `OS-1`; ordem
`OS-2` encerrada com o anexo `A-3` e token de um técnico com acesso à
`OS-2` (passo 6)

**Requisito CA04 — Remover anexo**  
Dado que a ordem possui um ou mais anexos,  
quando o técnico selecionar a opção Remover,  
então o sistema deve solicitar a confirmação da remoção.  
Quando o técnico confirmar,  
então o sistema deve remover o anexo e recalcular o espaço utilizado.  
Quando o técnico cancelar,  
então o anexo deve permanecer inalterado.

**Requisito CA05 — Tratamento de erros**  
Dado que ocorra uma falha ao enviar ou remover um anexo,  
quando a operação for concluída,  
então o sistema deve informar que não foi possível realizar a ação e
não deve apresentar o anexo como salvo ou removido.

| # | Ação | Dados | Resultado esperado |
|---|---|---|---|
| 1 | `DELETE /service-orders/{id}/attachments/{attachmentId}` | `id=OS-1`, `attachmentId=A-1` | 204 |
| 2 | `GET /service-orders/{id}/attachments` | `id=OS-1` | 200; `A-1` não aparece e o espaço utilizado não conta os 2 MB |
| 3 | `DELETE /service-orders/{id}/attachments/{attachmentId}` | `attachmentId=A-1` de novo | 404 |
| 4 | `DELETE /service-orders/{id}/attachments/{attachmentId}` | `id=OS-1`, `attachmentId=A-2`, sem token | 401; `A-2` continua na lista |
| 5 | `DELETE /service-orders/{id}/attachments/{attachmentId}` | `id=OS-1`, `attachmentId=A-2`, token sem acesso | 403; `A-2` continua na lista |
| 6 | `DELETE /service-orders/{id}/attachments/{attachmentId}` | `id=OS-2` (encerrada), `attachmentId=A-3` | 422; mensagem informando que a ordem está encerrada; `A-3` continua na lista |
