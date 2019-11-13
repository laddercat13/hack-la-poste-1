
import collections #permet de trier un dictionnaire

fichier_log= "/home/squilly/programmation/projet python/connexion.log"
fichier_warning= "/home/squilly/programmation/projet python/warning.txt"
fichier_utilisateurs= "/home/squilly/programmation/projet python/utilisateurs.txt"
fichier_suspect="/home/squilly/programmation/projet python/suspect.txt"
fichier_u_doublons="/home/squilly/programmation/projet python/doublons.txt"      #liste des fichiers a lire ou dans lesquels on souhaite ecrire

login=[] 
log=[]
danger=[]
ip_log=[]   #listes vides qui vont nous servir lors des differentes etapes
compteur = 0 #compteur a zero a incrementer demarrant a zero
#doublons_map = {} #dictionnaire vide destine a contenir les doublons


def menu():
    consigne = """ Quelle est votre demande :
            1 : Fichier Utilisateurs (liste des utilisateurs du fichier log)
            2 : Connexion suspecte
            3 : Fichier suspect (liste des utilisateurs ayant utilises les ip interdites)
            4 : Quit.\nENTREZ VOTRE CHOIX : """
   
    demande = int(input(consigne)) 

    while demande != 4 :

        if demande == 1 :
            print("fichier créé")
            u =  open(fichier_utilisateurs, 'w') #u = ouverture du fichier utilisateur en mode ecriture  

            with open(fichier_log, 'r') as l: #ouverture du fichier contenant les logs en mode lecture
                for line in l:                   #pour chaque ligne dans le fichier log 
                    login=line.split(";")      #on garde dans la liste login les informations entre les ; 
                    u.write(str(login[1])+"\n")             #ecriture dans le fichier utilisateur de la colonne 1 avec retour a la ligne
            u.close()                                     #fermeture du fichier utilisateur utilisateur apres ecriture
    
        elif demande == 2 :
            with open(fichier_log, "r") as t: #ouverture du fichier contenant les logs en mode lecture
                for line in t:                  #pour chaque ligne dans le fichier log
                    log=line.split(" ")         #on garde dans la liste log les informations en les séparant en deux groupes (ip,login,date+heure)
                    if log[1] <= str("07:59") or log[1] >= str("18:59") :   #si l'élément 1 de la liste (l'heure) n'est pas comprise entre 8h et 19h
                        print("Connexion suspecte : " +line)           #alors on affiche les lignes avec les heures non comprises dans ce créneau
        
        elif demande == 3 : 
            print("fichier créé")   
            with open(fichier_warning, "r") as w: #ouverture du fichier contenant les ip interdites en lecture
                for line in w:                      #pour chaque ligne dans le fichier warning
                    danger.append(line.strip())    #on ecrit les lignes dans la liste danger
        

            user_double = open (fichier_u_doublons, "w")      #user_double = ouverture fichier destine a contenir les utilisateurs suspect en doublons en ecriture

            with open (fichier_log, "r") as log:  #ouverture du fichier contenant les logs en lecture
                for line in log:                  #pour chaque ligne dans le fichier log
                    ip_log=line.split(";")       #on rentre les lignes dans la liste ip_log en separant les information (ip, login, date+heure)
                    if ip_log[0] in danger:         #si le l'ip presente dans la liste ip_log se trouve aussi dans danger
                        user_double.write(ip_log[1]+"\n")                 #ecriture des users correspondant aux ip interdite suite a la comparaison entre log et danger
    
            user_double.close()

            doublons_map = {} #dictionnaire vide destine a contenir les doublons
            
            with open (fichier_u_doublons, "r") as user_double: #ouverture fichier contenant les utilisateurs suspect en doublons
                for doublons in user_double:         #pour chaque doublons dans fichier_u_doublons
                    doublons=doublons.strip()           #on supprime les characteres et les espaces parasites
                    doublons_map[doublons]=doublons_map.get(doublons, 0)+1 #on incremente le dictionnaire avec les doublons utilisateurs en les inscrivant une seule fois

            doublons_map=collections.OrderedDict(sorted(doublons_map.items())) #on tri le dictionnaire dans l'ordre alphabetique

            with open(fichier_suspect, "w") as suspect:         #ouverture du fichier destine a contenir les suspects et le nombre de fois ou ils apparaissent
                for key, value in doublons_map.items():            #pour chaque utilisateur et son nombre de connexion dans le dictionnaire
                    suspect.write(key + " : " + str(value) + "\n")   #on ecrit dans le fichier_suspect le pseudo, son nombre de connexion en revenant a la ligne

        
        else :
            print("commande incorrecte")
        
        demande = int(input(consigne))

    print("merci au revoir.")

menu()