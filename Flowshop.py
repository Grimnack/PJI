# Classe flowshop dans le cadre du pji master 2016
import random

# les contraintes de gamme, toutes les tâches doivent passer sur toutes les machines, de la machine 1 à la machine m ;
# les contraintes de ressource, une machine ne peut traiter qu'une tâche à la fois.

class Flowshop(object):
    """
    Le probleme du Flowshop
    Executer toutes les taches sur chaque machine

    Une tache doit etre terminée pour être lancée sur une autre machine
    """
    def __init__(self, n, m, p):
        super(Flowshop, self).__init__()
        # Les données d'entrée du problème
        self.n = n # nombre de taches INT
        self.m = m # nombre de machines INT
        self.p = p[:] # p[i][j] temps de traitement du job i sur la machine j LIST OF LIST OF INT


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

    def evalCMAxRetard(self, certificat) :
        '''
        Renvoie (Cmax,retard)
        Cmax : la date de fin de l'execution des taches,
        soit la date de fin de travail de la dernière machine
        Retard : le retard de la dernière machine par rapport à la première 
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
        return (travail[-1],travail[-1] - travail[0])
   
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


#################################### LES TESTS ####################################

fl = Flowshop(5,2,[[2,3,2,3,2],[3,2,3,2,3]])

fl.certificatAlea()