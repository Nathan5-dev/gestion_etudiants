
from sqlmodel import SQLModel, Field
from typing import Optional

class EtudiantCreate(SQLModel):
    nom : str
    cycle : str
    option : str
    promotion : str

class EtudiantRead(SQLModel):
    id : int
    nom : str
    cycle : str
    option : str
    promotion : str

class NoteCreate(SQLModel):
    cours : str
    categorie : str
    credit : int
    valeur : float

class NoteRead(SQLModel):
    id : int
    cours : str
    categorie : str
    credit : int
    valeur : float = Field(ge=0, le=20)
    etudiant_id : Optional[int]

class NoteUpdate(SQLModel):
    cours : Optional[str]=None
    categorie: Optional[str]= None
    credit : Optional[int] = None
    valeur : Optional[float] = Field(default=None, ge=0, le=20)