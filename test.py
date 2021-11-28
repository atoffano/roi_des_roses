import time
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

def territoire(plateau, ligne, colonne, couleur):
    territoire = []
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

faux_plateau = [['.', '.', '.', '.', '.', 'B', 'B', '.', '.'], ['.', '.', '.', '.', 'R', 'R', 'B', '.', '.'], ['.', 'R', '.', '.', 'B', 'B', 'R', 'B', '.'], ['.', '.', '.', '.', '.', '.', '.', 'B', '.'], ['.', '.', '.', '.', 'R', '.', 'R', '.', 'B'], ['.', '.', '.', '.', 'R', '.', 'B', 'R', 'B'], ['.', '.', '.', '.', '.', '.', '.', 'B', 'R'], ['.', '.', '.', '.', '.', 'R', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', 'R', 'B']]

print(score(faux_plateau, "Rouge"))

print(score(faux_plateau, "Blanc"))