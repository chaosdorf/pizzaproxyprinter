#!/usr/bin/python3

import Image, ImageDraw, ImageFont #, wx
from Pos import Pos
import subprocess
import sys
import string

# QR Code Bindings
import qrencode # ubuntu install python-qrencode

class printBill(object):
    def __init__(self):
        # Data must be given as array of Pos-Classes see Pos.py
        self._PosArray = []
        # needed for Type-Proof  of incoming PosArray
        PosProof = Pos()
        self._printer = "TSP143-(STR_T-001)"
        self._document = "printfile.tmp"
        self._LogoFilename = "icon.bmp"
        self._mwst = True 
        self._endmsg = "Happy Hacking"
        # TEST
        #subprocess.call( callstring , shell=True ) 
        self._linefeed_Y = 0
    
    @property
    def PrintMwst(self):
        return self._mwst

    @PrintMwst.setter
    def PrintMwst(self, value):
        if type(value) == bool:
            #print("NO MWST")
            self._mwst = value
    
    @property
    def EndMsg(self):
        return self._endmsg    

    @EndMsg.setter
    def EndMsg(self,value):
        if type(value) == str:
            self._endmsg = value
               
    @property
    def printer(self):
        return "test"
     
    @printer.setter
    def printer(self, value):
        self._printer = value
    
    @property
    def document(self):
        pass

    @document.setter
    def printer(self, value):
        self._document = value

               
    @property
    def PosArray(self):
        return self._PosArray
    
    @PosArray.setter
    def PosArray(self, value):
        # needed for Type-Proof  of incoming PosArray
        PosProof = Pos()
        for element in value:
            #print(type(element) + " " + type(PosProof))
            if not type(element) == type(PosProof):
                # Exeption muss noch geschrieben werden hilfsweise das
                return "Error Type Missmatch. Need Type Pos"
                self._TypeOK = False
                break
            else:
                self._TypeOK = True
        if self._TypeOK:
            self._PosArray = value

    def generatePrintFile(self):
        self._loadLogo()
        
        # the main to Print Image
        doc = Image.new("RGB",(1000,4000),"#ffffff")
        # paste the logo into the main image @ Postition 0,0
        doc.paste(self._logo,(0,100))
        # get the Date_Image to merge
        datadoc = self._getDataImage()
     
        # Resize Data_Image
        newdatadoc = datadoc.resize((1000,8000))
        # Merge Data_Image with Print Image
        doc.paste(newdatadoc,(0,700))
        
        # Get the Billnumber Image to merge
        reNr = self._PosArray[0].reNr
        billnr = self._getReNr_Image(reNr)
        # Resize Billnumber_Image
        newbillnr = billnr.resize((500,200))
        # Merge Billnumber_Image with Print Image
        doc.paste(newbillnr,(500,20))

        # Get A QR-Code-Image of ID-URL in Form:
        # http://ihex.de/foo where foo ist the Billnumber
        qrmsg = "http://ihex.de/" + str(reNr)
        qrimage = self._getQR_Image(qrmsg)
        doc.paste(qrimage,(500,200))
        # Save PrintImage as PNG File
        doc.save(self._document, "PNG")  
        

       
    def printDocument(self):
        self._callstring = "lpr -P '" + self._printer + "' " + self._document
        subprocess.call(self._callstring , shell=True )  

    def _loadLogo(self):
        logo = Image.open(self._LogoFilename)
        self._logo = logo.resize((400,400))
       
    def _getDataImage(self):
        # calc Bill and return Billlist as Image
        lf = 14 # Linefeed

        # another Image for the Data (to resize later)
        datadoc = Image.new("RGB",(200,2000),"#ffffff")
        draw = ImageDraw.Draw(datadoc)
        draw.setink("#000000")
                                
        # BillHeader
        HeaderL1= "------- Bestellung -----  in Euro \n "
        HeaderL2= "Nr  Anz. Bez.               GP\n"
        HeaderL3= "--------------------------------"
        draw.text((0,0), HeaderL1)
        draw.text((0,2*lf),HeaderL2)
        draw.text((0,3*lf),HeaderL3)
        
        # Bill List
        Summe = 0.00
        Y = 4*lf # as Textposition        
        for pos in self._PosArray:
            GP = pos.Menge * pos.EP
            shortpostext = self._postextShorter(pos.postext)
            printline = str(pos.nr) + "# x " + str(pos.Menge) + " " + shortpostext + " " + "%3.2f" % (GP) + "\n"
            draw.text((0,Y), printline)
            Y = Y + lf
            Summe = Summe + GP
        # Sum and Tax
        Tax = 0.19 * Summe
        Brutto = Summe + Tax


        if self._mwst:
            # Print MwSt
            EndL1 = "Netto     " + "%5.2f" % Summe + "\n"
            EndL2 = "MwSt. 19% " + "%5.2f" % Tax + "\n"
            EndL3 = "Brutto    " + "%5.2f" % Brutto + "\n"

            Y = Y + lf
            draw.text((50,Y),EndL2)
            Y = Y + lf
            draw.text((50,Y),EndL3)
        else:
            EndL1 = "Summe :   " + "%.2f" % Summe + "\n"
            Y = Y + lf
            draw.text((50,Y),EndL1)


        # EndMessage

        Endl4 = "-----------------------------------"
        Endl5 = self._endmsg
        Endl6 = "-----------------------------------"
        Y = Y + lf + 50
        draw.text((0,Y),Endl4)
        Y = Y + lf * 2
        draw.text((0,Y),Endl5)
        Y = Y + lf * 2
        draw.text((0,Y),Endl6)
        
        self._linefeed_Y = Y
        return datadoc
    
    def _getReNr_Image(self, reNr):
        # another Image for the Billnumber (to resize later)
        reNrImg = Image.new("RGB",(40,20),"#ffffff")
        draw = ImageDraw.Draw(reNrImg)
        draw.setink("#000000")

        draw.text((0,0),str(reNr))
        return reNrImg
                                                

    def _prizeShorter(self, floatPrize):
        pass
        
    def _postextShorter(self, postext):
        platz = 18
        amo = len(postext) 
        if amo >= platz + 1:
            shortPosText = postext[0:platz] + "*"
        elif amo <= platz -1:
            emptycount = platz - amo
            shortPosText = postext
            while emptycount >= 1:
                shortPosText = shortPosText + " "
                emptycount = emptycount - 1
        else:
            shortPosText = postext
        return shortPosText                 

    def _getQR_Image(self, qrtext):
        #qrfile = open("qr.png","w")
        version , size, QRimage = qrencode.encode(qrtext, version=0 , level=0, hint=2, case_sensitive=True)
        #qrfile.close()
        sizedQRimage = QRimage.resize((450,450))
        return sizedQRimage
                            
        


        

BillPrinter = printBill()
BillPrinter.PrintMwst = False
BillPrinter.EndMsg = "Danke!"

posArray = []
pos1 = Pos()
pos1.nr = 1
pos1.postext = "Salami"
pos1.EP = 5.80
pos1.Menge = 1.0
pos1.reNr = "A0C12"

pos2 = Pos()
pos2.nr = 2
pos2.postext = "Schinken"
pos2.EP = 6.30
pos2.Menge = 3.0
pos1.reNr = "A0C12"

posArray.append(pos1)
posArray.append(pos2)



BillPrinter.PosArray = posArray
BillPrinter.generatePrintFile()
BillPrinter.printDocument()

