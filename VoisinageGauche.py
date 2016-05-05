import FlowshopCertificat as cert

class VoisinageGauche(object):
    """docstring for VoisinageGauche"""
    def __init__(self, flCertif):
        super(VoisinageGauche, self).__init__()
        self.iterator = 0
        self.certificat = flCertif

    def __eq__(self,other):
        return self.certificat == other.certificat

    def hasNext(self) :
        return self.iterator+1 < self.certificat.taille

    def next(self) :
        permut = self.certificat.permutation[:]
        pick = permut[self.iterator]
        for i in range(self.iterator+1,len(permut)) :
            permut[i-1] = permut[i]
        permut[-1] = pick
        self.iterator+= 1
        return VoisinageGauche(cert.FlowshopCertificat(permut))

    def giveName(self) :
        return "shift"