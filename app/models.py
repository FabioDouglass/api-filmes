from . import db

class Filme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100),unique=True, nullable=False)
    diretor = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    nota = db.Column(db.Integer)

    def to_dict(self):
        return {'id': self.id, 'titulo': self.titulo, 'diretor': self.diretor, 'ano': self.ano, 'nota': self.nota}