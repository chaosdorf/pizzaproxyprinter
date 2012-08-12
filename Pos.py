class Pos(object):
    def __init__(self):
        self._nr = 0 
        self._postext = ""
        self._EP = 0.00
        self._Menge = 0.00 
        self._reNr = 0
    @property
    def nr(self):
        return self._nr
    @nr.setter
    def nr(self, value):
        self._nr = value
 
    @property
    def postext(self):
        return self._postext
    @postext.setter
    def postext(self, value):
        self._postext = value
 
    @property
    def EP(self):
        return self._EP
    @EP.setter
    def EP(self, value):
        self._EP = value
 
    @property
    def Menge(self):
        return self._Menge
    @Menge.setter
    def Menge(self, value):
        self._Menge = value
 
    @property    # Rechnungsnummer
    def reNr(self): 
        return self._reNr
    @reNr.setter
    def reNr(self, value):
        if type(value) == str:
            self._reNr = value
