import re
import csv

# Lecture du fichier
def lire_fichier(fichier):
    try:
        with open(fichier, 'r', encoding='utf-8') as file:
            lignes = file.readlines()
            print(f"{len(lignes)} lignes ont été lues du fichier '{fichier}'.")
            return lignes
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{fichier}' est introuvable.")
        return []
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return []

# Extraction des données pertinentes
def extraire_donnees(lignes):
    donnees = []
    # Motif regex pour capturer les informations pertinentes
    pattern = re.compile(r"(\d{2}:\d{2}:\d{2}\.\d+)\sIP\s([\w\d\-\.]+)\s>\s([\d\.]+)\.(\d+):\sFlags\s\[(.*?)\].*length\s(\d+)")
    print("Extraction des données en cours...")

    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne.startswith("IP") and not ligne.startswith("11"):  # Ignore les lignes non pertinentes
            continue

        match = pattern.search(ligne)
        if match:
            donnees.append([
                match.group(1),  # Timestamp
                match.group(2),  # IP Source
                match.group(3),  # IP Destination
                match.group(4),  # Port Destination
                match.group(5),  # Flags
                match.group(6)   # Length
            ])
    print(f"{len(donnees)} correspondances trouvées.")
    return donnees

# Écriture dans un fichier CSV
def ecrire_csv(donnees, nom_csv):
    try:
        with open(nom_csv, "w", newline="") as fichier_csv:
            writer = csv.writer(fichier_csv)
            writer.writerow(["Timestamp", "IP Source", "IP Destination", "Port Destination", "Flags", "Length"])
            writer.writerows(donnees)
        print(f"Fichier CSV généré avec succès : {nom_csv} ({len(donnees)} lignes).")
    except PermissionError:
        print(f"Erreur : Impossible d'écrire dans le fichier '{nom_csv}'. Assurez-vous qu'il n'est pas ouvert.")
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier CSV : {e}")

# Génération d'un fichier Markdown
def generer_markdown(donnees, fichier_md):
    try:
        markdown = "# Rapport des Paquets Réseau\n\n"
        markdown += "| Timestamp       | IP Source      | IP Destination   | Port Destination | Flags | Length |\n"
        markdown += "|-----------------|----------------|------------------|------------------|-------|--------|\n"

        for donnee in donnees:
            markdown += f"| {donnee[0]} | {donnee[1]} | {donnee[2]} | {donnee[3]} | {donnee[4]} | {donnee[5]} |\n"

        with open(fichier_md, "w", encoding="utf-8") as fichier:
            fichier.write(markdown)
        print(f"Fichier Markdown généré avec succès : {fichier_md} ({len(donnees)} lignes).")
    except Exception as e:
        print(f"Erreur lors de la génération du fichier Markdown : {e}")

# Génération d'un fichier HTML
def generer_html(donnees, fichier_html):
    try:
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Rapport des Paquets Réseau</title>
            <style>
                table {
                    border-collapse: collapse;
                    width: 100%;
                }
                th, td {
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
            <h1>Rapport des Paquets Réseau</h1>
            <table>
                <tr>
                    <th>Timestamp</th>
                    <th>IP Source</th>
                    <th>IP Destination</th>
                    <th>Port Destination</th>
                    <th>Flags</th>
                    <th>Length</th>
                </tr>
        """
        for donnee in donnees:
            html += f"""
                <tr>
                    <td>{donnee[0]}</td>
                    <td>{donnee[1]}</td>
                    <td>{donnee[2]}</td>
                    <td>{donnee[3]}</td>
                    <td>{donnee[4]}</td>
                    <td>{donnee[5]}</td>
                </tr>
            """
        html += """
            </table>
        </body>
        </html>
        """
        with open(fichier_html, "w", encoding="utf-8") as fichier:
            fichier.write(html)
        print(f"Fichier HTML généré avec succès : {fichier_html}")
    except Exception as e:
        print(f"Erreur lors de la génération du fichier HTML : {e}")

# Programme principal
if __name__ == "__main__":
    nom_fichier = "DumpFile.txt"  # Nom du fichier d'entrée
    lignes = lire_fichier(nom_fichier)

    if not lignes:
        print("Aucune ligne lue. Vérifiez le fichier.")
    else:
        donnees = extraire_donnees(lignes)

        if donnees:
            # Génération des fichiers CSV, Markdown et HTML
            ecrire_csv(donnees, "resultats.csv")
            generer_markdown(donnees, "rapport_reseau.md")
            generer_html(donnees, "rapport_reseau.html")
        else:
            print("Aucune donnée extraite. Assurez-vous que le fichier contient des lignes pertinentes.")
