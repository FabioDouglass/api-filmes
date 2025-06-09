from flask import Blueprint, request, jsonify
from .models import Filme
from . import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

main = Blueprint('main', __name__)

#Listar todos os filmes
@main.route('/filmes', methods=['GET'])
def obter_filmes():
    """
    Retorna a lista de filmes
    ---
    tags:
      - Filmes
    operationId: obter_filmes
    responses:
      200:
        description: Lista de filmes disponível
        schema:
          type: array
          items:
            type: object
            properties:
              titulo:
                type: string
              diretor:
                type: string
              ano:
                type: integer
              nota:
                type: integer
    """
    filmes = db.session.query(Filme.titulo, Filme.diretor, Filme.ano, Filme.nota).all()
    return jsonify([{'titulo': titulo, 'diretor': diretor, 'ano': ano, 'nota': nota} for titulo, diretor, ano, nota in filmes])


#Registrar um filme
@main.route('/filme', methods=['POST'])
def adicionar_filme():
    """
    Adicionar filme
    ---
    tags:
      - Filmes
    operationId: adicionar_filme
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          required:
            - titulo
            - diretor
            - ano
          properties:
            titulo:
              type: string
              example: "Hereditary"
            diretor:
              type: string
              example: "Ari Aster"
            ano:
              type: integer
              example: 2018
            nota:
              type: integer
              example: 5
    responses:
      201:
        description: Filme adicionado com sucesso
      400:
        description: Dados inválidos
      409:
        description: Filme já cadastrado
    """
    dados = request.get_json()

    if not dados or 'titulo' not in dados or 'diretor' not in dados or 'ano' not in dados:
        return jsonify({'erro': 'Campos "titulo", "diretor" e "ano" são obrigatórios'}), 400
    novo_filme = Filme(titulo=dados['titulo'], diretor=dados['diretor'], ano=dados['ano'], nota=dados.get('nota'))
    try:

      db.session.add(novo_filme)
      db.session.commit()

      return jsonify({'mensagem': 'Filme adicionado com sucesso!'}), 201

    except IntegrityError:
      return {"mesage": "Filme já cadastrado!"}, 409

#Deletar um filme
@main.route('/filme/<string:titulo>', methods=['DELETE'])
def deletar_filme(titulo):
    """
    Deletar filme pelo título (corresponde parcialmente, insensível a maiúsculas)
    ---
    tags:
      - Filmes
    operationId: deletar_filme
    parameters:
      - name: titulo
        in: path
        type: string
        required: true
    responses:
      200:
        description: Filme deletado com sucesso
      404:
        description: Filme não encontrado
    """
    filme = db.session.query(Filme).filter(Filme.titulo.ilike(f"%{titulo}%")).first()

    if not filme:
        return jsonify({'erro': 'Filme não encontrado'}), 404

    db.session.delete(filme)
    db.session.commit()
    return jsonify({'mensagem': f'{filme.titulo} foi removido com sucesso.'})


#Buscar um filme
@main.route('/filme', methods=['GET'])
def obter_filme():
    """
    Retorna filmes pelo nome, diretor, ano ou nota
    ---
    tags:
      - Filmes
    operationId: obter_filme
    parameters:
      - name: titulo
        in: query
        type: string
        required: false
      - name: diretor
        in: query
        type: string
        required: false
      - name: ano
        in: query
        type: integer
        required: false
      - name: nota
        in: query
        type: integer
        required: false
    responses:
      200:
        description: Lista de filmes encontrados
        schema:
          type: array
          items:
            type: object
            properties:
              titulo:
                type: string
              diretor:
                type: string
              ano:
                type: integer
              nota:
                type: integer
    """
    titulo = request.args.get("titulo")
    diretor = request.args.get("diretor")
    ano = request.args.get("ano")
    nota = request.args.get("nota")

    filtros = []
    if titulo:
        filtros.append(Filme.titulo.ilike(f"%{titulo}%"))
    if diretor:
        filtros.append(Filme.diretor.ilike(f"%{diretor}%"))
    if ano:
        filtros.append(Filme.ano == int(ano))
    if nota:
        filtros.append(Filme.nota == int(nota))

    if not filtros:
        return jsonify({"erro": "Informe ao menos um parâmetro: titulo, diretor, ano ou nota."}), 400

    filmes = db.session.query(Filme).filter(*filtros).all()

    if not filmes:
        return jsonify([])

    resultado = []
    for filme in filmes:
        resultado.append({
            "titulo": filme.titulo,
            "diretor": filme.diretor,
            "ano": filme.ano,
            "nota": filme.nota
        })

    return jsonify(resultado), 200

#Atualizar nota
@main.route('/filme/<string:titulo>', methods=['PATCH'])
def atualizar_nota_filme(titulo):
    """
    Atualizar a nota do filme pelo título (busca parcial, insensível a maiúsculas)
    ---
    tags:
      - Filmes
    operationId: atualizar_nota_filme
    parameters:
      - name: titulo
        in: path
        type: string
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nota:
              type: number
              format: int
              description: Nova nota do filme
    responses:
      200:
        description: Nota atualizada com sucesso
      400:
        description: Nota inválida
      404:
        description: Filme não encontrado
    """
    filme = db.session.query(Filme).filter(func.lower(Filme.titulo) == titulo.lower()).first()

    if not filme:
        return jsonify({'erro': 'Filme não encontrado'}), 404

    data = request.get_json()
    if not data or 'nota' not in data:
        return jsonify({'erro': 'Campo "nota" é obrigatório'}), 400

    try:
        nova_nota = int(data['nota'])
    except ValueError:
        return jsonify({'erro': 'Campo "nota" deve ser um número'}), 400

    filme.nota = nova_nota
    db.session.commit()

    return jsonify({'mensagem': f'Nota do filme {filme.titulo} atualizada para {filme.nota}.'})
