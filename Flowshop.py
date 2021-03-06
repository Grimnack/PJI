# Classe flowshop dans le cadre du pji master 2016
import random
import FlowshopCertificat
import matplotlib.pyplot as plt
import time
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
    def __init__(self, n, m, p, d, ident=0, type_name="defaut"):
        super(Flowshop, self).__init__()
        # Les données d'entrée du problème
        self.type = type_name
        self.id = ident
        self.n = n # nombre de taches INT
        self.m = m # nombre de machines INT
        self.p = p[:] # p[i][j] temps de traitement du job i sur la machine j LIST OF LIST OF INT
        self.d = d[:] # d[i] date de fin souhaité du job i
        self.cptEval = 0

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

    def eval(self,certificat,cmax,tsum,tmax,usum) :
        '''
        [FlowshopCertificat]->[bool]->[bool]->[bool]->[bool]->[vecteurScore]
        Entrée le certificat a évaluer  
               les objectifs a renvoyer si leur valeur vaut True
        Renvoie Cmax,Tsum,Tmax,Usum
        '''
        if certificat.score != None :
            return certificat.score
        travail = [0] * self.m # Tableau témoins du temps de calcul par machine
        Tsum = 0 # Somme des retards 
        Tmax = 0 # Le retard le plus long
        Usum = 0 # Nombre de travaux en retard 

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
                            retard = travail[iMachine] - self.d[iTravail]
                            Usum += 1
                            Tsum = Tsum + retard
                            if retard > Tmax :
                                Tmax = retard
        Cmax = travail[-1] 

        vecteurScore = []

        if cmax :
            vecteurScore.append(Cmax)
        if tsum :
            vecteurScore.append(Tsum)
        if tmax :
            vecteurScore.append(Tmax)
        if usum :
            vecteurScore.append(Usum)

        certificat.score = vecteurScore
        self.cptEval += 1
        return vecteurScore

    def doTrace(self,voisinages,chaine,cmax,tsum,tmax,usum) :
        '''
        Fonction ajoutant les points de score au pyplot (graphique)
        '''
        for voisin in voisinages :
            (x,y) = self.eval(voisin.certificat,cmax,tsum,tmax,usum)
            plt.plot(x,y,chaine)

    def domine(self,scores1,scores2) :
        '''
        scores1 domine scores2 sisi scores1[i] <= scores2[i] et scores1 != scores2
        '''
        toujoursInfouEgal = True
        for i in range(len(scores2)) :
            if not (scores1[i] <= scores2[i]) :
                toujoursInfouEgal = False
        return toujoursInfouEgal and scores1 != scores2

    def domineFortement(self,scores1,scores2):
        domine = True
        for i in range(len(scores2)) :
            if not (scores1[i] < scores2[i]) :
                domine = False
        return domine

    def cleanse(self, listeVoisins,cmax,tsum,tmax,usum) :
        '''
        Supprime les éléments moins bons que d'autres dans la liste
        entrée liste L
        sortie liste L' plus petite ou égale
        '''
        #calcul du score pour tous le monde une seule fois
        for voisin in listeVoisins :
            self.eval(voisin.certificat,cmax,tsum,tmax,usum)

        nouvelle = []
        while listeVoisins : #tant que la liste n est pas vide
            test = listeVoisins.pop(0)
            dominated = False
            for voisin in listeVoisins :
                score1 = self.eval(voisin.certificat,cmax,tsum,tmax,usum)
                scoreTest = self.eval(test.certificat,cmax,tsum,tmax,usum)
                if self.domine(score1,scoreTest) :
                    dominated = True
                if self.domine(scoreTest,score1) :
                    listeVoisins.remove(voisin)
            if not dominated :
                nouvelle.append(test)
        return nouvelle

    def PLS(self,listeVoisins,archive=False,first=True,best=False,trace=False,cmax=True,tsum=True,tmax=False,usum=False) :
        '''

        Entrée : une liste de certificats acceptables

        option trace pour matplotlib

        cf algo du rapport
        '''
        start_time = time.time()
        self.cptEval = 0
        if trace :
            self.doTrace(listeVoisins,'ro',cmax,tsum,tmax,usum)
        for solution in listeVoisins :
            solution.visited = False
        pareto = listeVoisins[:]
        while listeVoisins != []:
            solution = randomPick(listeVoisins)
            while solution.hasNext() :
                solutionPrime = solution.next()
                solutionPrime.visited = False
                scoreSolutionPrime = self.eval(solutionPrime.certificat,cmax,tsum,tmax,usum)
                if trace :
                    self.doTrace([solution],'ro',cmax,tsum,tmax,usum)
                dominated = False
                for paretoElement in pareto :
                    scorePareto = self.eval(paretoElement.certificat,cmax,tsum,tmax,usum)
                    if trace :
                        self.doTrace([paretoElement],'ro',cmax,tsum,tmax,usum)
                    if self.domine(scoreSolutionPrime,scorePareto) :
                        pareto.remove(paretoElement)
                    elif self.domine(scorePareto,scoreSolutionPrime) :
                        dominated = True
                if not dominated and not solutionPrime in pareto: 
                    pareto.append(solutionPrime)
                    if first==True :
                        break
            if not solution.hasNext() :
                solution.visited = True
            listeVoisins = listeNonVisited(pareto)
        listeScore = []
        for voisin in pareto :
            evalFinale = self.eval(voisin.certificat,cmax,tsum,tmax,usum)
            listeScore.append(evalFinale)
        if trace :
            self.doTrace(pareto,'bo',cmax,tsum,tmax,usum)
            plt.show()
        timeTotal = time.time() - start_time
        return (listeScore,self.cptEval,timeTotal)


    def genereFileName(self,numIteration,cmax,tsum,tmax,usum,first,archive,nomVoisinage) :
        '''
        Utile pour la création de fichier de sortie
        Renvoie le nom de fichier correspondant a la configuration du problème
        '''
        chemin = self.type
        chemin = chemin +'_'+str(self.n)+'_'+str(self.m)+'_' + str(self.id)
        if cmax :
            chemin = chemin + '_cmax'
        if tsum :
            chemin = chemin + '_tsum'
        if tmax :
            chemin = chemin + '_tmax'
        if usum :
            chemin = chemin + '_tsum'
        if first :
            chemin = chemin + '_first'
        else : 
            chemin = chemin + '_best'
        if archive :
            chemin = chemin + '_archTrue'
        else :
            chemin = chemin + '_archFalse'
        chemin = chemin + '_' + nomVoisinage
        chemin = chemin + '_' + str(numIteration)
        chemin = chemin + '.out'
        return chemin



################################ GLOBAL ################################

# def ajouteLesNonVisited(listeDepart,listeDestination) :
#     for element in listeDepart :
#         if not element.visited :
#             listeDestination.append(element)

def listeNonVisited(listeVoisinages) :
    res = []
    for element in listeVoisinages :
        if not element.visited :
            res.append(element)
    return res 

# def randomPick(listeVoisinages) :
#     random.shuffle(listeVoisinages)
#     for voisin in listeVoisinages :
#         if not voisin.certificat.visited :
#             return (voisin,False)
#     return (listeVoisinages[0],True)

def randomPick(listeVoisinages) :
    random.shuffle(listeVoisinages)
    return listeVoisinages[0]
def randomPop(listeVoisinages) :
    random.shuffle(listeVoisinages)
    return listeVoisinages.pop()

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

