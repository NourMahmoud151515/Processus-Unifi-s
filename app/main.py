from fastapi import FastAPI
from app.models import Candidature
from app.notification import NotificationService
from app.repository import CandidatureRepository
from app.routes import creer_router
from app.services import CandidatureService


def create_app(repo=None, notification=None) -> FastAPI:
    repo = repo or CandidatureRepository()
    notification = notification or NotificationService()
    service = CandidatureService(repo, notification)
    app = FastAPI(title="Gestion de stages")
    app.include_router(creer_router(service))
    return app


def _app_demo() -> FastAPI:
    repo = CandidatureRepository()
    repo.ajouter(Candidature(id=1, etudiant_email="etudiant@exemple.tn", offre_id=1))
    return create_app(repo)


app = _app_demo()