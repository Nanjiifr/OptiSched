from tkinter import *
from tkinter import ttk


# main : fenêtre principale (la seule en fait)
def initfenetre():
    main = Tk()
    main.title("Emploi du temps")
    main.geometry('1050x600')
    main.resizable(True, True) 
    return main


# Fonctions utilitaires
# Fonction permettant d'entrer des couleurs rgb compatibles avec Tkinter
def rgb_convert(rgb):
    return "#%02x%02x%02x" % rgb  

# Efface tout les enfants (donc tous les éléments) de la fenetre main
def efface_fenetre(main):
    for c in main.winfo_children():
        c.destroy()


# Dico qui associe chaque matière à une couleur (interface graphique uniquement)
matières_couleurs = {'si':rgb_convert((120,120,120)),'math': rgb_convert((240,120,100)),'ses' : rgb_convert((140,250,150)),'nsi':rgb_convert((10,60,140)),'physique' : rgb_convert((220,140,240)),'allemand':rgb_convert((230,190,190)),'svt':rgb_convert((160,245,180)),'hist-geo':rgb_convert((160,170,240)),'anglais':rgb_convert((130,200,100)),'eps':rgb_convert((230,230,100)),'francais':rgb_convert((140,230,250)),'espagnol':rgb_convert((20,200,120)),'philosophie':rgb_convert((230,160,100))}
# Dico qui associe chaque classe à une couleur. Les secondes sont dans les tons rouges, les premières dans les tons verts, et les terminales dans les tons bleus
classes_couleurs = {"S1":'Maroon',"S2" : "DarkOrange", "S3" : "OrangeRed","S4":"Chocolate","S5":"Gold","S6":"Salmon","S7":"HotPink4","S8":"Coral2","P1":"LimeGreen","P2":"SpringGreen","P3":"Chartreuse","P4":"YellowGreen","P5":"Green","P6":"PaleGreen1","P7":"DarkOliveGreen1","P8":"LimeGreen","T1":"LightSteelBlue1","T2":"BlueViolet","T3":"CadetBlue1","T4":"Cyan","T5":"DarkOrchid","T6":"DeepSkyBlue","T7":"RoyalBlue2","T8":"Indigo"}



# liste des noms de classes
liste_niveaux = ["Seconde","Première","Terminale","Professeurs"]
# liste des numéros de classe
liste_noms = ["1","2","3","4","5","6","7","8"]


