import fltk
from random import randint


# dimensions du jeu
taille_case = 60
largeur_plateau = 8  # en nombre de cases
hauteur_plateau = 8  # en nombre de cases

FOND_MENU = 'IMAGES/fond.png'
FOND_REVERSI = 'IMAGES/reversi.png'
FOND_REVERSI_MINI = 'IMAGES/reversi_mini.png'
CRAYON = 'IMAGES/crayon.png'
NOMS = 'IMAGES/nom.png'
BOUTON = 'IMAGES/bouton.png'
BOUTON2 = 'IMAGES/bouton2.png'
# --------------------------- FONCTIONS -----------------------------------


def case_vers_pixel(coord_case):
    """
    Fonction recevant les coordonnées d'une case du plateau sous la
    forme d'un couple d'entiers (id_colonne, id_ligne) et renvoyant les
    coordonnées du pixel se trouvant au centre de cette case. Ce calcul
    prend en compte la taille de chaque case, donnée par la variable
    globale taille_case.

    >>> case_vers_pixel((1,1))
    (50.0, 50.0)
    >>> case_vers_pixel((8, 8))
    (750.0, 750.0)
    """
    i, j = coord_case
    return (i + .5) * taille_case - taille_case,\
           (j + .5) * taille_case - taille_case


def coord_case(case):
    """
    Fonction permettant de donner les coordonnés (ligne, collonne) d'une
    case en fonction de son numéro.

    :param case: int
        Numéro de la case allant de 1 à 64 sur un plateau de jeu 8x8.

    :return value : couple d'entier
        Correspond au némuro de la ligne et de la collonne pour forme des
        coordonnées.

    >>> coord_case(1)
    (1, 1)
    >>> coord_case(64)
    (8, 8)
    >>> coord_case(42)
    (2, 6)
    """
    if case % 8 == 0:
        collonne = case // 8
    else:
        collonne = (case // 8) + 1
    if case % 8 == 0:
        ligne = 8
    else:
        ligne = case % 8
    return (ligne, collonne)


def coordCase_vers_case(coord):
    """
    Fonction qui permet de convertir les coordonnées d'une case
    (ligne, collonne) en numéro de de cette même case ( de 1 à 64).

    :param coord : couple d'entier
        Correspond au némuro de la ligne et de la collonne pour forme des
        coordonnées.

    :return value : int
        Numéro de la case allant de 1 à 64 sur un plateau de jeu 8x8.

    >>> coordCase_vers_case((1,1))
    1
    >>> coordCase_vers_case((8,8))
    64
    >>> coordCase_vers_case((5, 2))
    13
    """
    x, y = coord
    case = largeur_plateau * (y - 1) + x
    return case


def pions(coord, couleur):
    """
    Cette fonction dessine un pion : cercle plein de la couleur choisi
    à la position donnée.

    :param coord : couple d'eniter
        Coordonnées en pixels
    :param couleur : str
    """
    x, y = coord
    fltk.cercle(x, y, taille_case / 2 - 5, remplissage=couleur, tag='supp')


def affiche_plateau():
    """
    Fonction dessinant le quadrillage du plateau de case en fonction de
    la hauteur et la largeur du plateau, ainsi que de la taille des cases.
    """
    fltk.rectangle(0, 0, largeur_plateau*taille_case,
                   hauteur_plateau*taille_case, remplissage='green')
    for x in range(0, largeur_plateau * taille_case, taille_case):
        fltk.ligne(x, 0, x, hauteur_plateau * taille_case)
    for y in range(0, hauteur_plateau * taille_case, taille_case):
        fltk.ligne(0, y, largeur_plateau * taille_case, y)


def affiche_pions(plateau):
    """
    Cette fonction permet de dessiner les pions sur le plateau de jeu,
    elle utilise 2 autres fonctions afin de convertir la liste en coordonnées,
    et une 3ème afin d'afficher les pions.

    :param plateau: list
        Cette liste correspond au plateau (0 = case vide, 1 = pion blanc,
                                           2 = pion noir).
    """
    case = None
    for i in range(len(plateau)):
        if plateau[i] != 0:
            case = i + 1
            coord = case_vers_pixel(coord_case(case))
            if plateau[i] == 1:      # Blanc
                pions(coord, 'white')
            elif plateau[i] == 2:    # Noir
                pions(coord, 'black')


def clic(Menu):
    """
    Fonction de détecter la touche utilisé par l'utilisateur, et permet
    de réaliser ou non une action en focntion de cette dernière et de ses
    coordonnées (s'il s'agit d'un clic souris).

    :return value: str OU couple de d'entier)
    """
    ev = fltk.attend_ev()
    ty = fltk.type_ev(ev)
    while ty != 'ClicGauche' and ty != 'Quitte':
        ev = fltk.attend_ev()
        ty = fltk.type_ev(ev)

    # Clics dans le menu
    if Menu == 'MENU':
        if ty == 'Quitte':
            return 'stop'
        elif ty == 'ClicGauche':
            x = fltk.abscisse(ev)
            y = fltk.ordonnee(ev)
            y2 = hauteur_plateau * taille_case
            x2 = largeur_plateau * taille_case
            if x > x2/3+100 and x < x2/1.5+100 and y > y2/3 and y < y2/2:
                return 'jouer'
            elif x > x2/3+100 and x < x2/1.5+100 and\
                    y > y2/1.9 and y < y2/1.443:
                return 'jouer_vs_ordi'
            elif x > 435 and x < 485 and y > 175 and y < 225:
                return 'nom'
            elif x > x2/3+100 and x < x2/1.5+100\
                    and y > y2/1.39 and y < y2/1.128:
                return 'sauvegarde'

    # Clics dans la partie
    elif Menu == 'jouer':
        if ty == 'Quitte':
            return 'stop'
        elif ty == 'ClicGauche':
            x_clic = fltk.abscisse(ev)
            y_clic = fltk.ordonnee(ev)
            # Dans le plateau de jeu
            if x_clic < 480 and y_clic < 480:
                x1 = 0
                y1 = 0
                cmpt_x = 0
                cmpt_y = 0
                while x_clic > x1:
                    x1 += taille_case
                    cmpt_x += 1
                while y_clic > y1:
                    y1 += taille_case
                    cmpt_y += 1
                return (cmpt_x, cmpt_y)
            # dans la partie d'informations à droite
            else:
                if x_clic > 635 and x_clic < 660\
                        and y_clic > 435 and y_clic < 460:
                    return 'pause'
                elif x_clic > 515 and x_clic < 545\
                        and y_clic > 200 and y_clic < 220:
                    return '0s'
                elif x_clic > 565 and x_clic < 595\
                        and y_clic > 200 and y_clic < 220:
                    return '1.5s'
                elif x_clic > 615 and x_clic < 645\
                        and y_clic > 200 and y_clic < 220:
                    return '3s'
                else:
                    return 'rien'

    # Dans le menu de fin de partie
    elif Menu == 'FIN':
        if ty == 'Quitte':
            return 'stop'
        elif ty == 'ClicGauche':
            x = fltk.abscisse(ev)
            y = fltk.ordonnee(ev)
            if x > 262 and x < 422 and y > 160 and y < 240:
                return 'MENU'


def ajoute_pion(plateau, case, joueur):
    """
    Fonction qui permet de modifier une valeur de la liste qui correspond
    au plateau de jeu, ce qui permet ici de rajouter un pion dans la liste
    en fonction donc du joueur, et de la case choisie par le joueur.

    :param case: int
        Numéro de la case
    :param joueur: int
        1 = Blanc et 2 = Noir
    :param plateau: list
    :return value: list
        Liste du plateau modifiée
    """
    if plateau[case - 1] == 0:
        plateau[case - 1] = joueur
    return plateau


def possibilite(plateau, joueur, menu):
    """
    Fonction qui permet de calculer d'afficher les possibilités d'emplacements
    où le joueur peut jouer.
    :param plateau : list
    :param joueur: int
    :param menu: str
    :return value:list
        Liste des cases où il est possible de jouer
    """
    lst_pos = []

    # Detection à droite
    for i in range(len(plateau)):
        if plateau[i] == joueur:
            k = i
            x, y = coord_case(k+1)
            while plateau[k] == joueur and x < 8:
                k += 1
                x, y = coord_case(k+1)
            if plateau[k] != 0:
                while plateau[k] != 0 and plateau[k] != joueur and x < 8:
                    k += 1
                    x, y = coord_case(k+1)
                if plateau[k] == 0:
                    lst_pos.append(k+1)

        # Detection à gauche
    for i in range(len(plateau)):
        if plateau[i] == joueur:
            k = i
            x, y = coord_case(k+1)
            while plateau[k] == joueur and x > 1:
                k -= 1
                x, y = coord_case(k+1)
            if plateau[k] != 0:
                while plateau[k] != 0 and plateau[k] != joueur and x > 1:
                    k -= 1
                    x, y = coord_case(k+1)
                if plateau[k] == 0:
                    lst_pos.append(k+1)

            # Detection en bas
    for i in range(len(plateau)):
        if plateau[i] == joueur:
            k = i
            while plateau[k] == joueur and k < 56:
                k += 8
            if plateau[k] != 0:
                while plateau[k] != 0 and plateau[k] != joueur and k < 56:
                    k += 8
                if plateau[k] == 0:
                    lst_pos.append(k+1)

            # Detection en haut
    for i in range(len(plateau)):
        if plateau[i] == joueur:
            k = i
            while plateau[k] == joueur and k > 7:
                k -= 8
            if plateau[k] != 0:
                while plateau[k] != 0 and plateau[k] != joueur and k > 7:
                    k -= 8
                if plateau[k] == 0:
                    lst_pos.append(k+1)

            # Detection diagonale haut/gauche
    for i in range(len(plateau)):
        if plateau[i] == joueur:
            k = i
            x, y = coord_case(k+1)
            if x > 1 and y > 1:
                while plateau[k] == joueur and x > 1 and y > 1:
                    k -= 9
                    x, y = coord_case(k+1)
                if plateau[k] != 0:
                    while plateau[k] != 0 and plateau[k] != joueur and x > 1\
                            and y > 1:
                        k -= 9
                        x, y = coord_case(k+1)
                    if plateau[k] == 0:
                        lst_pos.append(k+1)

            # Detection diagonale haut/droite
    for i in range(len(plateau)):
        if plateau[i] == joueur:
            k = i
            x, y = coord_case(k+1)
            if x != 8 and y != 1:
                while plateau[k] == joueur and x != 8 and y != 1:
                    k -= 7
                    x, y = coord_case(k+1)
                if plateau[k] != 0:
                    while plateau[k] != 0 and plateau[k] != joueur and x != 8\
                          and y != 1:
                        k -= 7
                        x, y = coord_case(k+1)
                    if plateau[k] == 0:
                        lst_pos.append(k+1)

            # Detection diagonale bas/gauche
    for i in range(len(plateau)):
        if plateau[i] == joueur:
            k = i
            x, y = coord_case(k+1)
            if x != 1 and y != 8:
                while plateau[k] == joueur and x != 1 and y != 8:
                    k += 7
                    x, y = coord_case(k+1)
                if plateau[k] != 0:
                    while plateau[k] != 0 and plateau[k] != joueur and x > 1\
                            and y < 8:
                        k += 7
                        x, y = coord_case(k+1)
                    if plateau[k] == 0:
                        lst_pos.append(k+1)

            # Detection diagonale bas/droite
    for i in range(len(plateau)):
        if plateau[i] == joueur:
            k = i
            x, y = coord_case(k+1)
            if x != 8 and y != 8:
                while plateau[k] == joueur and x < 8 and y < 8:
                    k += 9
                    x, y = coord_case(k+1)
                if plateau[k] != 0 and x < 8 and y < 8:
                    while plateau[k] != 0 and plateau[k] != joueur and x < 8\
                            and y < 8:
                        k += 9
                        x, y = coord_case(k+1)
                    if plateau[k] == 0:
                        lst_pos.append(k+1)

    # Affichage des cases possibles
    if menu == 'jouer' or (menu == 'jouer_vs_ordi' and joueur == 1):
        for case in lst_pos:
            x, y = case_vers_pixel(coord_case(case))
            fltk.cercle(x, y, taille_case/4-5, remplissage='Yellow',
                        tag='supp')
    return lst_pos


def pions_a_retrourner(plateau, joueur, new_pion):
    """
    Fonction qui calcule tous les pions à retrourner en fonction
    du nouveau pion posé par l'un des joueurs.

    :param plateau: list
    :param joueur: int
    :param new_pion: int
        Correspond à la case du nouveau pion.
    :retrurn value: list
        Correspond à la liste de pions à retourner.
    """
    a_retourner = []
    temp = []
    # Detection par rapport au nouveau pion
    # Detection à droite
    k = new_pion  # case suivante en indice
    x, y = coord_case(new_pion)
    if x < 8:
        x, y = coord_case(k+1)
        while plateau[k] != joueur and plateau[k] != 0 and x < 8:
            temp.append(k)
            k += 1
            x, y = coord_case(k+1)
        if plateau[k] == 0 or (k == 8 and plateau[k] != joueur):
            temp = []
        else:
            a_retourner.extend(temp)
            temp = []

    # Detection à gauche
    k = new_pion - 2
    x, y = coord_case(k+1)
    if x > 1:
        while plateau[k] != joueur and plateau[k] != 0 and x > 1:
            temp.append(k)
            k -= 1
        if x == 1 and plateau[k] == joueur:
            temp.append(k)
        if plateau[k] == 0 or (x == 1 and plateau[k] != joueur):
            temp = []
        else:
            a_retourner.extend(temp)
            temp = []

    # Detection en bas
    k = new_pion + 7
    if k < 56:
        while plateau[k] != joueur and plateau[k] != 0 and k < 56:
            temp.append(k)
            k += 8
        if plateau[k] == 0 or (k >= 56 and plateau[k] != joueur):
            temp = []
        else:
            a_retourner.extend(temp)
            temp = []

    # Detection en haut
    k = new_pion - 9
    if k > 7:
        while plateau[k] != joueur and plateau[k] != 0 and k > 7:
            temp.append(k)
            k -= 8
        if plateau[k] == 0 or (plateau[k] <= 7 and plateau[k] != joueur):
            temp = []
        else:
            a_retourner.extend(temp)
            temp = []

    # Detection diagonale haut/gauche
    k = new_pion - 10
    x, y = coord_case(new_pion)
    if x > 1 and y > 1:
        x, y = coord_case(k+1)
        while plateau[k] != joueur and plateau[k] != 0 and x > 1 and y > 1:
            temp.append(k)
            k -= 9
            x, y = coord_case(k+1)
        if plateau[k] == 0 or ((x == 1 or y == 1) and plateau[k] != joueur):
            temp = []
        else:
            a_retourner.extend(temp)
            temp = []

    # Detection diagonale haut/droite
    k = new_pion - 8
    x, y = coord_case(new_pion)
    if x != 8 and y != 1:
        x, y = coord_case(k+1)
        while plateau[k] != joueur and plateau[k] != 0 and x != 8 and y != 1:
            temp.append(k)
            k -= 7
            x, y = coord_case(k+1)
        if plateau[k] == 0 or ((x == 8 or y == 1) and plateau[k] != joueur):
            temp = []
        else:
            a_retourner.extend(temp)
            temp = []

    # Detection diagonale bas/gauche
    k = new_pion + 6
    x, y = coord_case(new_pion)
    if x > 1 and y < 8:
        x, y = coord_case(k+1)
        while plateau[k] != joueur and plateau[k] != 0 and x > 1 and y < 8:
            temp.append(k)
            k += 7
            x, y = coord_case(k+1)
        if plateau[k] == 0 or ((x == 1 or y == 8) and plateau[k] != joueur):
            temp = []
        else:
            a_retourner.extend(temp)
            temp = []

    # Detection diagonale bas/droite
    k = new_pion + 8
    x, y = coord_case(new_pion)
    if x < 8 and y < 8:
        x, y = coord_case(k+1)
        while plateau[k] != joueur and plateau[k] != 0 and x < 8 and y < 8:
            temp.append(k)
            k += 9
            x, y = coord_case(k+1)
        if plateau[k] == 0 or ((x == 8 or y == 8) and plateau[k] != joueur):
            temp = []
        else:
            a_retourner.extend(temp)
            temp = []
    return a_retourner


def retourner(plateau, joueur, a_retourner):
    """
    Fonction qui permet de modifier la liste du plateau afin de retourner
    les pions.

    :param plateau: list
    :param joueur: int
    :param a_retourner: list
        Correspond aux cases à retrourner
    :retrun value: list
        Liste du plateau modifiée
    """
    for i in a_retourner:
        if joueur == 1:
            plateau[i] = 1
        else:
            plateau[i] = 2
    return plateau


def score(plateau):
    """
    Fonction qui permet de calculer combien de pions possèdent chaque joueur.

    :param plateau: list
    :return value: couple
    """
    blanc = 0
    noir = 0
    for i in plateau:
        if i == 1:
            blanc += 1
        elif i == 2:
            noir += 1
    return (blanc, noir)


def impossible(possible):
    """
    Fonction qui permet de savoir si un joueur n'a aucune possibilité de
    jouer.
    :param possible: lst
    :return value: bool
        Vrai si impossible de jouer et faux si il peut jouer.
    """

    if possible == []:
        return True
    else:
        return False


def detection_fin(plateau, score_blanc, score_noir):
    """
    Fonction qui permet de détecter la fin de la partie, donc si le
    plateau de jeu est rempli. Elle identifie aussi quel est le joueur
    possédant le plus de pions, et donc le vainqueur.

    :param plateau: list
    :param score_blanc: int
    :param score_noir: int

    :return value: str
    """

    if score_blanc == 0:
        return 'blanc perd'
    elif score_noir == 0:
        return 'noir perd'
    if 0 not in plateau:
        if score_blanc > score_noir:
            return 'noir perd'
        elif score_blanc < score_noir:
            return 'blanc perd'
        else:
            return 'egalite'
    else:
        return 'Continue'


def ordinateur(plateau, joueur, possible, score_blanc, score_noir, tour):
    """
    Fonction qui permet de jouer automatiquement, elle prend en fonction
    beaucoup de paramètre afin d'identifier les meilleurs coups possibles.

    :param plateau: list
    :param joueur: int
    :param possible: list
    :param score_blanc: int
    :param score_noir: int
    :param tour: int
    :return value: int
        Correspond à la case joué
    """

    best = [1, 8, 57, 64]
    # Pas encore utilisé
    # bad1 = [2, 9, 10]
    # bad2 = [7, 15, 16]      # bad si coin vide
    # bad3 = [49, 50, 58]
    # bad4 = [55, 56, 63]
    # good = [3, 4, 5, 6, 17, 25, 33, 41, 59, 60, 61, 62, 24, 32, 40, 48]
    if tour == 1:
        temp = randint(1, len(possible))
        case = possible[temp-1]
        return case

    if tour == 3:
        pos = []
        for i in possible:
            x, y = coord_case(i)
            if x > 2 and x < 7 and y > 2 and y < 7:
                pos.append(i)
            if len(pos) != 0:
                temp = randint(1, len(pos))
                case = pos[temp-1]
                return case

    else:
        for i in best:
            if i in possible:
                return i

        dico = {}
        for j in possible:
            simul = list(plateau)
            ajoute_pion(simul, j, 2)
            a_retourner = pions_a_retrourner(simul, 2, j)
            dico[j] = len(a_retourner)
        maxi = 0
        ind_maxi = None
        for k in dico:
            if maxi < dico[k]:
                maxi = dico[k]
                ind_maxi = k
        return ind_maxi


def affichage_cote(score_blanc, score_noir, joueur, menu, nom_1, nom_2):
    """
    Fonction qui permet d'afficher toute la partie à droite durant une partie,
    elle affiche les scores, la personne qui doit jouer, d'un bouton de pause,
    ainsi que (si vs ordinateur) 3 boutons permettant de choisir la vitesse
    à laquelle l'ordinateur joue.

    :param score_blanc: int
    :param score_noir: int
    :param joueur: int
    :param menu: str
    :param nom_1: str
    :param nom_2: str
    """

    # Fond
    fltk.rectangle(481, -2, 680, 480, epaisseur='10',
                   remplissage='light blue')
    # Info
    fltk.image(595, 460, FOND_REVERSI_MINI, ancrage='center')
    fltk.texte(580, 20, 'Informations', ancrage='center', taille=14)
    fltk.ligne(528, 29, 633, 29)
    # Score blanc
    fltk.cercle(510, 70, 13, couleur='snow', remplissage='white')
    fltk.texte(510, 70, score_blanc, taille=10, ancrage='center')
    fltk.texte(530, 60, nom_1, taille=12)
    # Score noir
    fltk.cercle(510, 105, 13, remplissage='black')
    fltk.texte(510, 105, score_noir, couleur='white', taille=10,
               ancrage='center')
    # Bouton quitter
    fltk.rectangle(635, 435, 660, 460, remplissage='orangered')
    fltk.ligne(640, 440, 655, 455)
    fltk.ligne(640, 455, 655, 440)

    if menu == 'jouer':
        fltk.texte(530, 95, nom_2, taille=12)
    elif menu == 'jouer_vs_ordi':
        fltk.texte(530, 97, 'Ordinateur', taille=12)
    # A qui le tour
    if joueur == 1 or (joueur == 2 and menu == 'jouer'):
        # Couleur bordure flèches
        if menu == 'jouer' and joueur == 1:
            color = 'white'
        elif menu == 'jouer' and joueur == 2:
            color = 'black'
        elif menu == 'jouer_vs_ordi' and joueur == 1:
            color = 'white'
        # Flèche haut
        fltk.rectangle(570, 235, 590, 275, remplissage='blue2',
                       epaisseur=3, couleur=color)
        fltk.polygone([(560, 270), (600, 270), (580, 290)],
                      remplissage='blue2', epaisseur=3, couleur=color)
        # Flèche bas
        fltk.rectangle(570, 345, 590, 385, remplissage='blue2',
                       epaisseur=3, couleur=color)
        fltk.polygone([(560, 350), (600, 350), (580, 330)],
                      remplissage='blue2', epaisseur=3, couleur=color)
        # Au joueur de jouer
        if menu == 'jouer_vs_ordi':
            fltk.texte(510, 300, 'A vous de jouer !', taille=14)

            # Boutons temps de jeu de l'ordi
            fltk.texte(500, 175, "Temps de jeu de l'ordinateur",
                       taille=10, ancrage='nw')
            fltk.rectangle(515, 200, 545, 220)
            fltk.texte(525, 202, '0s', taille=10, ancrage='nw')
            fltk.rectangle(565, 200, 595, 220)
            fltk.texte(568, 202, '1.5s', taille=10, ancrage='nw')
            fltk.rectangle(615, 200, 645, 220)
            fltk.texte(625, 202, '3s', taille=10, ancrage='nw')

        # Affiche du nom du joueur qui doit jouer
        elif menu == 'jouer' and joueur == 1:
            fltk.texte(579, 310, (str(nom_1) + ' !'),
                       taille=14, ancrage='center')
        elif menu == 'jouer' and joueur == 2:
            fltk.texte(579, 310, (str(nom_2) + ' !'),
                       taille=14, ancrage='center')


def pause(joueur, score_blanc, score_noir, nom_1, nom_2):
    """
    Fonction qui permet d'afficher de controler le menu pause. Il est
    composé de 3 boutons qui permettent de reprendre, d'abandonner ou de
    quitter en sauvegardant.

    :param joueur: int
    :param score_blanc: int
    :param score_noir: int
    :param nom_1: str
    :param nom_2: str

    :return value: str
        Sortie correspond à l'action possible des 3 boutons.
    """

    fltk.rectangle(90, 140, 390, 340, remplissage='white', tag='pause')
    if joueur == 1:
        fltk.texte(240, 160, (str(nom_1) + ','), taille=13,
                   tag='pause', ancrage='center')
    elif joueur == 2:
        fltk.texte(240, 160, (str(nom_2) + ','), taille=13,
                   ancrage='center', tag='pause')
    # Reprendre
    fltk.rectangle(190, 195, 290, 235, tag='pause')
    fltk.texte(240, 215, 'REPRENDRE', taille=12,
               police='Tw Cen MT Condensed Extra Bold', ancrage='center',
               tag='pause')
    # Abandonner (retour menu)
    fltk.rectangle(190, 245, 290, 285, tag='pause')
    fltk.texte(240, 265, 'ABANDONNER', taille=12,
               police='Tw Cen MT Condensed Extra Bold', ancrage='center',
               tag='pause')
    # Sauvegarder et quitter
    fltk.rectangle(190, 295, 290, 335, tag='pause')
    fltk.texte(240, 303, 'SAUVEGARDER', taille=12,
               police='Tw Cen MT Condensed Extra Bold', ancrage='center',
               tag='pause')
    fltk.texte(240, 316, 'ET', taille=12,
               police='Tw Cen MT Condensed Extra Bold', ancrage='center',
               tag='pause')
    fltk.texte(240, 329, 'QUITTER', taille=12,
               police='Tw Cen MT Condensed Extra Bold', ancrage='center',
               tag='pause')
    fltk.mise_a_jour()

    ev = fltk.attend_ev()
    ty = fltk.type_ev(ev)
    while ty != 'ClicGauche' and ty != 'Quitte':
        ev = fltk.attend_ev()
        ty = fltk.type_ev(ev)

    if ty == 'Quitte':
        return 'stop'
    elif ty == 'ClicGauche':
        x = fltk.abscisse(ev)
        y = fltk.ordonnee(ev)
        # Reprendre
        if x > 190 and x < 290 and y > 195 and y < 235:
            pass
        # Abandonner
        elif x > 190 and x < 290 and y > 245 and y < 285:
            return 'FIN'
        # Quitter et sauvegarder
        elif x > 190 and x < 290 and y > 295 and y < 335:
            return 'save'


def save(plateau, joueur, mode, nom_1, nom_2):
    """
    Fonction permettant d'ouvrir un fichier texte, et d'y écrire des
    informations permettant de sauvegarder les données d'une partie pour
    pour la reprendre plus tard (attention, une fermeture du porgramme
                                 écrase le fichier)
    :param plateau: list
    :param joueur: int
    :param mode: str
    :param nom_1: str
    :param nom_2: str
    """
    f = open('save.txt', 'w')
    chaine_plateau = ''
    for elem in plateau:
        chaine_plateau += str(elem)
    a_sauv = [chaine_plateau, str(joueur), mode, str(nom_1), str(nom_2)]
    for i in a_sauv:
        f.write(i + '\n')
    f.close()


def charger():
    """
    Fonction permettant d'ouvirir le fichier texte de la fonction précédente,
    et ainsi de récupérer les données de la partie quittée.

    return value: tuple
        Varibles des données nécessaires pour reprendre la partie.
    """
    f = open('save.txt', 'r')
    L = []
    for i in f:
        L.append(i.strip())
    f.close()

    tableau = []
    for j in L[0]:
        tableau.append(int(j))
    joueur = int(L[1])
    mode = L[2]
    nom_1 = L[3]
    nom_2 = L[4]
    return plateau, joueur, mode, nom_1, nom_2


def ecrire():
    """
    Fonction permettant d'utiliser le clavier afin de choisir des pseudos,
    mais ne l'affiche pas en temps réel. On peut y utiliser des caractères
    minuscules et les chiffres.

    :return value: couple de str
    """
    nom_1 = ''
    nom_2 = ''
    lettre = 'azertyuiopqsdfghjklmwxcvbn\
                1234567890'
    ty = 'Touche'
    while ty == 'Touche':
        ev = fltk.attend_ev()
        ty = fltk.type_ev(ev)
        for i in lettre:
            if fltk.touche_pressee(i):
                nom_1 += str(i)
    ty = 'Touche'
    while ty == 'Touche':
        ev = fltk.attend_ev()
        ty = fltk.type_ev(ev)
        for j in lettre:
            if fltk.touche_pressee(j):
                nom_2 += str(j)
    if nom_1 == '':
        nom_1 = 'Joueur 1'
    if nom_2 == '':
        nom_2 = 'Joueur 2'
    if nom_2 == nom_1:
        nom_2 += '_2'
    return(nom_1, nom_2)


def MENU():
    """
    Fonction permettant d'afficher le menu principal du jeu, qui contient 4
    boutons, qui permettent de lancer 1 contre 1, 1 vs ordinateur, ou de
    charger la partie précédente.
    """
    x = taille_case * largeur_plateau
    y = taille_case * hauteur_plateau
    fltk.image(0, 0, FOND_MENU, ancrage='nw')
    # Bouton 2 joueurs
    # fltk.rectangle(x/3+100, y/3, x/1.5+100, y/2, remplissage='Blue')
    fltk.image(x/3+100, y/3, BOUTON, ancrage='nw')
    fltk.texte(x/2+100, 5*y/12, "2 JOUEURS", ancrage='center', taille=18,
               police='Tw Cen MT Condensed Extra Bold', couleur='dark orange2')

    # Bouton vs ordi
    # fltk.rectangle(x/3+100, y/1.9, x/1.5+100, y/1.443, remplissage='Blue')
    fltk.image(x/3+100, y/1.9, BOUTON2, ancrage='nw')
    fltk.texte(x/2+100, 0.61*y, "        VS\nORDINATEUR", ancrage='center',
               taille=18, police='Tw Cen MT Condensed Extra Bold',
               couleur='dark orange2')

    # Bouton de lancement à partir d'une sauvegarde
    # fltk.rectangle(x/3+100, y/1.39, x/1.5+100, y/1.128, remplissage='Blue')
    fltk.image(x/3+100, y/1.39, BOUTON, ancrage='nw')
    fltk.texte(x/2+100, 0.8*y, 'SAUVEGARDE', ancrage='center', taille=18,
               police='Tw Cen MT Condensed Extra Bold', couleur='dark orange2')

    # autres images
    fltk.image(365, 120, FOND_REVERSI, ancrage='center')
    fltk.image(300, 470, NOMS, ancrage='center')

    # Bouton changement noms
    fltk.image(515, 265, CRAYON, ancrage='center')
    # fltk.rectangle(435, 175, 485, 225)


def MENU_fin(detec):
    """
    Fonction permettant d'afficher le menu de fin, il indique le vainqueur,
    et possède un bouton qui permet de revenir au menu principal.

    :param detec: str
        Indique le joueur perdant, ou égalité
    :return value: str
    """

    x = taille_case * largeur_plateau
    y = taille_case * hauteur_plateau
    fltk.image(0, 0, FOND_MENU, ancrage='nw')  # Fond vert
    fltk.image(365, 435, FOND_REVERSI, ancrage='center')  # Logo

    fltk.image(262, 160, BOUTON, ancrage='nw')  # Bouton Menu
    fltk.texte(343, 200, 'MENU', ancrage='center', taille=25,
               police='Tw Cen MT Condensed Extra Bold', couleur='dark orange2')
    # fltk.rectangle(262, 160, 422, 240)

    if detec == 'blanc perd':
        fltk.texte(x/2+100, y/5, 'Le joueur noir gagne !', taille=30,
                   police='Tw Cen MT Condensed Extra Bold', ancrage='center')
    elif detec == 'noir perd':
        fltk.texte(x/2+100, y/5, 'Le joueur blanc gagne !', taille=30,
                   police='Tw Cen MT Condensed Extra Bold', ancrage='center')
    elif detec == 'egalite':
        fltk.texte(x/2+100, y/5, 'Egalité !', taille=30,
                   police='Tw Cen MT Condensed Extra Bold', ancrage='center')

    val_clic = clic('FIN')
    if val_clic == 'stop':
        return 'stop'
    elif val_clic == 'MENU':
        return 'set'
    else:
        return 'FIN'


# ---------------------- BOUCLE DE JEU ------------------------------

fltk.cree_fenetre(taille_case * largeur_plateau + 200,
                  taille_case * hauteur_plateau)
menu = 'set'
temps_ordi = 1.5

# Boucle du programme
while menu != 'stop':

    # Boucle qui permet d'établir les variables par défaut et de les assignés
    while menu == 'set':
        plateau_defaut = [0, 0, 0, 0, 0, 0, 0, 0,     # liste qui représente
                          0, 0, 0, 0, 0, 0, 0, 0,     # le plateau de jeu (8x8)
                          0, 0, 0, 0, 0, 0, 0, 0,     # 1 = blanc
                          0, 0, 0, 1, 2, 0, 0, 0,     # 2 = noir
                          0, 0, 0, 2, 1, 0, 0, 0,     # 0 = vide
                          0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0]
        tour = 0
        joueur = 1
        nom_1 = 'Joueur 1'
        nom_2 = 'Joueur 2'
        a_retourner_defaut = ['temp']
        a_retourner = a_retourner_defaut.copy()

        plateau = plateau_defaut.copy()
        menu = 'MENU'

    # Boucle qui permet de récupérer les données de la partie précédente
    # quittée (si pas de partie précédente, une nouvelle partie se lance.)
    while menu == 'sauvegarde':
        plateau, joueur, mode, nom_1, nom_2 = charger()
        menu = mode
        break


# MENU PRINCIPAL
    while menu == 'MENU':
        menu = MENU()

        val_clic = clic('MENU')
        # Affichage de la personalisation des pseudos
        while val_clic == 'nom':
            fltk.rectangle(500, 100, 650, 230, tag='supp')
            fltk.ligne(500, 165, 650, 165, tag='supp')
            fltk.texte(450, 300, 'Entrer le nom du premier joueur\npuis '
                       + "clicr n'importe où,\n"+'ensuite entrer le second,'
                       + " et enfin,\nclicr pour valider.", taille=11,
                       tag='supp')
            fltk.polygone([(550, 295), (575, 295), (562.5, 270)],
                          couleur='red', tag='supp')
            fltk.texte(563, 285, '!', couleur='red', taille=12,
                       ancrage='center', tag='supp')
            fltk.texte(502, 237, '*Uniquement des lettres minuscules\n\
                       et chiffres.', taille=7, tag='supp')

            fltk.texte(578, 132, nom_1, taille=14,
                       ancrage='center', tag='supp')
            fltk.texte(578, 198, nom_2, taille=14,
                       ancrage='center', tag='supp')
            fltk.mise_a_jour()
            nom_1, nom_2 = ecrire()
            fltk.efface('supp')
            val_clic = clic('MENU')

        if val_clic == 'stop':
            menu = 'stop'
        elif val_clic == 'jouer':
            menu = 'jouer'
        elif val_clic == 'jouer_vs_ordi':
            menu = 'jouer_vs_ordi'
        elif val_clic == 'sauvegarde':
            menu = 'sauvegarde'
        else:
            menu = 'MENU'


# PARTIE EN COURS
    while menu == 'jouer' or menu == 'jouer_vs_ordi':
        fltk.efface_tout()
        affiche_plateau()
        affiche_pions(plateau)
        score_blanc, score_noir = score(plateau)
        affichage_cote(score_blanc, score_noir, joueur, menu, nom_1, nom_2)
        possible = possibilite(plateau, joueur, menu)
        fltk.mise_a_jour()
        if menu == 'jouer' or (menu == 'jouer_vs_ordi' and joueur == 1):
            val_clic = clic('jouer')
        fin_boucle = False
        while type(val_clic) == str and val_clic != 'stop':
            # Changement temps de jeu ordinateur
            if menu == 'jouer_vs_ordi':
                if val_clic == '0s':
                    temps_ordi = 0
                elif val_clic == '1.5s':
                    temps_ordi = 1.5
                elif val_clic == '3s':
                    temps_ordi = 3

            # Bouton pause
            if val_clic == 'pause':
                val_pause = pause(joueur, score_blanc,
                                  score_noir, nom_1, nom_2)
                if val_pause == 'FIN':
                    if joueur == 1:
                        detec = 'blanc perd'
                    elif joueur == 2:
                        detec = 'noir perd'
                    menu = 'FIN'
                    fin_boucle = True
                    break
                elif val_pause == 'save':
                    save(plateau, joueur, menu, nom_1, nom_2)
                    menu = 'MENU'
                    fin_boucle = True
                    break
                else:
                    fltk.efface('pause')
            val_clic = clic('jouer')

        if val_clic == 'stop':
            menu = 'stop'
            break
        if fin_boucle:
            pass
        else:
            detec = detection_fin(plateau, score_blanc, score_noir)
            if detec == 'Continue':
                if impossible(possible) is False:
                    if menu == 'jouer' or (menu == 'jouer_vs_ordi' and
                                           joueur == 1):
                        case = coordCase_vers_case(val_clic)
                        while case not in possible:
                            val_clic = clic('jouer')
                            if val_clic == 'stop':
                                menu = 'stop'
                                break
                            else:
                                case = coordCase_vers_case(val_clic)
                    elif joueur == 2 and menu == 'jouer_vs_ordi':
                        fltk.attente(temps_ordi)
                        case = ordinateur(plateau, joueur, possible,
                                          score_blanc, score_noir, tour)

                    ajoute_pion(plateau, case, joueur)
                    a_retourner = pions_a_retrourner(plateau, joueur, case)
                    fltk.efface('supp')
                    plateau = retourner(plateau, joueur, a_retourner)
                    fltk.mise_a_jour()

            elif detec == 'blanc perd' or detec == 'noir perd'\
                    or detec == 'egalite':
                menu = 'FIN'
                fltk.efface_tout()
            # joueur suivant
            if joueur == 1:
                joueur = 2
            else:
                joueur = 1
            tour += 1

# MENU DE FIN DE PARTIE
    while menu == 'FIN':
        menu = MENU_fin(detec)
        fltk.mise_a_jour()
fltk.ferme_fenetre()
# import doctest
# print(doctest.testmod())
