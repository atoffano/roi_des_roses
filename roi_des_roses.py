import random    

### Initialisation du jeu ###
def init_jeu(nb_lignes, nb_colonnes):

    # Initialisation des variables
    plateau = [["." for count in range(nb_colonnes)] for count in range(nb_lignes)]
    l_roi = nb_lignes//2
    c_roi = nb_colonnes//2
    pioche = ["N1","NE1","E1","SE1","S1","SO1","O1","NO1","N2","NE2","E2","SE2","S2","SO2","O2","NO2","N3","NE3","E3","SE3","S3","SO3","O3","NO3"]
    main_b = []
    main_r = []
    defausse = []

    random.shuffle(pioche) # On mélange la pioche
    main_r = pioche[0:5] # On distribue les 5 premières cartes au joueur rouge..
    main_b = pioche[5:10] # ..Et les 5 suivantes au joueur blanc
    del pioche[0:10] # On supprime les cartes piochées de la pioche

    return (plateau, l_roi, c_roi, main_r, main_b, pioche, defausse)


### Affichage de l'état du jeu ###

# Affiche la main du joueur de la couleur renseignée
def afficher_main(couleur, main):
    print(f"{couleur} : ", end="")
    for carte in main:
        print(f"{carte} ", end="")
    print ("")


def afficher_jeu(plateau, l_roi, c_roi, main_r, main_b):
    afficher_main("Rouge", main_r)
    afficher_main("Blanc", main_b)

    for i in range(len(plateau)):
        print("-"*46)
        for j in range(len(plateau[0])) :
            car = ""
            if l_roi == i and c_roi == j:
                car = "X"
            else:
                car = " "
            if plateau[i][j] == "B" :
                car = car + "B"
            elif plateau[i][j] == "R" :
                car = car + "R"
            else:
                car = car + " "
            print(f"| {car} ",end="")
        print ("|")
    print("-"*46)

#modif *46

plt, lr, cr, mr, mb, pioche, defausse = init_jeu(9, 9)
afficher_jeu(plt,lr,cr,mr,mb)




### Mouvement du roi possible ###
#def mouvement_possible(plateau, l_roi, c_roi, carte):
#    if plateau[l_roi][c_roi] + 


### Main jouable ###
def main_jouable(plateau, l_roi, c_roi, main):
    pass


### Demande une action à un joueur ###
def demande_action(couleur, plateau, l_roi, c_roi, main):
    pass


### Bouge le roi ###
def bouge_le_roi(plateau, l_roi, c_roi, main_r, main_b, defausse, carte, couleur):
    pass


### Definition des territoires ###
def territoire(plateau, ligne, colonne, couleur):
    pass


### Scores ###
def score(plateau, couleur):
    pass


### Boucle de jeu principale ###
def main():
    pass
