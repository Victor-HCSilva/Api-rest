import unittest
import requests
import json
import uuid

# --- Configuração ---
BASE_URL = "http://localhost:8000/books/" # Ajuste se seu host/porta for diferente
# Se precisar de autenticação, configure o header aqui:
# HEADERS = {
#     "Content-Type": "application/json",
#     "Accept": "application/json",
#     "Authorization": "Token SEU_TOKEN_AQUI"
# }
# Por enquanto, sem autenticação:
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

class TestBooksAPI(unittest.TestCase):

    created_book_id = None # Para armazenar o ID do livro criado e usá-lo em outros testes
    sample_book_data = {
        "title": "Test Book Title",
        "author": "Test Author",
        "age": 2023, # Ano de publicação
        "state": "Novo",
        "pages": 100,
        "publishing_company": "Test Publisher"
    }
    updated_book_data = {
        "title": "Updated Test Book Title",
        "author": "Updated Test Author",
        "age": 2024,
        "state": "Usado",
        "pages": 150,
        "publishing_company": "Updated Test Publisher"
    }

    def test_01_create_book(self):
        """Testa a criação de um novo livro (POST)."""
        print("\n--- Testando POST /books/ ---")
        response = requests.post(BASE_URL, data=json.dumps(self.sample_book_data), headers=HEADERS)
        self.assertEqual(response.status_code, 201, f"Erro ao criar livro: {response.status_code} - {response.text}")
        response_data = response.json()
        self.assertIn("id_book", response_data, "ID do livro não encontrado na resposta de criação.")
        self.assertIn("title", response_data)
        self.assertEqual(response_data["title"], self.sample_book_data["title"])

        # Guarda o ID do livro criado para usar nos próximos testes
        TestBooksAPI.created_book_id = response_data["id_book"]
        print(f"Livro criado com ID: {TestBooksAPI.created_book_id}")
        print(f"Resposta: {response_data}")

    def test_02_list_books(self):
        """Testa a listagem de todos os livros (GET)."""
        print("\n--- Testando GET /books/ ---")
        response = requests.get(BASE_URL, headers=HEADERS)
        self.assertEqual(response.status_code, 200, f"Erro ao listar livros: {response.status_code} - {response.text}")
        response_data = response.json()
        self.assertIsInstance(response_data, list, "A resposta da listagem não é uma lista.")
        self.assertTrue(len(response_data) > 0, "A lista de livros está vazia após a criação.")
        # Verifica se o livro criado está na lista (opcional, mas bom)
        if TestBooksAPI.created_book_id:
            found = any(book.get("id_book") == TestBooksAPI.created_book_id for book in response_data)
            self.assertTrue(found, "Livro criado não encontrado na listagem.")
        print(f"Livros listados (primeiros 5): {response_data[:5]}")

    def test_03_retrieve_book(self):
        """Testa a recuperação de um livro específico (GET)."""
        self.assertIsNotNone(TestBooksAPI.created_book_id, "ID do livro não foi definido no teste de criação.")
        print(f"\n--- Testando GET /books/{TestBooksAPI.created_book_id}/ ---")
        url = f"{BASE_URL}{TestBooksAPI.created_book_id}/"
        response = requests.get(url, headers=HEADERS)
        self.assertEqual(response.status_code, 200, f"Erro ao recuperar livro: {response.status_code} - {response.text}")
        response_data = response.json()
        self.assertEqual(response_data["id_book"], TestBooksAPI.created_book_id)
        self.assertEqual(response_data["title"], self.sample_book_data["title"])
        print(f"Livro recuperado: {response_data}")

    def test_04_update_book_put(self):
        """Testa a atualização completa de um livro (PUT)."""
        self.assertIsNotNone(TestBooksAPI.created_book_id, "ID do livro não foi definido no teste de criação.")
        print(f"\n--- Testando PUT /books/{TestBooksAPI.created_book_id}/ ---")
        url = f"{BASE_URL}{TestBooksAPI.created_book_id}/"
        response = requests.put(url, data=json.dumps(self.updated_book_data), headers=HEADERS)
        self.assertEqual(response.status_code, 200, f"Erro ao atualizar livro (PUT): {response.status_code} - {response.text}")
        response_data = response.json()
        self.assertEqual(response_data["title"], self.updated_book_data["title"])
        self.assertEqual(response_data["author"], self.updated_book_data["author"])
        self.assertEqual(response_data["pages"], self.updated_book_data["pages"])
        print(f"Livro atualizado (PUT): {response_data}")

        # Atualiza os dados de sample para o PATCH testar sobre o mais recente
        TestBooksAPI.sample_book_data = response_data.copy() # Copia os dados atualizados

    def test_05_update_book_patch(self):
        """Testa a atualização parcial de um livro (PATCH)."""
        self.assertIsNotNone(TestBooksAPI.created_book_id, "ID do livro não foi definido no teste de criação.")
        print(f"\n--- Testando PATCH /books/{TestBooksAPI.created_book_id}/ ---")
        url = f"{BASE_URL}{TestBooksAPI.created_book_id}/"
        patch_data = {"state": "Quase Novo", "pages": 155}
        response = requests.patch(url, data=json.dumps(patch_data), headers=HEADERS)
        self.assertEqual(response.status_code, 200, f"Erro ao atualizar livro (PATCH): {response.status_code} - {response.text}")
        response_data = response.json()
        self.assertEqual(response_data["state"], patch_data["state"])
        self.assertEqual(response_data["pages"], patch_data["pages"])
        # Verifica se os outros campos não foram alterados
        self.assertEqual(response_data["title"], TestBooksAPI.sample_book_data["title"])
        print(f"Livro atualizado (PATCH): {response_data}")


    def test_06_delete_book(self):
        """Testa a exclusão de um livro (DELETE)."""
        self.assertIsNotNone(TestBooksAPI.created_book_id, "ID do livro não foi definido no teste de criação.")
        print(f"\n--- Testando DELETE /books/{TestBooksAPI.created_book_id}/ ---")
        url = f"{BASE_URL}{TestBooksAPI.created_book_id}/"
        response = requests.delete(url, headers=HEADERS)
        self.assertEqual(response.status_code, 204, f"Erro ao deletar livro: {response.status_code} - {response.text}")
        print(f"Livro com ID {TestBooksAPI.created_book_id} deletado.")

        # Tenta recuperar o livro deletado para confirmar (deve dar 404)
        print(f"\n--- Verificando se o livro foi deletado (espera 404) ---")
        response_get_deleted = requests.get(url, headers=HEADERS)
        self.assertEqual(response_get_deleted.status_code, 404, "Livro não foi deletado corretamente ou endpoint não retorna 404.")
        print(f"Tentativa de GET no livro deletado retornou: {response_get_deleted.status_code}")

    def test_07_retrieve_non_existent_book(self):
        """Testa a recuperação de um livro que não existe (GET)."""
        non_existent_id = uuid.uuid4() # Gera um UUID aleatório que provavelmente não existe
        print(f"\n--- Testando GET /books/{non_existent_id}/ (não existente) ---")
        url = f"{BASE_URL}{non_existent_id}/"
        response = requests.get(url, headers=HEADERS)
        self.assertEqual(response.status_code, 404, f"Endpoint não retornou 404 para livro inexistente: {response.status_code} - {response.text}")
        print(f"Tentativa de GET em livro inexistente retornou: {response.status_code}")

if __name__ == '__main__':
    # Para garantir que os testes rodem na ordem definida pelos nomes (test_01, test_02, ...)
    # unittest.main() por padrão executa em ordem alfabética.
    # Podemos criar um TestSuite para controlar a ordem se necessário,
    # mas nomear com prefixos numéricos geralmente funciona.
    suite = unittest.TestSuite()
    suite.addTest(TestBooksAPI('test_01_create_book'))
    suite.addTest(TestBooksAPI('test_02_list_books'))
    suite.addTest(TestBooksAPI('test_03_retrieve_book'))
    suite.addTest(TestBooksAPI('test_04_update_book_put'))
    suite.addTest(TestBooksAPI('test_05_update_book_patch'))
    suite.addTest(TestBooksAPI('test_06_delete_book'))
    suite.addTest(TestBooksAPI('test_07_retrieve_non_existent_book'))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

    # Alternativamente, para rodar todos os testes da classe na ordem alfabética (padrão do unittest.main()):
    # unittest.main(verbosity=2)
