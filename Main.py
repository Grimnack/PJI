import Flowshop
import FlowshopCertificat
# import matplotlib.pyplot as plt

n = 5
m = 4
matrix = [[5,4,4,3],
          [5,4,4,6],
          [3,2,3,3],
          [6,4,4,2],
          [3,4,1,5]]
d = [25,20,10,30,30] # a faire a la main

fl = Flowshop.Flowshop(n,m,matrix,d)

# fl.certificatAlea()

# TEST DES FONCTIONS DE VOISINAGE

certificat = FlowshopCertificat.FlowshopCertificat([0,1,2,3,4])


# CMAX ET RETARD MARCHENT
def testEvals() :
    print("CMAX = ", fl.evalCMAx(certificat))
    print("Retard = ", fl.evalSommeRetards(certificat))

def testVoisinsSimpleCouteux() :
    print('''certificat d'origine : ''', certificat.permutation)
    print('''voisinsSimple''',certificat.voisinsSimple())
    
def testVoisinsMelangeTotalCouteux():
    print('''voisinsMelangeTotal''',certificat.voisinsMelangeTotal())

def testOptimisationDirecteSimple(trace = False):
    #on choisit des certificats au hasard
    listeCertificat = []
    for i in range(10) :
        listeCertificat.append(fl.certificatAlea())
    fl.optimisationDirecteSimple(listeCertificat, trace)
    for certificat in listeCertificat :
        print(certificat.permutation)

def testOptimisationCompleteSimple(trace = False):
    #on choisit des certificats au hasard
    listeCertificat = []
    for i in range(10) :
        listeCertificat.append(fl.certificatAlea())
    fl.optimisationCompleteSimple(listeCertificat,trace)
    for certificat in listeCertificat :
        print(certificat.permutation)

testOptimisationDirecteSimple(trace = True)
# testOptimisationCompleteSimple()