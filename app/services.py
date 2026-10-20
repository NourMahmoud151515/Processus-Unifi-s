from app.models import Candidature, Statut


class CandidatureIntrouvable(Exception):
    pass


class TransitionInvalide(Exception):
    pass


class CandidatureService:
    def __init__(self, repo, notification):
        self.repo = repo
        self.notification = notification

    def _get(self, candidature_id: int) -> Candidature:
        c = self.repo.trouver(candidature_id)
        if c is None:
            raise CandidatureIntrouvable(f"Candidature {candidature_id} introuvable")
        return c

    def consulter(self, candidature_id: int) -> Candidature:
        c = self._get(candidature_id)
        if c.statut == Statut.DEPOSEE:
            c.statut = Statut.EN_COURS
            self.repo.sauvegarder(c)
        return c

    def accepter(self, candidature_id: int) -> Candidature:
        return self._decider(candidature_id, Statut.ACCEPTEE)

    def refuser(self, candidature_id: int) -> Candidature:
        return self._decider(candidature_id, Statut.REFUSEE)

    def _decider(self, candidature_id: int, nouveau: Statut) -> Candidature:
        c = self._get(candidature_id)
        if c.statut != Statut.EN_COURS:
            raise TransitionInvalide(
                f"Impossible de passer de {c.statut.value} à {nouveau.value}"
            )
        c.statut = nouveau
        self.repo.sauvegarder(c)
        self.notification.notifier(
            c.etudiant_email,
            f"Votre candidature à l'offre {c.offre_id} est {nouveau.value}.",
        )
        return c