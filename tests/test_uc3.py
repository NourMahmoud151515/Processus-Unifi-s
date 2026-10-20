import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.models import Candidature, Statut
from app.notification import NotificationService
from app.repository import CandidatureRepository
from app.services import CandidatureService, TransitionInvalide


def construire(statut=Statut.EN_COURS, envoyeur=None):
    repo = CandidatureRepository()
    repo.ajouter(Candidature(1, "etu@exemple.tn", 10, statut))
    notif = NotificationService(envoyeur=envoyeur, max_essais=3)
    return repo, notif


# --- Test d'intégration : route -> service -> dépôt -> notification ---
def test_accepter_de_bout_en_bout():
    envoyes = []
    repo, notif = construire(envoyeur=lambda e, m: envoyes.append((e, m)))
    client = TestClient(create_app(repo, notif))

    r = client.post("/candidatures/1/accepter")

    assert r.status_code == 200
    assert r.json() == {"id": 1, "statut": "ACCEPTEE"}
    assert repo.trouver(1).statut == Statut.ACCEPTEE
    assert len(envoyes) == 1 and envoyes[0][0] == "etu@exemple.tn"


def test_api_candidature_introuvable():
    client = TestClient(create_app())
    assert client.post("/candidatures/99/accepter").status_code == 404


def test_api_transition_invalide():
    repo, notif = construire(statut=Statut.DEPOSEE)
    client = TestClient(create_app(repo, notif))
    assert client.post("/candidatures/1/accepter").status_code == 409


# --- Tests unitaires ---
def test_refuser_change_le_statut():
    repo, notif = construire(envoyeur=lambda e, m: None)
    service = CandidatureService(repo, notif)
    assert service.refuser(1).statut == Statut.REFUSEE


def test_impossible_de_decider_deux_fois():
    repo, notif = construire(envoyeur=lambda e, m: None)
    service = CandidatureService(repo, notif)
    service.accepter(1)
    with pytest.raises(TransitionInvalide):
        service.refuser(1)


def test_notification_reessaie_puis_reussit():
    tentatives = []

    def instable(e, m):
        tentatives.append(1)
        if len(tentatives) < 3:
            raise ConnectionError("SMTP indisponible")

    notif = NotificationService(envoyeur=instable, max_essais=3)
    assert notif.notifier("a@b.tn", "msg") is True
    assert len(tentatives) == 3


def test_echec_notification_ne_bloque_pas_la_decision():
    def toujours_en_echec(e, m):
        raise ConnectionError("SMTP down")

    repo, notif = construire(envoyeur=toujours_en_echec)
    service = CandidatureService(repo, notif)
    assert service.accepter(1).statut == Statut.ACCEPTEE
    assert len(notif.echecs) == 1