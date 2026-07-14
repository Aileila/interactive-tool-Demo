#!/usr/bin/env python3
"""Pousse les plans et leurs prompts vers les bases Notion de suivi.

Usage : NOTION_TOKEN=... python3 scripts/sync_notion.py [--dry-run]

Lit bible.json, plans.json, 00_histoire/histoire.md (pour le nom du projet)
et notion.json (identifiants des bases, crees une fois pour toutes).

Idempotent : relancer met a jour les lignes existantes sans les dupliquer.
Champs pilotes par le depot (ecrases a chaque sync) : prompt, valeur de plan,
duree, modele, personnage, voix off, ordre.
Champs pilotes par l'humain dans Notion (jamais touches) : notes, image
choisie, et le statut — sauf passage automatique a "integre" quand le PNG
du plan est present dans 04_assets/ et que le statut n'est pas "a refaire".

Necessite une integration Notion (https://www.notion.so/my-integrations)
ayant acces a la page racine, et son jeton dans NOTION_TOKEN.
"""

import json
import os
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_prompts import (  # noqa: E402
    CHEMIN_BIBLE, CHEMIN_PLANS, RACINE, STYLIZE_MAX,
    charger_json, construire_prompt, valider_plans,
)
from build_animation import construire_prompt_animation  # noqa: E402

CHEMIN_NOTION = RACINE / "notion.json"
CHEMIN_HISTOIRE = RACINE / "00_histoire" / "histoire.md"
DOSSIER_ASSETS = RACINE / "04_assets"

API = "https://api.notion.com/v1"
VERSION_API = "2025-09-03"


