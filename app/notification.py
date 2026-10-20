class NotificationService:
    """Envoie un e-mail avec réessais. Un échec ne bloque pas la décision."""

    def __init__(self, envoyeur=None, max_essais: int = 3):
        self.envoyeur = envoyeur or self._envoyer_log
        self.max_essais = max_essais
        self.echecs: list[tuple[str, str]] = []

    @staticmethod
    def _envoyer_log(email: str, message: str) -> None:
        print(f"[EMAIL] à {email} : {message}")

    def notifier(self, email: str, message: str) -> bool:
        for _ in range(self.max_essais):
            try:
                self.envoyeur(email, message)
                return True
            except Exception:
                continue
        self.echecs.append((email, message))
        return False