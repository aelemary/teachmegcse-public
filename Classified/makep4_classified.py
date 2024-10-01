from PIL import Image
import json
from fpdf import FPDF #fpdf2 is required
from PyPDF2 import PdfMerger
from tools import searchinx
subject="physics"
subjectCode="9702"
jsondirectory=f"D:\TeachmeGCSE\json_files\{subjectCode}\{subject}_p4_db.json"
chapternamesJson="D:\TeachmeGCSE\json_files\chapters.json"
questionLocation=f"D:\TeachmeGCSE\Images\subject_questions\{subjectCode}\p1"
outputDirectory=f"D:\TeachmeGCSE\pdf_path\p1_classified\{subjectCode}"

def MakeP4Classified(jsondirectory, chapterJsondirectory, outputDirectory, questionLocation, MSlocation, subject, subjectCode, hasIndex=True, hasAd=True, hasChapterPages=True, hasMS=True):
    yinpage=0
    i=0 #total counter
    ChapterPages=[]
    pageNumber=0
    questionFinished=False
    classifiedPDF=FPDF("portrait","pt",[1600,2263])
    VerticalLine=Image.open("D:\TeachmeGCSE\images\misc\\verticalline.png").resize((30,2000)) #importing verticalline, and resizing to fit whole page
    chapteri=0 #an index that traverses the chapter json file, to find the specific subject needed
    questionCounter=1
    currenty=0
    imgHeight=0
    firstPage=True
    flag=True #flag that records whether the json file has ended
    newChapter=False
    questionData=json.load(open(jsondirectory,'r'))
    chapterData=json.load(open(chapterJsondirectory,'r'))
    startofQuestion=True
    while chapterData[chapteri]["subject"]!=subject:
        chapteri+=1
    while flag:
        try:
            questionData[i]["questionName"]
        except:
            break
        if newChapter and hasChapterPages:
            classifiedPDF.add_page()
            ChapterPages.append(pageNumber) #stores page number in array to add it to the index later
            classifiedPDF.set_font("Arial", size= 150,style="B")
            classifiedPDF.set_xy(500,800)
            classifiedPDF.cell(w=700,h=500,border=False,txt=f"Chapter {questionData[i]['Chapter']}: ", center=True) #puts the chapter number in the middle of the title page
            classifiedPDF.set_xy(800,1200)
            classifiedPDF.set_font("Arial", size=77,style="U")
            classifiedPDF.multi_cell(txt=f"{chapterData[chapteri]['name'][3:]}", border=False,print_sh=True,w=1000,align="X")
            chapteri+=1
            newChapter=False
            questionCounter=1
            firstQuestioninChapter=True
        else:          
            if chapterData[i]["Chapter"]!=chapterData[i-1]["Chapter"]:
                if firstPage and hasAd: #checks if "hasAd" is True and its the first page of document to put ad for teachmeGCSE
                    classifiedPDF.add_page()
                    classifiedPDF.set_xy(700,1131)
                    classifiedPDF.set_font("Arial", size=150)
                    classifiedPDF.cell(txt="teachmegcse.com",center=True)
                    firstPage=False                        
                i+=1
                newChapter=True
                break
            else:
                if firstQuestioninChapter:
                    firstQuestioninChapter=False
                    i-=1
                ThisQ=chapterData[i]["questionName"]
                currentImg=Image.open(f"{questionLocation}\{ThisQ}")
                startY=0
                endY=0
                if currentImg.height-endY<2000:
                    classifiedPDF.add_page()
                    if startofQuestion==True:
                        classifiedPDF.set_xy(115,300)
                        classifiedPDF.set_font("Arial", size=37)
                        classifiedPDF.cell(border=False,txt=f"{questionCounter})")
                    questionCounter+=1
                    classifiedPDF.image(currentImg,180, 300, 1420,currentImg.height)
                    classifiedPDF.set_xy(770,2150)
                    classifiedPDF.set_font("Arial", size=55)#puts page number at the bottom of the page
                    classifiedPDF.cell(txt=str(pageNumber), center=True)
                else:
                    startofQuestion=True
                    while questionFinished==False:
                        classifiedPDF.add_page()
                        classifiedPDF.set_xy(115,300)
                        classifiedPDF.set_font("Arial", size=37)
                        if startofQuestion:
                            classifiedPDF.cell(border=False,txt=f"{questionCounter})")
                            startofQuestion=False
                        while currenty<2000:
                            foundStop=True
                            currenty+=1
                            for i in range(currenty,currenty+50):
                                if searchinx(currentImg,(0,0,0),i)!=-1:
                                    foundStop=False
                                    break
                            if foundStop:
                                endY=currenty+25
                        classifiedPDF.image(currentImg.crop(0,startY,currentImg.width,endY), 175, 300,1420,endY-startY)
                        startY=endY
                        
                            