def appel_api(token, methode, chemin, corps=None):
    requete = urllib.request.Request(
        f"{API}{chemin}",
        method=methode,
        data=json.dumps(corps).encode("utf-8") if corps is not None else None,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": VERSION_API,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(requete) as reponse:
            return json.load(reponse)
    except urllib.error.HTTPError as erreur:
        sys.exit(
            f"ERREUR API Notion ({erreur.code}) sur {methode} {chemin} :\n"
            f"{erreur.read().decode('utf-8')}"
        )


def texte(valeur):
    return {"rich_text": [{"text": {"content": valeur}}] if valeur else []}


def titre(valeur):
    return {"title": [{"text": {"content": valeur}}]}


def lire_titre(page, nom_propriete):
    fragments = page["properties"][nom_propriete]["title"]
    return "".join(f["plain_text"] for f in fragments)


def nom_du_projet():
    """Premier titre de niveau 1 de l'histoire."""
    for ligne in CHEMIN_HISTOIRE.read_text(encoding="utf-8").splitlines():
        if ligne.startswith("# "):
            return ligne[2:].strip()
    sys.exit(f"ERREUR : aucun titre '# ' dans {CHEMIN_HISTOIRE}")


def lignes_a_pousser():
    """Construit les lignes plan a synchroniser, sans rien appeler."""
    bible = charger_json(CHEMIN_BIBLE)
    plans = charger_json(CHEMIN_PLANS)
    valider_plans(plans)
    lignes = []
    for ordre, plan in enumerate(plans, start=1):
        lignes.append({
            "plan": plan["id"],
            "ordre": ordre,
            "valeur_plan": plan["valeur_plan"],
            "duree_s": plan["duree_s"],
            "modele": "V7 + oref" if plan["personnage"] else "V8.1 + hd",
            "personnage": plan["personnage_id"] or "",
            "prompt": construire_prompt(plan, bible),
            "prompt_fr": construire_prompt(plan, bible, langue="fr"),
            "prompt_animation": construire_prompt_animation(plan, bible),
            "voix_off": plan["voix_off"],
            "png_present": (DOSSIER_ASSETS / f"{plan['id']}.png").exists(),
        })
    return bible, plans, lignes


def trouver_ou_creer_projet(token, config, bible, plans, nom):
    reponse = appel_api(
        token, "POST", f"/data_sources/{config['data_source_projets']}/query",
        {"filter": {"property": "Nom", "title": {"equals": nom}}},
    )
    duree_totale = sum(p["duree_s"] for p in plans)
    proprietes = {
        "Nom": titre(nom),
        "Ratio": texte(bible["ratio"]),
        "Sref": texte(bible["sref"]),
        "Nb plans": {"number": len(plans)},
        "Duree totale (s)": {"number": duree_totale},
    }
    if reponse["results"]:
        page = reponse["results"][0]
        appel_api(token, "PATCH", f"/pages/{page['id']}", {"properties": proprietes})
        return page["id"], "mis a jour"
    proprietes["Statut"] = {"select": {"name": "generation images"}}
    page = appel_api(token, "POST", "/pages", {
        "parent": {"type": "data_source_id",
                   "data_source_id": config["data_source_projets"]},
        "properties": proprietes,
    })
    return page["id"], "cree"


def plans_existants(token, config, id_projet):
    """Titre -> (id de page, statut) des plans deja lies a ce projet."""
    existants = {}
    curseur = None
    while True:
        corps = {"filter": {"property": "Projet",
                            "relation": {"contains": id_projet}}}
        if curseur:
            corps["start_cursor"] = curseur
        reponse = appel_api(
            token, "POST",
            f"/data_sources/{config['data_source_plans']}/query", corps,
        )
        for page in reponse["results"]:
            statut = page["properties"]["Statut"]["select"]
            existants[lire_titre(page, "Plan")] = (
                page["id"], statut["name"] if statut else None,
            )
        if not reponse.get("has_more"):
            return existants
        curseur = reponse["next_cursor"]


def pousser_plan(token, config, id_projet, ligne, existants):
    proprietes = {
        "Plan": titre(ligne["plan"]),
        "Ordre": {"number": ligne["ordre"]},
        "Valeur de plan": {"select": {"name": ligne["valeur_plan"]}},
        "Duree (s)": {"number": ligne["duree_s"]},
        "Modele": {"select": {"name": ligne["modele"]}},
        "Personnage": texte(ligne["personnage"]),
        "Prompt": texte(ligne["prompt"]),
        "Prompt FR": texte(ligne["prompt_fr"]),
        "Prompt animation": texte(ligne["prompt_animation"]),
        "Voix off": texte(ligne["voix_off"]),
        "Projet": {"relation": [{"id": id_projet}]},
    }
    if ligne["plan"] in existants:
        id_page, statut = existants[ligne["plan"]]
        if ligne["png_present"] and statut != "a refaire":
            proprietes["Statut"] = {"select": {"name": "integre"}}
        appel_api(token, "PATCH", f"/pages/{id_page}", {"properties": proprietes})
        return "mis a jour"
    proprietes["Statut"] = {"select": {
        "name": "integre" if ligne["png_present"] else "a generer"}}
    appel_api(token, "POST", "/pages", {
        "parent": {"type": "data_source_id",
                   "data_source_id": config["data_source_plans"]},
        "properties": proprietes,
    })
    return "cree"


def main():
    dry_run = "--dry-run" in sys.argv
    bible, plans, lignes = lignes_a_pousser()
    nom = nom_du_projet()

    if dry_run:
        print(f"DRY RUN : projet '{nom}', {len(lignes)} plans a synchroniser")
        for ligne in lignes:
            etat_png = "png present" if ligne["png_present"] else "png absent"
            print(f"  {ligne['plan']} — {ligne['valeur_plan']} — "
                  f"{ligne['modele']} — {etat_png}")
        return

    token = os.environ.get("NOTION_TOKEN")
    if not token:
        sys.exit(
            "ERREUR : NOTION_TOKEN absent de l'environnement.\n"
            "Creer une integration sur https://www.notion.so/my-integrations, "
            "lui donner acces a la page racine du suivi, puis :\n"
            "  NOTION_TOKEN=... python3 scripts/sync_notion.py"
        )
    config = charger_json(CHEMIN_NOTION)

    id_projet, action = trouver_ou_creer_projet(token, config, bible, plans, nom)
    print(f"Projet '{nom}' : {action}")
    existants = plans_existants(token, config, id_projet)
    for ligne in lignes:
        action = pousser_plan(token, config, id_projet, ligne, existants)
        print(f"  {ligne['plan']} : {action}")
    print(f"OK : {len(lignes)} plans synchronises vers Notion")


if __name__ == "__main__":
    main()
