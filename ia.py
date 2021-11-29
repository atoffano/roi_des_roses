def name():
    return "Tata Suzanne"

def play(plateau , l_roi , c_roi , main_r , main_b , couleur):
    main = main_b
    if couleur == "Rouge":
        main = main_r
    if len(main) < 5:
        return "pioche"
    else:
        for carte in main:
            if mouvement_possible(plateau, l_roi, c_roi, carte):
                return carte
        return "passe"