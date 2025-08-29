from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from database import SessionLocal, engine
import models, schemas
from fastapi_pagination import Page, paginate, add_pagination

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/atletas",
    tags=["Atletas"]
)

# Dependência para sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Criar atleta
@router.post("/", response_model=schemas.AtletaResponse)
def criar_atleta(atleta: schemas.AtletaCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Atleta).filter(models.Atleta.cpf == atleta.cpf).first()
    if existing:
        raise HTTPException(status_code=303, detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}")

    db_atleta = models.Atleta(**atleta.dict())
    db.add(db_atleta)
    db.commit()
    db.refresh(db_atleta)
    return db_atleta

# Listar atletas com query params e paginação
@router.get("/", response_model=Page[schemas.AtletaResponse])
def listar_atletas(nome: Optional[str] = None, cpf: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Atleta)
    if nome:
        query = query.filter(models.Atleta.nome.contains(nome))
    if cpf:
        query = query.filter(models.Atleta.cpf == cpf)
    return paginate(query.all())

# Atualizar atleta
@router.put("/{atleta_id}", response_model=schemas.AtletaResponse)
def atualizar_atleta(atleta_id: int, atleta: schemas.AtletaCreate, db: Session = Depends(get_db)):
    db_atleta = db.query(models.Atleta).filter(models.Atleta.id == atleta_id).first()
    if not db_atleta:
        raise HTTPException(status_code=404, detail="Atleta não encontrado")

    existing = db.query(models.Atleta).filter(models.Atleta.cpf == atleta.cpf, models.Atleta.id != atleta_id).first()
    if existing:
        raise HTTPException(status_code=303, detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}")

    for key, value in atleta.dict().items():
        setattr(db_atleta, key, value)
    db.commit()
    db.refresh(db_atleta)
    return db_atleta

# Deletar atleta
@router.delete("/{atleta_id}")
def deletar_atleta(atleta_id: int, db: Session = Depends(get_db)):
    db_atleta = db.query(models.Atleta).filter(models.Atleta.id == atleta_id).first()
    if not db_atleta:
        raise HTTPException(status_code=404, detail="Atleta não encontrado")
    db.delete(db_atleta)
    db.commit()
    return {"message": f"Atleta {db_atleta.nome} deletado com sucesso!"}
