import glob
import os
import Flowshop
import FlowshopCertificat
import VoisinageSimple as simple
import VoisinageGauche as gauche
import VoisinageSwap as swap
import matplotlib.pyplot as plt

def listBass() :
    '''
    Renvoie la liste de tous les .dat de type bass
    '''
    return glob.glob('data/data/bass/*.dat')

def listLief() :
    '''
    Renvoie la liste de tous les .dat de type lief
    '''
    return glob.glob('data/data/lief/*.dat')

def listRuiz() :
    '''
    Renvoie la liste de tous les .dat de type ruiz
    '''
    return glob.glob('data/data/ruiz/*.dat')

def listUnif() :
    '''
    Renvoie la liste de tous les .dat de type bass
    '''
    return glob.glob('data/data/unif/*.dat')

def creeFichier(pathname,listeScore) :
    '''
    cree le fichier et ecris les scores dedans
    '''
    f = open(pathname,'w')
    for score in listeScore :
        for element in score :
            f.write(str(element)+'\t')
        f.write('\n')
    f.close()

os.mkdir('test')
print(creeFichier('test/test.out',[(1,2,3),(4,5,6)] ))

#######################################################

###                    SCRIPT                       ###

#######################################################

# lesBass = listBass()
# lesLief = listLief()
# lesRuiz = listRuiz()
# lesUnif = listUnif()

