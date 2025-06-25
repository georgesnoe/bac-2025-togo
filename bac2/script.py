import requests
import threading
import sys
import json
from io import SEEK_SET
from typing import Any, List


# Nombre de threads par défaut
# Pour accélerer le processus
TOTAL_THREADS = int(sys.argv[1]) if len(sys.argv) > 2 else 10

# Limite des erreurs
ERROR_LIMIT = 1000


def get_data(table_number: int) -> Any:
    """
        Cette fonction récupère les informations
        de l'élève avec le {numero_de_table} et
        les renvoie sous le format json
    """

    r = requests.get(f"https://example.com/bac2025?n={table_number}")
    if r.ok:
        return json.loads(r.text)
    return {}


class Tache(threading.Thread):
    def __init__(self, id: int) -> None:
        """
            Constructeur de la classe
            Il récupère un identifiant qu'il utilisera
            pour la suite des opérations
        """

        super().__init__()
        self.id = id
        self.errors = 0
        # Nom du fichier csv
        self.nom_fichier_csv = f"resultats_bac_2025_partie_{id}"

    def run(self) -> None:
        """
            Si le nombre d'erreurs atteint 1000,
            je suppose que la limite a été atteinte
        """

        while self.errors < ERROR_LIMIT:

            data = get_data(self.id)

            # Si le résultat n'existe pas
            # c'est une erreur
            if not data:
                self.errors += TOTAL_THREADS
            # Au cas contraire, on réinitialise le compteur
            else:
                self.errors = 0

    def write_to_file(self, data: List[str]) -> None:
        """
            Ecrire les données de l'étudiant dans
            un fichier csv dont le nom
            est sous le format
            {resultats_bac_2025_partie_{id}}
        """

        with open(self.nom_fichier_csv, "a+") as file:
            # Ecrire les données suivi d'une nouvelle ligne
            for value in data:
                file.write(f"{value},")

            # Remplacer la dernière virgule par un
            # caractère de nouvelle ligne
            file.seek(file.tell() - 1, SEEK_SET)
            file.write("\n")


if __name__ == "__main__":
    """
        Fonction principale
    """

    # Initialiser tous les threads
    for i in range(TOTAL_THREADS):
        # Débute à partir de 1
        thread = Tache(i + 1)
        thread.start()
        thread.join()  # Attendre la fin du thread avant de fermer le programme

    # Ce code ne sera jamais exécuté tant que tous les threads
    # n'auront pas fini leur exécution
    sys.exit(0)
