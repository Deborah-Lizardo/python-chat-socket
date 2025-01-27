# Chat com Sockets em Python

Este é um projeto de chat implementado em Python utilizando **Sockets TCP**, desenvolvido como parte da matéria **"Conectividade em Sistemas Ciberfísicos"**. O sistema permite a comunicação entre múltiplos clientes conectados a um servidor, oferecendo funcionalidades como mensagens públicas (broadcast), privadas (unicast), validação de nicknames, e exibição de usuários conectados.

**Feito por:** Anna Quezia e Deborah Lizardo

## Funcionalidades

### Requisitos Funcionais

#### 1. **Mensagem de boas-vindas (Broadcast)**:
Ao conectar, o sistema envia uma mensagem de boas-vindas para todos os usuários conectados: "O cliente <nome_usuario> entrou no chat dos Little Cats."

- **Erro de Envio**: Se houver erro ao enviar a mensagem, o sistema registra o erro e tenta enviar para os outros clientes.

#### 2. **Envio de mensagens privadas (Unicast)**:
O sistema permite enviar mensagens privadas para um usuário específico, identificado pelo seu **nickname**.

- **Erro de Envio**: Se o destinatário não for encontrado ou ocorrer erro na conexão, o sistema retorna uma mensagem de erro.

#### 3. **Exibição do IP e porta dos clientes**:
O servidor exibe o IP e a porta de cada cliente ao se conectar no formato: "<nome_usuario> se conectou com o IP <ip_cliente> por meio da porta <porta_cliente>."

- **Erro de Conexão**: Se o servidor não conseguir identificar o IP ou a porta, ele exibirá uma mensagem de erro e não permitirá a conexão.

#### 4. **Mensagem de saída (Broadcast)**:
Quando um cliente sai, o sistema envia a mensagem de saída para todos os clientes: "<nome_usuario> saiu do chat dos Little Cats."

- **Erro de Envio**: Se houver erro ao enviar a mensagem de saída, o cliente será removido da lista de clientes conectados.

#### 5. **Validação de Nickname**:
O sistema valida que o nickname fornecido pelo usuário seja único e não vazio. Caso contrário, solicita que o cliente forneça um nome.

- **Erro de Validação**: Se o nickname for inválido, o sistema solicita um novo nome.

#### 6. **Lista de usuários conectados**:
O servidor deve permitir ao cliente visualizar uma lista com os nicknames de todos os usuários conectados.

- **Erro de Listagem**: Se não houver clientes conectados, o sistema informará ao usuário.

#### 7. **Exibição do remetente nas mensagens privadas**:
Quando um usuário envia uma mensagem privada, o destinatário verá claramente o nickname do remetente.

#### 8. **Validação de Nickname nas mensagens privadas**:
O sistema valida que o remetente esteja enviando a mensagem para um nickname válido, e caso contrário, retorna um erro.

---

## Como Funciona

O projeto segue uma arquitetura **cliente-servidor** usando **sockets TCP**. O servidor é responsável por gerenciar a comunicação entre múltiplos clientes conectados, enquanto os clientes enviam e recebem mensagens.


---

## Estrutura do Projeto

/chat-python-sockets  
&nbsp;&nbsp;&nbsp;&nbsp;/server.py      # Código do servidor  
&nbsp;&nbsp;&nbsp;&nbsp;/client.py      # Código do cliente  
&nbsp;&nbsp;&nbsp;&nbsp;/README.md      # Este arquivo  


