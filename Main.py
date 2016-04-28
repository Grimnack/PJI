import Flowshop
import FlowshopCertificat
import VoisinageSimple as simple
import VoisinageGauche as gauche
import matplotlib.pyplot as plt

# n = 5
# m = 4
# matrix = [[5,4,4,3],
#           [5,4,4,6],
#           [3,2,3,3],
#           [6,4,4,2],
#           [3,4,1,5]]
# d = [25,20,10,30,30] # a faire a la main
# fl = Flowshop.Flowshop(n,m,matrix,d)
# certificat = FlowshopCertificat.FlowshopCertificat([0,1,2,3,4])

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
    fl.PLS(voisinageSimple, trace)
    for voisin in voisinageSimple :
        print(voisin.certificat.permutation)

def testOptimisationDirecteGauche(trace = False) :
    voisinageGauche = []
    for i in range(10) :
        voisinageGauche.append(gauche.VoisinageGauche(fl.certificatAlea()))
    fl.PLS(voisinageGauche, trace)
    for voisin in voisinageGauche :
        print(voisin.certificat.permutation)

def testLecture() :
    fl = Flowshop.lecture("data/data/bass/bass_5_9_1.dat")
    print(fl)

def testSimpleData(pathname) :
    fl = Flowshop.lecture(pathname)
    voisinageSimple = []
    for i in range(10) :
        voisinageSimple.append(simple.VoisinageSimple(fl.certificatAlea()))
    fl.PLS(voisinageSimple, True)
    for voisin in voisinageSimple :
        print(voisin.certificat.permutation)

def testSimpleDataBest(pathname) :
    fl = Flowshop.lecture(pathname)
    voisinageSimple = []
    for i in range(10) :
        voisinageSimple.append(simple.VoisinageSimple(fl.certificatAlea()))
    fl.PLS(voisinageSimple, trace=True,first=False)
    for voisin in voisinageSimple :
        print(voisin.certificat.permutation)

def tesGenereFileName(fl) :
    for i in range(10) :
        print(fl.genereFileName(i,True,True,True,True,True,'shift'))
        print(fl.genereFileName(i,False,False,True,True,True,'shift'))
        print(fl.genereFileName(i,False,False,False,False,True,'shift'))        

fl = Flowshop.lecture("data/data/bass/bass_10_10_5.dat")
certif = FlowshopCertificat.FlowshopCertificat([2, 3, 1, 0, 8, 7, 6, 5, 4, 9])
voisin = simple.VoisinageSimple(certif)
print(fl.PLS([voisin],archive=False,first=False,trace=False,cmax=True,tsum=True,tmax=False,usum=False))

# testSimpleDataBest("data/data/bass/bass_10_10_1.dat")
# testSimpleData("data/data/bass/bass_10_10_1.dat")
# testLecture()
# testOptimisationDirecteSimple(trace = True)
# testOptimisationDirecteGauche(trace = True)
# testDomine()