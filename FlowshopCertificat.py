
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
        self.taille = len(liste)
        self.score = None #score des evals 

    def __eq__(self,other) :
        return self.permutation == other.permutation


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


def echange(tableau, indice1, indice2) :
    tmp = tableau[indice1]
    tableau[indice1] = tableau[indice2]
    tableau[indice2] = tmp
