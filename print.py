#!/usr/bin/python3

# 13.08.2012 by Oerb
# use as ever you want
# ****************************
# PizzaProxyPrinter
# ****************************
# www.oerb.de
# github/chaosdorf
#


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
        self._nextline_Y = 0
        self._print_Y = 200
        # Parameters
        self.font_path = "/usr/share/fonts/truetype/msttcorefonts/arial.ttf"
        self.i = 0
    
    # MwSt(Tax) / Brutto Visible or Not
    @property
    def PrintMwst(self):
        return self._mwst

    @PrintMwst.setter
    def PrintMwst(self, value):
        if type(value) == bool:
            #print("NO MWST")
            self._mwst = value
    
    # Create your personal Endmessage 
    # standard is "Happy Hacking"
    @property
    def EndMsg(self):
        return self._endmsg    

    @EndMsg.setter
    def EndMsg(self,value):
        if type(value) == str:
            self._endmsg = value
    
    # change the local Printername 
    # standard is "TSP143-(STR_T-001)
    # so you know where it is designet for ;)
    @property
    def printer(self):
        return "test"
     
    @printer.setter
    def printer(self, value):
        self._printer = value
    
    # Documentname is for choose a diferen Filename
    # Read/Write the Output Printpage
    # could be usefull some day ;)
    @property
    def document(self):
        pass

    @document.setter
    def printer(self, value):
        self._document = value

    # If you want no Bill Printer just LineText than
    # set True
    @property
    def linePrinter(self):
        return self._linePrinter
    @linePrinter.setter
    def linePrinter(self, value):
        if type(value) == bool:
            self._linePrinter = True
        else:
            print("Error: Property linePrint has to be Bool")



    # takes an array of Property Classes Type Pos
    # see example at the End how to use
    # it proofs the type !!!
    @property
    def PosArray(self):
        return self._PosArray
    
    @PosArray.setter
    def PosArray(self, value):
        # needed for Type-Proof  of incoming PosArray
        PosProof = Pos()
        for element in value:
            if not type(element) == type(PosProof):
                # type proof for good objectorientation
                self._TypeOK = False
                break
            else:
                self._TypeOK = True
        if self._TypeOK:
            self._PosArray = value

    def generatePrintFile(self):
        self._loadLogo()
        
        # get the Date_Image to merge
        datadoc = self._getDataImage()
        # calculate Bill Y toot define the lp option size for 
        # Printing without foo whitelines
        width, height = datadoc.size
        h = int((height + 2100) / 4000)
        if h == 0 :
            h = 4000
        else:
            if (h%2 == 0):  # pruefung ob h gerade ist
                h = h * 4000
            else:
                h = (h + 1) * 4000  
        doc_size = ( 1200, h )
        self._print_Y = h / 20
        # the main to Print Image
        # Formatanpassung, so dass keine 
        doc = Image.new("RGB",(doc_size),"#ffffff")
        # paste the logo into the main image @ Postition x0,y100
        doc.paste(self._logo,(0,0))
        # get the Date_Image to merge
        datadoc = self._getDataImage()
     
        # Merge Data_Image with Print Image
        doc.paste(datadoc,(0,1800))
        
        # Get the Billnumber Image to merge
        reNr = self._PosArray[0].reNr
        #billnr = self._getReNr_Image(reNr)
        oldFontpath = self.font_path
        self.font_path = "/usr/share/fonts/truetype/ubuntu-font-family/UbuntuMono-B.ttf"
        newbillnr = self._getTextImage(reNr,250,"red")
        newbillnr = newbillnr.rotate(90)
        self.font_path = oldFontpath
        # Resize Billnumber_Image
        #newbillnr = billnr.resize((600,300))
        # Merge Billnumber_Image with Print Image
        doc.paste(newbillnr,(900,20))   

        # Get A QR-Code-Image of ID-URL in Form:
        # http://ihex.de/foo where foo ist the Billnumber
        qrmsg = "http://ihex.de/" + str(reNr)
        qrimage = self._getQR_Image(qrmsg)
        doc.paste(qrimage,(200,850))
        # Save PrintImage as PNG File
        #doc = doc.resize((700,2000))
        doc.save(self._document, "PNG")  
        

    # use the Shell lpr command to print the imagefile  
    def printDocument(self):
        self._callstring = "lp -o scaling=" + str(self._print_Y)  + "  -d '" + self._printer + "' " + self._document 
        subprocess.call(self._callstring , shell=True )  

    # return a sized Image-module
    def _getSizedImage(self, filename, xsize, ysize):
        img = Image.open(filename)
        sizedimg = img.resize((xsize,ysize))
        return sizedimg 
    
    # returns an image from text in the given fontsize
    def _getTextImage(self, text, font_size, colour):
        font = ImageFont.truetype(self.font_path, font_size)
        img_size = font.getsize(text) # returns ( X, Y )
        image = Image.new("RGB", img_size, "#ffffff")
        draw = ImageDraw.Draw(image)
        x, y = 0, 0
        draw.text((x, y), text, fill=colour, font=font)
