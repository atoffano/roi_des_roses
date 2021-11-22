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
    main_a_afficher = couleur + " : "
    for i in range(len(main)-1):
        main_a_afficher += main[i] + " "
    main_a_afficher += main[-1]
    print(main_a_afficher)

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
plt , lr, cr, mr, mb, pioche , defausse = init_jeu(9, 9)
afficher_jeu(plt , lr, cr, mr, mb)




### Mouvement du roi possible ###
def mouvement_possible(plateau, l_roi, c_roi, carte):
    new_l_roi = l_roi
    new_c_roi = c_roi
    dist_parcourue = int(carte[-1]) # Récupère l'ordre de grandeur associé à la carte (i.e 1, 2 ou 3)
    for i in range(len(carte)-1):  # On calcule les coordonnées d'arrivée du roi en fonction du/des vecteurs (N, E, S, O) associés à la carte
        if carte[i] == 'N':
            new_l_roi -= dist_parcourue
        elif carte[i] == 'E':
            new_c_roi += dist_parcourue        
        elif carte[i] == 'S':
            new_l_roi += dist_parcourue
        else:
            new_c_roi -= dist_parcourue

    if plateau[new_l_roi][new_c_roi] != ".": # On vérifie que la case d'arrivée est bien vide
        return False

    if 0 <= new_l_roi <= len(plateau) and 0 <= new_c_roi <= len(plateau): # On vérifie finalement  que la position finale n'est pas hors du plateau
        return True # Si toutes les conditions sont validées, le mouvement est possible !
    return False 


### Main jouable ###
def main_jouable(plateau, l_roi, c_roi, main):
    main_jouable = []
    for carte in main: # Pour chaque carte dans la main du joueur, si le mouvement est possible, ajoute la carte à une liste.
        if mouvement_possible(plateau, l_roi, c_roi, carte) == True:
            main_jouable.append(carte)
    return main_jouable # On retourne la liste de cartes jouables


### Demande une action à un joueur ###
def demande_action(couleur, plateau, l_roi, c_roi, main):
    print("Vous  êtes le  joueur " + couleur + ", que souhaitez -vous  faire ?\n")
# On demande une action et on teste sa validité. On recommence jusqu'à ce que le joueur donne une action valide
    while True: 
        action = input()
        if action == "passe":
            return action
        if action == "pioche" and len(main) < 5: # On vérifie que la main n'est pas pleine si le joueur choisit de piocher.
            return action
        if action in main_jouable(plateau, l_roi, c_roi, main):
            return action
        print("Action impossible, que souhaitez-vous faire ? ")


### Bouge le roi ###
def bouge_le_roi(plateau, l_roi, c_roi, main_r, main_b, defausse, carte, couleur):
    new_l_roi = l_roi
    new_c_roi = c_roi
    dist_parcourue = int(carte[-1]) # Récupère l'ordre de grandeur associé à la carte (i.e 1, 2 ou 3)
    for i in range(len(carte)-1):  # On calcule les coordonnées d'arrivée du roi en fonction du/des vecteurs (N, E, S, O) associés à la carte
        if carte[i] == 'N':
            new_l_roi -= dist_parcourue
        elif carte[i] == 'E':
            new_c_roi += dist_parcourue        
        elif carte[i] == 'S':
            new_l_roi += dist_parcourue
        else:
            new_c_roi -= dist_parcourue


### Definition des territoires ###
def territoire(plateau, ligne, colonne, couleur):
    territoire = []
    if plateau[ligne][colonne] == couleur: # Si la case est de la bonne couleur, on ajoute ses coordonnées à la liste des territoires.
        territoire.append([ligne, colonne])
        territoire_voisins = check_voisins(plateau, ligne, colonne, couleur) # On regarde si cette case possède des voisins de même couleur.
        while territoire_voisins != []: # Tant qu'il ne reste pas de cases voisines de la même couleur (i.e que le bord du territoire n'a pas été atteint):
            for voisin in territoire_voisins: # Pour chaque case de la même couleur voisine de notre case:
                if voisin not in territoire: # On l'ajoute au territoire si elle n'y est pas déjà.
                    territoire.append(voisin)
                    territoire_voisins += check_voisins(plateau, voisin[0], voisin[1], couleur) # On vérifie si elle n'a pas des cases voisines de la même couleur.
                    # Si oui, on les ajoute à la liste des voisins qui vont à leur tour (i.e à la prochaine itération) être scannés pour déterminer leurs cases adjacentes..
                territoire_voisins.remove(voisin) # On supprime la case de la liste à analyser
        a_renvoyer = [] # Les 3 lignes suivantes permettent de convertir le territoire d'un format liste de listes vers liste de tuples.
        for case in territoire:
            a_renvoyer.append(tuple(case))
        return a_renvoyer
    return [] # Si la case d'origine n'est pas de la bonne couleur, on renvoie une liste vide.

# Fonction enregistrant les coordonnées des voisins nord, sud, est et ouest d'une case fournie si elles sont de la même couleur et renvoyant leur coordonnées.
def check_voisins(plateau, ligne, colonne, couleur):
    voisins = []
    if ligne + 1 < len(plateau) and plateau[ligne +1] [colonne] == couleur: # On vérifie ici si il existe bien une case au Sud de celle d'origine(i.e on est au bord du plateau), et si sa la couleur correspond.
        voisins.append([ligne +1, colonne]) # Si oui, on l'ajoute à une liste qui sera retournée.
    if ligne - 1 >= 0 and plateau[ligne -1] [colonne] == couleur:
        voisins.append([ligne -1, colonne])
    if colonne + 1 < len(plateau) and plateau[ligne] [colonne + 1] == couleur:
        voisins.append([ligne, colonne + 1])    
    if colonne - 1 >= 0 and plateau[ligne] [colonne - 1] == couleur:
        voisins.append([ligne, colonne - 1])
    return voisins
plt = [["R" for count in range(9)] for count in range(9)]

plt[2][5]="R"
plt[2][6]="R"
plt[2][7]="R"
plt[3][4]="R"
plt[4][4]="R"
plt[5][4]="R"
plt[5][6]="R"
plt[2][4]="R"
plt[5][5]="R" 
plt[1][5]="R"
plt[0][5]="R"


print(len(territoire(plt, 2, 4, "R")))
print(len(list(dict.fromkeys(territoire(plt, 2, 4, "R")))))

### Scores ###
def score(plateau, couleur):
    


### Boucle de jeu principale ###
def main():
#   plt, lr, cr, mr, mb, pioche, defausse = init_jeu(9, 9)
    pass
