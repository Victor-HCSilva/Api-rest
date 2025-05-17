**Resumo**

*   **GET /users/:**  **PÚBLICO** - Lista usuários (sem senha).
*   **POST /users/:**  **PRIVADO (Autenticado)** - Criar um novo usuário.
*   **GET /users/{pk}/:** **PRIVADO (Autenticado)** - Detalhes de um usuário específico (sem senha na resposta).
*   **PUT/PATCH /users/{pk}/:** **PRIVADO (Autenticado)** - Atualizar um usuário existente.
*   **DELETE /users/{pk}/:** **PRIVADO (Autenticado)** - Excluir um usuário.

**Observações Importantes:**

*   **`get_permissions()` Dinâmico:** O `ViewSet` usa o método `get_permissions()` para definir as permissões **dinamicamente** com base na ação (`self.action`). Isso permite ter diferentes níveis de acesso para diferentes operações no mesmo endpoint `/users/`.
*   **`get_serializer_class()` Dinâmico:** Similarmente, `get_serializer_class()` escolhe o serializador correto (`UserListSerializer` para listar, `UserDetailSerializer` para outras ações) dependendo da ação.
*   **`IsAuthenticated` vs `AllowAny`:** `IsAuthenticated` significa que o usuário deve estar logado (fornecer credenciais válidas). `AllowAny` significa que não há necessidade de autenticação, o endpoint é acessível a todos.
*   **Segurança da Senha:**  Mesmo que `UserDetailSerializer` inclua o campo `senha`, lembre-se que `write_only=True` impede que a senha seja retornada nas respostas da API para operações de leitura (retrieve, list, etc.). A senha só é usada para criar e atualizar (desserialização) e é sempre hasheada antes de ser salva no banco de dados.

Este `ViewSet` configura um conjunto de endpoints para gerenciar usuários, com a listagem sendo pública e as demais ações (criação, detalhes, atualização, exclusão) sendo protegidas e exigindo autenticação.
