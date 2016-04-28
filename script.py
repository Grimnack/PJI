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
def creeFichier(pathname,listeScore,complexite,temps) :
    '''
    cree le fichier et ecris les scores dedans
    '''
    f = open(pathname,'w')
    for score in listeScore :
        for element in score :
            f.write(str(element)+'\t')
        f.write('\n')
    f.write("#C#\n")
    f.write(str(complexite)+'\n')
    f.write("#T#\n")
    f.write(str(temps))
    f.close()

def scriptList(listType,typeName,objectifs,dossier) :
    '''
    param listType  la liste de tous les chemin pour les datas d'un certain type
    param typeName  le nom de ce certain type 
    param objectifs les configurations d'objectifs
    param dossier   le chemin vers le dossier dans lequel seront rangé les resultats DOIT FINIR PAR UN '/'

    lance le script mais pour un seul type
    '''
    archiveL = [False]
    firstL = [True,False]
    for pathname in listType :
        fl = Flowshop.lecture(pathname)
        fl.type = typeName
        for config in objectifs :
            for first in firstL :
                for archive in archiveL :
                    for i in range(30) :
                        r.seed(i)
                        certif       = fl.certificatAlea()
                        print(certif.permutation,config,first)
                        #Simple
                        voisinSimple = simple.VoisinageSimple(certif)
                        cheminSimple = fl.genereFileName(i,config[0],config[1],config[2],config[3],first,archive,voisinSimple.giveName())
                        print(cheminSimple)
                        print(pathname)
                        (resSimple,nbEval,time)    = fl.PLS([voisinSimple],archive=archive,best=(not first),first=first,trace=False,cmax=config[0],tsum=config[1],tmax=config[2],usum=config[3])
                        creeFichier(dossier+cheminSimple,resSimple,nbEval,time)
                        #Shift
                        # voisinGauche = gauche.VoisinageGauche(certif)
                        # cheminGauche = fl.genereFileName(i,config[0],config[1],config[2],config[3],first,archive,voisinGauche.giveName())
                        # print(cheminGauche)
                        # (resGauche,nbEval,time)    = fl.PLS([voisinGauche],archive=archive,best=(not first),first=first,trace=False,cmax=config[0],tsum=config[1],tmax=config[2],usum=config[3])
                        # creeFichier(dossier+cheminGauche,resGauche,nbEval,time)
                        #Swap
                        # voisinSwap = swap.VoisinageSwap(certif)
                        # cheminSwap = fl.genereFileName(i,config[0],config[1],config[2],config[3],first,archive,voisinSwap.giveName())
                        # print(cheminSwap)
                        # (resSwap,nbEval,time)      = fl.PLS([voisinSwap],archive=archive,best=(not first),first=first,trace=False,cmax=config[0],tsum=config[1],tmax=config[2],usum=config[3])
                        # creeFichier(dossier+cheminSwap,resSwap,nbEval,time)






#######################################################

###                    SCRIPT                       ###

#######################################################

lesBass = listBass()
# print(lesBass)
# lesLief = listLief()
# lesRuiz = listRuiz()
# lesUnif = listUnif()

# os.mkdir('sortie')
# os.mkdir('sortie/bass')
# os.mkdir('sortie/lief')
# os.mkdir('sortie/ruiz')
# os.mkdir('sortie/unif')

objectifs = lesCouples()

# print(lesBass[0])

scriptList(lesBass,'bass',objectifs,'sortie/bass/')
# scriptList(lesLief,'lief',objectifs,'sortie/lief/')
# scriptList(lesRuiz,'ruiz',objectifs,'sortie/ruiz/')
# scriptList(lesUnif,'unif',objectifs,'sortie/unif/')


