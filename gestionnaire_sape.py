
class Etudiant:
    def __init__(self,id,nom,notes):
        self.id=id
        self.nom=nom
        self.notes=notes

    def calculer_moyenne(self, notes:list):
        moyenne = sum(note for cours,note in notes)/len(notes)
        return moyenne

    def __str__(self,id, nom ,notes: list):
        print("-" * 34)
        print(f"|{"ID":<5}|{"Noms":^15}|{"Moyennes":^10}|")
        print("-" * 34)
        self.moyenne = sum(note for cours,note in notes)
        print(f"|{self.notes:<5}|{self.nom:^15}|{self.moyenne :^10.2f}|")
        print("-" * 34)


BASE_DONNEES_ETUDIANTS = [
    Etudiant("E001","Nathan cirhuza",[
             ("Algo", 18),
             ("Anglais", 17),
             ("Algebre", 19)
         ]),
    Etudiant("E002", "Ghislain cirhuza", [
        ("Algo", 14),
        ("Anglais", 15),
        ("Algebre", 10)
    ]),
    Etudiant("E003", "Joseph", [
        ("Algo", 12),
        ("Anglais", 10),
        ("Algebre", 9)
    ]),
    Etudiant("E004", "Matin", [
        ("Algo", 10),
        ("Anglais", 15),
        ("Algebre", 13)
    ]),
    Etudiant("E005", "Jean", [
        ("Algo", 17),
        ("Anglais", 11),
        ("Algebre", 12)
    ])

]


#fonction pour afficher toutes les informations d'un etudiant
def trouver_etudiant(ID):
    trouve = False
    for etudiant in BASE_DONNEES_ETUDIANTS:
        if  ID == etudiant.id:
            print(f"|| ID :{etudiant.id} ")
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
                for etudiant in BASE_DONNEES_ETUDIANTS:
                    if etudiant.id == ID:
                        print(f"|| Etudiant : {etudiant.nom}")
                        print(f"|| Moyenne : {etudiant.calculer_moyenne(etudiant.notes)}")
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

