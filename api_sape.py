
from fastapi import  HTTPException, status, Depends, APIRouter,Query
from sqlmodel import  Session,select
from database import  Etudiants, Notes, get_session, Utilisateur
from schemas import NoteCreate, NoteRead,EtudiantRead,EtudiantCreate, NoteUpdate, UtilisateurCreate,UtilisateurRead
from typing import List, Optional, Union, Dict
from  auth import hash_password, verifier_password, creer_acces_token, get_curent_user, TOKEN_EXPIRE_MUNITES
from fastapi.security import OAuth2PasswordRequestForm
from datetime import  timedelta



routeur_etudiant = APIRouter(tags=[" Étudiants"])
routeur_notes= APIRouter(tags=[" Notes"])
routeur_Utilisateur = APIRouter(tags=[" Utilisateurs "])


@routeur_etudiant.get("/etudiants",response_model=List[EtudiantRead])
async def get_all_students(
    nom: Optional[str] = Query(
        default=None,
        description="Recherche partielle par nom de l'étudiant"
    ),
    skip: int = Query(default=0,ge=0,
            description="Nombre d'étudiants à ignorer"
        ),
    limit: int = Query(default=3,ge=1,le=100,
            description="Nombre maximum d'étudiants à retourner"
        ),
    session: Session = Depends(get_session)):
    """ Une route qui permet de récupérer les étudiants avec recherche par nom """

    statement = select(Etudiants)
    if nom:
        statement = statement.where(
            Etudiants.nom.ilike(f"%{nom}%")
        )
    statement = statement.offset(skip).limit(limit)
    etudiants = session.exec(statement).all()
    return etudiants


@routeur_etudiant.get('/etudiant/{etudiant_id}')
async def get_student(
        etudiant_id: int,
        session : Session = Depends(get_session)
                    ) -> EtudiantRead:
    """ Une route qui permet de de récupérer un étudiant"""

    etu : Optional[EtudiantRead]= session.get(Etudiants,etudiant_id)

    if  etu == None:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé !")
    return etu


@routeur_etudiant.post('/etudiant',response_model= EtudiantRead)
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

@routeur_notes.post('/etudiant/{id_etudiant}/notes', response_model=NoteRead)
async def create_note(id_etudiant: int,
                      etudiant_note: NoteCreate,
                      connexion : Session = Depends(get_session),
                      current_user : Utilisateur=Depends(get_curent_user)):
    """ Une route qui permet d'ajouter  une note a un étudiant  """

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


@routeur_notes.get('/notes', response_model=List[NoteRead])
async def get_notes(session: Session = Depends(get_session)):

    """ Une route qui retourne toutes les notes """
    requete = select(Notes)
    notes =  session.exec(requete).all()
    return notes

@routeur_notes.get('/notes/{etudiant_id}', response_model=Union[List[NoteRead], Dict])
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


@routeur_etudiant.get('/moyenne/{etudiant_id}')
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


@routeur_notes.patch('/note/{note_id}', response_model=NoteRead)
async def update_note(note_id : int,
                      note_data : NoteUpdate,
                      session : Session = Depends(get_session),
                      current_user : Utilisateur=Depends(get_curent_user)):
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


@routeur_Utilisateur.post('/auth/register',
          response_model=UtilisateurRead,
          status_code=status.HTTP_201_CREATED)
async def inscription_utilisateur(user_data : UtilisateurCreate,
                                  session : Session = Depends(get_session)):
    """ Route pour enregistrer un nouvel utilisateur ! """

    requete = select(Utilisateur).where(Utilisateur.username == user_data.username)
    user_exist  = session.exec(requete).first()

    if  user_exist:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail=" Non d'utilisateur deja utilise")

    pwd_hash = hash_password(user_data.password)
    user = Utilisateur(
        username = user_data.username,
        password_hash= pwd_hash
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@routeur_Utilisateur.get('/users', response_model= List[UtilisateurRead])
async  def get_utilisateurs(connexion : Session = Depends(get_session),
                            current_user : Utilisateur=Depends(get_curent_user)) :
    """ retourne tous les utilisateurs """

    utilisateurs = connexion.exec(select(Utilisateur)).all()
    return utilisateurs

@routeur_Utilisateur.post('/login')
async def login_fonction(
        form_donnes : OAuth2PasswordRequestForm = Depends(),
        session : Session = Depends(get_session)) -> dict :
    """ Route porteuse pour renvoyer le jwt de l'utilisateur """

    statement = select(Utilisateur).where(
        Utilisateur.username == form_donnes.username,
    )
    user = session.exec(statement).first()
    password_verifie = verifier_password(
         password=form_donnes.password,
        hashed_password=user.password_hash
    )
    if not  user or not password_verifie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=" nom d'utilisateur ou mot de passe invalide ! ",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = creer_acces_token(
        donnes= {"sub": str(user.id)},
        expitation_delta= timedelta(minutes=TOKEN_EXPIRE_MUNITES)
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }





# @app.delete('/etudiant/{etudiant_id}')
# async def delete_student(etudiant_id : str) -> dict :
#     for etudiant in Etudiants :
#         if etudiant_id == etudiant['id']:
#             Etudiants.remove(etudiant)
#             return {"message": f" l'étudiant {etudiant['id']} supprime avec succes ! ",
#                     "etudiant": etudiant}
#     raise HTTPException(status.HTTP_404_NOT_FOUND, detail =" l'étudiant non trouve ")