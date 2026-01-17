from fastapi.params import Depends
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from database import get_session, Utilisateur
from sqlmodel import Session,select
from jose import  JWTError, jwt
from fastapi import HTTPException, status



pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated = "auto"
)
def hash_password(password : str ) -> str:
    return pwd_context.hash(password)

def verifier_password(password: str, hashed_password: str) -> bool:
    return  pwd_context.verify(password, hashed_password)


SECRET_KEY = "CHANGE-MO-TO-A-SECURE-RANDOM-STRING"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MUNITES = 30

dependence_OAuth2 = OAuth2PasswordBearer(tokenUrl="/login")

def creer_acces_token(
        donnes : dict,
        expitation_delta : timedelta | None = None ):

    """ Fonction pour generer un JWT """
    a_encoder = donnes.copy()

    expire = datetime.now() + ( expitation_delta or timedelta(TOKEN_EXPIRE_MUNITES))
    a_encoder.update({"exp" : expire})

    jwt_encode = jwt.encode(
        a_encoder,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return jwt_encode


erreur = HTTPException(   # erreurs de reference
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=" Token invalide ou expiré ! ",
            headers={"WWW-Authenticate": "Bearer"}
        )

## La fonction de dependence pour retourner un utilisateur apres verification de son ID
def get_curent_user(token : str = Depends(dependence_OAuth2),
                    session : Session = Depends(get_session)) -> Utilisateur:
    try:
        playload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=ALGORITHM
        )
        id_utilisaeur : str | None = playload.get("sub")
        if not id_utilisaeur :
            raise erreur

    except JWTError :
        raise erreur

    requete = select(Utilisateur).where(Utilisateur.id == int(id_utilisaeur))
    user = session.exec(requete).first()
    if not user:
        raise erreur
    return user
#-------------------------------------------------------