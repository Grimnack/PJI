# Classe flowshop dans le cadre du pji master 2016
import random

# les contraintes de gamme, toutes les tâches doivent passer sur toutes les machines, de la machine 1 à la machine m ;
# les contraintes de ressource, une machine ne peut traiter qu'une tâche à la fois.

############################## PROBLEME ##############################

class Flowshop(object):
    """
    Le probleme du Flowshop
    Executer toutes les taches sur chaque machine

    Une tache doit etre terminée pour être lancée sur une autre machine
    """
    def __init__(self, n, m, p, d):
        super(Flowshop, self).__init__()
        # Les données d'entrée du problème
        self.n = n # nombre de taches INT
        self.m = m # nombre de machines INT
        self.p = p[:] # p[i][j] temps de traitement du job i sur la machine j LIST OF LIST OF INT
        self.d = d[:] # d[i] date de fin souhaité du job i

    def certificatAlea(self) :
        """
        renvoie un certificat aleatoire possible 
        de l'instance du problème flowshop 
        """
        listeTaches = [0]*self.n
        for i in range(self.n) :
            listeTaches[i]=i
        random.shuffle(listeTaches)
        print(listeTaches)
        return FlowshopCertificat(listeTaches)

    def evalCMAx(self, certificat) :
        '''
        Renvoie Cmax
        Cmax : la date de fin de l'execution des taches,
        soit la date de fin de travail de la dernière machine 
        '''
        travail = [0] * self.m # Tableau témoins du temps de calcul par machine

        for iTravail in certificat.permutation :
            for iMachine in range(self.m) :
                if iMachine == 0 : #La machine 0 n'attends personne sauf elle
                    travail[0] = travail[0] + self.p[iTravail][0]
                else :
                    if travail[iMachine - 1] >= travail[iMachine] :
                        travail[iMachine] = travail[iMachine-1] + self.p[iTravail][iMachine]
                    else :
                        travail[iMachine] = travail[iMachine] + self.p[iTravail][iMachine]
        
        # Le couple (Cmax,retard) 
        return travail[-1]

    def evalSommeRetards(self,certificat) :
        '''
        Renvoie la somme des retards
        '''
        travail = [0] * self.m # Tableau témoins du temps de calcul par machine
        retards = 0

        for iTravail in certificat.permutation :
            for iMachine in range(self.m) :
                if iMachine == 0 : #La machine 0 n'attends personne sauf elle
                    travail[0] = travail[0] + self.p[iTravail][0]
                else :
                    if travail[iMachine - 1] >= travail[iMachine] :
                        travail[iMachine] = travail[iMachine-1] + self.p[iTravail][iMachine]
                    else :
                        travail[iMachine] = travail[iMachine] + self.p[iTravail][iMachine]
                    if iMachine == self.m -1 :
                        if travail[iMachine] > self.d[iTravail] :
                            retards = retards + travail[iMachine] - self.d[iTravail]
        return retards

    def optimisationCompleteSimple(self,listeCertificats) :
        '''
        Entrée : une liste de certificats acceptables

        pour chaque certificats on calcule les voisins,
        on ajoute tous les meilleurs voisins pour l'iteration suivante
        si pas de meilleurs on laisse notre certificat actuel 
        '''


    def optimisationCompleteTotale(self,listeCertificats) :
        pass

    def optimisationDirecteSimple(self,listeCertificats) :
        pass

    def optimisationDirecteTotale(self,listeCertificats) :  
        pass

 
############################# CERTIFICAT #############################


class FlowshopCertificat(object):
    """
    Dans le Flowshop de permutation on lance les taches dans le 
    même ordre sur toutes les machines donc notre certificat est 
    la liste ordonnée des taches a executer.


    Certificat possible:
    longueur n
    ne contient pas de doublon

    """
    def __init__(self, liste):
        super(FlowshopCertificat, self).__init__()
        self.permutation = liste[:]
        self.best = False # un nouvel attribut pour l'optimisation
        #                   vaut True si tous ses voisins sont moins bon
          
    def estCorrecte(self,tailleProbleme) :
        """
        Renvoie True si le certificat est possible 
        """
        if len(self.permutation) != tailleProbleme :
            return False
        dejaVu = [False] * tailleProbleme
        for tache in self.permutation :
            if not dejaVu[tache] :
                dejaVu[tache] = True
            else :
                return False
        return True 

    def voisinsSimple(self) :
        '''
        Renvoie la liste des voisins du certificat instancié,
        avec des permutation côte à côte

        Par exemple : [1,2,3,4] peut donner [2,1,3,4] [1,3,2,4] [4,2,3,1]
        '''
        res = []
        for i in range(len(self.permutation)) :
            permut = self.permutation[:]
            if i == len(permut)-1 :
                echange(permut,i,0)
            else :
                echange(permut,i,i+1)
            res.append(permut)
        # pour le momment renvoie un liste de liste il faut plus tard l'ensembel des FlowshopCertificat 
        return res

    def voisinsMelangeTotal(self) :
        '''
        Renvoie la liste des voisins du certificat instancié
        avec toutes les permutation possible si on change un 
        permutation[i] avec un permutation[j]
        '''
        res = [] 
        for i in range(len(self.permutation)) :
            for j in range(len(self.permutation)) :
                permut = self.permutation[:]
                if i != j :
                    echange(permut,i,j)
                    res.append(permut)
        #pour le momment renvoie un set de liste le top serait de renvoyer l ensemble des FlowshopCertificat
        return res


################################ GLOBAL ################################

def flowshopAlea(n,m,maxRandP,maxRandD) :
    '''
    entrée : n le nombre de taches
             m le nombre de machines
             maxRand le nombre pour majorer les chiffres random aleatoire
    sortie : fl un problème de Flowshop aleatoire
    '''
    p = []
    for i in range(n) :
        p.append([0]*m)
    p[0][0] = 2
    d = [0] * n
    for i in range(n):
        for j in range(m):
            alea = r.randint(1,maxRandP)
            p[i][j] = alea
        d[i] = r.randint(1,maxRandD)
    return Flowshop(n,m,p,d)

def echange(tableau, indice1, indice2) :
    tmp = tableau[indice1]
    tableau[indice1] = tableau[indice2]
    tableau[indice2] = tmp


#################################### LES TESTS ####################################

n = 5
m = 4
matrix = [[5,4,4,3],
          [5,4,4,6],
          [3,2,3,3],
          [6,4,4,2],
          [3,4,1,5]]
d = [0,0,0,0,0] # a faire a la main

fl = Flowshop(n,m,matrix,d)

# fl.certificatAlea()

# TEST DES FONCTIONS DE VOISINAGE

certificat = FlowshopCertificat([1,2,3,4,5,6,7])

print('''certificat d'origine : ''', certificat.permutation)
print('''voisinsSimple''',certificat.voisinsSimple())
print('''voisinsMelangeTotal''',certificat.voisinsMelangeTotal())