import pytest

rr = pytest.importorskip("roi_des_roses")
plt, lr, cr, mr, mb, pioche, defausse = rr.init_jeu(7, 7)
def test_init_jeu():
    assert plt == [["." for count in range(7)] for count in range(7)], "Plateau non conforme"
    assert lr == 7//2 and cr == 7//2, "Roi mal placé"
    assert len(mr) == 5 and len(mb) == 5, "Les mains doivent être composées de 5 cartes !"
    assert len(pioche) == 14, "Pioche de la mauvaise taille"
    assert mb  in pioche and mr not in pioche and mr not in mb, "Duplication de carte"
    assert defausse == [], "La défausse doit être une liste vide"
