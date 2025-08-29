from pydantic import BaseModel

class AtletaBase(BaseModel):
    nome: str
    cpf: str
    centro_treinamento: str
    categoria: str

class AtletaCreate(AtletaBase):
    pass

class AtletaResponse(AtletaBase):
    id: int

    class Config:
        orm_mode = True
