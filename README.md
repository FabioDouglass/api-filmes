# Backend Acervo Filmes

Projeto de MVP da sprint de Desenvolvimento Fullstack básico.
O projeto consiste em uma estrutura de acervo de filmes, onde é possível registrar, listar, apagar e editar filmes.

## Baixar o projeto

   ```bash
   git clone https://github.com/FabioDouglass/api-filmes
   cd api-filmes
   ```

## Rodar Projeto

1. **Instalar as dependências:**

   pip3 install -r requirements.txt

2. **Inicie a Aplicação:**

   ```bash
   flask run
   ```

## Acessar Documentação

Abra [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs) no navegador

## URl para requisições

http://127.0.0.1:5000/filme
http://127.0.0.1:5000/filmes

- **Listar todos os filmes:**

  ```http
  GET /filmes
  ```

- **Listar um filme por titulo**

  ```http
  GET /filmes?titulo=$titulo

  ```

- **Editar a nota de um filme:**

  ```http
  PATCH /filmes?titulo=$titulo
  Body:
  {
    "nota": int
  }
  ```

  - **Deletar um filme por título:**

  ```http
  DELETE /filmes?titulo=$titulo
  ````

- **Cadastrar um filme:**

  ```http
  POST /api/filme
  Body:
  {
  "ano": int,
  "diretor": str,
  "nota": int,
  "titulo": str
}
 ```



  

  