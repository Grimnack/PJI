import FlowshopCertificat as cert

class VoisinageSimple(object):
    """docstring for VoisinageSimple"""
    def __init__(self, flCertif):
        super(VoisinageSimple, self).__init__()
        self.iterator = 0
        self.certificat = flCertif

    def __eq__(self,other):
        return self.certificat == other.certificat

    def __str__(self) :
        return str(self.certificat)

    def hasNext(self) :
        return self.iterator+1 <= self.certificat.taille

    def next(self) :
        '''
        version voisinsSimple avec iterator
        '''
        permut = self.certificat.permutation[:]
        if self.iterator == len(permut)-1 :
            cert.echange(permut,self.iterator,0)
        else :
            cert.echange(permut,self.iterator,self.iterator+1)
        self.iterator += 1
        return VoisinageSimple(cert.FlowshopCertificat(permut)) 

    def giveName(self) :
        return "cont"

