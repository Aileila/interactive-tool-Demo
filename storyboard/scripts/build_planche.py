#!/usr/bin/env python3
"""Genere 05_planche/storyboard.pdf a partir de 02_decoupage/plans.json et
des images deposees dans 04_assets/ (P01.png, P02.png, ...).

Usage : python3 scripts/build_planche.py

Un plan sans image est signale (case grise dans le PDF + liste en console)
mais ne bloque jamais la generation.
Le PDF est un artefact derive : ne jamais l'editer a la main.
"""

import io
import json
import os
import sys
from pathlib import Path

from PIL import Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

RACINE = (
    Path(os.environ["STORYBOARD_RACINE"]).resolve()
    if os.environ.get("STORYBOARD_RACINE")
    else Path(__file__).resolve().parent.parent
)
CHEMIN_PLANS = RACINE / "02_decoupage" / "plans.json"
DOSSIER_ASSETS = RACINE / "04_assets"
CHEMIN_SORTIE = RACINE / "05_planche" / "storyboard.pdf"

PAGE = landscape(A4)
MARGE = 12 * mm
COLONNES = 3
LIGNES = 2
GOUTTIERE = 8 * mm
RATIO_IMAGE = 16 / 9
HAUTEUR_LEGENDE = 22 * mm
# Les vignettes sont recompressees a l'embarquement pour garder un PDF
# leger ; les originaux de 04_assets/ ne sont jamais modifies.
LARGEUR_VIGNETTE_PX = 1200
QUALITE_JPEG = 82


def vignette_compressee(chemin_image):
    image = Image.open(chemin_image).convert("RGB")
    if image.width > LARGEUR_VIGNETTE_PX:
        hauteur = round(image.height * LARGEUR_VIGNETTE_PX / image.width)
        image = image.resize((LARGEUR_VIGNETTE_PX, hauteur))
    tampon = io.BytesIO()
    image.save(tampon, "JPEG", quality=QUALITE_JPEG)
    tampon.seek(0)
    return tampon


def charger_plans():
    if not CHEMIN_PLANS.exists():
        sys.exit(f"ERREUR : fichier manquant : {CHEMIN_PLANS}")
    with open(CHEMIN_PLANS, encoding="utf-8") as f:
        return json.load(f)


def couper_texte(pdf, texte, police, taille, largeur_max):
    """Coupe un texte en lignes qui tiennent dans largeur_max."""
    lignes = []
    courante = ""
    for mot in texte.split():
        essai = f"{courante} {mot}".strip()
        if pdf.stringWidth(essai, police, taille) <= largeur_max:
            courante = essai
        else:
            if courante:
                lignes.append(courante)
            courante = mot
    if courante:
        lignes.append(courante)
    return lignes


def dessiner_vignette(pdf, plan, x, y, largeur):
    """Dessine une case : image (ou placeholder) + legende. Renvoie True si
    l'image existait."""
    hauteur_image = largeur / RATIO_IMAGE
    chemin_image = DOSSIER_ASSETS / f"{plan['id']}.png"
    image_presente = chemin_image.exists()

    y_image = y - hauteur_image
    if image_presente:
        pdf.drawImage(
            ImageReader(vignette_compressee(chemin_image)), x, y_image,
            width=largeur, height=hauteur_image,
            preserveAspectRatio=True, anchor="c",
        )
        pdf.setStrokeColorRGB(0.2, 0.2, 0.2)
        pdf.rect(x, y_image, largeur, hauteur_image)
    else:
        pdf.setFillColorRGB(0.9, 0.9, 0.9)
        pdf.rect(x, y_image, largeur, hauteur_image, fill=1)
        pdf.setFillColorRGB(0.4, 0.4, 0.4)
        pdf.setFont("Helvetica-Oblique", 9)
        pdf.drawCentredString(
            x + largeur / 2, y_image + hauteur_image / 2,
            f"image manquante : 04_assets/{plan['id']}.png",
        )

    y_texte = y_image - 5 * mm
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(
        x, y_texte,
        f"{plan['id']} — {plan['duree_s']} s — {plan['valeur_plan']}",
    )
    if plan["voix_off"]:
        pdf.setFont("Helvetica-Oblique", 8)
        y_ligne = y_texte - 4 * mm
        for ligne in couper_texte(
            pdf, plan["voix_off"], "Helvetica-Oblique", 8, largeur
        )[:3]:
            pdf.drawString(x, y_ligne, ligne)
            y_ligne -= 3.5 * mm

    return image_presente


def main():
    plans = charger_plans()
    largeur_page, hauteur_page = PAGE
    largeur_case = (largeur_page - 2 * MARGE - (COLONNES - 1) * GOUTTIERE) / COLONNES
    hauteur_case = largeur_case / RATIO_IMAGE + HAUTEUR_LEGENDE

    CHEMIN_SORTIE.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(CHEMIN_SORTIE), pagesize=PAGE)
    pdf.setTitle("Storyboard")

    manquantes = []
    par_page = COLONNES * LIGNES
    for i, plan in enumerate(plans):
        position = i % par_page
        if position == 0 and i > 0:
            pdf.showPage()
        colonne = position % COLONNES
        ligne = position // COLONNES
        x = MARGE + colonne * (largeur_case + GOUTTIERE)
        y = hauteur_page - MARGE - ligne * (hauteur_case + GOUTTIERE)
        if not dessiner_vignette(pdf, plan, x, y, largeur_case):
            manquantes.append(plan["id"])

    pdf.save()
    print(f"OK : {CHEMIN_SORTIE.relative_to(RACINE)} ({len(plans)} plans)")
    if manquantes:
        print(
            f"ATTENTION : {len(manquantes)} image(s) manquante(s) dans "
            f"04_assets/ : {', '.join(manquantes)}"
        )


if __name__ == "__main__":
    main()
