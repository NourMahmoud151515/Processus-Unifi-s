from typing import Optional
from app.models import Candidature


class CandidatureRepository:
    """Accès aux données (en mémoire pour l'instant)."""

    def __init__(self):
        self._data: dict[int, Candidature] = {}

    def ajouter(self, candidature: Candidature) -> None:
        self._data[candidature.id] = candidature

    def trouver(self, candidature_id: int) -> Optional[Candidature]:
        return self._data.get(candidature_id)

    def sauvegarder(self, candidature: Candidature) -> None:
        self._data[candidature.id] = candidature