
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
        self.visited = False
        self.iterator = 0
        self.taille = len(liste) 

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

    def hasNext(self) :
        return self.iterator+1 <= self.taille

    def next(self) :
        '''
        version voisinsSimple avec iterator
        '''
        permut = self.permutation
        if self.iterator == len(permut)-1 :
            echange(permut,self.iterator,0)
        else :
            echange(permut,self.iterator,self.iterator+1)
        self.iterator += 1
        return FlowshopCertificat(permut) 


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

def echange(tableau, indice1, indice2) :
    tmp = tableau[indice1]
    tableau[indice1] = tableau[indice2]
    tableau[indice2] = tmp
