#!/usr/bin/env python3
"""Assemble les clips Seedance de 06_clips/ en un bout-a-bout.

Usage : python3 scripts/assemble_film.py
        STORYBOARD_RACINE=<autre-projet> python3 scripts/assemble_film.py

Lit plans.json et 06_clips/ (clips nommes G01.mp4, P01.mp4, ...), coupe
chaque clip a sa duree utile (duree_s), normalise (1920x1080, 30 i/s,
sans son — le son se fait au montage), et concatene dans l'ordre des plans
vers 05_planche/film.mp4.

Un plan sans clip est saute et signale, jamais bloquant.
Necessite ffmpeg. Le film est un artefact derive : ne pas l'editer.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_prompts import CHEMIN_PLANS, RACINE, charger_json  # noqa: E402

DOSSIER_CLIPS = RACINE / "06_clips"
CHEMIN_SORTIE = RACINE / "05_planche" / "film.mp4"

LARGEUR, HAUTEUR, IPS = 1920, 1080, 30


def ffmpeg(arguments):
    resultat = subprocess.run(
        ["ffmpeg", "-v", "error", "-y"] + arguments,
        capture_output=True, text=True,
    )
    if resultat.returncode != 0:
        sys.exit(f"ERREUR ffmpeg :\n{resultat.stderr}")


def main():
    if not shutil.which("ffmpeg"):
        sys.exit("ERREUR : ffmpeg introuvable. L'installer puis relancer.")
    plans = charger_json(CHEMIN_PLANS)

    presents = [p for p in plans if (DOSSIER_CLIPS / f"{p['id']}.mp4").exists()]
    absents = [p["id"] for p in plans if p not in presents]
    if not presents:
        sys.exit(
            f"Aucun clip dans {DOSSIER_CLIPS.relative_to(RACINE)}/ "
            f"(attendus : {plans[0]['id']}.mp4, ...). Rien a assembler."
        )

    with tempfile.TemporaryDirectory() as dossier_temp:
        temp = Path(dossier_temp)
        liste_concat = []
        for plan in presents:
            source = DOSSIER_CLIPS / f"{plan['id']}.mp4"
            normalise = temp / f"{plan['id']}.mp4"
            filtre = (
                f"scale={LARGEUR}:{HAUTEUR}:force_original_aspect_ratio=decrease,"
                f"pad={LARGEUR}:{HAUTEUR}:(ow-iw)/2:(oh-ih)/2,fps={IPS}"
            )
            ffmpeg([
                "-i", str(source), "-t", str(plan["duree_s"]),
                "-vf", filtre, "-an",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                "-pix_fmt", "yuv420p", str(normalise),
            ])
            liste_concat.append(f"file '{normalise}'")
            print(f"  {plan['id']} : {plan['duree_s']} s")

        fichier_liste = temp / "liste.txt"
        fichier_liste.write_text("\n".join(liste_concat), encoding="utf-8")
        CHEMIN_SORTIE.parent.mkdir(parents=True, exist_ok=True)
        ffmpeg([
            "-f", "concat", "-safe", "0", "-i", str(fichier_liste),
            "-c", "copy", str(CHEMIN_SORTIE),
        ])

    duree_totale = sum(p["duree_s"] for p in presents)
    print(f"OK : {CHEMIN_SORTIE.relative_to(RACINE)} — "
          f"{len(presents)} clips, {duree_totale} s")
    if absents:
        print(f"ATTENTION : {len(absents)} plan(s) sans clip, sautes : "
              f"{', '.join(absents)}")


if __name__ == "__main__":
    main()
