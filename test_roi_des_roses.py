from roi_des_roses import *
import pytest

rr =pytest.importorskip("roi_des_roses")

def intersection(l1, l2):
    l3 = [value for value in l1 if value in l2]
    return l3

def test_init_jeu(nb_lignes, nb_colonnes):
    plt, lr, cr, mr, mb, pioche, defausse = init_jeu(nb_lignes, nb_colonnes)

# Vérifie que le plateau est bien formatté
    if plt != [["." for count in range(nb_colonnes)] for count in range(nb_lignes)]: 
        return "init_jeu n'a pas passé le test: Plateau non conforme"

# Vérifie que les dimensions données pour former le plateau sont bien conformes.
    if nb_colonnes != nb_lignes or nb_lignes % 2 == 0 or nb_lignes < 3: 
        return "init_jeu n'a pas passé le test: Dimensions du plateau non conformes"

# Vérifie que le roi est bien dans la case centrale
    if lr != nb_lignes // 2 or cr != nb_colonnes // 2: 
        return "init_jeu n'a pas passé le test: Position du Roi mal initialisée"

# Vérifie que l'intégrité du jeu de cartes et leur répartition entre les mains de joueurs et la pioche.
    jeu = ["N1","NE1","E1","SE1","S1","SO1","O1","NO1","N2","NE2","E2","SE2","S2","SO2","O2","NO2","N3","NE3","E3","SE3","S3","SO3","O3","NO3"]
    if len(jeu) != len(pioche) + len(mr) + len(mb):
        return "init_jeu n'a pas passé le test: Le jeu de cartes n'est pas de la bonne taille !"
    if len(mr) != 5 or len(mb) != 5:
        return "init_jeu n'a pas passé le test: Les cartes en main ne sont pas nombre de 5 !"
    if intersection(mr, mb) != [] or intersection(mr, pioche) != [] or intersection(mb, pioche) != []: 
        return "init_jeu n'a pas passé le test: Une carte existe en deux exemplaires !"

# Vérifie que la défausse est bien initialisée et vide.
    if defausse != []:
        return "init_jeu n'a pas passé le test: Defausse non vide"

    return "init_jeu a passé le test"

print(test_init_jeu(9,9))


def test_mouvement_possible(plateau, l_roi, c_roi, carte):
    pass


def test_main_jouable(plateau, l_roi, c_roi, main):
    pass