import random
import copy
import numpy as np
import random
import time
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
    action = input(f"Vous êtes le joueur {couleur}, que souhaitez vous faire ? ")
# On demande une action et on teste sa validité. On recommence jusqu'à ce que le joueur donne une action valide
    while True: 
        if action == "passe" and main_jouable(plateau, l_roi, c_roi, main) == [] and len(main) == 5:
            return action
        if action == "pioche" and len(main) < 5: # On vérifie que la main n'est pas pleine si le joueur choisit de piocher.
            return action
        if action in main_jouable(plateau, l_roi, c_roi, main):
            return action
        action = input("Action impossible, que souhaitez-vous faire ? ")


####################
### Bouge le roi ###
####################

def bouge_le_roi(plateau, l_roi, c_roi, main_r, main_b, defausse, carte, couleur):
    plateau = copy.deepcopy(plateau)
    main_r = copy.deepcopy(main_r)
    main_b = copy.deepcopy(main_b)
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
    couleur = copy.deepcopy(couleur)
    couleur = "R" if couleur == "Rouge" else "B"
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
        if territoire_case != []:
            somme_territoires.append(territoire_case)
        for case in territoire_case:
            if case in to_check and case != to_check[0]:
                to_check.remove(case)
        to_check.remove(to_check[0])
    for zone in somme_territoires:
        score += len(zone)**2
    return score

################################
### Boucle de jeu principale ###
################################

def main():
    plt, lr, cr, mr, mb, pioche, defausse = init_jeu(9,9) #initialisation du jeu
    jeu_fini = False #variable pour arreter la boucle
    joueur = "Rouge"  # les rouges commencent (cf regle)
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

        action = play(plt , lr , cr , mr , mb , couleur)#return action
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

    stat[cnt] = (sb,sr)


##################################################################################################################

def position_arrive_carte(carte,l_roi, c_roi):  #fonction qui retourne positon eventuelle du roi si je joue la carte placée argument
    new_l_roi = l_roi
    new_c_roi = c_roi
    dist_parcourue = int(carte[-1])
    for i in range(len(carte)-1):
        if carte[i] == 'N':
            new_l_roi -= dist_parcourue
        elif carte[i] == 'E':
            new_c_roi += dist_parcourue        
        elif carte[i] == 'S':
            new_l_roi += dist_parcourue
        else:
            new_c_roi -= dist_parcourue
    return (new_l_roi, new_c_roi)

def play_demolition_man(plateau, l_roi, c_roi, main_r, main_b, couleur):
    if couleur == "Rouge":
        main = main_r
        pion = "R"
        main_adv = main_b
        pion_adv = "B"
    else :
        main = main_b
        pion = "B"
        main_adv = main_r
        pion_adv = "R"
    
    mj = main_jouable(plateau, l_roi, c_roi, main)

    if mj == [] and len(main)==5:    #si je peux pas jouer de carte ni piocher je passe
       return "passe"

    if mj == [] and len(main) != 5: #si je peux pas jouer de carte mais piocher je pioche
        return "pioche"

    score_voisin = dict()
    for carte in mj:    #pour chaque carte de ma main jouable
        new_l_roi, new_c_roi = position_arrive_carte(carte,l_roi, c_roi)    #je calcule la potentiel postion du roi si je joue cette carte
        mj_adv = main_jouable(plateau, new_l_roi, new_c_roi, main_adv)  #je regarde la main adv jouable au prochain tour si je joue cette carte 
        if mj_adv == [] :   #si l'adversaire ne pourra pas jouer de carte
            return carte    #je joue cette carte

        # calcul des pions de notre couleur adjacents à la case d'arriver de cette carte
        voisin = 0
       
        try :   #pour eviter problème d'out of range (du à une sortie du plateau ?!)

            if plateau[new_l_roi+1][new_c_roi] == pion:
                voisin += 1
            if plateau[new_l_roi-1][new_c_roi] == pion:
                voisin += 1
            if plateau[new_l_roi][new_c_roi+1] == pion:
                voisin += 1
            if  plateau[new_l_roi][new_c_roi-1] == pion:
                voisin += 1

        except IndexError:
            pass

        else :
            score_voisin = { carte : int(voisin) }
            if score_voisin[carte] >= 2:    # si au moins 2 pions adjacents: je joue cette carte (fusion d'un territoire)
                return carte

        finally:

            # calcul des pions de notre couleur adjacents à la case d'arriver de cette carte
            voisin_adv = 0
            try:

                if plateau[new_l_roi+1][new_c_roi] == pion_adv:
                    voisin_adv += 1
                if plateau[new_l_roi-1][new_c_roi] == pion_adv:
                    voisin_adv += 1
                if plateau[new_l_roi][new_c_roi+1] == pion_adv:
                    voisin_adv += 1
                if plateau[new_l_roi][new_c_roi-1] == pion_adv:
                    voisin_adv += 1

            except IndexError:
                pass

            else:
                score_voisin_adv = { carte : int(voisin_adv) }
                if score_voisin_adv[carte] >= 2:    # si au moins 2 pions adverses adjacents: je joue cette carte (blocage d'un territoire)
                    return carte
                if score_voisin[carte] == 1:    # si 1 pion adjacent: je joue cette carte
                    return carte
            finally:

                if len(main)<5: #si je peux piocher, je pioche
                    return "pioche"

                else:   #si je peux pas piocher ni passer, je joue une carte de merde au pif
                    i = random.randint(0, (len(mj)-1))
                    return mj[i]

