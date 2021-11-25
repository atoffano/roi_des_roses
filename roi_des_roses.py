import random    

#############################
### Initialisation du jeu ###
#############################
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


##################################
### Affichage de l'état du jeu ###
##################################

# Affiche la main du joueur de la couleur renseignée
def afficher_main(couleur, main):
    main_a_afficher = couleur + " : "
    if main != []:
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

#################################
### Mouvement du roi possible ###
#################################
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
 # On vérifie que la position finale n'est pas hors du plateau, et qu'elle n'est pas occupée.
    if 0 <= new_l_roi < len(plateau) and 0 <= new_c_roi < len(plateau) and plateau[new_l_roi][new_c_roi] == ".":
        return True
    return False

####################
### Main jouable ###
####################

def main_jouable(plateau, l_roi, c_roi, main):
    main_jouable = []
    for carte in main: # Pour chaque carte dans la main du joueur, si le mouvement est possible, ajoute la carte à une liste.
        if mouvement_possible(plateau, l_roi, c_roi, carte) == True:
            main_jouable.append(carte)
    return main_jouable # On retourne la liste de cartes jouables

######################################
### Demande une action à un joueur ###
######################################

def demande_action(couleur, plateau, l_roi, c_roi, main):
    print("Vous  êtes le  joueur " + couleur + ", que souhaitez -vous  faire ?\n")
# On demande une action et on teste sa validité. On recommence jusqu'à ce que le joueur donne une action valide
    while True: 
        action = input()
        if action == "passe" and main_jouable(plateau, l_roi, c_roi, main) == []:
            return action
        if action == "pioche" and len(main) < 5: # On vérifie que la main n'est pas pleine si le joueur choisit de piocher.
            return action
        if action in main_jouable(plateau, l_roi, c_roi, main):
            return action
        print("Action impossible, que souhaitez-vous faire ? ")


####################
### Bouge le roi ###
####################

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
    if couleur == "Rouge":
        plateau[new_l_roi][new_c_roi] = "R"     #on pose un pion de la bonne couleur
        main_r.remove(carte)            #on supprime la carte de la main du joueur
    else:
        plateau[new_l_roi][new_c_roi] = "B"
        main_b.remove(carte)
    defausse.append(carte)              #on ajoute cette carte à la defausse
    return (plateau, new_l_roi, new_c_roi, main_r, main_b, defausse)

##################################
### Definition des territoires ###
##################################

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

##############
### Scores ###
##############

def score(plateau, couleur):
    score = 0
    somme_territoires = []
    to_check =  [(i,j) for i in range(len(plateau)) for j in range(len(plateau))]
    while to_check != []:
        ligne = to_check[0][0]
        col = to_check[0][1]
        territoire_case = territoire(plateau, ligne, col, couleur)
        somme_territoires += territoire_case
        for case in territoire_case:
            if case in to_check:
                to_check.remove(case)
    for zone in somme_territoires:
        score += len(zone)**2

################################
### Boucle de jeu principale ###
################################

def main():
    plt, lr, cr, mr, mb, pioche, defausse = init_jeu(9,9) #initialisation du jeu
    jeu_fini = False #variable pour arreter la boucle
    joueur = "Blanc"  # les blancs commencent (comme les echecs, mais on peut changer si c'est raciste x) )
    action_pre = ""   #variable qui me permet de modifer jeu_fini et d'arreter le jeu si les deux joueurs passent à la suite
    pion_R = 0        #compteur de pion rouge
    pion_B = 0          #compteur de pion blanc
    
    while jeu_fini == False:   #boucle du jeu
        if joueur == "Rouge":
            couleur = "Rouge"   #pour qu'a chaque tour, on associe la main et la couleur du bon joueur
            main = mr
        if joueur == "Blanc":
            couleur = "Blanc"
            main = mb

        afficher_jeu(plt, lr, cr, mr, mb)   #on affiche l'état du jeu

        action = demande_action(couleur, plt, lr, cr, main)#return soit passe, soit pioche, soit une carte jouable

###a ajouter: si pioche vide ? fin de la partie ? remelange de la defausse ?

    # Si le joueur pioche:
        if action == "pioche": 
            if pioche == []: # Si la pioche est vide, on mélange la défausse avant de la remettre dans la pioche.
                random.shuffle(defausse)
                pioche = defausse
                defausse = []
            main.append(pioche[0]) # On la transfère la première carte de la pioche à la main du joueur
            pioche.remove(pioche[0])
            action_pre = "pioche"   # On note que ce tour la, le joueur a pioché.
    # Si le joueur passe:
        elif action == "passe":
            if action_pre == "passe":   # Si les deux joueurs passent à la suite, la partie prend fin à ce tour.
                jeu_fini = True
            action_pre = "passe"    
    # L'action est une carte: 
        else: 
            plt, lr, cr, mr, mb, defausse = bouge_le_roi(plt, lr,cr, mr, mb, defausse, action, couleur) # On fait bouger le roi et on update le jeu en fonction
            action_pre = "carte"    #ce tour la, le joueur a joué
            if joueur == "Blanc":
                pion_B += 1
            else :
                pion_R += 1
            if pion_R == 26 or pion_B == 26:       # Permet d'arrêter la partie quand tous les pions  d'une couleur ont été joués.
                jeu_fini = True
        if joueur == "Blanc":   #permet de changer de joueur a chaque fin de tour
            joueur = "Rouge"
        else:
            joueur = "Blanc"
    # Si on sort de la boucle de jeu:
    sb = score(plt, "Blanc")
    sr = score(plt, "Rouge")
    print(f"Rouge: {sr}")
    print(f"Blanc: {sb}")       # On affiche les scores
    if sr > sb :
        print("Rouge a gagné la partie")        # On affiche le gagnant
    elif sr < sb :
        print("Blanc a gagné la partie")
    else:
        print("Egalité")

if __name__ == "__main__":      #code pour executer la fonction main à l'ouverture du fichier
    main()

# TODO : scores(), tests