#        draw.rectangle(((x, y), (x + img_size[0], y + img_size[1])), outline="green")

        #image.save("textimg" + str(self.i) + ".png")
        #self.i +=1
        return image
        
         
    def _getLineImg(self, height, colour):
        img = Image.new("RGB", (1189, height), colour)
        img_GP = Image.new("RGB", (10, height), colour)
        img.save("lineImg" + str(self.i) + ".png")

        return (img, img_GP)

    # sends the Logo as Image in resized Format
    def _loadLogo(self):
        logo = Image.open(self._LogoFilename)
        self._logo = logo.resize((700,700))
    
    def _getBillImage(self):
        # calculates Bill and return Billlist as an Array of Images
        font_size = 80
        colour = "#000000"
        imagelist = [] 
       
        # Header
        HeaderL1 = "   Bestellung   "   
        HeaderL1_GP = "in Euro "
        HeaderL2 = "Nr  Anz. Bez. "              
        HeaderL2_GP = "GP  "
        
        img = self._getTextImage(HeaderL1, font_size, colour)
        img_GP = self._getTextImage(HeaderL1_GP, font_size, colour)
        imagelist.append((img, img_GP))
        imagelist.append(self._getLineImg(50, "#ffffff"))

        img = self._getTextImage(HeaderL2, font_size, colour)
        img_GP = self._getTextImage(HeaderL2_GP, font_size, colour)
        imagelist.append((img, img_GP))

        imagelist.append(self._getLineImg(5, "#ffffff"))
        imagelist.append(self._getLineImg(2, "#000000"))
        imagelist.append(self._getLineImg(50, "#ffffff"))
                        

       
        
        Summe = 0.00

        for pos in self._PosArray:
            GP = pos.Menge * pos.EP

            shortpostext = self._postextShorter(pos.postext)

            printline = str(pos.nr) + "# x " + str(pos.Menge) + " " + shortpostext + " " 
            print_GP = "%3.2f" % (GP)

            img = self._getTextImage(printline, font_size, colour) 
            img_GP = self._getTextImage(print_GP, font_size, colour)
            imagelist.append((img, img_GP))
            
            Summe = Summe + GP
            
        # Sum and Tax
        Tax = 0.19 * Summe
        Brutto = Summe + Tax
        
        Netto_txt =  "              Netto:" 
        Netto_GP = "%5.2f" % Summe 
        Tax_txt =    "              MwSt. 19%:" 
        Tax_GP = "%5.2f" % Tax
        Brutto_txt = "              Brutto:" 
        Brutto_GP = "%5.2f" % Brutto
        Summe_txt =  "              Summe:" 
        Summe_GP = "%5.2f" % Summe

        if self._mwst:
            # Print MwSt
            imagelist.append(self._getLineImg(50, "#ffffff"))
            imagelist.append(self._getLineImg(2, "#000000"))

            img = self._getTextImage(Netto_txt, font_size, colour)
            img_GP = self._getTextImage(Netto_GP, font_size, colour)
            imagelist.append((img, img_GP))
            img = self._getTextImage(Tax_txt, font_size, colour)
            img_GP = self._getTextImage(Tax_GP, font_size, colour)
            imagelist.append((img, img_GP))

            imagelist.append(self._getLineImg(5, "#ffffff"))
            imagelist.append(self._getLineImg(2, "#000000"))
            
            img = self._getTextImage(Brutto_txt, font_size, colour)
            img_GP = self._getTextImage(Brutto_GP, font_size, colour)
            imagelist.append((img, img_GP))
            
        else:
            # do not print MwSt just an Order
            imagelist.append(self._getLineImg(50, "#ffffff"))
            imagelist.append(self._getLineImg(2, "#000000"))

            img = self._getTextImage(Summe_txt, font_size, colour)
            img_GP = self._getTextImage(Summe_GP, font_size, colour)
            imagelist.append((img, img_GP))
                                                
        
        # End Message
        imagelist.append(self._getLineImg(150, "#ffffff"))
        imagelist.append(self._getLineImg(4, "#000000"))

        img = self._getTextImage(self._endmsg, font_size, "red")
        img_GP = self._getTextImage(" ", font_size , colour)
        imagelist.append((img, img_GP))

        
        
        return imagelist                     

    def _getDataImage(self):
        # merges the Imagelist to one Image
        mainImgSize = 1200
        imagelist = self._getBillImage()
        newimg_width = 0
        newimg_height = 0


        for img, img_GP in imagelist:
            width, height = img.size
            newimg_height = newimg_height + height

#            if width > newimg_width:
#                newimg_width = width

        newImg = Image.new("RGB",(mainImgSize, newimg_height),"#ffffff")
        x, y = 0, 0
        i = 0
        for img, img_GP in imagelist:
            width, height = img.size
            GP_width, GP_height = img_GP.size
            newImg.paste(img, (x, y))
            x_GP = mainImgSize - GP_width
#            print("y_GP: " + str(x_GP))
#            print("GP_width: " + str(GP_width))
#            print("img width: " + str(width))
            newImg.paste(img_GP, (x_GP, y))
            #newImg.save("img-img_GP" + str(i) + ".png")
            #i +=1
            y = y + height 

        return newImg
                
       
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
        sizedQRimage = QRimage.resize((800,800))
        return sizedQRimage
                            
        

class main(object):
    def __init__(self):

        # Test / Help Example        

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

        i = 5
        while i > 0:
            posArray.append(pos1)
            posArray.append(pos2)
            i -= 1

        BillPrinter.PosArray = posArray
        BillPrinter.generatePrintFile()
        BillPrinter.printDocument()

if __name__== "__main__":
    start = main()
