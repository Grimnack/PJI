import Flowshop
import FlowshopCertificat
import VoisinageSimple as simple
import VoisinageGauche as gauche
import matplotlib.pyplot as plt

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

def testDomine() :
    green = (1,1)
    center = (2,2)
    red = (3,1)
    blue = (3,3)
    jaune = (1,3)
    print("center domine blue : " , fl.domine(center,blue))
    print("green domine center : ", fl.domine(green,center))
    print("greed domine red : " , fl.domine(green,red))
    print("green domine jaune : ", fl.domine(green,jaune))
    print("green est domine par jaune", fl.domine(jaune,green))
    print("green est domine par red", fl.domine(red,green))

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
# testDomine()