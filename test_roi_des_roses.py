import pytest

rr = pytest.importorskip("roi_des_roses")
plt, lr, cr, mr, mb, pioche, defausse = rr.init_jeu(7, 7)
def test_init_jeu():
    assert plt == [["." for count in range(7)] for count in range(7)], "Plateau non conforme"
    assert lr == 7//2 and cr == 7//2, "Roi mal placé"
    assert len(mr) == 5 and len(mb) == 5, "Les mains doivent être composées de 5 cartes !"
    assert len(pioche) == 14, "Pioche de la mauvaise taille"
    assert mb not in pioche and mr not in pioche and mr not in mb, "Duplication de carte"
    assert defausse == [], "La défausse doit être une liste vide"

def test_afficher_main(couleur, main):
    

def test_afficher_jeu(plateau, l_roi, c_roi, main_r, main_b):
        pass

def test_mouvement_possible(plateau, l_roi, c_roi, carte):
    pass

def test_main_jouable(plateau, l_roi, c_roi, main):
    pass

def test_demande_action(couleur, plateau, l_roi, c_roi, main):
    pass

def test_bouge_le_roi(plateau, l_roi, c_roi, main_r, main_b, defausse, carte, couleur):
    pass

def test_territoire(plateau, ligne, colonne, couleur):
    pass

def test_check_voisins(plateau, ligne, colonne, couleur):
    pass

def test_score(plateau, couleur):
    pass

def test_main():
    pass