#!/usr/bin/env python3
"""Genere 03_prompts/prompts.md a partir de 01_bible/bible.json et
02_decoupage/plans.json.

Usage : python3 scripts/build_prompts.py

Le fichier produit est un artefact derive : ne jamais l'editer a la main.
Pour corriger un prompt, corriger bible.json ou plans.json et relancer.
"""

import json
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
CHEMIN_BIBLE = RACINE / "01_bible" / "bible.json"
CHEMIN_PLANS = RACINE / "02_decoupage" / "plans.json"
CHEMIN_SORTIE = RACINE / "03_prompts" / "prompts.md"

STYLIZE_MAX = 250

CHAMPS_PLAN = [
    "id", "duree_s", "valeur_plan", "sujet", "action", "lieu",
    "lumiere", "focale", "personnage", "personnage_id", "voix_off",
]


def charger_json(chemin):
    if not chemin.exists():
        sys.exit(f"ERREUR : fichier manquant : {chemin}")
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def valider_plans(plans):
    """Verifie le schema et la contrainte de rythme.

    Contrainte de rythme : jamais trois valeurs de plan identiques
    consecutives.
    """
    erreurs = []
    for i, plan in enumerate(plans):
        manquants = [c for c in CHAMPS_PLAN if c not in plan]
        if manquants:
            erreurs.append(f"plan {plan.get('id', i)} : champs manquants {manquants}")
        if plan.get("personnage") and not plan.get("personnage_id"):
            erreurs.append(f"plan {plan.get('id', i)} : personnage=true mais personnage_id vide")
    for i in range(len(plans) - 2):
        v = plans[i]["valeur_plan"]
        if v == plans[i + 1]["valeur_plan"] == plans[i + 2]["valeur_plan"]:
            erreurs.append(
                f"rythme : trois '{v}' consecutifs a partir de {plans[i]['id']}"
            )
    if erreurs:
        sys.exit("ERREUR de validation :\n  - " + "\n  - ".join(erreurs))


def trouver_personnage(bible, personnage_id):
    for perso in bible["personnages"]:
        if perso["id"] == personnage_id:
            return perso
    sys.exit(f"ERREUR : personnage_id '{personnage_id}' absent de bible.json")


def parametres_modele(plan, bible):
    """Regle d'affectation du modele (etat Midjourney juillet 2026).

    --oref (coherence de personnage) n'existe qu'en V7. Donc :
      plan avec personnage -> V7  + --oref <url> --ow <ow>
      plan sans personnage -> V8.1 + --hd
    """
    if plan["personnage"]:
        perso = trouver_personnage(bible, plan["personnage_id"])
        return f"--v 7 --oref {perso['oref_url']} --ow {perso['ow']}"
    return "--v 8.1 --hd"


def construire_prompt(plan, bible):
    """Ordre impose : sujet -> action -> environnement -> lumiere -> parametres.

    Aucun texte incruste dans l'image : les titres sont ajoutes en post.
    """
    stylize = min(int(bible["stylize"]), STYLIZE_MAX)
    description = ", ".join([
        plan["sujet"],
        plan["action"],
        plan["lieu"],
        plan["lumiere"],
        f"objectif {plan['focale']}",
    ])
    parametres = " ".join([
        f"--ar {bible['ratio']}",
        f"--sref {bible['sref']}",
        f"--s {stylize}",
        parametres_modele(plan, bible),
    ])
    return f"{description} {parametres}"


def avertissements(bible):
    """Liste les valeurs encore au placeholder A_CREER."""
    avert = []
    if bible["sref"] == "A_CREER":
        avert.append("bible.json : sref = A_CREER (creer le moodboard, voir bible.md)")
    for perso in bible["personnages"]:
        if perso["oref_url"] == "A_CREER":
            avert.append(
                f"bible.json : oref_url du personnage '{perso['id']}' = A_CREER "
                "(generer le portrait de reference, voir bible.md)"
            )
    return avert


def main():
    bible = charger_json(CHEMIN_BIBLE)
    plans = charger_json(CHEMIN_PLANS)
    valider_plans(plans)

    lignes = [
        "# Prompts Midjourney",
        "",
        "GENERE par scripts/build_prompts.py — ne pas editer a la main.",
        "Pour corriger un prompt : corriger bible.json ou plans.json, relancer.",
        "",
        f"Ratio {bible['ratio']} — sref {bible['sref']} — "
        f"stylize {min(int(bible['stylize']), STYLIZE_MAX)}",
        "",
    ]

    for plan in plans:
        lignes.append(
            f"## {plan['id']} — {plan['valeur_plan']} — {plan['duree_s']} s"
        )
        lignes.append("")
        lignes.append("```")
        lignes.append(construire_prompt(plan, bible))
        lignes.append("```")
        lignes.append("")
        if plan["voix_off"]:
            lignes.append(f"Voix off : {plan['voix_off']}")
            lignes.append("")
        lignes.append(f"Image attendue : 04_assets/{plan['id']}.png")
        lignes.append("")

    CHEMIN_SORTIE.parent.mkdir(parents=True, exist_ok=True)
    CHEMIN_SORTIE.write_text("\n".join(lignes), encoding="utf-8")
    print(f"OK : {len(plans)} prompts ecrits dans {CHEMIN_SORTIE.relative_to(RACINE)}")

    for a in avertissements(bible):
        print(f"ATTENTION : {a}")


if __name__ == "__main__":
    main()
