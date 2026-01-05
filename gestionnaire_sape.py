
import json

# Variable globale pour stocker les étudiants
BASE_DONNEES_ETUDIANTS = []

class Etudiant:
    def __init__(self,id,nom,Type,notes):
        self.id=id
        self.nom=nom
        self.Type= Type
        self.notes=notes

    def __str__(self):
        if self.Type == "master":
            return f" EtudiantMaster ({self.id},{self.nom},{self.Type},{self.notes})"
        else:
            return f" Etudiant ({self.id},{self.nom},{self.Type},{self.notes})"

    def calculer_moyenne(self):
        """Calcule la moyenne des notes de l'étudiant"""
        if not self.notes:
            return 0.0
        return sum(note for c, note in self.notes) / len(self.notes)


class EtudiantMaster(Etudiant):

    def calculer_moyenne(self):
        """Pour les masters, la moyenne doit être >= 12 sinon 0"""
        if not self.notes:
            return 0.0
        moyenne = sum(note for c, note in self.notes) / len(self.notes)
        if moyenne >= 12:
            return moyenne
        else:
            return 0.0

def importer_donnees(nom_fichier):
    liste_objet=[]

    with open(nom_fichier,"r",encoding='utf-8') as f:
        liste = json.load(f)
        for etudiant in liste:
            id = etudiant["id"]
            nom = etudiant["nom"]
            Type = etudiant["Type"]
            notes = [tuple(C) for C in etudiant["notes"]]
            if Type == "master":
                liste_objet.append(EtudiantMaster(id,nom,Type,notes))
            else:
                liste_objet.append(Etudiant(id,nom,Type,notes))
    return liste_objet

def exporter_en_json(etudiants :list,nom_fichier):
    liste_etudiants =[]
    for e in etudiants:
        d = {
            'id':e.id,
            'nom':e.nom,
            'Type':e.Type,
            'notes': list(e.notes)
        }
        liste_etudiants.append(d)
    with open(nom_fichier,"w",encoding="utf-8") as f:
        json.dump(liste_etudiants,f,indent=2)


def charger_donnees(nom_fichier):
    """Charge les données et initialise BASE_DONNEES_ETUDIANTS"""
    global BASE_DONNEES_ETUDIANTS
    BASE_DONNEES_ETUDIANTS = importer_donnees(nom_fichier)
    return BASE_DONNEES_ETUDIANTS


#fonction pour afficher toutes les informations d'un etudiant
def trouver_etudiant(ID):
    trouve = False
    for etudiant in BASE_DONNEES_ETUDIANTS:
        if  ID == etudiant.id:
            print(f"|| ID :{etudiant.id} ")
            print(f"|| Type : {etudiant.Type}")
            print(f"|| Nom : {etudiant.nom}")
            print("_" * 32)
            print(f"|{"Cours":^15}|{"note":^15}|")
            print(f"{"-"*32}")
            for n in etudiant.notes:
                print(f"|{n[0]:^15}|{n[1]:^15}|")
            print(f"{"-" * 32}")
            trouve = True
    return  trouve


# fonction pour ajouter une note a un etudiant
def ajouter_note(ID, cours, note):
    for etudiant in BASE_DONNEES_ETUDIANTS:
        if etudiant.id == ID:
            etudiant.notes.append((cours, note))
            print("-"*20,f"\n Note ajoutee avec succès à {etudiant.nom} !")
            return True
    print( "-"*20,f"\n aucun étudiant trouvé avec l'ID {ID} !")


def filtrer_etudiant(seuil):
    print("-" * 34)
    print(f"|{"ID":<5}|{"Noms":^15}|{"Moyennes":^10}|")
    print("-" * 34)
    trouve=False
    for etudiant in BASE_DONNEES_ETUDIANTS:
        moyenne = sum( note for c,note in etudiant.notes)/len(etudiant.notes)
        if moyenne < seuil:
            trouve = True
            print(f"|{etudiant.id:<5}|{etudiant.nom:^15}|{moyenne:^10.2f}|")

    if not trouve:
        print(f"{"Aucun":^34}")
    print("-"*34)

    # programme principal
def programme_principale():
        while True:
            # Menu
            print("\n")
            print("=" * 10, " Menu principal ", "=" * 10, "\n")
            print(" Operation a effectuer parmi ces options : ")
            print("1. Trouver un etudiant par ID. ")
            print("2. Afficher la moyenne d'un etudiant ")
            print("3. Ajouter une note a un etudiant.  ")
            print("4. Filtrer les etudaints")
            print("5. Quitter ")

            try:
                choix = int(input("Choisir : "))
            except Exception as e:
                print(e)
                print("le choix doit etre un  entier !")

            if choix == 1:
                id = input("Entrer l'ID de l'etudiant :")
                if not trouver_etudiant(id):
                    print("Cet etudiant n'existe pas !")

            elif choix == 2:
                ID = input(" Donne l'Id de l'etudiant :")
                trouve = False
                for etudiant in BASE_DONNEES_ETUDIANTS:
                    if etudiant.id == ID:
                        trouve = True
                        print(f"|| Etudiant : {etudiant.nom}")
                        print(f"|| Moyenne : {etudiant.calculer_moyenne():.2f}")
                if not trouve:
                    print(f"Aucun étudiant trouvé avec l'ID {ID}")
            elif choix == 3:
                print(" Donnez les informations :")
                while True:
                    id = input("ID de l'etudiant:")
                    cour = input("nom du cours :")
                    try:
                        note = float(input(" Note obtenu au cours :"))
                    except Exception as e:
                        print("-" * 20, "\n la note doit être un nombre !")
                        print(e)
                        break

                    if note < 0 or note > 20:
                        print("-" * 20, "\n la note doit être comprise entre 0 et 20. !")
                        break

                    ajouter_note(id, cour, note)
                    break
            elif choix == 4:
                print("-" * 20, "\n Afficher les étudiants dont la moyenne est en dessous du Seuil")
                while True:
                    try:
                        Seuil = int(input("Seuil :"))
                    except Exception as e:
                        print("-" * 20, "\n le seuil doit être un nombre !")
                        print(e)
                        break
                    if Seuil < 1 or Seuil > 20:
                        print("-" * 20, "\n le seuil doit être compris entre 1 et 20. !")
                        break
                    filtrer_etudiant(Seuil)
                    break

            elif choix == 5:
                break
            else:
                print("Choix invalide, Veillez réessayer !")

