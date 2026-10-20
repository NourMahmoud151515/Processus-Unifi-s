from fastapi import APIRouter, HTTPException
from app.services import CandidatureIntrouvable, TransitionInvalide


def creer_router(service) -> APIRouter:
    router = APIRouter(prefix="/candidatures", tags=["candidatures"])

    def reponse(c):
        return {"id": c.id, "statut": c.statut.value}

    def executer(action, candidature_id: int):
        try:
            return reponse(action(candidature_id))
        except CandidatureIntrouvable as e:
            raise HTTPException(status_code=404, detail=str(e))
        except TransitionInvalide as e:
            raise HTTPException(status_code=409, detail=str(e))

    @router.post("/{candidature_id}/consulter")
    def consulter(candidature_id: int):
        return executer(service.consulter, candidature_id)

    @router.post("/{candidature_id}/accepter")
    def accepter(candidature_id: int):
        return executer(service.accepter, candidature_id)

    @router.post("/{candidature_id}/refuser")
    def refuser(candidature_id: int):
        return executer(service.refuser, candidature_id)

    return router