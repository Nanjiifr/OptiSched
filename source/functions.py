import random

class Graphe:
    def __init__(self, graphe):
        """
        Initialise un graphe avec la matrice donnée.

        Args:
            graphe (list): Matrice d'adjacence représentant le graphe.

        Raises:
            AssertionError: Si la matrice n'est pas carrée.
        """
        if graphe != []:
            for i in range(len(graphe)):
                assert len(graphe) == len(graphe[i]), "Revoir la matrice !"
        self.graphe = graphe

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères du graphe.

        Returns:
            str: Représentation du graphe.
        """
        matrice = ""
        for i in self.graphe:
            for j in i:
                matrice += str(j) + "\t"
            matrice += "\n"
        return matrice

    def ajouter_sommet(self):
        """
        Ajoute un sommet au graphe en lui ajoutant une ligne et une colonne dans la matrice d'adjacence.
        """
        newS = [0]
        for s in range(len(self.graphe)):
            self.graphe[s].append(0)
            newS.append(0)
        self.graphe.append(newS)

    def ajouter_arrete(self, sommet1:int, sommet2:int):
        """
        Ajoute une arête entre deux sommets du graphe.

        Args:
            sommet1 (int): Indice du premier sommet.
            sommet2 (int): Indice du deuxième sommet.

        Raises:
            AssertionError: Si les indices des sommets ne sont pas valides.
        """
        self.verif(sommet1, sommet2)
        self.graphe[sommet1][sommet2] = 1
        self.graphe[sommet2][sommet1] = 1

    def verif(self, *args):
        """
        Vérifie si les arguments sont des entiers valides.

        Args:
            *args: Arguments à vérifier.

        Raises:
            AssertionError: Si un argument n'est pas un entier valide.
        """
        for i in args:
            assert type(i) == int, "Tous les arguments doivent être des entiers !"
            assert i < len(self.graphe), "L'élément n'est pas dans la matrice !"

    def est_adjacent(self, sommet1:int, sommet2:int):
        """
        Vérifie si deux sommets sont adjacents dans le graphe.

        Args:
            sommet1 (int): Indice du premier sommet.
            sommet2 (int): Indice du deuxième sommet.

        Returns:
            bool: True si les sommets sont adjacents, False sinon.

        Raises:
            AssertionError: Si les indices des sommets ne sont pas valides.
        """
        self.verif(sommet1, sommet2)
        return self.graphe[sommet1][sommet2] == 1

    def mat2dico(self):
        """
        Convertit la matrice d'adjacence en un dictionnaire d'adjacence.

        Returns:
            dict: Dictionnaire représentant les adjacences du graphe.
        """
        dico = {}
        for i in range(len(self.graphe)):
            dico[i] = []
            for j in range(len(self.graphe)):
                if self.graphe[i][j] == 1:
                    dico[i].append(j)
        return dico

    def degre_sommet(self, sommet:int):
        """
        Calcule le degré d'un sommet et ses successeurs.

        Args:
            sommet (int): Indice du sommet.

        Returns:
            tuple: Le degré du sommet et la liste de ses successeurs.
        """
        lsucess = self.mat2dico()
        deg = len(lsucess[sommet])
        return deg, lsucess[sommet]

    def colorWP(self):
        """
        Applique l'algorithme de coloration de graphes Welsh-Powell.

        Returns:
            list: Liste des couleurs attribuées à chaque sommet.
        """
        colors = [i for i in range(0, 100)]
        sommets = {i: self.degre_sommet(i)[1] for i in range(len(self.graphe))}
        sommets = sorted(sommets.keys(), key=lambda x: len(sommets[x]), reverse=True)
        s_coul = {i: "" for i in range(len(self.graphe))}
        while len(sommets) != 0:
            s_coul[sommets[0]] = colors[0]
            som_adj = [sommets[0]]
            for i in range(1, len(sommets)):
                if all(
                    not self.est_adjacent(sommets[i], som_adj[j])
                    for j in range(len(som_adj))
                ):
                    som_adj.append(sommets[i])
                    s_coul[sommets[i]] = colors[0]
            del colors[0]
            for i in som_adj:
                del sommets[sommets.index(i)]
            som_adj = []
        return [s_coul[i] for i in range(len(self.graphe))]

def color_graphe(classe_prof:list):
    """
    Colore le graphe des classes des professeurs.

    Args:
        classe_prof (list): Liste des classes des professeurs.

    Returns:
        list: Liste des couleurs attribuées à chaque classe.
    """
    graphe = Graphe([])
    for i in range(len(classe_prof)):
        graphe.ajouter_sommet()

    for i in range(len(classe_prof)):
        for j in range(len(classe_prof)):
            if (
                classe_prof[i][0] == classe_prof[j][0]
                or classe_prof[i][1] == classe_prof[j][1]
            ):
                graphe.ajouter_arrete(i, j)

    return graphe.colorWP()

def rep_jour(classe_prof:list, couleurs:list, samedi:bool):
    """
    Génère un emploi du temps pour les classes des professeurs.

    Args:
        classe_prof (list): Liste des classes des professeurs.
        couleurs (list): Liste des couleurs attribuées à chaque classe.
        samedi (bool): Indique si le samedi est inclus dans l'emploi du temps.

    Returns:
        list: Emploi du temps généré.
    """
    edt = []
    if samedi:
        mat_jour = (max(couleurs) + 1) // 5
        mat_sam = (max(couleurs) + 1) % 5
        for i in range(5):
            matieres_j = []
            for j in range(mat_jour):
                cours = []
                col = couleurs[random.randint(0, len(couleurs) - 1)]
                while col == -1:
                    col = couleurs[random.randint(0, len(couleurs) - 1)]
                for k in range(len(couleurs)):
                    if couleurs[k] == col:
                        cours.append(classe_prof[k])
                        couleurs[k] = -1
                matieres_j.append(cours)
            edt.append(sorted(matieres_j, key=lambda x: len(x), reverse=True))

        col2 = []
        for i in range(len(couleurs)):
            if couleurs[i] != -1:
                col2.append(couleurs[i])

        edt.append([])

        for i in range(len(col2)):
            col = col2[i]
            cours = []
            for j in range(len(couleurs)):
                if couleurs[j] == col:
                    cours.append(classe_prof[j])
                    couleurs[j] = -1
            if cours != []:
                edt[5].append(cours)
        edt_mer = edt[4]
        edt[4] = edt[2]
        edt[2] = edt_mer
    else:
        mat_jour = (max(couleurs) + 1) // 4
        mat_mer = (max(couleurs) + 1) % 4
        for i in range(4):
            matieres_j = []
            for j in range(mat_jour):
                cours = []
                col = couleurs[random.randint(0, len(couleurs) - 1)]
                while col == -1:
                    col = couleurs[random.randint(0, len(couleurs) - 1)]
                for k in range(len(couleurs)):
                    if couleurs[k] == col:
                        cours.append(classe_prof[k])
                        couleurs[k] = -1
                matieres_j.append(cours)
            edt.append(sorted(matieres_j, key=lambda x: len(x), reverse=True))

        col2 = []
        for i in range(len(couleurs)):
            if couleurs[i] != -1:
                col2.append(couleurs[i])

        edt.append([])

        for i in range(len(col2)):
            col = col2[i]
            cours = []
            for j in range(len(couleurs)):
                if couleurs[j] == col:
                    cours.append(classe_prof[j])
                    couleurs[j] = -1
            if cours != []:
                edt[4].append(cours)
        edt_mer = edt[4]
        edt[4] = edt[2]
        edt[2] = edt_mer
    return edt

def reform(edt:list, dico_prof:dict):
    """
    Réorganise l'emploi du temps généré.

    Args:
        edt (list): Emploi du temps généré.
        dico_prof (dict): Dictionnaire des professeurs.

    Returns:
        list: Emploi du temps réorganisé.
    """
    edt_form = []
    for jour in range(len(edt)):
        for heure in range(len(edt[jour])):
            for cours in range(len(edt[jour][heure])):
                if heure + 8 >= 12:
                    edt_form.append(
                        [
                            dico_prof[edt[jour][heure][cours][1]][0],
                            edt[jour][heure][cours][1],
                            jour,
                            heure + 9,
                            edt[jour][heure][cours][-1],
                            edt[jour][heure][cours][0]
                        ]
                    )
                else:
                    edt_form.append(
                        [
                            dico_prof[edt[jour][heure][cours][1]][0],
                            edt[jour][heure][cours][1],
                            jour,
                            heure + 8,
                            edt[jour][heure][cours][-1],
                            edt[jour][heure][cours][0]
                        ]
                    )

    return edt_form

def edt_dico(edt_form:list):
    """
    Convertit l'emploi du temps réorganisé en un dictionnaire.

    Args:
        edt_form (list): Emploi du temps réorganisé.

    Returns:
        dict: Dictionnaire représentant l'emploi du temps.
    """
    edt_dico = {}
    for i in range(len(edt_form)):
        if not edt_form[i][-1] in edt_dico.keys():
            edt_dico[edt_form[i][-1]] = []
        edt_dico[edt_form[i][-1]].append(edt_form[i][0:-1:])
    return edt_dico

def edt_prof(edt_dico:dict):
    """
    Génère un emploi du temps pour chaque professeur.

    Args:
        edt_dico (dict): Dictionnaire représentant l'emploi du temps.

    Returns:
        dict: Dictionnaire des emplois du temps des professeurs.
    """
    edt_prof = {}
    for classe in edt_dico.keys():
        for cours in edt_dico[classe]:
            if not cours[1] in edt_prof.keys():
                edt_prof[cours[1]]=[]
            edt_prof[cours[1]].append(cours[:-1:])
    return edt_prof

#Associe dans DicoClasseMatiere_prof les prof(info) et les matières/classes(clés)
def ProfParClasse(fichierclasse:list, fichierprof:list, dicoIClasse:dict, dicoEdt:dict):
    """
    Associe à chaque classe les professeurs pour chaque matière en fonction de l'emploi du temps.

    Args:
        fichierclasse (list): Liste des classes.
        fichierprof (list): Liste des professeurs.
        dicoIClasse (dict): Dictionnaire associant chaque classe à un identifiant.
        dicoEdt (dict): Dictionnaire représentant l'emploi du temps.

    Returns:
        dict: Dictionnaire associant chaque classe à ses professeurs pour chaque matière.
    """
    # Initialisation des variables
    DicoClasseMatiere_Professeur = {}
    dicoProf = {prof[0]: (prof[1], int(prof[2])) for prof in fichierprof[1:]}
    matierevariable = ['spe1', 'spe2', 'spe3', 'lv1', 'lv2']

    # Itération sur les classes
    for i in range(len(fichierclasse) - 1):
        IClasse = dicoIClasse[fichierclasse[i + 1][1]]
        DicoClasseMatiere_Professeur[fichierclasse[i + 1][0]] = {}

        # Récupération des spécialités et langues
        spe1, spe2, spe3 = fichierclasse[i + 1][2:5]
        lv1, lv2 = fichierclasse[i + 1][5], fichierclasse[i + 1][6]

        # Itération sur les matières de l'emploi du temps de la classe
        for cle, heure in dicoEdt[IClasse].items():
            # Pour les spécialités et les langues
            if cle in matierevariable:
                if cle == "spe1":
                    mat = spe1
                elif cle == "spe2":
                    mat = spe2
                elif cle == "spe3" and IClasse == 1:
                    mat = spe3
                elif cle == "lv1":
                    mat = lv1
                elif cle == "lv2":
                    mat = lv2
            else:
                mat = cle

            # Le cas hlp
            if mat == "hlp": 
                if IClasse == 1:
                    mat = "philosophie"
                else:
                    mat = "francais"

            # Récupération des professeurs pouvant enseigner cette matière
            profs = [prof[0] for prof in fichierprof[1::] if prof[1] == mat]

            # Cas où il n'y a pas de professeur pour cette matière
            if not profs:
                print("Pas de prof pour la matière:", mat)
                return False

            # Sélection aléatoire du professeur parmi ceux disponibles
            profs = sorted(profs, key= lambda x: dicoProf[x][1], reverse=True)
            prof_selected = None
            for prof in profs:
                if dicoProf[prof][1] >= heure:
                    prof_selected = prof
                    break
            
            # Vérification si un professeur a été sélectionné
            if not prof_selected:
                print("Aucun prof disponible pour la matière:", mat)
                return False
            
            # Mise à jour du nombre d'heures disponibles pour le professeur sélectionné
            dicoProf[prof_selected] = (dicoProf[prof_selected][0], dicoProf[prof_selected][1] - heure)

            # Assignation du professeur à la matière pour cette classe
            DicoClasseMatiere_Professeur[fichierclasse[i + 1][0]][mat] = prof_selected

    return DicoClasseMatiere_Professeur



#Les hlp ont 3h/2h de francais, 3h/2h de philo, donc le progamme normal ne fonctionne pas pour eux. 
def cashlp(Ic:int,classe_prof:list,c:str,DicoClasseMatiere_Professeur:dict):
    """
    Génère les cours de HLP pour une classe donnée.

    Args:
        Ic (int): Identifiant de la classe.
        classe_prof (list): Liste des cours de la classe.
        c (str): Nom de la classe.
        DicoClasseMatiere_Professeur (dict): Dictionnaire associant chaque classe à ses professeurs pour chaque matière.

    Returns:
        list: Liste des cours mise à jour.
    """
    proffrancais = DicoClasseMatiere_Professeur[c]["francais"]
    profphilo = DicoClasseMatiere_Professeur[c]["philosophie"]
    if Ic == 0: n=3
    else: n=2
    for i in range(n):
        classe_prof.append((c,proffrancais))
        classe_prof.append((c,profphilo))
    return classe_prof
    
def ListeClasseProf(DicoClasseMatiere_Professeur:dict,dicoEdt:dict,dicoClasse:dict,dicoIClasse:dict):
    """
    Génère la liste des cours pour chaque classe.

    Args:
        DicoClasseMatiere_Professeur (dict): Dictionnaire associant chaque classe à ses professeurs pour chaque matière.
        dicoEdt (dict): Dictionnaire représentant l'emploi du temps.
        dicoClasse (dict): Dictionnaire associant chaque classe à ses caractéristiques.
        dicoIClasse (dict): Dictionnaire associant chaque classe à un identifiant.

    Returns:
        list: Liste des cours pour chaque classe.
    """
    classe_prof = []
    langue = ['espagnol','anglais','allemand','chinois']
    for classe,dico in DicoClasseMatiere_Professeur.items():
        Iclasse = dicoIClasse[dicoClasse[classe][0]]
        for matière,prof in dico.items():
            if matière in langue:
                matière = 'lv1'
            nbheure = dicoEdt[Iclasse][matière]
            for i in range(nbheure):
                classe_prof.append((classe,prof))
        # Cas des spé de la Terminale
        if Iclasse == 0:
            spe1 = dicoClasse[classe][1]
            if spe1 == "hlp": classe_prof = cashlp(Iclasse,classe_prof,classe,DicoClasseMatiere_Professeur)
            else: 
                prof = DicoClasseMatiere_Professeur[classe][spe1]
                for i in range(6):
                    classe_prof.append((classe,prof))
                
            spe2 = dicoClasse[classe][2]
            if spe2 == "hlp": classe_prof = cashlp(Iclasse,classe_prof,classe,DicoClasseMatiere_Professeur)
            else: 
                prof = DicoClasseMatiere_Professeur[classe][spe2]
                for i in range(6):
                    classe_prof.append((classe,prof))
        # Cas des spé de la Première
        if Iclasse == 1:
            spe1 = dicoClasse[classe][1]
            if spe1 == "hlp": classe_prof = cashlp(Iclasse,classe_prof,classe,DicoClasseMatiere_Professeur)
            else: 
                prof = DicoClasseMatiere_Professeur[classe][spe1]
                for i in range(4):
                    classe_prof.append((classe,prof))
               
            spe2 = dicoClasse[classe][2]
            if spe2 == "hlp": classe_prof = cashlp(Iclasse,classe_prof,classe,DicoClasseMatiere_Professeur)
            else: 
                prof = DicoClasseMatiere_Professeur[classe][spe2]
                for i in range(4):
                    classe_prof.append((classe,prof))
                
            spe3 = dicoClasse[classe][3]
            if spe3 == "hlp": classe_prof = cashlp(Iclasse,classe_prof,classe,DicoClasseMatiere_Professeur)
            else: 
                prof = DicoClasseMatiere_Professeur[classe][spe3]
                for i in range(4):
                    classe_prof.append((classe,prof))
    return classe_prof

#Fonction qui attribue les cours à une salle
def attribuer_salle(EDT:list, dicoProf:dict, dicoSalle:dict, fichiersalle:list):
    """
    Attribue une salle à chaque cours dans l'emploi du temps.

    Args:
        EDT (list): Emploi du temps.
        dicoProf (dict): Dictionnaire associant chaque professeur à sa matière.
        dicoSalle (dict): Dictionnaire associant chaque salle à sa spécialité.
        fichiersalle (list): Liste des salles disponibles.

    Returns:
        list: Emploi du temps mis à jour avec les salles attribuées à chaque cours.
    """
    # Dictionnaire pour mémoriser les salles utilisées
    memoire = set()

    # Dictionnaire pour les salles associables avec certaines matières
    spesalle = {"svt": [], "physique": [], "nsi": [], "si": [], "eps": []}
    for salle, spe in dicoSalle.items():
        if spe in spesalle.keys():
            spesalle[spe].append(salle)

    for jour in range(len(EDT)):
        for heure in range(len(EDT[jour])):
            memoireheure = set()
            for cours in range(len(EDT[jour][heure])):
                professeur = dicoProf[EDT[jour][heure][cours][1]]
                matiere = professeur[0]

                # Si la matière est spéciale et a une salle associée
                if matiere in spesalle.keys() and spesalle[matiere]:
                    salle = spesalle[matiere][0]
                    for s in spesalle[matiere]:
                        if s not in memoireheure:
                            salle = s
                            break
                    else:
                        print("Pas assez de salles spécialisées pour", matiere)
                        return False
                else:
                    # Choix de la salle standard
                    salle = None
                    for i in range(1, len(fichiersalle)):
                        if fichiersalle[i][0] not in memoireheure:
                            salle = fichiersalle[i][0]
                            break
                    if salle is None:
                        print("Pas assez de salles disponibles pour", matiere)
                        return False

                # Attribution de la salle au cours en reconstruisant le tuple avec la salle
                cours_attribue = EDT[jour][heure][cours] + (salle,)
                EDT[jour][heure][cours] = cours_attribue
                memoireheure.add(salle)

    return EDT