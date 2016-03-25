import glob
import os
import Flowshop
import FlowshopCertificat
import VoisinageSimple as simple
import VoisinageGauche as gauche
import VoisinageSwap as swap
import matplotlib.pyplot as plt
import random as r


# OK !
def lesCouples() :
    '''
    renvoie la liste des couples d'objectifs
    '''
    res = []
    for i in range(3) :
        for j in range(i+1,4) :
            tmp = [False,False,False,False]
            tmp[i] = True
            tmp[j] = True
            res.append(tmp)
    return res

# OK !
def listBass() :
    '''
    Renvoie la liste de tous les .dat de type bass
    '''
    return glob.glob('data/data/bass/*.dat')

# OK !
def listLief() :
    '''
    Renvoie la liste de tous les .dat de type lief
    '''
    return glob.glob('data/data/lief/*.dat')

# OK !
def listRuiz() :
    '''
    Renvoie la liste de tous les .dat de type ruiz
    '''
    return glob.glob('data/data/ruiz/*.dat')

# OK !
def listUnif() :
    '''
    Renvoie la liste de tous les .dat de type bass
    '''
    return glob.glob('data/data/unif/*.dat')

# OK !
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

def scriptList(listType,typeName,objectifs,dossier) :
    '''
    param listType  la liste de tous les chemin pour les datas d'un certain type
    param typeName  le nom de ce certain type 
    param objectifs les configurations d'objectifs
    param dossier   le chemin vers le dossier dans lequel seront rangé les resultats DOIT FINIR PAR UN '/'

    lance le script mais pour un seul type
    '''
    for pathname in listType :
        fl = Flowshop.lecture(pathname)
        fl.type = typeName
        for config in objectifs :
            first = True
            for i in range(30) :
                r.seed(i)
                certif       = fl.certificatAlea()
                #Simple
                voisinSimple = simple.VoisinageSimple(certif)
                resSimple    = fl.PLS([voisinSimple],first=first,trace=False,cmax=config[0],tsum=config[1],tmax=config[2],usum=config[3])
                cheminSimple = fl.genereFileName(i,config[0],config[1],config[2],config[3],first,voisinSimple.giveName())
                creeFichier(dossier+cheminSimple,resSimple)
                #Shift
                voisinGauche = gauche.VoisinageGauche(certif)
                resGauche    = fl.PLS([voisinGauche],first=first,trace=False,cmax=config[0],tsum=config[1],tmax=config[2],usum=config[3])
                cheminGauche = fl.genereFileName(i,config[0],config[1],config[2],config[3],first,voisinGauche.giveName())
                creeFichier(dossier+cheminGauche,resGauche)
                #Swap
                voisinSwap   = swap.VoisinageSwap(certif)
                resSwap      = fl.PLS([voisinSwap],first=first,trace=False,cmax=config[0],tsum=config[1],tmax=config[2],usum=config[3])
                cheminSwap = fl.genereFileName(i,config[0],config[1],config[2],config[3],first,voisinSwap.giveName())
                creeFichier(dossier+cheminSwap,resSwap)
            first = False
            for i in range(30) :
                r.seed(i)
                certif       = fl.certificatAlea()
                #Simple
                voisinSimple = simple.VoisinageSimple(certif)
                resSimple    = fl.PLS([voisinSimple],first=first,trace=False,cmax=config[0],tsum=config[1],tmax=config[2],usum=config[3])
                cheminSimple = fl.genereFileName(i,config[0],config[1],config[2],config[3],first,voisinSimple.giveName())
                creeFichier(dossier+cheminSimple,resSimple)
                #Shift
                voisinGauche = gauche.VoisinageGauche(certif)
                resGauche    = fl.PLS([voisinGauche],first=first,trace=False,cmax=config[0],tsum=config[1],tmax=config[2],usum=config[3])
                cheminGauche = fl.genereFileName(i,config[0],config[1],config[2],config[3],first,voisinGauche.giveName())
                creeFichier(dossier+cheminGauche,resGauche)
                #Swap
                voisinSwap   = swap.VoisinageSwap(certif)
                resSwap      = fl.PLS([voisinSwap],first=first,trace=False,cmax=config[0],tsum=config[1],tmax=config[2],usum=config[3])
                cheminSwap = fl.genereFileName(i,config[0],config[1],config[2],config[3],first,voisinSwap.giveName())
                creeFichier(dossier+cheminSwap,resSwap)





#######################################################

###                    SCRIPT                       ###

#######################################################

# lesBass = listBass()
# lesLief = listLief()
# lesRuiz = listRuiz()
# lesUnif = listUnif()

# os.mkdir('sortie')
# os.mkdir('sortie/bass')
# os.mkdir('sortie/lief')
# os.mkdir('sortie/ruiz')
# os.mkdir('sortie/unif')

# objectifs = lesCouples()

# scriptList(lesBass,'bass',objectifs,'sortie/bass/')
# scriptList(lesLief,'lief',objectifs,'sortie/lief/')
# scriptList(lesRuiz,'ruiz',objectifs,'sortie/ruiz/')
# scriptList(lesUnif,'unif',objectifs,'sortie/unif/')


