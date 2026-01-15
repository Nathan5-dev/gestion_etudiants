
from sqlmodel import create_engine, SQLModel, Field, Relationship, Session
from  typing import Optional, List


 #moteur de connection a la BD
DATABASE_URL = "sqlite:///./etudiants.db"

moteur = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)



def get_session():
    with Session(moteur) as session :
        yield session




class Etudiants(SQLModel, table = True):
    id : Optional[int] = Field( default=None, primary_key=True )
    nom : str
    cycle : str
    option: str
    promotion : str

    notes : List['Notes'] = Relationship(back_populates='etudiant', cascade_delete=True)

class Notes(SQLModel, table = True):
    id : Optional[int] = Field(default=None, primary_key=True)
    cours : str
    categorie : str
    credit : int = Field(ge=1, le=15)
    valeur : float =Field(ge=0, le= 20)

    etudiant_id : int = Field(
        default=None,
        foreign_key="etudiants.id"
    )

    etudiant : Optional["Etudiants"] = Relationship(back_populates='notes')









