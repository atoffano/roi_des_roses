import pytest

rr = pytest.importorskip("roi_des_roses")

def test_init_jeu():
    plt, lr, cr, mr, mb, pioche, defausse = rr.init_jeu(7, 7)
    assert plt == [["." for count in range(7)] for count in range(7)], "Plateau non conforme"
    assert lr == 7//2 and cr == 7//2, "Roi mal placé"
    assert len(mr) == 5 and len(mb) == 5, "Les mains doivent être composées de 5 cartes !"
    assert len(pioche) == 14, "Pioche de la mauvaise taille"
    assert mb not in pioche and mr not in pioche and mr not in mb, "Duplication de carte"
    assert defausse == [], "La défausse doit être une liste vide"
    mr_1 = mr
    mb_1 = mb
    plt, lr, cr, mr, mb, pioche, defausse = rr.init_jeu(7, 7)
    assert mb != mb_1 and mr_1 != mr, " Il faudrait distribuer les cartes de manière aléatoire entre les parties.."

faux_plateau = [['.', '.', '.', '.', '.', 'B', 'B', '.', '.'], ['.', '.', '.', '.', 'R', 'R', 'B', '.', '.'], ['.', 'R', '.', '.', 'B', 'B', 'R', 'B', '.'], ['.', '.', '.', '.', '.', '.', '.', 'B', '.'], ['.', '.', '.', '.', 'R', '.', 'R', '.', 'B'], ['.', '.', '.', '.', 'R', '.', 'B', 'R', 'B'], ['.', '.', '.', '.', '.', '.', '.', 'B', 'R'], ['.', '.', '.', '.', '.', 'R', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', 'R', 'B']]
faux_l_roi = 3
faux_c_roi = 2
faux_deck = ["N1","NE1","E1","SE1","S1","SO1","O1","NO1","N2","NE2","E2","SE2","S2","SO2","O2","NO2","N3","NE3","E3","SE3","S3","SO3","O3","NO3"]
fausse_main_rouge = ["S1","SO1","O1"]
fausse_main_blanc = ["SE1","NE2","N3","E2"]
fausse_defausse = []

def test_afficher_main(capsys):
#Test d'affichage d'une main vide
    rr.afficher_main("Rouge", [])
    out, err = capsys.readouterr()
    assert out == "Rouge : \n", "Erreur d'affichage de la main vide"
#Test d'affichage d'une main Rouge
    rr.afficher_main("Rouge", fausse_main_rouge)
    out, err = capsys.readouterr()
    assert out == "Rouge : S1 SO1 O1\n", "Erreur d'affichage de la main Rouge"
#Test d'affichage d'une main Blanche
    rr.afficher_main("Blanc", fausse_main_blanc)
    out, err = capsys.readouterr()
    assert out == "Blanc : SE1 NE2 N3 E2\n", "Erreur d'affichage de la main Blanche"

def test_afficher_jeu(capsys):
    rr.afficher_jeu(faux_plateau, faux_l_roi, faux_c_roi, fausse_main_rouge, fausse_main_blanc)
    out, err = capsys.readouterr()
    assert "Rouge : S1 SO1 O1\nBlanc : SE1 NE2 N3 E2\n"in out, "Erreur d'affichage des main"
    assert "Rouge : S1 SO1 O1\nBlanc : SE1 NE2 N3 E2\n----------------------------------------------\n|    |    |    |    |    |  B |  B |    |    |\n----------------------------------------------\n|    |    |    |    |  R |  R |  B |    |    |\n----------------------------------------------\n|    |  R |    |    |  B |  B |  R |  B |    |\n----------------------------------------------\n|    |    | X  |    |    |    |    |  B |    |\n----------------------------------------------\n|    |    |    |    |  R |    |  R |    |  B |\n----------------------------------------------\n|    |    |    |    |  R |    |  B |  R |  B |\n----------------------------------------------\n|    |    |    |    |    |    |    |  B |  R |\n----------------------------------------------\n|    |    |    |    |    |  R |    |    |    |\n----------------------------------------------\n|    |    |    |    |    |    |    |  R |  B |\n----------------------------------------------\n" in out, "Erreur d'affichage du plateau"
    
def test_mouvement_possible():
# Dictionnaires contenant l'output de la fonction mouvement_possible() à tester et les cartes associées.
    mvmnt_pos_output_1 = {}
    mvmnt_pos_output_2 = {}

# Contient la carte et sa jouabilité à deux positions du roi différentes (3,2 et 1,7).
    coup_valide_1 = {'N1': True, 'NE1': True, 'E1': True, 'SE1': True, 'S1': True, 'SO1': True, 'O1': True, 'NO1': False, 'N2': True, 'NE2': False, 'E2': True, 'SE2': False, 'S2': True, 'SO2': True, 'O2': True, 'NO2': True, 'N3': True, 'NE3': False, 'E3': True, 'SE3': True, 'S3': True, 'SO3': False, 'O3': False, 'NO3': False}
    coup_valide_2 = {'N1': True, 'NE1': True, 'E1': True, 'SE1': True, 'S1': False, 'SO1': False, 'O1': False, 'NO1': False, 'N2': False, 'NE2': False, 'E2': False, 'SE2': False, 'S2': False, 'SO2': True, 'O2': False, 'NO2': False, 'N3': False, 'NE3': False, 'E3': False, 'SE3': False, 'S3': True, 'SO3': False, 'O3': False, 'NO3': False}

# Contient les cartes du deck emmenant le roi hors du plateau.
    out_of_bound_1 = ['SO3', 'O3', 'NO3']
    out_of_bound_2 = ['N2', 'NE2', 'E2', 'SE2', 'N3', 'NE3', 'E3', 'SE3', 'NO3']

# On essaye de jouer toutes les cartes du jeu et on enregistre l'output de la fonction..
    for carte in faux_deck:
        mvmnt_pos_output_1[carte] = rr.mouvement_possible(faux_plateau, faux_l_roi, faux_c_roi, carte) # .. Dans un premier temps comme si le roi était en (3,2)..
        mvmnt_pos_output_2[carte] = rr.mouvement_possible(faux_plateau, 1, 7, carte) # ..Et comme s'il était en 1,7 dans un second temps.

#On teste pour chaque carte si l'output de la fonction matche bien les coups réellement possibles..
    for carte, jouabilite in mvmnt_pos_output_1.items(): # ..Pour la position 1
        assert jouabilite == coup_valide_1[carte], "Le Roi ne doit pas pouvoir sortir du plateau!" if carte in out_of_bound_1 else "Le Roi ne peut arriver sur un pion !"

    for carte, jouabilite in mvmnt_pos_output_2.items(): # ..Pour la position 2
        assert jouabilite == coup_valide_2[carte], "Le Roi ne doit pas pouvoir sortir du plateau!" if carte in out_of_bound_2 else "Le Roi ne peut arriver sur un pion !"

def test_main_jouable():
    main_jouable_1 = rr.main_jouable(faux_plateau, faux_l_roi, faux_c_roi, faux_deck)
    main_jouable_2 = rr.main_jouable(faux_plateau, 1, 7, faux_deck)
    for carte in main_jouable_1:
        assert len(main_jouable_1) == 17, "Des cartes jouables n'ont pas été retournées"
        assert carte in ['N1', 'NE1', 'E1', 'SE1', 'S1', 'SO1', 'O1', 'N2', 'E2', 'S2', 'SO2', 'O2', 'NO2', 'N3', 'E3', 'SE3', 'S3'], "Une carte injouable a été retournée"
    for carte in main_jouable_2:
        assert len(main_jouable_2) == 6, "Des cartes jouables n'ont pas été retournées"
        assert carte in ['N1', 'NE1', 'E1', 'SE1', 'SO2', 'S3'], "Une carte injouable a été retournée"

# def call_boucle_inf():
#     stuck = True
#     assert stuck == False, "Fonction bloquée dans une boucle infinie"

# def test_demande_action(monkeypatch, capsys):
#     from threading import Timer
#     timeout = 1
#     t = Timer(timeout, call_boucle_inf)
#     t.start()
#     monkeypatch.setattr('builtins.input', lambda: "pioche")
#     assert rr.demande_action("Blanc", faux_plateau, faux_l_roi, faux_c_roi, []) == "pioche", "Expected 'pioche' got something else in return"
#     t.cancel()
#     t.join()
    # t = Timer(timeout, call_boucle_inf)
    # t.start()
    # for carte in fausse_main_blanc:
    #     if carte != "NE2": # On traite la seule carte injouable de la main séparément.
    #         monkeypatch.setattr('builtins.input', lambda: carte)
    #         assert rr.demande_action("Blanc", faux_plateau, faux_l_roi, faux_c_roi, ["SO1","O1","NO1","N2","NE2"]) == carte, "La fonction ne renvoie pas la carte jouée!"
    #     elif carte == "NE2":
    #         monkeypatch.setattr('builtins.input', lambda: carte)
    #         assert rr.demande_action("Blanc", faux_plateau, faux_l_roi, faux_c_roi, ["SO1","O1","NO1","N2","NE2"]) == carte, "La fonction renvoie une carte injouable!"
    # t.cancel()
    # t.join()
    # t = Timer(timeout, call_boucle_inf)
    # t.start()
    # monkeypatch.setattr('builtins.input', lambda: "N1")
    # assert rr.demande_action("Blanc", faux_plateau, faux_l_roi, faux_c_roi, ["N1", "N1", "N1", "N1", "N1"]) == "N1", "La fonction renvoie une carte malgré une carte injouable"
    # t.cancel()
    # t.join()
    # t = Timer(timeout, call_boucle_inf)
    # t.start()
    # monkeypatch.setattr('builtins.input', lambda: "passe")
    # assert rr.demande_action("Blanc", faux_plateau, faux_l_roi, faux_c_roi, ["N1", "N1", "N1", "N1", "N1"]) == "passe", "La fonction ne passe pas !"
    # t.cancel()

def calc_pos_arrivee(faux_l_roi, faux_c_roi, carte):
    true_l_roi = faux_l_roi
    true_c_roi = faux_c_roi
    dist_parcourue = int(carte[-1]) # Récupère l'ordre de grandeur associé à la carte (i.e 1, 2 ou 3)
    for i in range(len(carte)-1):  # On calcule les coordonnées d'arrivée du roi en fonction du/des vecteurs (N, E, S, O) associés à la carte
        if carte[i] == 'N':
            true_l_roi -= dist_parcourue
        elif carte[i] == 'E':
            true_c_roi += dist_parcourue        
        elif carte[i] == 'S':
            true_l_roi += dist_parcourue
        else:
            true_c_roi -= dist_parcourue
    return true_l_roi, true_c_roi
    
def test_bouge_le_roi():
    for main_joueurs in [fausse_main_rouge, fausse_main_blanc]:
        for carte in main_joueurs:
            plateau, new_l_roi, new_c_roi, main_r, main_b, defausse = rr.bouge_le_roi(faux_plateau, faux_l_roi, faux_c_roi, main_joueurs, [], fausse_defausse, carte, "Rouge")
            true_l_roi, true_c_roi = calc_pos_arrivee(faux_l_roi, faux_c_roi, carte)
            assert true_l_roi == new_l_roi, "Ligne d'arrivée du roi mal calculée"
            assert true_c_roi == new_c_roi, "Colonne d'arrivée du roi mal calculée"
            assert plateau[new_l_roi][new_c_roi] == "R", "Case d'arrivée du roi mal annotée sur le plateau"
            assert carte not in main_r, "Carte jouée non supprimée de la main"
            assert carte in defausse, "La carte jouée n'est pas arrivée dans la défausse"
# def test_territoire():
#     assert rr.territoire(faux_plateau, 0, 0, "Rouge") == [], "Un territoire != [] a été retourné pour une case vide"
#     assert rr.territoire(faux_plateau, 2, 1, "Blanc") == [], "Un territoire != [] a été retourné alors que la case testée et de la couleur opposée"
#     assert rr.territoire(faux_plateau, 1, 6, "Blanc") == [], "Un territoire != [] a été retourné alors que la case testée et de la couleur opposée"
print(rr.territoire(faux_plateau, 1, 6, "Blanc"))
print(faux_plateau[1][3])
print(faux_plateau[1][4])
print(faux_plateau[1][5])
print(faux_plateau[1][6])
print('lui')
print(faux_plateau[1][7])
print(faux_plateau[1][8])


# def test_check_voisins(plateau, ligne, colonne, couleur):
#     pass

# def test_score(plateau, couleur):
#     pass

# def test_main():
#     pass