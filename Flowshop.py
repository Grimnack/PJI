# Classe flowshop dans le cadre du pji master 2016
import random
import FlowshopCertificat
import matplotlib.pyplot as plt
# les contraintes de gamme, toutes les tâches doivent passer sur toutes les machines, de la machine 1 à la machine m ;
# les contraintes de ressource, une machine ne peut traiter qu'une tâche à la fois.

plt.autoscale(tight=False)
plt.xlabel("CMAX")
plt.ylabel("Retard")
# plt.axis([0,100,0,100])
############################## PROBLEME ##############################

class Flowshop(object):
    """
    Le probleme du Flowshop
    Executer toutes les taches sur chaque machine

    Une tache doit etre terminée pour être lancée sur une autre machine
    """
    def __init__(self, n, m, p, d, ident=0):
        super(Flowshop, self).__init__()
        # Les données d'entrée du problème
        self.id = ident
        self.n = n # nombre de taches INT
        self.m = m # nombre de machines INT
        self.p = p[:] # p[i][j] temps de traitement du job i sur la machine j LIST OF LIST OF INT
        self.d = d[:] # d[i] date de fin souhaité du job i

    def __str__(self):
        return "problème id : " + str(self.id) + "\n n = " + str(self.n) + "\n m = " + str(self.m) + "\n p = " + str(self.p)+ "\n d = " + str(self.d)

    def certificatAlea(self) :
        """
        renvoie un certificat aleatoire possible 
        de l'instance du problème flowshop 
        """
        listeTaches = [0]*self.n
        for i in range(self.n) :
            listeTaches[i]=i
        random.shuffle(listeTaches)
        return FlowshopCertificat.FlowshopCertificat(listeTaches)

    def eval(self,certificat) :
        '''
        Renvoie Cmax,retards
        '''
        if certificat.score != None :
            return certificat.score
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
        certificat.score = (travail[-1],retards) 
        return (travail[-1],retards)

    def doTrace(self,voisinages,chaine) :
        for voisin in voisinages :
            (scoreCMAX,scoreRETARD) = self.eval(voisin.certificat)
            plt.plot(scoreCMAX,scoreRETARD,chaine)

    def domine(self,scores1,scores2) :
        '''
        scores1 domine scores2 sisi scores1[i] <= scores2[i] et scores1 != scores2
        '''
        toujoursInfouEgal = True
        SUP = False

        for i in range(len(scores2)) :
            if not (scores1[i] <= scores2[i]) :
                toujoursInfouEgal = False
            if scores1[i] < scores2[i] :
                SUP = True
        return toujoursInfouEgal and SUP

    def domineFortement(self,scores1,scores2):
        domine = True
        for i in range(len(scores2)) :
            if not (scores1[i] < scores2[i]) :
                domine = False
        return domine

    def cleanse(self, listeVoisins) :
        '''
        Supprime les éléments moins bons que d'autres dans la liste
        entrée liste L
        sortie liste L' plus petite ou égale
        '''
        #calcul du score pour tous le monde une seule fois
        for voisin in listeVoisins :
            self.eval(voisin.certificat)

        nouvelle = []
        while listeVoisins : #tant que la liste n est pas vide
            test = listeVoisins.pop(0)
            dominated = False
            for voisin in listeVoisins :
                score1 = self.eval(voisin.certificat)
                scoreTest = self.eval(test.certificat)
                if self.domine(score1,scoreTest) :
                    dominated = True
                if self.domine(scoreTest,score1) :
                    listeVoisins.remove(voisin)
            if not dominated :
                nouvelle.append(test)
        return nouvelle


    def optimisationDirecteSimple(self,listeInit,trace=False) :
        '''

        Entrée : une liste de certificats acceptables

        option trace pour matplotlib

        pour chaque certificats on calcule les voisins,
        on ajoute uniquement le premier meilleur voisin pour l'iteration suivante
        si pas de meilleurs on laisse notre certificat actuel 
        '''
        listeVoisins = self.cleanse(listeInit)
        allVisited = False
        if trace :
            self.doTrace(listeVoisins,'ro')
        while True:
            (voisin,allVisited) = randomPick(listeVoisins)
            if allVisited :
                break
            voisin.certificat.visited = True
            while voisin.hasNext() :
                candidat = voisin.next()
                scoreCandidat= self.eval(candidat.certificat)
                if trace :
                    plt.plot(scoreCandidat[0],scoreCandidat[1],'ro')
                dominated = False
                for test in listeVoisins :
                    scoreTest = self.eval(test.certificat)
                    if self.domine(scoreCandidat,scoreTest) :
                        listeVoisins.remove(test)
                    elif self.domine(scoreTest,scoreCandidat) :
                        dominated = True
                if not dominated and not (candidat in listeVoisins)  :
                    listeVoisins.append(candidat)
                    break
        if trace :
            self.doTrace(listeVoisins,'bo') 
            plt.show()

        return listeVoisins
 

################################ GLOBAL ################################

def randomPick(listeVoisinages) :
    random.shuffle(listeVoisinages)
    for voisin in listeVoisinages :
        if not voisin.certificat.visited :
            return (voisin,False)
    return (listeVoisinages[0],True)

def nbVisited(listeCertificats) :
    cpt = 0
    for certificat in listeCertificats :
        if certificat.visited :
            cpt+= 1
    return cpt

def strLineIntoIntList(chaine) :
    strList = chaine.split()
    intList = []
    for strElt in strList :
        intList.append(int(float(strElt)))
    return intList

def lecture(pathname) :
    '''
    prend le pathname d'un fichier .dat et renvoie une instance de Flowshop a partir de se fichier
    '''
    fichier = open(pathname)
    n = int(float(fichier.readline())) #oui c est moche mais bon
    m = int(float(fichier.readline()))
    p = []
    d = []
    identifiant = int(float(fichier.readline()))
    for i in range(n) :
        indice = int(float(fichier.readline()))
        fin = int(float(fichier.readline()))
        d.append(fin)
        chaine = fichier.readline()
        p.append(strLineIntoIntList(chaine))
    fichier.close()
    return Flowshop(n,m,p,d,ident=identifiant)



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
            FlowshopCertificat.FlowshopCertificat(permut) 
            alea = random.randint(1,maxRandP)
            p[i][j] = alea
            d[i] = random.randint(1,maxRandD)
    return Flowshop(n,m,p,d)

