from  fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from database import moteur
from api_sape import  routeur_etudiant, routeur_Utilisateur, routeur_notes


@asynccontextmanager
async def life_span(app: FastAPI):
    SQLModel.metadata.create_all(moteur)
    print("Démarrage de l'application ...")
    yield
    print("Arrêt de l'application...")

version_app = "V 1.0.0"

app = FastAPI(
    lifespan=life_span,
    version=version_app,
    title=" Students Manager",
    summary=" Gérer les notes et les étudiants ",
    description=" Une application universitaire de gestion des étudiants ",
    contact= None
    )

app.include_router(routeur_etudiant)
app.include_router(routeur_notes)
app.include_router(routeur_Utilisateur)

