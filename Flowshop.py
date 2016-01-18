# Classe flowshop dans le cadre du pji master 2016


# les contraintes de gamme, toutes les tâches doivent passer sur toutes les machines, de la machine 1 à la machine m ;
# les contraintes de ressource, une machine ne peut traiter qu'une tâche à la fois.

class Flowshop(object):
    """
    Le probleme du Flowshop
    Executer toutes les taches sur chaque machine
    """
    def __init__(self, n):
        super(Flowshop, self).__init__()
        # Les données d'entrée du problème
        self.n = n # nombre de taches
        self.m = m # nombre de machines
        self.p = p[:] # p[i][j] temps de traitement du job i sur la machine j
        