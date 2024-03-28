import csv
import functions
import affichage

# Recuperation des fichier prof.csv et classe.csv, avec les info necessaires
# prof(nom,matiere,nbheuremax) / classe(nom,niveau,spe1,spe2,spe3,lv1,lv2)
with open("OptiSched/source/Classeur1.csv") as file_name:
    file_read = csv.reader(file_name)
    fichierprof = list(file_read)

with open("OptiSched/source/Classeur2.csv") as file_name:
    file_read = csv.reader(file_name)
    fichierclasse = list(file_read)
    
with open("OptiSched/source/Classeur3.csv") as file_name:
    file_read = csv.reader(file_name)
    fichiersalle = list(file_read)

#On classifie les info reçues
nbclasse = len(fichierclasse)-1
nbprof = len(fichierprof)-1
nbsalle = len(fichierclasse)-1

dicoClasse = {}
for i in fichierclasse[1::]:
    dicoClasse[i[0]] = (i[1],i[2],i[3],i[4],i[5],i[6])
dicoProf = {}
for i in fichierprof[1::]:
    dicoProf[i[0]] = (i[1],i[2])
dicoSalle = {}
for i in fichiersalle[1::]:
    dicoSalle[i[0]] = (i[1])  
    
    
#Constantes sur les emplois du temps du lycée
dicoIClasse = {'terminale':0,'premiere':1,'seconde':2}

dicoEdt = [{'hist-geo':3,'lv1':2,'lv2':2,'physique':1,'svt':1,'eps':2,'philosophie':4,'spe1':6,'spe2':6,"math":0,"ses":0,"nsi":0,"si":0, "francais":0},
       {'hist-geo':3,'lv1':2,'lv2':2,'physique':1,'svt':1,'eps':2,'francais':4,'spe1':4,'spe2':4,'spe3':4,"math":0,"philosophie":0, "ses":0, "nsi":0,"si":0},
       {'hist-geo':3,'lv1':3,'lv2':3,'physique':3,'svt':2,'eps':2,'francais':4,'math':4,'ses':2,'nsi':2,"si":0}]

nbmatiereclasse = [9,10,10]
nheureiveau = [27,27,28]

lmatiere = ['hist-geo','anglais','allemand','physique','svt','eps','francais','math','ses','nsi',"espagnol","si","chinois"]



# Crée et trie par ordre alphabétique une liste des noms des professeurs 
liste_profs = []
for i in fichierprof:
    if i[0] != 'nom':
        liste_profs.append(i[0])
liste_profs = sorted(liste_profs)


#Variables définies par les fonctions
DicoClasseMatiere_Professeur = functions.ProfParClasse(fichierclasse,fichierprof,dicoIClasse,dicoEdt)
classe_prof = functions.ListeClasseProf(DicoClasseMatiere_Professeur,dicoEdt,dicoClasse,dicoIClasse)
couleurs = functions.color_graphe(classe_prof)
edt = functions.rep_jour(classe_prof, couleurs, False)
edt_salle = functions.attribuer_salle(edt, dicoProf, dicoSalle, fichiersalle)
edt_form = functions.reform(edt, dicoProf)
edt_dico = functions.edt_dico(edt_form)
edt_prof = functions.edt_prof(edt_dico)
fenetremain = affichage.initfenetre()
edt,repas = affichage.creerCanvasImage(fenetremain)

# Lance les fonctions principales
affichage.create_menu_edt(fenetremain,edt,edt_dico,liste_profs,edt_prof,edt_form)
affichage.affiche_cours(edt_dico['S1'],edt)

# Affiche le logo de la fenetre
fenetremain.iconbitmap('logo.ico')
 

#Boucle principale
fenetremain.mainloop()