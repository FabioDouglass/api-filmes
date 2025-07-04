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

  ```bash
   pip3 install -r requirements.txt
  ````

OBS: Projeto feito com Python 3.13.2


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
  GET /filme?titulo=$titulo

  ```

- **Editar a nota de um filme:**

  ```http
  PATCH /filme/{titulo}
  Body:
  {
    "nota": int
  }
  ```

  - **Deletar um filme por título:**

  ```http
  DELETE /filme/{titulo}
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



  

  