# Crée une section regroupant les boutons du menu principal
def create_menu_edt(main,edt,edt_dico,liste_profs,edt_prof,edt_form):
    """
    

    Parameters
    ----------
    main : WINDOW
        Fenetre du programme.
    edt : CANVAS
        Canvas ou sera affiché l'emplois du temps
    edt_dico : DICTIONNAIRE
        Emplois du temps des élèves
    liste_profs : LIST
        Liste des noms de tous les professeurs.
    edt_prof : DICTIONNAIRE
        Emplois du temps des professeurs
    edt_form : DICTIONNAIRE
        Dictionnaire global des emplois du temps

    Returns
    -------
    menu : FRAME
        Zone d'affichage avec les boutons du menu.

    """
    # Crée une section contenant le menu 
    menu = ttk.Frame(main, padding=10)
    menu.grid(column=1,row=0)
    
    description = Label(menu,text="Emploi du temps de la \nSeconde 1 ")
    description.grid(column = 0,row=0)
    # Barre déroulante de selection du niveau à afficher
    select_niv = StringVar(main)
    select_niv.set(liste_niveaux[0])
    
    selecteur_niv = OptionMenu(menu, select_niv, *liste_niveaux)
    selecteur_niv.config(width=20, font=("Helvetica", 12))
    selecteur_niv.grid(column = 0, row = 1)
    
    # Menu déroulant du numéro de la classe à afficher
    select_nb = StringVar(main)
    select_nb.set(liste_noms[0])
    
    selecteur_nb = OptionMenu(menu, select_nb, *liste_noms)
    selecteur_nb.config(width=20, font=("Helvetica", 12))
    selecteur_nb.grid(column = 0, row = 2)
    
    
    # Affiche l'emplois du temps en fonction des informations rentrées dans le menu
    def rafraichir_infos(*args):
        if select_niv.get() == 'Professeurs':
            if select_nb.get() not in edt_prof :
                description.config(text= "Ce professeur n'a \npas de cours",foreground="red")
            else :     
                description.config(text= f'Emploi du temps de \n{select_niv.get()} {select_nb.get()}',foreground="black")
                affiche_profs(edt_prof[select_nb.get()],edt,edt_form)
            
            # Met à jour le menu déroulant
            selecteur_nb = OptionMenu(menu, select_nb, *liste_profs)
            selecteur_nb.config(width=20, font=("Helvetica", 12))
            selecteur_nb.grid(column = 0, row = 2)
            if select_nb.get() not in liste_profs:
                select_nb.set(liste_profs[0])
                
            

            
        # Affiche l'emplois du temps d'une classe et ses informations
        elif str(select_niv.get()[0]+select_nb.get()) in edt_dico:
            affiche_cours(edt_dico[str(select_niv.get()[0]+select_nb.get())],edt)
            # Affiche le nom de la classe dans le label au dessus des menus déroulants
            description.config(text= f'Emploi du temps de la \n{select_niv.get()} {select_nb.get()}',foreground="black")
            
            # Met à jour le menu déroulant
            selecteur_nb = OptionMenu(menu, select_nb, *liste_noms)
            selecteur_nb.config(width=20, font=("Helvetica", 12))
            selecteur_nb.grid(column = 0, row = 2)
            if select_nb.get() in liste_profs:
                select_nb.set(liste_noms[0])



        # Dans le cas où la classe sélectionnée n'existe pas    
        else : 
            description.config(text= "Cette classe n'existe pas\n",foreground="red")
            selecteur_nb = OptionMenu(menu, select_nb, *liste_noms)
            selecteur_nb.config(width=20, font=("Helvetica", 12))
            selecteur_nb.grid(column = 0, row = 2)
            if select_nb.get() in liste_profs:
                select_nb.set(liste_noms[0])

        
    # Appelle la fonction pour rafraichir l'emplois du temps quand les listes
    # déroulantes sont modifiées
    select_niv.trace("w",rafraichir_infos)
    select_nb.trace("w",rafraichir_infos)
    return menu


# Fonction qui affiche les rectangles des différentes heures de cours
def affiche_cours(edt_liste,edt):
    """

    Parameters
    ----------
    edt_liste : LIST
        Liste des horraires des cours.
    edt : CANVA
        Zone où est affiché l'emplois du temps.

    Returns
    -------
    None.

    """
    
    # Crée des formes pour cacher le précédent emplois du temps
    margeX,margeY = 50,50
    for j in range(6):
        for i in range(11):
            if not i==4:
                edt.create_rectangle((120*j+margeX,50*i+margeY,120*(j+1)+margeX,50*i+margeY+49), fill=rgb_convert((235,235,235)),outline=rgb_convert((235,235,235)))
    for i in range(11):
        edt.create_line((0+margeX, 50*i+margeY), (800+margeX, 50*i+margeY), width=1, fill='black')
        
    
    for i in range(len(edt_liste)):
        # Assertions pour les erreurs de saisie des données
        assert edt_liste[i][0] in matières_couleurs, "Erreur d'association des couleurs aux matières dans l'affichage (voir dico matière_couleur)"
        assert 6>=edt_liste[i][2]>=0, f"Jour de la semaine impossible pour {edt_liste[i][0]} : {edt_liste[i][1]}"
        assert 18>=edt_liste[i][3]>=8, f"Heure impossible pour {edt_liste[i][0]} le jour {edt_liste[i][1]} : {edt_liste[i][2]} "

        # Affiche les matières
        couleur = matières_couleurs[edt_liste[i][0]]
        edt.create_rectangle((120*edt_liste[i][2]+margeX,50*(edt_liste[i][3]-8)+margeY,120*(edt_liste[i][2]+1)+margeX,50*(edt_liste[i][3]-8)+margeY+50), fill=couleur,outline=couleur)
        edt.create_text((margeX+60+(120*edt_liste[i][2]), 50*(edt_liste[i][3]-8)+margeY+10),text=edt_liste[i][0].upper(),fill="black",font='tkDefaeultFont 12')
        edt.create_text((margeX+55+(120*edt_liste[i][2]), 50*(edt_liste[i][3]-8)+margeY+25),text=edt_liste[i][4],fill="black",font='tkDefaeultFont 9')
        edt.create_text((margeX+55+(120*edt_liste[i][2]), 50*(edt_liste[i][3]-8)+margeY+40),text=edt_liste[i][1],fill="black",font='tkDefaeultFont 9')
        
        
