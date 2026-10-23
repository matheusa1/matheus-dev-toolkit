# Anexos da ordem de serviço

Como técnico responsável por uma ordem de serviço,
quero anexar, consultar e remover arquivos da ordem,
para registrar as evidências do atendimento antes de encerrá-la.

## Objetivo

Disponibilizar uma área de anexos na ordem de serviço, permitindo que o
técnico envie arquivos, acompanhe o espaço utilizado e mantenha os
anexos consistentes com as regras do sistema.

## Critérios de aceitação

### CA01 — Exibir os anexos da ordem

Dado que o técnico acessou uma ordem de serviço,
quando a área de anexos for carregada,
então o sistema deve exibir:

- Lista de anexos já enviados, com nome, tamanho e data de envio;
- Ação para enviar um novo anexo;
- Ação para remover um anexo;
- Espaço total utilizado pelos anexos da ordem.

### CA02 — Enviar anexo

Dado que o técnico está na área de anexos,
quando selecionar um arquivo e confirmar o envio,
então o sistema deve salvar o arquivo, incluí-lo na lista e
recalcular o espaço utilizado.

### CA03 — Validar o arquivo enviado

Dado que o técnico selecionou um arquivo,
quando tentar enviá-lo,
então o sistema deve validar que:

- O tipo do arquivo é imagem ou PDF;
- O tamanho do arquivo não passa de 10 MB;
- O espaço total da ordem não passa de 50 MB após o envio.

Quando alguma validação falhar,
então o sistema deve impedir o envio e exibir uma mensagem informando
o motivo.

### CA04 — Remover anexo

Dado que a ordem possui um ou mais anexos,
quando o técnico selecionar a opção Remover,
então o sistema deve solicitar a confirmação da remoção.
Quando o técnico confirmar,
então o sistema deve remover o anexo e recalcular o espaço utilizado.
Quando o técnico cancelar,
então o anexo deve permanecer inalterado.

### CA05 — Tratamento de erros

Dado que ocorra uma falha ao enviar ou remover um anexo,
quando a operação for concluída,
então o sistema deve informar que não foi possível realizar a ação e
não deve apresentar o anexo como salvo ou removido.

## Regras de negócio

- Ordens de serviço encerradas não permitem enviar nem remover anexos.
- O espaço utilizado é a soma do tamanho dos anexos ativos da ordem.
- Anexos removidos não compõem o espaço utilizado.
- O técnico só vê e altera anexos das ordens às quais tem acesso.

## Fora do escopo

- Pré-visualização do conteúdo dos anexos;
- Edição ou renomeação de anexos já enviados;
- Envio de anexos pelo aplicativo do cliente.

## Resultado esperado

Ao final, o técnico deverá conseguir gerenciar os anexos de uma ordem
de serviço, ver o espaço utilizado atualizado e encerrar a ordem com as
evidências do atendimento registradas.
