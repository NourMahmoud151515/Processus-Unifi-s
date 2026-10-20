# UC3 - Traiter une candidature (accepter / refuser)

**Ticket :** #3 | **Branche :** `uc3-traiter-candidature` | **Acteur principal :** RH
**Acteur secondaire :** Service e-mail

**Préconditions**
- La RH est authentifiée.
- La candidature existe.

**Postcondition (succès)**
- La candidature est ACCEPTEE ou REFUSEE, et le candidat a été notifié (ou la notification est en file d'échec).

## Scénario nominal
1. La RH consulte la candidature : son statut passe de DEPOSEE à EN_COURS.
2. La RH choisit « Accepter ».
3. Le système vérifie que le statut est EN_COURS.
4. Le système enregistre le statut ACCEPTEE.
5. Le système demande l'envoi d'un e-mail au candidat.
6. Le système confirme la décision à la RH.

## Scénarios alternatifs
- **A1 - Refus** : à l'étape 2, la RH choisit « Refuser » ; le statut devient REFUSEE, même suite.
- **A2 - Candidature introuvable** : le système répond 404.
- **A3 - Décision impossible** (statut ≠ EN_COURS, ou déjà décidée) : le système répond 409, rien n'est modifié.
- **A4 - Échec d'envoi e-mail** : le système réessaie 3 fois ; si l'échec persiste, la décision reste valide et l'échec est mémorisé.

## Règles métier
- R1 : seule une candidature EN_COURS peut être acceptée ou refusée.
- R2 : une décision est définitive.
- R3 : un échec de notification ne doit jamais annuler la décision.

## Traçabilité scénario → tests
| Scénario | Test |
|---|---|
| Nominal | `test_accepter_de_bout_en_bout` (intégration) |
| A1 | `test_refuser_change_le_statut` |
| A2 | `test_api_candidature_introuvable` |
| A3 | `test_api_transition_invalide`, `test_impossible_de_decider_deux_fois` |
| A4 / R3 | `test_notification_reessaie_puis_reussit`, `test_echec_notification_ne_bloque_pas_la_decision` |