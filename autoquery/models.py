
from BeaQuery import db

    
class Consultas(db.Model):
    ConsultaId = db.Column(db.Integer, primary_key = True, nullable = False )
    Task = db.Column(db.String(100), nullable = False)
    DataCadastro = db.Column(db.DateTime(25), nullable =  False)
    MultiplasAbas = db.Column(db.Boolean, nullable = False) 

    def __repr__(self):
        return f'<Consultas {self.ConsultaId}>'  
    
 
