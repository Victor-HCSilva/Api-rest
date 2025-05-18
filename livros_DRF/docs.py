

- **MVC:** `Model-View-Controller`

### **Endpoints da API de Usuários**

- **GET `/users/`** — **PÚBLICO**: Lista todos os usuários (sem incluir senhas).
- **POST `/users/`** — **PRIVADO (Autenticado)**: Cria um novo usuário.
- **GET `/users/{pk}/`** — **PRIVADO (Autenticado)**: Retorna os detalhes de um usuário específico (sem senha).
- **PUT/PATCH `/users/{pk}/`** — **PRIVADO (Autenticado)**: Atualiza um usuário existente.
- **DELETE `/users/{pk}/`** — **PRIVADO (Autenticado)**: Exclui um usuário.

### **Observações Importantes**

- **Permissões dinâmicas com `get_permissions()`:**
  O `ViewSet` utiliza o método `get_permissions()` para definir dinamicamente as permissões com base na ação (`self.action`). Isso permite diferentes níveis de acesso em um mesmo endpoint `/users/`.

- **Serializadores dinâmicos com `get_serializer_class()`:**
  De forma semelhante, o método `get_serializer_class()` seleciona o serializador apropriado:
  - `UserListSerializer` para listagem
  - `UserDetailSerializer` para as demais ações.

- **Controle de acesso:**
  - `IsAuthenticated`: exige autenticação (usuário logado).
  - `AllowAny`: acesso público, sem necessidade de autenticação.

- **Segurança da senha:**
  Mesmo que o `UserDetailSerializer` inclua o campo `senha`, ele é definido como `write_only=True`, o que significa que **nunca será retornado nas respostas da API**. A senha só é utilizada em operações de criação e atualização, sendo **sempre armazenada de forma segura (hasheada)** no banco de dados.
