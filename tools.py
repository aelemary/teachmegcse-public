from PIL import Image


def searchinx(img,searchcolour,constanty:int, startofimg=True ,doublecheck=False):
    currentpixel=img.load()
    if startofimg:
        start=0
        end=img.width-1
        step=1
    else:
        start=img.width-1
        end=0
        step=-1
    for i in range(start,end,step):
        if currentpixel[i,constanty]==searchcolour:
            if doublecheck:
                if currentpixel[i+1,constanty]==searchcolour:
                    return i
            else:
                return i
    return -1
def searchiny(img,searchcolour,constantx:int,startofimg=True,doublecheck=False,notColour=False):
    currentpixel=img.load()    
    if startofimg:
        start=0
        end=img.height-1
        step=1
    else:
        start=img.height-1
        end=0
        step=-1
    if notColour:
        for i in range(start,end,step):
            if currentpixel[constantx,i]!=searchcolour:
                if doublecheck:
                    if currentpixel[constantx,i+1]!=searchcolour:
                        return i
                else:
                    return i
    else:
        for i in range(start,end,step):
            if currentpixel[constantx,i]==searchcolour:
                if doublecheck:
                    if currentpixel[constantx,i+1]==searchcolour:
                        return i
                else:
                    return i
    return -1

def combinearrayImages(imageArray:list,savepath):
    x=imageArray[0].width
    y=0
    for image in imageArray:
        y+=image.height
    if len(imageArray)==1:
        imageArray[0].save(savepath)
    else: #merges all the images in the array if theres more than one image
        currenty=0
        newimage=Image.new('RGB',[x,y], (255,255,255))
        for image in imageArray:
            newimage.paste(image,(0,currenty))
            currenty+=image.height
        newimage.save(savepath)
