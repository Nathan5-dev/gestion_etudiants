from fastapi.params import Depends
from passlib.context import CryptContext
from sqlalchemy.util import deprecated
from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordBearer



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


