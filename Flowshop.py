# Classe flowshop dans le cadre du pji master 2016
import random
import FlowshopCertificat
import matplotlib.pyplot as plt
# les contraintes de gamme, toutes les tâches doivent passer sur toutes les machines, de la machine 1 à la machine m ;
# les contraintes de ressource, une machine ne peut traiter qu'une tâche à la fois.

plt.autoscale(tight=False)
plt.xlabel("CMAX")
plt.ylabel("Retard")
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
        return FlowshopCertificat.FlowshopCertificat(listeTaches)

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

    def optimisationDirecteSimple(self,listeCertificats,trace=False) :
        '''

        Entrée : une liste de certificats acceptables

        option trace pour matplotlib

        pour chaque certificats on calcule les voisins,
        on ajoute uniquement le premier meilleur voisin pour l'iteration suivante
        si pas de meilleurs on laisse notre certificat actuel 
        '''
        for certificat in listeCertificats :
            scoreCMAX = self.evalCMAx(certificat)
            scoreRETARD = self.evalSommeRetards(certificat)
            if trace :
                plt.plot(scoreCMAX,scoreRETARD,'ro')
            while certificat.hasNext() :
                nouveauCertif = certificat.next()
                nouveauCMAX = self.evalCMAx(nouveauCertif)
                nouveauRETARD = self.evalSommeRetards(nouveauCertif)
                aPlacer = False
                if trace :
                    plt.plot(nouveauCMAX,nouveauRETARD,'ro')
                # ici il faut remove tous les moins bon
                for test in listeCertificats :
                    testCmax = self.evalCMAx(test)
                    testRetard = self.evalSommeRetards(test) 
                    if testCmax >= nouveauCMAX and testRetard >= nouveauRETARD :
                        listeCertificats.remove(test)
                        aPlacer = True
                    elif testCmax > nouveauCMAX or testRetard > nouveauRETARD :
                        aPlacer = True
                if aPlacer :
                    listeCertificats.append(nouveauCertif)
                    break
                        
        if trace :
            for certificat in listeCertificats :
                scoreRETARD = self.evalSommeRetards(certificat)
                scoreCMAX = self.evalCMAx(certificat)
                plt.plot(scoreCMAX,scoreRETARD,'bo')
            plt.show()
        return listeCertificats


    # Bon ici le soucis c est de savoir quand et comment retirer
    # les certificats qui sont moins bon (mon bon score dans les deux evals)
    def optimisationCompleteSimple(self,listeCertificats) :
        '''
        Complete veut dire qu'on prend tous les meilleurs
        Utilisation de voisin Simple 
        '''
        for certificat in listeCertificats :
            scoreCMAX = self.evalCMAx(certificat)
            scoreRETARD = self.evalSommeRetards(certificat)

            while certificat.hasNext() :
                nouveauCertif = certificat.next()
                nouveauCMAX = self.evalCMAx(nouveauCertif)
                nouveauRETARD = self.evalSommeRetards(nouveauCertif)
                if scoreCMAX < nouveauCMAX and scoreRETARD < nouveauRETARD :
                    listeCertificats.remove(certificat)
                    listeCertificats.append(nouveauCertif)
                elif scoreCMAX < nouveauCMAX or scoreRETARD < nouveauRETARD :
                    listeCertificats.append(nouveauCertif)
        return listeCertificats        

    def optimisationCompleteTotale(self,listeCertificats) :
        pass


    def optimisationDirecteTotale(self,listeCertificats) :  
        pass

 

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
            FlowshopCertificat.FlowshopCertificat(permut) 
            alea = r.randint(1,maxRandP)
            p[i][j] = alea
            d[i] = r.randint(1,maxRandD)
    return Flowshop(n,m,p,d)

