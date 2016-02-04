import Flowshop
import FlowshopCertificat


n = 5
m = 4
matrix = [[5,4,4,3],
          [5,4,4,6],
          [3,2,3,3],
          [6,4,4,2],
          [3,4,1,5]]
d = [20,0,30,30,0] # a faire a la main

fl = Flowshop.Flowshop(n,m,matrix,d)

# fl.certificatAlea()

# TEST DES FONCTIONS DE VOISINAGE

certificat = FlowshopCertificat.FlowshopCertificat([0,1,2,3,4])

print("CMAX = ", fl.evalCMAx(certificat))
print("Retard = ", fl.evalSommeRetards(certificat))

# print('''certificat d'origine : ''', certificat.permutation)
# print('''voisinsSimple''',certificat.voisinsSimple())
# print('''voisinsMelangeTotal''',certificat.voisinsMelangeTotal())