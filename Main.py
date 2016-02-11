import Flowshop
import FlowshopCertificat
import VoisinageSimple as simple
import VoisinageGauche as gauche
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
certificat = FlowshopCertificat.FlowshopCertificat([0,1,2,3,4])

def testOptimisationDirecteSimple(trace = False):
    #on choisit des certificats au hasard
    voisinageSimple = []
    for i in range(10) :
        voisinageSimple.append(simple.VoisinageSimple(fl.certificatAlea()))
    fl.optimisationDirecteSimple(voisinageSimple, trace)
    for voisin in voisinageSimple :
        print(voisin.certificat.permutation)

def testOptimisationDirecteGauche(trace = False) :
    voisinageGauche = []
    for i in range(10) :
        voisinageGauche.append(gauche.VoisinageGauche(fl.certificatAlea()))
    fl.optimisationDirecteSimple(voisinageGauche, trace)
    for voisin in voisinageGauche :
        print(voisin.certificat.permutation)

testOptimisationDirecteSimple(trace = True)
# testOptimisationDirecteGauche(trace = True)