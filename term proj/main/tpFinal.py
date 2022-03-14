from cmu_112_graphics import *
from tkinter import simpledialog
from tkinter import colorchooser
from PIL import ImageTk, Image,ImageOps,ImageEnhance,ImageDraw,ImageGrab
#inspirations from https://apps.apple.com/us/app/ee35-film-camera/id1313164055, past project https://www.youtube.com/watch?v=4ZWqAcqtjkc&feature=youtu.be and adobe photoshop effects

class editPhotoMode(Mode):
    def appStarted(mode):
        mode.file = filedialog.askopenfilename(initialdir = "/",title = "Select file",
                            filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        mode.imgx = mode.width//3
        mode.imgy = mode.height//2
        mode.img = Image.open(mode.file)
        mode.orgImgWidth,mode.orgImgHeight = mode.img.size
        mode.xfactor,mode.yfactor = 2,2
        mode.resized = mode.img.resize((mode.orgImgWidth//mode.xfactor,mode.orgImgHeight//mode.yfactor))
        mode.imgWidth,mode.imgHeight = mode.resized.size[0],mode.resized.size[1]

        mode.test = ImageTk.PhotoImage(mode.resized)
        mode.mouseMovedDelay = 10
        mode.storedImg = None
        mode.imgX1 = None
        mode.imgY1 = None
        mode.list = []

        # buttons and sliders from: https://www.deviantart.com/kimmaida/art/Black-UI-Icon-Set-199154951
        mode.slidertrack = ImageTk.PhotoImage(Image.open('slidertrack.png'))
        mode.hueSlidertrack = ImageTk.PhotoImage(Image.open('hueSlidertrack.png'))
        mode.tempSlidertrack = ImageTk.PhotoImage(Image.open('tempSlidertrack.png'))
        mode.tintSlidertrack = ImageTk.PhotoImage(Image.open('tintSlidertrack.png'))
        #########################################################################
        mode.sliderlen = Image.open('slidertrack.png').size[0]
        mode.sliderBrightness = ImageTk.PhotoImage(Image.open('slider.png'))
        mode.sliderBrightnessx = mode.width*7//8 - 40 
        mode.sliderContrast = ImageTk.PhotoImage(Image.open('slider.png'))
        mode.sliderContrastx = mode.width*7//8 - 40 
        mode.sliderSaturation = ImageTk.PhotoImage(Image.open('slider.png'))
        mode.sliderSaturationx = mode.width*7//8 - 40 
        mode.sliderHue = ImageTk.PhotoImage(Image.open('slider.png'))
        mode.sliderHuex = mode.width*7//8 - 40 
        mode.sliderTemp = ImageTk.PhotoImage(Image.open('slider.png'))
        mode.sliderTempx = mode.width*7//8 - 40 
        mode.sliderTint = ImageTk.PhotoImage(Image.open('slider.png'))
        mode.sliderTintx = mode.width*7//8 - 40 

        #############################################################
        mode.plus = ImageTk.PhotoImage(Image.open('plus.png'))
        mode.minus = ImageTk.PhotoImage(Image.open('minus.png'))
        mode.button = ImageTk.PhotoImage(Image.open('button.png'))
        mode.rectbutton = ImageTk.PhotoImage(Image.open('rectbutton.png'))
        mode.saveButton = ImageTk.PhotoImage(Image.open('save.png'))
        mode.infoButton = ImageTk.PhotoImage(Image.open('info.png'))
        mode.penButton = ImageTk.PhotoImage(Image.open('pen.png'))
        mode.eraserButton = ImageTk.PhotoImage(Image.open('eraser.png'))
        mode.colorPicker = ImageTk.PhotoImage(Image.open('colorpicker.png'))
        #############################################################
        mode.zoomIn = ImageTk.PhotoImage(Image.open('zoomin.png'))
        mode.zoomOut = ImageTk.PhotoImage(Image.open('zoomout.png'))
        ############################################################
        mode.storedImg = None
        mode.bw = False
        mode.sharpen = False
        mode.blur = False
        mode.sepia = False
        mode.filter1 = False
        mode.filter2 = False
        mode.filter = []
        mode.effect = dict()
        #############################################################
        mode.drawingMode = False
        mode.eraserMode = False
        mode.paintColor = 'black'
        mode.inCanvas = False
        mode.imgDraw = False
        mode.dots1 = []
        mode.dots2 = []
        mode.centers = [[]]


    #############################################################################
    def originalResizedPic(mode,img,imageWidth,imageHeight):
        newimg = Image.new(mode='RGB', size=img.size)
        for x in range(0,imageWidth):
            for y in range(0,imageHeight):
                r,g,b = img.getpixel((x,y))
                newimg.putpixel((x,y),(r,g,b))
        newimg = newimg.resize((imageWidth//mode.xfactor,imageHeight//mode.yfactor))
        return newimg
    
    def originalPic(mode,img,imageWidth,imageHeight):
        newimg = Image.new(mode='RGB', size=img.size)
        for x in range(0,imageWidth):
            for y in range(0,imageHeight):
                r,g,b = img.getpixel((x,y))
                newimg.putpixel((x,y),(r,g,b))
        return newimg
    
    def resize(mode,img,imageWidth,imageHeight,xfactor,yfactor):
        originalResizeX,originalResizeY = int(mode.orgImgWidth//mode.xfactor),int(mode.orgImgHeight//mode.yfactor)
        if abs(int(img.size[0]//xfactor) - originalResizeX) <= 10 and abs(int(img.size[1]//yfactor) - originalResizeY) <= 10:
            originalImg = editPhotoMode.originalResizedPic(mode,mode.img,mode.orgImgWidth,mode.orgImgHeight)
            if ('bw' in mode.filter):
                originalImg = editPhotoMode.convertToBW(mode,originalImg,originalResizeX,originalResizeY)
            if ('blur' in mode.filter):
                originalImg = editPhotoMode.boxBlur(mode,originalImg,originalResizeX,originalResizeY)
            if ('sharpen1' in mode.filter):
                originalImg = editPhotoMode.sharpen(mode,originalImg,1,originalResizeX,originalResizeY)
            if ('sharpen2' in mode.filter):
                originalImg = editPhotoMode.sharpen(mode,originalImg,2,originalResizeX,originalResizeY)
            if ('sepia' in mode.filter):
                originalImg = editPhotoMode.sepia(mode,originalImg,originalResizeX,originalResizeY)
            if ('filter1' in mode.filter):
                originalImg = editPhotoMode.filter1(mode,originalImg,originalResizeX,originalResizeY)
            if ('brightness' in mode.effect):
                n = mode.effect['brightness']
                originalImg = editPhotoMode.changeBrightness(mode,originalImg,n,originalResizeX,originalResizeY)
            if ('contrast' in mode.effect):
                n = mode.effect['contrast']
                originalImg = editPhotoMode.changeContrast(mode,originalImg,n,originalResizeX,originalResizeY)
            if ('saturation' in mode.effect):
                n = mode.effect['saturation']
                originalImg = editPhotoMode.changeSaturation(mode,originalImg,n,originalResizeX,originalResizeY)
            if ('hue' in mode.effect):
                n = mode.effect['hue']
                originalImg = editPhotoMode.changeHue(mode,originalImg,n,originalResizeX,originalResizeY)
            if ('tint' in mode.effect):
                n = mode.effect['tint']
                originalImg = editPhotoMode.changeTint(mode,originalImg,n,originalResizeX,originalResizeY)
            mode.imgWidth = imageWidth//xfactor
            mode.imgHeight = imageHeight//yfactor
            return originalImg
        else:
            resized = img.resize((int(img.size[0]//xfactor),int(img.size[1]//yfactor)))
            mode.imgWidth = imageWidth//xfactor
            mode.imgHeight = imageHeight//yfactor
            return resized

#question: save the canvas
    def saveImg(mode):
        path = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        if not path:
            return 
        image = mode.resized
        image = image.convert("RGB")
        image.save(path, 'JPEG')

#image grab module from = https://pillow.readthedocs.io/en/stable/reference/ImageGrab.html 
    def takeScreenShot(mode):
        x1,y1,x2,y2 = editPhotoMode.getImgPos(mode)
        width = x2-x1
        height = y2-y1
        #Note: this code only works with screens of resolution 3360*2100
        image = ImageGrab.grab((x1*2,y1*2+108,x2*2,y2*2+108))
        path = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        if not path:
            return 
        image = image.convert("RGB")
        image.save(path,'JPEG')
    
    def getImgPos(mode):
        midX,midY = mode.imgx,mode.imgy
        midImgWidth = mode.resized.size[0]/2
        midImgHeight = mode.resized.size[1]/2
        x1 = midX - midImgWidth
        y1 = midY - midImgHeight
        x2 = midX + midImgWidth
        y2 = midY + midImgHeight
        mode.imgX1 = x1
        mode.imgY1 = y1
        mode.list += [x1,y1,x2,y2]
        return x1,y1,x2,y2
    
    def withInImg(mode,x,y):
        x1,y1,x2,y2 = editPhotoMode.getImgPos(mode)
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True
        else:
            return False
    
    def chooseColor(mode):
        color = colorchooser.askcolor()
        return color

    def collide(mode,x1,y1,x2,y2,r):
        dist = ((x1-x2)**2 + (y1-y2)**2)**0.5
        if dist < (2*r):
            return True
        return False

    def truncate(mode,n):
        if n < 0:
            n = 0
        elif n > 255:
            n = 255
        else:
            return n
        return n
    
    # math conversion from: http://www.niwa.nu/2013/05/math-behind-colorspace-conversions-rgb-hsl/
    def RGBToHSL(mode,r,g,b):
        r,g,b = r/255,g/255,b/255
        maxhue = max(r,g,b)
        minhue = min(r,g,b)
        diff = maxhue - minhue
        L = (maxhue+minhue)/2

        if diff == 0:
            S,H = 0,0
            return H,S,L
        if L <= 0.5:
            S = (maxhue-minhue)/(maxhue+minhue)
        elif L > 0.5:
            S = (maxhue-minhue)/(2-maxhue-minhue)
        if diff == 0: H = 0
        elif maxhue == r: 
            H = (g-b)/diff
        elif maxhue == g:
            H = 2 + (b-r)/diff
        elif maxhue == b:
            H = 4 + (r-g)/diff
        H = H * 60
        if H < 0: H = H + 360
        
        return H,S,L
    
    #math conversion from:https://www.rapidtables.com/convert/color/hsl-to-rgb.html
    def HSLtoRGB(mode,h,s,l):
        if h==0 and s==0:
            R,G,B = int(l*255),int(l*255),int(l*255)
            return R,G,B
        
        c = (1-abs(2*l-1))*s
        x = c*(1-abs((h/60)%2-1))
        m = l-c/2
        if 0<=h<60:
            tempR, tempG, tempB = c,x,0
        elif 60<=h<120:
            tempR, tempG, tempB = x,c,0
        elif 120<=h<180:
            tempR, tempG, tempB = 0,c,x
        elif 180<=h<240:
            tempR, tempG, tempB = 0,x,c
        elif 240<=h<300:
            tempR, tempG, tempB = x,0,c
        elif 300<=h<=360:
            tempR, tempG, tempB = c,0,x
        R,G,B = int((tempR + m)*255), int((tempG + m)*255),int((tempB + m)*255)
        return R,G,B

    def truncateRGB(mode,n):
        if n < 0: 
            n = n + 1
        elif n > 1:
            n = n - 1
        return n

    def testRGB(mode,temp,temp1,temp2):
        result = None
        if 6 * temp <1:
            result = temp2 + (temp1-temp2)*6*temp
        elif 2 * temp <1:
            result = temp1
        elif 3 * temp <2:
            result = temp2+(temp1-temp2)*(2/3-temp)*6
        else:
            result = temp
        return result

    #################################filters#####################################
    # B&W
    # greyscale algorithm from https://www.dfstudios.co.uk/articles/programming/image-programming-algorithms/image-processing-algorithms-part-3-greyscale-conversion/
    # take the mean of each RGB value -> intensity
    def convertToBW(mode,img,imageWidth,imageHeight):
        for x in range(0,imageWidth):
            for y in range(0,imageHeight):
                r,g,b = img.getpixel((x,y))
                i = (r+g+b)//3
                img.putpixel((x,y),(i,i,i))
        return img
    
    #sharpen kernel matrix 1 from https://chrisalbon.com/machine_learning/preprocessing_images/sharpen_images/
    def sharpen(mode,img,n,imageWidth,imageHeight): #n=1 or n=2
        if n == 1:
            sharpen = ([[0, -1, 0], 
                        [-1, 5, -1], 
                        [0, -1, 0]])
        #kernal matrix from http://www.foundalis.com/res/imgproc.htm, this gives a stronger effect
        elif n == 2:
            sharpen = ([[-1,-1,-1],
                        [-1,9,-1],
                        [-1,-1,-1]])
        newimg = Image.new(mode='RGB', size=img.size)
        for x in range(0,imageWidth):
            for y in range(0,imageHeight):
                r,g,b = img.getpixel((x,y))
                newimg.putpixel((x,y),(r,g,b))
        for x in range(1,imageWidth-1): #col
            for y in range(1,imageHeight-1): #row
                r,g,b = img.getpixel((x,y))
                r0,g0,b0 = r * sharpen[1][1],g * sharpen[1][1],b * sharpen[1][1]
            
                r1,g1,b1 = img.getpixel(((x-1),(y-1)))
                r1,g1,b1 = r1 * sharpen[0][0],g1 * sharpen[0][0],b1 * sharpen[0][0]

                r2,g2,b2 = img.getpixel((x,(y-1)))
                r2,g2,b2 = r2 * sharpen[1][0],g2 * sharpen[1][0],b2 * sharpen[1][0]

                r3,g3,b3 = img.getpixel(((x+1),(y-1)))
                r3,g3,b3 = r3 * sharpen[2][0],g3 * sharpen[2][0],b3 * sharpen[2][0]
                
                r4,g4,b4 = img.getpixel(((x-1),y))
                r4,g4,b4 = r4 * sharpen[0][1],g4 * sharpen[0][1],b4 * sharpen[0][1]

                r5,g5,b5 = img.getpixel(((x+1),y))
                r5,g5,b5 = r5 * sharpen[2][1],g5 * sharpen[2][1],b5 * sharpen[2][1]

                r6,g6,b6 = img.getpixel(((x-1),(y+1)))
                r6,g6,b6 = r6 * sharpen[0][2],g6 * sharpen[0][2],b6 * sharpen[0][2]

                r7,g7,b7 = img.getpixel((x,(y+1)))
                r7,g7,b7 = r7 * sharpen[1][2],g7 * sharpen[1][2],b7 * sharpen[1][2]

                r8,g8,b8 = img.getpixel(((x+1),(y+1)))
                r8,g8,b8 = r8 * sharpen[2][2],g8 * sharpen[2][2],b8 * sharpen[2][2]

                newr = int(editPhotoMode.truncate(mode,r0+r1+r2+r3+r4+r5+r6+r7+r8))
                newg = int(editPhotoMode.truncate(mode,g0+g1+g2+g3+g4+g5+g6+g7+g8))
                newb = int(editPhotoMode.truncate(mode,b0+b1+b2+b3+b4+b5+b6+b7+b8))
                newimg.putpixel((x,y),(newr,newg,newb))
        return newimg

    def boxBlur(mode,img,imageWidth,imageHeight):
        blur = ([1,1,1],
                [1,1,1],
                [1,1,1])
        #takes the average of surrounding pixels
        newimg = Image.new(mode='RGB', size=img.size)
        for x in range(0,imageWidth):
            for y in range(0,imageHeight):
                r,g,b = img.getpixel((x,y))
                newimg.putpixel((x,y),(r,g,b))
        for x in range(1,imageWidth - 1): #col
            for y in range(1,imageHeight - 1): #row
                r,g,b = img.getpixel((x,y))
                r0,g0,b0 = r * blur[1][1],g * blur[1][1],b * blur[1][1]
            
                r1,g1,b1 = img.getpixel(((x-1),(y-1)))
                r1,g1,b1 = r1 * blur[0][0],g1 * blur[0][0],b1 * blur[0][0]

                r2,g2,b2 = img.getpixel((x,(y-1)))
                r2,g2,b2 = r2 * blur[1][0],g2 * blur[1][0],b2 * blur[1][0]

                r3,g3,b3 = img.getpixel(((x+1),(y-1)))
                r3,g3,b3 = r3 * blur[2][0],g3 * blur[2][0],b3 * blur[2][0]
                
                r4,g4,b4 = img.getpixel(((x-1),y))
                r4,g4,b4 = r4 * blur[0][1],g4 * blur[0][1],b4 * blur[0][1]

                r5,g5,b5 = img.getpixel(((x+1),y))
                r5,g5,b5 = r5 * blur[2][1],g5 * blur[2][1],b5 * blur[2][1]

                r6,g6,b6 = img.getpixel(((x-1),(y+1)))
                r6,g6,b6 = r6 * blur[0][2],g6 * blur[0][2],b6 * blur[0][2]

                r7,g7,b7 = img.getpixel((x,(y+1)))
                r7,g7,b7 = r7 * blur[1][2],g7 * blur[1][2],b7 * blur[1][2]

                r8,g8,b8 = img.getpixel(((x+1),(y+1)))
                r8,g8,b8 = r8 * blur[2][2],g8 * blur[2][2],b8 * blur[2][2]

                newr = int((1/9)*(r0+r1+r2+r3+r4+r5+r6+r7+r8))
                newg = int((1/9)*(g0+g1+g2+g3+g4+g5+g6+g7+g8))
                newb = int((1/9)*(b0+b1+b2+b3+b4+b5+b6+b7+b8))
                newimg.putpixel((x,y),(newr,newg,newb))
        return newimg
    
    #sepia matrix from: https://stackoverflow.com/questions/1061093/how-is-a-sepia-tone-created
    def sepia(mode,img,imageWidth,imageHeight): 
        sepia = ([0.393,0.769,0.189],
                [0.349,0.686,0.168],
                [0.272,0.534,0.131])
        newimg = Image.new(mode='RGB', size=img.size)
        for x in range(0,imageWidth):
            for y in range(0,imageHeight):
                r,g,b = img.getpixel((x,y))
                i = (r+g+b)//3
                newimg.putpixel((x,y),(i,i,i))
        for x in range(1,imageWidth-1): #col
            for y in range(1,imageHeight-1): #row
                r,g,b = img.getpixel((x,y))
                r = int(sepia[0][0]*r + sepia[0][1]*g + sepia[0][2]*b)
                g = int(sepia[1][0]*r + sepia[1][1]*g + sepia[1][2]*b)
                b = int(sepia[2][0]*r + sepia[2][1]*g + sepia[2][2]*b)
                newimg.putpixel((x,y),(r,g,b))
        return newimg

#inspirations from https://instasize.com 
    def filter1(mode,img,imageWidth,imageHeight):
        img = editPhotoMode.changeSaturation(mode,img,0.1,imageWidth,imageHeight)
        img = editPhotoMode.changeHue(mode,img,10,imageWidth,imageHeight)
        img = editPhotoMode.changeTint(mode,img,-10,imageWidth,imageHeight)
        img = editPhotoMode.changeTemperature(mode,img,+20,imageWidth,imageHeight)
        img = editPhotoMode.changeBrightness(mode,img,20,imageWidth,imageHeight)
        return img
    
    def filter2(mode,img,imageWidth,imageHeight):
        img = editPhotoMode.changeBrightness(mode,img,-20,imageWidth,imageHeight)
        img = editPhotoMode.changeContrast(mode,img,20,imageWidth,imageHeight)
        img = editPhotoMode.changeSaturation(mode,img,-0.2,imageWidth,imageHeight)
        img = editPhotoMode.changeHue(mode,img,-10,imageWidth,imageHeight)
        img = editPhotoMode.changeTint(mode,img,5,imageWidth,imageHeight)
        return img


    #################################effects#####################################

    # brightness algorithm from https://www.dfstudios.co.uk/articles/programming/image-programming-algorithms/image-processing-algorithms-part-4-brightness-adjustment/
    # add brightness to each RGB value
    def changeBrightness(mode,img,n,imageWidth,imageHeight): #-255<n<255
        for x in range(0,imageWidth):
            for y in range(0,imageHeight):
                r,g,b = img.getpixel((x,y)) #im.load()[x,y] 
                newr = editPhotoMode.truncate(mode,r + n)
                newg = editPhotoMode.truncate(mode,g + n)
                newb = editPhotoMode.truncate(mode,b + n)
                img.putpixel((x,y),(newr,newg,newb))
        return img
    

    # contrast:https://www.dfstudios.co.uk/articles/programming/image-programming-algorithms/image-processing-algorithms-part-5-contrast-adjustment/
    # factor = 259(contrast+255)/255(259-contrast) (-255<contrast<255)
    # R' = factor(R-128) + 128 within the valid range of 0 to 255
    
    def changeContrast(mode,img,n,imageWidth,imageHeight): #-255<n<255
        f = 259*(n+255)/(255*(259-n)) #such that 0<F<129 and rbg values are between 128 and 255 -> mid-level intensity to it's extreme
        for x in range(0,imageWidth):
            for y in range(0,imageHeight):
                r,g,b = img.getpixel((x,y))
                newr = int(editPhotoMode.truncate(mode,(f*(r-128)+128)))
                newg = int(editPhotoMode.truncate(mode,(f*(g-128)+128)))
                newb = int(editPhotoMode.truncate(mode,(f*(b-128)+128)))
                img.putpixel((x,y),(newr,newg,newb))
        return img
    
    def changeSaturation(mode,img,n,imageWidth,imageHeight): #0.1<n<1
        for x in range(0,imageWidth):
            for y in range(0,imageHeight):
                r,g,b = img.getpixel((x,y))
                h,s,l = editPhotoMode.RGBToHSL(mode,r,g,b)
                s = s + n
                if s>1: s = 1
                elif s<0: s = 0
                r1,g1,b1 = editPhotoMode.HSLtoRGB(mode,h,s,l)
                img.putpixel((x,y),(r1,g1,b1))
        return img
    
    def changeHue(mode,img,n,imageWidth,imageHeight): #-360<n<360 #HSV range table from: https://stackoverflow.com/questions/12357732/hsv-color-ranges-table
        for x in range(0,imageWidth):
            for y in range(0,imageHeight):
                r,g,b = img.getpixel((x,y))
                h,s,l = editPhotoMode.RGBToHSL(mode,r,g,b)
                h = h+n
                if h>360:
                    h=360
                elif h<0:
                    h=0
                r1,g1,b1 = editPhotoMode.HSLtoRGB(mode,h,s,l)
                img.putpixel((x,y),(r1,g1,b1))
        return img


    def changeTemperature(mode,img,n,imageWidth,imageHeight): #-255<n<255
        #increase red and decrease blue #adjust the warmness/coldness
        for x in range(0,imageWidth): #col
            for y in range(0,imageHeight): #row
                r,g,b = img.getpixel((x,y))
                r = editPhotoMode.truncate(mode,r + n)
                g = g
                b = editPhotoMode.truncate(mode,b - n)
                img.putpixel((x,y),(r,g,b))
        return img
    
    def changeTint(mode,img,n,imageWidth,imageHeight): #-255<n<255 #tint changes from green to magenta
        for x in range(0,imageWidth): #col
            for y in range(0,imageHeight): #row
                r,g,b = img.getpixel((x,y))
                r = r
                g = editPhotoMode.truncate(mode,g+n)
                b = b
                img.putpixel((x,y),(r,g,b))
        return img

##################################events########################################
    def mousePressed(mode,event):
        editPhotoMode.zoomIn(mode,event)
        editPhotoMode.zoomOut(mode,event)
        editPhotoMode.saveButton(mode,event)
        editPhotoMode.infoButton(mode,event)
        #################################################################
        editPhotoMode.drawingMode(mode,event)
        editPhotoMode.eraseButton(mode,event)
        editPhotoMode.colorButton(mode,event)
        mode.paintOnCanvas = editPhotoMode.withInImg(mode,event.x,event.y)
        #################################################################
        bwX = mode.width*7//8 - mode.sliderlen - 60
        bwY = mode.height//5 
        yDistToRecBut = 80

        #press B&W
        if bwX - 20 <= event.x <= bwX + 20 and bwY - 10 <= event.y <= bwY + 20:
            if mode.bw == False:
                mode.storedImg = editPhotoMode.originalPic(mode,mode.resized,mode.imgWidth,mode.imgHeight)
                mode.resized = editPhotoMode.convertToBW(mode,mode.resized,mode.imgWidth,mode.imgHeight)
                mode.test = ImageTk.PhotoImage(mode.resized)
                mode.filter.append('bw')
                mode.bw = True 
            else:
                mode.resized = mode.storedImg
                mode.test = ImageTk.PhotoImage(mode.resized)
                mode.bw = False
        
        #press sharpen
        if bwX - 20 <= event.x <= bwX + 20 and bwY + yDistToRecBut - 10 <= event.y <= bwY + yDistToRecBut + 20:
            if mode.sharpen == False:
                mode.storedImg = editPhotoMode.originalPic(mode,mode.resized,mode.imgWidth,mode.imgHeight)
                n = int(simpledialog.askstring(title="Prompt",
                                    prompt="Please key in the sharpening factor (1 or 2):"))
                if n == 1 or n == 2:
                    mode.resized = editPhotoMode.sharpen(mode,mode.resized,n,mode.imgWidth,mode.imgHeight)
                    mode.test = ImageTk.PhotoImage(mode.resized)
                    mode.sharpen = True
                    if n == 1:
                        mode.filter.append('sharpen1')
                    elif n==2:
                        mode.filter.append('sharpen2')
            else:
                mode.resized = mode.storedImg
                mode.test = ImageTk.PhotoImage(mode.resized)
                mode.sharpen = False
                if ('sharpen1'in mode.filter):
                    mode.filter.remove('sharpen1')
                elif('sharpen2'in mode.filter):
                    mode.filter.remove('sharpen2')
            
        #press blur
        if bwX - 20 <= event.x <= bwX + 20 and bwY + 2*yDistToRecBut - 10 <= event.y <= bwY + 2*yDistToRecBut + 20:
            mode.resized = editPhotoMode.boxBlur(mode,mode.resized,mode.imgWidth,mode.imgHeight)
            mode.test = ImageTk.PhotoImage(mode.resized)
            mode.filter.append('blur')
        
        #press sepia
        if bwX - 20 <= event.x <= bwX + 20 and bwY + 3*yDistToRecBut - 10 <= event.y <= bwY + 3*yDistToRecBut + 20:
            if mode.sepia == False:
                mode.storedImg = editPhotoMode.originalPic(mode,mode.resized,mode.imgWidth,mode.imgHeight)            
                mode.resized = editPhotoMode.sepia(mode,mode.resized,mode.imgWidth,mode.imgHeight)
                mode.test = ImageTk.PhotoImage(mode.resized)
                mode.sepia = True
                mode.filter.append('sepia')
            else:
                mode.resized = mode.storedImg
                mode.test = ImageTk.PhotoImage(mode.resized)
                mode.sepia = False
                mode.filter.remove('sepia')
        
        #press filter1
        if bwX - 20 <= event.x <= bwX + 20 and bwY + 4*yDistToRecBut - 10 <= event.y <= bwY + 4*yDistToRecBut + 20:
            if mode.filter1 == False:
                mode.storedImg = editPhotoMode.originalPic(mode,mode.resized,mode.imgWidth,mode.imgHeight)
                mode.resized = editPhotoMode.filter1(mode,mode.resized,mode.imgWidth,mode.imgHeight)
                mode.test = ImageTk.PhotoImage(mode.resized)
                mode.filter1 = True
                mode.filter.append('filter1')
            else:
                mode.resized = mode.storedImg
                mode.test = ImageTk.PhotoImage(mode.resized)
                mode.filter1 = False
                mode.filter.remove('filter1')
        
        #press filter2
        if bwX - 20 <= event.x <= bwX + 20 and bwY + 5*yDistToRecBut - 10 <= event.y <= bwY + 5*yDistToRecBut + 20:
            if mode.filter2 == False:
                mode.storedImg = editPhotoMode.originalPic(mode,mode.resized,mode.imgWidth,mode.imgHeight)
                mode.resized = editPhotoMode.filter2(mode,mode.resized,mode.imgWidth,mode.imgHeight)
                mode.test = ImageTk.PhotoImage(mode.resized)
                mode.filter2 = True
                mode.filter.append('filter2')
            else:
                mode.resized = mode.storedImg
                mode.test = ImageTk.PhotoImage(mode.resized)
                mode.filter2 = False
                mode.filter.remove('filter2')


        brightnessButX = mode.width*7//8 - 60 + mode.sliderlen // 2
        brightnessButY = mode.height//5 
        brightnessTrackX = mode.width*7//8 - 40
        xDistToTrack = 20
        yDistToTrack = 35
        minusX = mode.width*7//8 - 60 - mode.sliderlen // 2 
        minusY = brightnessButY + yDistToTrack
        plusX = mode.width*7//8 - 20 + mode.sliderlen // 2
        yDistToBut = 80

        #brightness
        #press -
        brightness = 2 * 255 // 4 - 50
        if brightnessButX - 20 <= event.x <= brightnessButX + 20 and brightnessButY - 20 <= event.y <= brightnessButY + 20:
            brightness = int(simpledialog.askstring(title="Prompt",
                                  prompt="Please key in the Brightness value adjustment (-255 < Brightness < 255):"))
            if brightness < -255:
                brightness = -255
            if brightness > 255:
                brightness = 255
            mode.resized = editPhotoMode.changeBrightness(mode,mode.resized, brightness, mode.imgWidth,mode.imgHeight)
            mode.test = ImageTk.PhotoImage(mode.resized)
            mode.sliderBrightnessx += (mode.sliderlen//510)*brightness
            if 'brightness' not in mode.effect:
                mode.effect['brightness'] = brightness
            else:
                mode.effect['brightness'] += brightness

        if minusX - 10 <= event.x <= minusX + 10 and minusY - 10 <= event.y <= minusY + 10:
            mode.resized = editPhotoMode.changeBrightness(mode,mode.resized, -brightness, mode.imgWidth,mode.imgHeight)
            mode.test = ImageTk.PhotoImage(mode.resized)
            mode.sliderBrightnessx -= mode.sliderlen//4
            if 'brightness' not in mode.effect:
                mode.effect['brightness'] = -brightness
            else:
                mode.effect['brightness'] -= brightness

        #press +
        if plusX- 10 <= event.x <= plusX + 10 and minusY- 10 <= event.y <= minusY + 10:
            mode.resized = editPhotoMode.changeBrightness(mode,mode.resized, +brightness, mode.imgWidth,mode.imgHeight)
            mode.test = ImageTk.PhotoImage(mode.resized)
            mode.sliderBrightnessx += mode.sliderlen//4
            if 'brightness' not in mode.effect:
                mode.effect['brightness'] = brightness
            else:
                mode.effect['brightness'] += brightness

        
        #contrast
        contrast = 50
        if brightnessButX - 20 <= event.x <= brightnessButX + 20 and brightnessButY + yDistToBut - 20 <= event.y <= brightnessButY + yDistToBut + 20:
            contrast = int(simpledialog.askstring(title="Prompt",
                                  prompt="Please key in the Contrast value adjustment (-255 < Contrast < 255):"))
            if contrast < -255:
                contrast = -255
            if contrast > 255:
                contrast = 255
            mode.resized = editPhotoMode.changeContrast(mode,mode.resized, contrast, mode.imgWidth,mode.imgHeight)
            mode.test = ImageTk.PhotoImage(mode.resized)
            mode.sliderContrastx += (mode.sliderlen//510)*contrast
            if 'contrast' not in mode.effect:
                mode.effect['contrast'] = contrast
            else:
                mode.effect['contrast'] += contrast

        if minusX -10 <= event.x <= minusX + 10 and minusY + yDistToBut - 10 <= event.y <= minusY + yDistToBut + 10:
            mode.resized = editPhotoMode.changeContrast(mode,mode.resized, -contrast, mode.imgWidth,mode.imgHeight)
            mode.test = ImageTk.PhotoImage(mode.resized)
            mode.sliderContrastx -= mode.sliderlen//4
            if 'contrast' not in mode.effect:
                mode.effect['contrast'] = -contrast
            else:
                mode.effect['contrast'] -= contrast

        if plusX -10 <= event.x <= plusX + 10 and minusY + yDistToBut - 10 <= event.y <= minusY + yDistToBut + 10:
            mode.resized = editPhotoMode.changeContrast(mode,mode.resized, +contrast, mode.imgWidth,mode.imgHeight)
            mode.test = ImageTk.PhotoImage(mode.resized)
            mode.sliderContrastx += mode.sliderlen//4
            if 'contrast' not in mode.effect:
                mode.effect['contrast'] = contrast
            else:
                mode.effect['contrast'] += contrast

        #saturation
        saturation = 0.2
        if brightnessButX - 20 <= event.x <= brightnessButX + 20 and brightnessButY + 2*yDistToBut - 20 <= event.y <= brightnessButY + 2*yDistToBut + 20:
            saturation = float(simpledialog.askstring(title="Prompt",
                                  prompt="Please key in the Saturation value adjustment (-1 < Saturation < 1):"))
            if saturation < -1.0:
                saturation = 1.0
            if saturation > 1.0:
                saturation = 1.0
            mode.resized = editPhotoMode.changeSaturation(mode,mode.resized, saturation, mode.imgWidth,mode.imgHeight)
            mode.test = ImageTk.PhotoImage(mode.resized) 
            mode.sliderSaturationx += mode.sliderlen/2 * saturation
            if 'saturation' not in mode.effect:
                mode.effect['saturation'] = saturation
            else:
                mode.effect['saturation'] += saturation

        if minusX -10 <= event.x <= minusX + 10 and minusY + 2*yDistToBut - 10 <= event.y <= minusY + 2*yDistToBut + 10:
            mode.resized = editPhotoMode.changeSaturation(mode,mode.resized, -saturation, mode.imgWidth,mode.imgHeight)
            mode.test = ImageTk.PhotoImage(mode.resized) 
            mode.sliderSaturationx -= mode.sliderlen//4
            if 'saturation' not in mode.effect:
                mode.effect['saturation'] = -saturation
            else:
                mode.effect['saturation'] -= saturation

        if plusX -10 <= event.x <= plusX + 10 and minusY + 2*yDistToBut - 10 <= event.y <= minusY + 2*yDistToBut + 10:           
            mode.resized = editPhotoMode.changeSaturation(mode,mode.resized, +saturation, mode.imgWidth,mode.imgHeight)
            mode.test = ImageTk.PhotoImage(mode.resized)
            mode.sliderSaturationx += mode.sliderlen//4
            if 'saturation' not in mode.effect:
                mode.effect['saturation'] = saturation
            else:
                mode.effect['saturation'] += saturation
        
        #hue
        hue = 36
        if brightnessButX - 20 <= event.x <= brightnessButX + 20 and brightnessButY + 3*yDistToBut - 20 <= event.y <= brightnessButY + 3*yDistToBut + 20:
            hue = int(simpledialog.askstring(title="Prompt",
                                  prompt="Please key in the Hue value adjustment (-360 < Hue < 360):"))
            if hue < -360:
                hue = -360
            elif hue >360:
                hue = 360
            mode.resized = editPhotoMode.changeHue(mode,mode.resized, hue, mode.imgWidth,mode.imgHeight)
            mode.test = ImageTk.PhotoImage(mode.resized)
            mode.sliderHuex += mode.sliderlen/720  *hue

            if 'hue' not in mode.effect:
                mode.effect['hue'] = hue
            else:
                mode.effect['hue'] += hue

        if minusX -10 <= event.x <= minusX + 10 and minusY + 3*yDistToBut - 10 <= event.y <= minusY + 3*yDistToBut + 10:
            mode.resized = editPhotoMode.changeHue(mode,mode.resized, -hue, mode.imgWidth,mode.imgHeight)
            mode.test = ImageTk.PhotoImage(mode.resized)
            mode.sliderHuex -= mode.sliderlen//20
            if 'hue' not in mode.effect:
                mode.effect['hue'] = -hue
            else:
                mode.effect['hue'] -= hue

        if plusX -10 <= event.x <= plusX + 10 and minusY + 3*yDistToBut - 10 <= event.y <= minusY + 3*yDistToBut + 10:           
            mode.resized = editPhotoMode.changeHue(mode,mode.resized, +hue, mode.imgWidth,mode.imgHeight)
            mode.test = ImageTk.PhotoImage(mode.resized)
            mode.sliderHuex += mode.sliderlen//20
            if 'hue' not in mode.effect:
                mode.effect['hue'] = hue
            else:
                mode.effect['hue'] += hue
        
        #temp
        temp = 25
        if brightnessButX - 20 <= event.x <= brightnessButX + 20 and brightnessButY + 4*yDistToBut - 20 <= event.y <= brightnessButY + 4*yDistToBut + 20:
            temp = int(simpledialog.askstring(title="Prompt",
                                  prompt="Please key in the Temperature value adjustment (-255 < Temp < 255):"))
            if temp < -255:
                temp = -255
            if temp > 255:
                temp = 255
            mode.resized = editPhotoMode.changeTemperature(mode,mode.resized, temp, mode.imgWidth,mode.imgHeight)
            mode.test = ImageTk.PhotoImage(mode.resized)
            mode.sliderTempx += mode.sliderlen/510 * temp
            if 'temp' not in mode.effect:
                mode.effect['temp'] = temp
            else:
                mode.effect['temp'] += temp

        if minusX -10 <= event.x <= minusX + 10 and minusY + 4*yDistToBut - 10 <= event.y <= minusY + 4*yDistToBut + 10:
            mode.resized = editPhotoMode.changeTemperature(mode,mode.resized, -temp, mode.imgWidth,mode.imgHeight)
            mode.test = ImageTk.PhotoImage(mode.resized)            
            mode.sliderTempx -= mode.sliderlen//20
            if 'temp' not in mode.effect:
                mode.effect['temp'] = -temp
            else:
                mode.effect['temp'] -= temp

        if plusX -10 <= event.x <= plusX + 10 and minusY + 4*yDistToBut - 10 <= event.y <= minusY + 4*yDistToBut + 10:           
            mode.resized = editPhotoMode.changeTemperature(mode,mode.resized, +temp, mode.imgWidth,mode.imgHeight)
            mode.test = ImageTk.PhotoImage(mode.resized)            
            mode.sliderTempx += mode.sliderlen//20
            if 'temp' not in mode.effect:
                mode.effect['temp'] = temp
            else:
                mode.effect['temp'] += temp
        
        #tint
        tint = 25
        if brightnessButX - 20 <= event.x <= brightnessButX + 20 and brightnessButY + 5*yDistToBut - 20 <= event.y <= brightnessButY + 5*yDistToBut + 20:
            tint = int(simpledialog.askstring(title="Prompt",
                                  prompt="Please key in the Tint value adjustment (-255 < Tint < 255):"))
            if tint < -255:
                tint = -255
            elif tint > 255:
                tint = 255
            mode.resized = editPhotoMode.changeTint(mode,mode.resized,tint, mode.imgWidth,mode.imgHeight)
            mode.test = ImageTk.PhotoImage(mode.resized)                
            mode.sliderTintx += mode.sliderlen/510 * tint
            if 'tint' not in mode.effect:
                mode.effect['tint'] = tint
            else:
                mode.effect['temp'] += tint

        if minusX -10 <= event.x <= minusX + 10 and minusY + 5*yDistToBut - 10 <= event.y <= minusY + 5*yDistToBut + 10:
            mode.resized = editPhotoMode.changeTint(mode,mode.resized, -tint, mode.imgWidth,mode.imgHeight)
            mode.test = ImageTk.PhotoImage(mode.resized)            
            mode.sliderTintx -= mode.sliderlen//20
            if 'tint' not in mode.effect:
                mode.effect['tint'] = -tint
            else:
                mode.effect['tint'] -= tint

        if plusX -10 <= event.x <= plusX + 10 and minusY + 5*yDistToBut - 10 <= event.y <= minusY + 5*yDistToBut + 10:           
            mode.resized = editPhotoMode.changeTint(mode,mode.resized, +tint, mode.imgWidth,mode.imgHeight)
            mode.test = ImageTk.PhotoImage(mode.resized)            
            mode.sliderTintx += mode.sliderlen//20
            if 'tint' not in mode.effect:
                mode.effect['tint'] = tint
            else:
                mode.effect['tint'] += tint


    def mouseDragged(mode,event):
        if mode.paintOnCanvas and mode.drawingMode:
            editPhotoMode.paint(mode,event)
        if mode.paintOnCanvas and mode.eraserMode:
            editPhotoMode.eraser(mode,event)
    
    def mouseReleased(mode,event):
        if mode.drawingMode:
            totalLines = len(mode.centers)
            if totalLines == 1:
                mode.centers[0].append((event.x,event.y))
                mode.centers.append([])
                
            elif mode.drawingMode and totalLines >= 2:
                mode.centers[totalLines-1].append((event.x,event.y))
                mode.centers.append([])
            

#question: the dots are not connected
    def paint(mode,event):
        totalLines = len(mode.centers)
        if totalLines == 1:
            mode.centers[0].append((event.x,event.y))
            mode.imgDraw = True
        else:
            mode.centers[totalLines-1].append((event.x,event.y))
            mode.imgDraw = True
        
    
#question:index out of range
    def eraser(mode,event):
        totalLines = len(mode.centers)
        for line in range(totalLines-1):
            totalDot = len(mode.centers[line])
            i = 0
            if totalDot >1 and mode.centers[line] != []:
                while i < totalDot:
                    (x,y) = mode.centers[line][i]
                    if editPhotoMode.collide(mode,x,y,event.x,event.y,3):
                        mode.centers[line].remove((x,y))
                        firstHalf = mode.centers[line][:i]
                        secondHalf = mode.centers[line][i+1:]
                        orgline = mode.centers[line]
                        mode.centers.remove(orgline)
                        mode.centers.insert(line,firstHalf)
                        mode.centers.insert(line+1,secondHalf)
                        break
                    i += 1
                    

    def keyPressed(mode,event):
        editPhotoMode.moveImg(mode,event)
        if event.key =='p':
            if mode.imgDraw:
                editPhotoMode.takeScreenShot(mode)
            else:editPhotoMode.saveImg(mode)
        elif event.key == 'q':
            mode.app.setActiveMode(mode.app.splashScreenMode)

    #change image size and move image 
    #move image by wasd keys
    def moveImg(mode,event):
        if event.key == 'w':
            mode.imgy -= 10
        elif event.key == 's':
            mode.imgy += 10
        elif event.key == 'a':
            mode.imgx -= 10
        elif event.key == 'd':
            mode.imgx += 10

    def zoomIn(mode,event):
        buttonx = 20
        buttony = mode.height - 20
        buttonDist = 25
        if buttonx - 10 <= event.x <= buttonx + 10 and buttony - buttonDist - 10<= event.y<=buttony - buttonDist + 10:
            zoomed = editPhotoMode.resize(mode,mode.resized,mode.imgWidth,mode.imgHeight,1/2,1/2)
            mode.resized = zoomed
            mode.imgWidth,mode.imgHeight = mode.resized.size[0],mode.resized.size[1]
            mode.test = ImageTk.PhotoImage(zoomed)
    
    def zoomOut(mode,event):
        buttonx = 20
        buttony = mode.height - 20
        buttonDist = 25
        if buttonx - 10 <=event.x<=buttonx + 10 and buttony - 2*buttonDist - 10<= event.y<=buttony - 2*buttonDist + 10:
            zoomed = editPhotoMode.resize(mode,mode.resized,mode.imgWidth,mode.imgHeight,2,2)
            mode.resized = zoomed
            mode.imgWidth,mode.imgHeight = mode.resized.size[0],mode.resized.size[1]
            mode.test = ImageTk.PhotoImage(zoomed)
    
    def saveButton(mode,event):
        buttonx = 20
        buttony = mode.height - 20
        if buttonx - 10 <= event.x <= buttonx + 10 and buttony - 10 <= event.y <= buttony + 10:
            if mode.imgDraw:
                editPhotoMode.takeScreenShot(mode)
            else:
                editPhotoMode.saveImg(mode)
    
    def infoButton(mode,event):
        buttonx = 20
        buttony = mode.height - 20
        buttonDist = 25
        if buttonx - 10 <=event.x<=buttonx + 10 and buttony - 3*buttonDist - 10<= event.y<=buttony - 3*buttonDist + 10:
            mode.app.setActiveMode(mode.app.helpMode)
    
    def drawingMode(mode,event):
        buttonx = 20
        buttony = mode.height - 20
        buttonDist = 25
        if buttonx - 10 <=event.x<=buttonx + 10 and buttony - 4*buttonDist - 10<= event.y<=buttony - 4*buttonDist + 10:
            mode.drawingMode = not mode.drawingMode
            mode.eraserMode = False
    
    def eraseButton(mode,event):
        buttonx = 20
        buttony = mode.height - 20
        buttonDist = 25
        if buttonx - 10 <=event.x<=buttonx + 10 and buttony - 5*buttonDist - 10<= event.y<=buttony - 5*buttonDist + 10:
            mode.eraserMode = not mode.eraserMode
            mode.drawingMode = False
    
#method from: https://www.youtube.com/watch?v=NDCirUTTrhg 
    def colorButton(mode,event):
        buttonx = 20
        buttony = mode.height - 20
        buttonDist = 25
        if buttonx - 10 <=event.x<=buttonx + 10 and buttony - 6*buttonDist - 10<= event.y<=buttony - 6*buttonDist + 10:
            mode.paintColor = editPhotoMode.chooseColor(mode)[1]


####################################drawings#####################################        
    def drawImg(mode,canvas):
        canvas.create_image(mode.imgx,mode.imgy,image = mode.test,anchor = CENTER) 

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill = 'grey68')
        editPhotoMode.drawImg(mode,canvas)
        editPhotoMode.drawSlidersAndButtons(mode,canvas)
        editPhotoMode.drawZoomInAndOutButtons(mode,canvas)
        #if mode.drawingMode == True and mode.paintOnCanvas == True:
        editPhotoMode.paintOnCanvas(mode,canvas)

#draw on image method from: https://www.daniweb.com/programming/software-development/code/216929/saving-a-tkinter-canvas-drawing-python
    def paintOnCanvas(mode,canvas):
        totalLines = len(mode.centers)
        for line in range(totalLines):
            totalDot = len(mode.centers[line])
            if totalDot > 2:
                for i in range(totalDot - 1):
                    x1,y1 = mode.centers[line][i]
                    x2,y2 = mode.centers[line][i+1]
                    imageX1,imageY1,imageX2,imageY2 = editPhotoMode.getImgPos(mode)
                    if imageX1 < x1 < imageX2 and imageY1 < y1 < imageY2:
                        canvas.create_line(x1,y1,x2,y2,fill = mode.paintColor,width = 3)
                        """
                        imgDraw = ImageDraw.Draw(mode.resized)
                        x1OnImg = x1 - mode.imgX1
                        y1OnImg = y1 - mode.imgY1
                        x2OnImg = x2 - mode.imgX1
                        y2OnImg = y2 - mode.imgY1
                        imgDraw.line([(x1OnImg,y1OnImg),(x2OnImg,y2OnImg)],fill = mode.paintColor,width = 3)
                        """
        

    def drawZoomInAndOutButtons(mode,canvas):
        buttonx = 20
        buttony = mode.height - 20
        buttonDist = 25
        #draw save button
        canvas.create_image(buttonx,buttony,image = mode.saveButton)
        #draw zoom in and zoom out
        canvas.create_image(buttonx,buttony - buttonDist,image = mode.zoomIn)
        canvas.create_image(buttonx,buttony - 2*buttonDist,image = mode.zoomOut)
        #draw info button
        canvas.create_image(buttonx,buttony - 3*buttonDist,image = mode.infoButton)
        #draw pen button
        canvas.create_image(buttonx,buttony - 4*buttonDist,image = mode.penButton)
        #draw eraser button
        canvas.create_image(buttonx,buttony - 5*buttonDist,image = mode.eraserButton)
        #draw color picker button
        canvas.create_image(buttonx,buttony - 6*buttonDist,image = mode.colorPicker)
    
    def drawOneSet(mode,canvas,effect,butX,butY,trackX,yDistToTrack,trackImg,sliderX,sliderImg,minusX,plusX):
        canvas.create_image(butX,butY,image = mode.button) 
        canvas.create_text(butX, butY, text = effect,fill = 'white') 
        canvas.create_image(trackX, butY + yDistToTrack,image = trackImg) 
        canvas.create_image(sliderX, butY + yDistToTrack,image = sliderImg) 
        canvas.create_image(minusX,butY + yDistToTrack,image = mode.minus) 
        canvas.create_image(plusX ,butY + yDistToTrack,image = mode.plus) 
    
    def drawOneFilter(mode,canvas,effect,button,butX,butY):
        canvas.create_image(butX,butY ,image = button) 
        canvas.create_text(butX,butY, text = effect,fill = 'white')

    def drawSlidersAndButtons(mode,canvas):
        brightnessButX = mode.width*7//8 - 60 + mode.sliderlen // 2
        brightnessButY = mode.height//5 
        brightnessTrackX = mode.width*7//8 - 40
        xDistToTrack = 20
        yDistToTrack = 35
        minusX = mode.width*7//8 - 60 - mode.sliderlen // 2 
        plusX = mode.width*7//8 - 20 + mode.sliderlen // 2
        yDistToBut = 80
        editPhotoMode.drawOneSet(mode,canvas,'Brightness',brightnessButX,brightnessButY,brightnessTrackX,yDistToTrack,mode.slidertrack,mode.sliderBrightnessx,mode.sliderBrightness,minusX,plusX)
        editPhotoMode.drawOneSet(mode,canvas,'Contrast',brightnessButX,brightnessButY + yDistToBut,brightnessTrackX,yDistToTrack,mode.slidertrack,mode.sliderContrastx,mode.sliderContrast,minusX,plusX)
        editPhotoMode.drawOneSet(mode,canvas,'Saturation',brightnessButX,brightnessButY + 2*yDistToBut,brightnessTrackX,yDistToTrack,mode.slidertrack,mode.sliderSaturationx,mode.sliderSaturation,minusX,plusX)
        editPhotoMode.drawOneSet(mode,canvas,'Hue',brightnessButX,brightnessButY + 3*yDistToBut,brightnessTrackX,yDistToTrack,mode.hueSlidertrack,mode.sliderHuex,mode.sliderHue,minusX,plusX)
        editPhotoMode.drawOneSet(mode,canvas,'Temperature',brightnessButX,brightnessButY + 4*yDistToBut,brightnessTrackX,yDistToTrack,mode.tempSlidertrack,mode.sliderTempx,mode.sliderTemp,minusX,plusX)
        editPhotoMode.drawOneSet(mode,canvas,'Tint',brightnessButX,brightnessButY + 5*yDistToBut,brightnessTrackX,yDistToTrack,mode.tintSlidertrack,mode.sliderTintx,mode.sliderTint,minusX,plusX)

        #B&W
        
        bwX = mode.width*7//8 - mode.sliderlen - 60
        bwY = mode.height//5 
        yDistToRecBut = 80
        editPhotoMode.drawOneFilter(mode,canvas,'B&W',mode.rectbutton,bwX,bwY)
        editPhotoMode.drawOneFilter(mode,canvas,'Sharpen',mode.rectbutton,bwX,bwY + yDistToRecBut)
        editPhotoMode.drawOneFilter(mode,canvas,'Blur',mode.rectbutton,bwX,bwY + 2*yDistToRecBut)
        editPhotoMode.drawOneFilter(mode,canvas,'Sepia',mode.rectbutton,bwX,bwY + 3*yDistToRecBut)
        editPhotoMode.drawOneFilter(mode,canvas,'Rose',mode.rectbutton,bwX,bwY + 4*yDistToRecBut)
        editPhotoMode.drawOneFilter(mode,canvas,'Oak',mode.rectbutton,bwX,bwY + 5*yDistToRecBut)



class helpMode(Mode):
    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill = 'grey68')
        helpInfo = (' 1. Select a filter effect by pressing the corresponding buttons \n 2. Change the image properties by pressing + and - buttons  \n 3. Press the buttons of the properties to key in a more specific value\n 4. Press button i for help \n 5. Press button + and - to zoom in and zoom out \n 6. Press w, a, s, d on keyboard to change the image position \n 7. Press the save button to save image \n 8. Press the pen to start drawing, use the color picker to change the paint color \n 9. Press the eraser to erase \n 10. Press Left on keyboard to continue ')
        canvas.create_text(mode.width/2, mode.height/2, text = helpInfo, font = 'Times 30')
    
    def keyPressed(mode,event):
        if event.key == 'Left':  
            mode.app.setActiveMode(mode.app.editPhotoMode)

class MyModalApp(ModalApp):
    def appStarted(app):
        app.helpMode = helpMode()
        app.editPhotoMode = editPhotoMode()
        app.splashScreenMode = splashScreenMode()
        app.setActiveMode(app.splashScreenMode)
        app.mouseMovedDelay = 10

class splashScreenMode(Mode):
    def mousePressed(mode,event):
        if mode.width//2 - 80 <= event.x <= mode.width//2 + 80 and mode.height//3 + 130 - 30 <= event.y <= mode.height//3 + 150 + 30: 
            mode.app.setActiveMode(mode.app.editPhotoMode)
        elif mode.width//2 - 80 <= event.x <= mode.width//2 + 80 and mode.height//3 + 250 - 30 <= event.y <= mode.height//3 + 250 + 30:
            mode.app.setActiveMode(mode.app.helpMode)

    def keyPressed(mode,event):
        if event.key == 'p':
            mode.app.setActiveMode(mode.app.editPhotoMode)

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill = 'grey68')
        canvas.create_image(mode.width//2,mode.height//4 + 80,image = ImageTk.PhotoImage(Image.open('title.png')))
        canvas.create_image(mode.width//2,mode.height//3 + 150,image = ImageTk.PhotoImage(Image.open('startbutton.png')))
        canvas.create_image(mode.width//2,mode.height//3 + 250,image = ImageTk.PhotoImage(Image.open('helpbutton.png')))


app = MyModalApp(width=1680, height=942)