def play(plateau , l_roi , c_roi , main_r , main_b , couleur):
    if couleur == "Rouge":
        return play_demolition_man(plateau , l_roi , c_roi , main_r, main_b, couleur)
    return play_graou(plateau, l_roi, c_roi, main_r, main_b, couleur)

def play_suzanne(plateau , l_roi , c_roi , main_r):
    main = main_r
    if len(main) < 5:
        return "pioche"
    else:
        for carte in main:
            if mouvement_possible(plateau, l_roi, c_roi, carte):
                return carte
        return "passe"

def play_graou(plateau, l_roi, c_roi, main_r, main_b, couleur):
    main = main_b
    option = main_jouable(plateau, l_roi, c_roi, main)
    if len(main) == 5 and option == []:
        return 'passe'
    if len(main) < 5:
        return "pioche"
    return get_value(option, main_r, plateau, couleur, l_roi, c_roi)

def center_value(plt, l_pion, c_pion, carte):
    center = len(plt)//2
    return abs(l_pion-center + c_pion-center)
    
def calc_pos(carte):
    dist_parcourue = int(carte[-1]) # Récupère l'ordre de grandeur associé à la carte (i.e 1, 2 ou 3)
    c_pion = 0
    l_pion = 0
    for i in range(len(carte)-1):  # On calcule les coordonnées d'arrivée du pion en fonction du/des vecteurs (N, E, S, O) associés à la carte
        if carte[i] == 'N':
            l_pion -= dist_parcourue
        elif carte[i] == 'E':
            c_pion += dist_parcourue        
        elif carte[i] == 'S':
            l_pion += dist_parcourue
        else:
            c_pion -= dist_parcourue
    return l_pion, c_pion

def get_value(option, main_r, plateau, couleur, l_roi, c_roi):
    plt = copy.deepcopy(plateau)
    terr_value = {}
    concentration_value ={}
    spread_value = {}
    for carte in option:
        l_pion, c_pion = calc_pos(carte)
        plt[l_pion][c_pion] == "R" if couleur == "Rouge" else "B"
        concentration_value[center_value(plt, l_pion, c_pion, carte)] = carte
        terr_value[len(territoire(plt, l_pion, c_pion, couleur))**2] = carte
        spread_value[len(check_voisins(plateau, l_pion, c_pion, couleur))] = carte
    coup = converge(plt, max(concentration_value.keys()), max(terr_value.keys()), max(spread_value.keys()))
    if coup == 'terr_value':
        return terr_value[max(terr_value.keys())]
    elif coup == 'concentration_value':
        return concentration_value[max(concentration_value.keys())]
    return spread_value[max(spread_value.keys())]
    # if max(terr_value.keys()) != 0:
    #     return terr_value[max(terr_value.keys())]
    # return concentration_value[min(concentration_value.keys())]

def converge(plt, concentration_value, terr_value, spread_value):
    concentration_value = concentration_value*coeff['cv']
    terr_value = terr_value*coeff['tv']
    spread_value = spread_value*coeff['sv']
    decision = max(concentration_value, terr_value, spread_value)
    if  decision == terr_value:
        return 'terr_value'
    elif decision == concentration_value:
        return 'concentration_value'
    return 'spread_value'


if __name__ == "__main__":      #code pour executer la fonction main à l'ouverture du fichier
    cnt = 0
    graou = 0
    suzanne = 0
    draw = 0
    stat = {}
    ngame = 1000
    coeff = {'tv':-5.310000000000012, 'sv':3.5899999999999985, 'cv':7.130000000000021}
    while cnt < ngame:
        start = time.time() 
        main()
        cnt += 1
    for keys, value in stat.items():
        if value[0] > value[1]:
            graou += 1
        elif value[0] < value[1]:
            suzanne += 1
        else:
            draw += 1
    print('wr de graou ' + str(graou*100/ngame) + '%')
    print('wr de demolition_man ' + str(suzanne*100/ngame) + '%')
    print('taux draw ' + str(draw*100/ngame) + '%')
    print(coeff)
