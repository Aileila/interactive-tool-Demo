#!/usr/bin/env python3
"""Genere 03_prompts/animation.md : le document d'execution Seedance.

Usage : python3 scripts/build_animation.py
        STORYBOARD_RACINE=<autre-projet> python3 scripts/build_animation.py

Lit bible.json (bloc animation), plans.json (champs mouvement / camera) et
l'etat de 04_assets/ (les images sont les premieres frames). Un plan sans
image est liste comme non animable, sans bloquer les autres.

Principe : le prompt d'animation ne redecrit pas l'image (Seedance la voit),
il decrit le temps — ce qui bouge, ce que fait la camera, a quel tempo.
Le fichier produit est un artefact derive : ne jamais l'editer a la main.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_prompts import (  # noqa: E402
    CHEMIN_BIBLE, CHEMIN_PLANS, RACINE,
    charger_json, valider_plans,
)

CHEMIN_SORTIE = RACINE / "03_prompts" / "animation.md"
DOSSIER_ASSETS = RACINE / "04_assets"
DOSSIER_CLIPS = RACINE / "06_clips"

CHAMPS_ANIMATION = ["mouvement", "camera"]
CHAMPS_ANIMATION_EN = ["mouvement_en", "camera_en"]


def valider_animation(bible, plans):
    erreurs = []
    if "animation" not in bible:
        erreurs.append("bible.json : bloc 'animation' manquant")
    else:
        for cle in ["modele", "resolution", "paliers_generation_s",
                    "style", "style_en", "contraintes"]:
            if cle not in bible["animation"]:
                erreurs.append(f"bible.json : animation.{cle} manquant")
    for plan in plans:
        manquants = [c for c in CHAMPS_ANIMATION if not plan.get(c)]
        if manquants:
            erreurs.append(f"plan {plan['id']} : champs manquants {manquants}")
        presents_en = [c for c in CHAMPS_ANIMATION_EN if plan.get(c)]
        if presents_en and len(presents_en) != len(CHAMPS_ANIMATION_EN):
            erreurs.append(
                f"plan {plan['id']} : version anglaise d'animation incomplete, "
                f"il faut les deux champs {CHAMPS_ANIMATION_EN}"
            )
    if erreurs:
        sys.exit("ERREUR de validation animation :\n  - " + "\n  - ".join(erreurs))


def construire_prompt_animation(plan, bible, langue=None):
    """Mouvement -> camera -> style global. Pas de description d'image."""
    animation = bible["animation"]
    if langue is None:
        langue = "en" if all(plan.get(c) for c in CHAMPS_ANIMATION_EN) else "fr"
    if langue == "en":
        return (f"{plan['mouvement_en']}. Camera: {plan['camera_en']}. "
                f"{animation['style_en']}.")
    return (f"{plan['mouvement']}. Caméra : {plan['camera']}. "
            f"{animation['style']}.")


def construire_prompt_complet(plan, bible):
    """Variante text-to-video : prompt autonome, sans image de depart.

    A n'utiliser qu'en secours (plan sans personnage, ou i2v qui morphe) :
    sans premiere frame, Seedance ne garantit pas l'identite visuelle
    d'un plan a l'autre.
    """
    animation = bible["animation"]
    if all(plan.get(c) for c in ["sujet_en", "action_en", "lieu_en",
                                 "lumiere_en", "mouvement_en", "camera_en"]):
        description = ", ".join([
            plan["sujet_en"], plan["action_en"],
            plan["lieu_en"], plan["lumiere_en"],
        ])
        return (f"{description}. {plan['mouvement_en']}. "
                f"Camera: {plan['camera_en']}. {animation['style_en']}.")
    description = ", ".join([
        plan["sujet"], plan["action"], plan["lieu"], plan["lumiere"],
    ])
    return (f"{description}. {plan['mouvement']}. "
            f"Caméra : {plan['camera']}. {animation['style']}.")


def palier_generation(duree_s, paliers):
    """Plus petit palier Seedance couvrant la duree utile du plan."""
    for p in sorted(paliers):
        if p >= duree_s:
            return p
    return max(paliers)


def main():
    bible = charger_json(CHEMIN_BIBLE)
    plans = charger_json(CHEMIN_PLANS)
    valider_plans(plans)
    valider_animation(bible, plans)
    animation = bible["animation"]

    lignes = [
        "# Document d'exécution animation — Seedance",
        "",
        "GENERE par scripts/build_animation.py — ne pas editer a la main.",
        "Pour corriger : bible.json (bloc animation) ou plans.json, relancer.",
        "",
        f"Modèle : {animation['modele']} — mode image-to-video — "
        f"résolution {animation['resolution']} — ratio {bible['ratio']}",
        "",
        "Contraintes globales (à respecter sur chaque plan) :",
        "",
    ]
    for contrainte in animation["contraintes"]:
        lignes.append(f"- {contrainte}")
    lignes.append("")

    sans_image = []
    for plan in plans:
        image = DOSSIER_ASSETS / f"{plan['id']}.png"
        image_ok = image.exists()
        if not image_ok:
            sans_image.append(plan["id"])
        generation = palier_generation(plan["duree_s"], animation["paliers_generation_s"])

        lignes.append(f"## {plan['id']} — {plan['valeur_plan']} — "
                      f"utile {plan['duree_s']} s / générer {generation} s")
        lignes.append("")
        lignes.append(
            f"Première frame : 04_assets/{plan['id']}.png"
            + ("" if image_ok else "  ⚠ IMAGE MANQUANTE — générer l'image d'abord")
        )
        lignes.append("")
        lignes.append("```")
        lignes.append(construire_prompt_animation(plan, bible))
        lignes.append("```")
        lignes.append("")
        lignes.append(
            "Variante text-to-video (secours : plan sans personnage, ou "
            "i2v qui morphe — identite visuelle non garantie) :"
        )
        lignes.append("")
        lignes.append("```")
        lignes.append(construire_prompt_complet(plan, bible))
        lignes.append("```")
        lignes.append("")
        if plan["voix_off"]:
            lignes.append(f"Bande son en regard : {plan['voix_off']}")
            lignes.append("")
        lignes.append(f"Clip attendu : 06_clips/{plan['id']}.mp4")
        lignes.append("")

    CHEMIN_SORTIE.parent.mkdir(parents=True, exist_ok=True)
    DOSSIER_CLIPS.mkdir(parents=True, exist_ok=True)
    CHEMIN_SORTIE.write_text("\n".join(lignes), encoding="utf-8")
    print(f"OK : {len(plans)} fiches d'animation dans "
          f"{CHEMIN_SORTIE.relative_to(RACINE)}")
    if sans_image:
        print(f"ATTENTION : {len(sans_image)} plan(s) sans premiere frame "
              f"dans 04_assets/ : {', '.join(sans_image)}")


if __name__ == "__main__":
    main()