# Fonction qui affiche les rectangles des différentes heures des professeurs
def affiche_profs(edt_liste,edt,edt_form):
    """

    Parameters
    ----------
    edt_liste : LIST
        Liste des horraires des cours.
    edt : CANVA
        Zone où est affiché l'emplois du temps.

    Returns
    -------
    None.

    """
    
    # Crée des formes pour cacher le précédent emplois du temps
    margeX,margeY = 50,50
    for j in range(6):
        for i in range(11):
            if not i==4:
                edt.create_rectangle((120*j+margeX,50*i+margeY,120*(j+1)+margeX,50*i+margeY+49), fill=rgb_convert((235,235,235)),outline=rgb_convert((235,235,235)))
    for i in range(11):
        edt.create_line((0+margeX, 50*i+margeY), (800+margeX, 50*i+margeY), width=1, fill='black')
        
    

    
                
    
    
    for i in range(len(edt_liste)):
        # Assertions pour les erreurs de saisie des données
        assert edt_liste[i][0] in matières_couleurs, "Erreur d'association des couleurs aux matières dans l'affichage (voir dico matière_couleur)"
        assert 6>=edt_liste[i][2]>=0, f"Jour de la semaine impossible pour {edt_liste[i][0]} : {edt_liste[i][1]}"
        assert 18>=edt_liste[i][3]>=8, f"Heure impossible pour {edt_liste[i][0]} le jour {edt_liste[i][1]} : {edt_liste[i][2]} "

        # Affiche les matières
        classe_actuelle = ""
        for j in range(len(edt_form)):
            if edt_liste[i][1] == edt_form[j][1] and edt_liste[i][2] == edt_form[j][2] and edt_liste[i][3] == edt_form[j][3]:
                 # Attribue la classe et la salle aux professeurs pour leurs différentes heures de cour
                classe_actuelle = edt_form[j][5] 
                salle_actuelle = edt_form[j][4] 
                
                couleur = classes_couleurs[edt_form[j][5]]
        if classe_actuelle == "":
            couleur = rgb_convert((120,140,140))
            
            
        edt.create_rectangle((120*edt_liste[i][2]+margeX,50*(edt_liste[i][3]-8)+margeY,120*(edt_liste[i][2]+1)+margeX,50*(edt_liste[i][3]-8)+margeY+50), fill=couleur,outline=couleur)
        edt.create_text((margeX+60+(120*edt_liste[i][2]), 50*(edt_liste[i][3]-8)+margeY+10),text=classe_actuelle,fill="black",font='tkDefaeultFont 12')
        edt.create_text((margeX+55+(120*edt_liste[i][2]), 50*(edt_liste[i][3]-8)+margeY+40),text=salle_actuelle,fill="black",font='tkDefaeultFont 9')

        
# Crée le canvas où seront affichés les emplois du temps    
def creerCanvasImage(main):
    """
    

    Parameters
    ----------
    main : WINDOW
        Fenetre où s'affiche le programme

    Returns
    -------
    edt : CANVAS
        Canvas où va s'afficher l'emplois du temps.
    repas : IMAGE
        Pour de tkinter ne supprime pas l'image de la bannière des repas.

    """
    edt = Canvas(main, width=800, height=560, bg=rgb_convert((235,235,235)))
    edt.grid(column=0,row=0)   
     
    # Crée la base de l'emplois du temps (lignes, heures, jours de la semaine...)
    margeX,margeY = 50,50
    
    for i in range(11):
        edt.create_line((0+margeX, 50*i+margeY), (800+margeX, 50*i+margeY), width=1, fill='black')
        edt.create_text((margeX-20, 50*i+margeY),text=str(i+8)+'h',fill="black",font='tkDefaeultFont 10')
    
    semaine = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi"]
    for i in range(6) :
        edt.create_text((margeX+50+(i*120), margeY-15),text=semaine[i],fill="black",font='tkDefaeultFont 14')
        
    # Affiche la banière du repas
    repas = PhotoImage(file = "repas.gif")
    edt.create_image(margeX,margeY+202,image=repas,anchor="nw")
    return edt,repas

    


