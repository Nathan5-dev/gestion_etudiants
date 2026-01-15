
import json

from fastapi import FastAPI, HTTPException, status, Depends
from sqlmodel import SQLModel, Session,select
from database import  moteur, Etudiants, Notes, get_session
from schemas import NoteCreate, NoteRead,EtudiantRead,EtudiantCreate, NoteUpdate
from contextlib import asynccontextmanager
from typing import List, Optional, Union, Dict



# with open("donnes.json","r", encoding="utf-8") as f1 :
#     Etudiants : list = json.load(f1)

@asynccontextmanager
async def life_span(app: FastAPI):
    SQLModel.metadata.create_all(moteur)
    print("Démarrage de l'application ...")
    yield
    print("Arrêt de l'application...")

app = FastAPI(lifespan=life_span)



@app.get("/etudiants", response_model=List[EtudiantRead])
async def get_all_students( session : Session = Depends(get_session)):
    """ Une route qui permet de récupérer tout les étudiants """

    etudiants = session.exec(select(Etudiants)).all()
    return etudiants

@app.get('/etudiant/{etudiant_id}')
async def get_student(
        etudiant_id: int,
        session : Session = Depends(get_session)
                    ) -> EtudiantRead:
    """ Une route qui permet de de récupérer un étudiant"""

    etu : Optional[EtudiantRead]= session.get(Etudiants,etudiant_id)

    if  etu == None:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé !")
    return etu


@app.post('/etudiant',response_model= EtudiantRead)
async def create_student(
        etudiant: EtudiantCreate,
        session : Session = Depends(get_session)
        ) -> EtudiantCreate:
    """ Une route qui permet de créer un étudiant """

    etu = Etudiants.model_validate(etudiant)
    session.add(etu)
    session.commit()
    session.refresh(etu)

    return etu

@app.post('/etudiant/{id_etudiant}/notes', response_model=NoteRead)
async def create_note(id_etudiant: int,
                      etudiant_note: NoteCreate,
                      connexion : Session = Depends(get_session)):
    """ Une route qui permet d'ajouter  une note pour un étudiant  """

    etu = connexion.get(Etudiants, id_etudiant)
    if not etu:
        raise HTTPException(status_code=404, detail=f"Étudiant avec id :{id_etudiant}  non trouvé !")

    note = Notes(
        cours= etudiant_note.cours,
        categorie = etudiant_note.categorie,
        credit = etudiant_note.credit,
        valeur = etudiant_note.valeur,
        etudiant_id = id_etudiant
    )
    connexion.add(note)
    connexion.commit()
    connexion.refresh(note)
    return note


@app.get('/notes', response_model=List[NoteRead])
async def get_notes(session: Session = Depends(get_session)):

    """ Une route qui retourne toutes les notes """
    requete = select(Notes)
    notes =  session.exec(requete).all()
    return notes

@app.get('/notes/{etudiant_id}', response_model=Union[List[NoteRead], Dict])
async def get_etudiant_notes(
        etudiant_id : int,
        conn : Session = (Depends(get_session))
    ):
    etu = conn.get(Etudiants,etudiant_id)
    if not etu:
        raise HTTPException(
            status_code=404,
            detail=f"Étudiant avec id :{etudiant_id}  non trouvé !")
    notes = etu.notes
    if len(notes)== 0 :
        return {'Message': f"L'étudiant avec id : {etudiant_id} n'a pas de note !"}
    return notes

@app.get('/moyenne/{etudiant_id}')
async def get_moyenne( etudiant_id : int,
                    session : Session = Depends(get_session)) -> Dict:
    """ Route pour retourner la moyenne d'un étudiant via son Id """

    etu = session.get(Etudiants, etudiant_id)
    if not etu:
        raise HTTPException(
            status_code=404,
            detail=f"Étudiant avec id :{etudiant_id}  non trouvé !")
    notes : list = etu.notes
    if len(notes)== 0 :
        return {'Message': f"L'étudiant avec id : {etudiant_id} n'a pas de note !"}
    else :
         credits_n =0
         points =0
         for n in notes:
             credits_n += n.credit
             points += n.valeur * n.credit
         moy = points / (credits_n *20)
         moyenne = round(moy*20, 2)
         return {
                'Etudiant' : etu.id,
                'nom' : etu.nom,
                'promotion' : f"{etu.promotion}  {etu.option} | {etu.cycle}",
                'Moyenne' : moyenne
            }


@app.patch('/note/{note_id}', response_model=NoteRead)
async def update_note(note_id : int,
                      note_data : NoteUpdate,
                      session : Session = Depends(get_session)):
    """ Route pour mettre a jour une note """

    note = session.get(Notes, note_id)
    if not  note:
        raise HTTPException(
            status_code=404,
            detail=" Note non trouve !"
        )
    update_data = note_data.model_dump(exclude_unset=True)
    for cle , valeur in update_data.items():
        setattr(note, cle, valeur )
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


#
#
# @app.delete('/etudiant/{etudiant_id}')
# async def delete_student(etudiant_id : str) -> dict :
#     for etudiant in Etudiants :
#         if etudiant_id == etudiant['id']:
#             Etudiants.remove(etudiant)
#             return {"message": f" l'étudiant {etudiant['id']} supprime avec succes ! ",
#                     "etudiant": etudiant}
#     raise HTTPException(status.HTTP_404_NOT_FOUND, detail =" l'étudiant non trouve ")