import FlowshopCertificat as cert

class VoisinageSwap(object):
    """docstring for VoisinageSwap"""
    def __init__(self, flCertif):
        super(VoisinageSwap, self).__init__()
        self.i = -1
        self.j = 1
        self.certificat = flCertif

    def __eq__(self,other):
        return self.certificat == other.certificat

    def hasNext(self) :
        return (self.j < self.certificat.taille - 1 or self.i < self.certificat.taille -2 ) 

    def next(self) :
        if self.i == -1 :
            self.i = 0
            return self
        permut = self.certificat.permutation[:]
        cert.echange(permut,self.i,self.j)
        if (self.j < self.certificat.taille - 1) :
            self.j += 1
        elif (self.i < self.certificat.taille -2) :
            self.i += 1
            self.j = i + 1
        return permut
        
    def giveName(self) :
        return "swap"