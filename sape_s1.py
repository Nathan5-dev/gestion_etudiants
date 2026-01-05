from Analyse_performances_etudiants.gestionnaire_sape import charger_donnees, programme_principale



# point d'entrée du programme
if __name__ == "__main__":

    print("Programme principale en cours... ")

    charger_donnees("donnes.json")

    programme_principale()





