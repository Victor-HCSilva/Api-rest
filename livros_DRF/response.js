let response;

fetch('http://127.0.0.1:8000/books/') // URL da API
  .then(response => {
    if (!response.ok) {
      throw new Error(`Erro na requisição: ${response.status}`); // Trata erros HTTP
    }
    return response.json(); // Converte a resposta para JSON
  })
  .then(data => {
    response = data;
    console.log('Dados recebidos:', data); 
    
  })
  .catch(error => {
    console.error('Ocorreu um erro:', error); 
  });


