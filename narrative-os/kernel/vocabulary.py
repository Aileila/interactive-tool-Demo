"""Vocabulaire de prédicats — décision Q8 (Phase 3).

Noyau commun minimal (transversal aux domaines, cf. docs/phase-3) :
spatial, possession, propriété libre, épistémique/volitif, appartenance,
dissimulation. Toute autre relation est déclarée par le monde dans son champ
`vocabulary` (extensions de domaine). Un prédicat inconnu est un refus R-VOCAB-1.

Drapeaux :
- functional      : au plus une valeur d'objet par sujet (situé-à).
- exclusiveObject : un même objet ne peut être en relation qu'avec un sujet
                    (possède : un objet n'a qu'un possesseur).
"""

CORE = {
    "situé-à":   {"functional": True},
    "possède":   {"exclusiveObject": True},
    "est":       {},
    "croit":     {},
    "sait":      {},
    "veut":      {},
    "intention": {},
    "cache":     {},
    "membre-de": {},
}


def build_vocabulary(world):
    """Noyau + extensions déclarées. Erreur si une extension redéfinit le noyau."""
    vocab = {name: dict(flags) for name, flags in CORE.items()}
    errors = []
    for ext in world.data.get("vocabulary", []):
        name = ext["name"]
        if name in CORE:
            errors.append(f"vocabulaire : l'extension '{name}' redéfinit un prédicat du noyau")
            continue
        vocab[name] = {k: v for k, v in ext.items() if k != "name"}
    return vocab, errors
