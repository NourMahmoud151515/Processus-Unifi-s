from dataclasses import dataclass
from enum import Enum


class Statut(str, Enum):
    DEPOSEE = "DEPOSEE"
    EN_COURS = "EN_COURS"
    ACCEPTEE = "ACCEPTEE"
    REFUSEE = "REFUSEE"


@dataclass
class Candidature:
    id: int
    etudiant_email: str
    offre_id: int
    statut: Statut = Statut.DEPOSEE