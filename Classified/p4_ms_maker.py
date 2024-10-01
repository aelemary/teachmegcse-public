
from PIL import Image
import sys
from pdf2image import convert_from_path
import pytesseract
from os.path import exists
import json
import os
sys.path.append("D:\TeachmeGCSE\python_files")
from tools import combinearrayImages
from tools import searchinx
from tools import searchiny
subjectcode=9702
thissubjectName="physics"
jsonfilename="physics_p4_ms_db.json"
mypdfDirectory=f"D:\TeachmeGCSE\pdf_path\past_papers\{subjectcode}" 
myoutputdirectory=f"D:\TeachmeGCSE\images\ms\{subjectcode}\p4"
myjsonfilelocation=f"D:\TeachmeGCSE\json_files\{subjectcode}\{jsonfilename}"
Mspdf="9702_m22_ms_22.pdf"
firstimg=False
skippages=7
def makeQuestionMs(MSpdf,subjectName,pdfDirectory, outputDirectory,jsonfilelocation):
    questionNumber=1 #a value that is compared to the text in the start of the iamges to find out whether a new question has started
    endofQ=False #flag used to differentiate between page end and question end since different actions are taken for both
    totalPages=convert_from_path(f"{pdfDirectory}\{MSpdf}") #converts the pdf to a series of images
    currentQuestion=[] #stores images that are within the same question
    MSpages=[] #records only the relevant pages in totalPages array, removes all of the examiner notices
    firstPage=False
    firstJson=True
    MSData=[]
    currentfilenumber=1
    if exists(jsonfilelocation):
        with open(jsonfilelocation,'r') as jsonfile:
            MSData=json.load(jsonfile)
            firstJson=False
    while exists(f"{outputDirectory}\{subjectName}_ms_{currentfilenumber}.jpg"):
        print(currentfilenumber)
        currentfilenumber+=1
    for i in range(3,len(totalPages)):
        thisPage=totalPages[i].crop(( searchinx(totalPages[i],(0,0,0),210),searchiny(totalPages[i],(0,0,0),500)+68,searchinx(totalPages[i],(0,0,0),210,startofimg=False), searchiny(totalPages[i],(0,0,0),500,False)))
        if firstPage:
            MSpages.append(thisPage)
            thisPage.save(f"{outputDirectory}\{subjectName}_page_{i}.jpg")
        print(pytesseract.image_to_string(thisPage)[0])
        if pytesseract.image_to_string(thisPage)[0]=="1" and firstPage==False:
            firstPage=True
            MSpages.append(thisPage)
            thisPage.save(f"{outputDirectory}\{subjectName}_page_{i}.jpg")
    for page in MSpages:
        firstNum=pytesseract.image_to_string(page)[0]
        if int(firstNum)==1 and questionNumber>7:
            firstNum=pytesseract.image_to_string(page)[:2]
        print(f"{firstNum}: tesseract") #reads the first text in ocr image
        if firstNum=="A": 
            firstNum=4
        if firstNum=="B": 
            firstNum=6
        if questionNumber!=int(firstNum): #compares the first number in page to the question number to check if a new question has started
            combinearrayImages(currentQuestion,f"{outputDirectory}\{subjectName}_ms_{currentfilenumber}.jpg")
            if firstJson: 
                MSData=[{"fileName": f"{subjectName}_ms_{currentfilenumber}", "questionNumber":questionNumber, "paperCode":MSpdf}]
                firstJson=False
            else: 
                MSData.append({"fileName": f"{subjectName}_ms_{currentfilenumber}", "questionNumber":questionNumber, "paperCode":MSpdf})
            currentfilenumber+=1
            questionNumber+=1
            endofQ=False
            currentQuestion=[] #initialises the array so a new question can be added into the array
        pixel=page.load() 
        y=0
        pixelcolour=pixel[0,y]
        while pixelcolour !=(255,255,255)  and y<page.height: #makes sure that the line of reference isnt over
            pixelcolour=pixel[0,y]
            if pixelcolour==(255,255,255):
                    pixelcolour=pixel[0,y+1]
                    if pixelcolour==(255,255,255): #the comparison is done twice due to some error pixels in the pdf in the middle of the line
                        endofQ=True
                        print(1)
                        break #if the line has ended it means that the question has ended or its the end of the page
            y+=1
        if endofQ:
            currentQuestion.append(page.crop((0,0,page.width,y))) #crops the image to the point where the question ended and puts it into the currentquestion array
            print(len(currentQuestion), "len")
            combinearrayImages(currentQuestion,f"{outputDirectory}\{subjectName}_ms_{currentfilenumber}.jpg")
            if firstJson:
                MSData=[{"fileName": f"{subjectName}_ms_{currentfilenumber}", "questionNumber":questionNumber, "paperCode":MSpdf}]
                firstJson=False
            else:
                MSData.append({"fileName": f"{subjectName}_ms_{currentfilenumber}", "questionNumber":questionNumber, "paperCode":MSpdf})
            questionNumber+=1
            currentfilenumber+=1
            if y<page.height:  #checks if its the end of the page, if not, the rest is put into an array and stored as the new image
                currentQuestion=[page.crop((0,y+114,page.width,page.height))] #crops from where the first question stopped to the end of the page
                endofQ=False
        else: 
            currentQuestion.append(page)
    if len(currentQuestion)!=0: #checks if there are any items remaining in currentquestion array, and saves all of the data in it into a new iamge
        combinearrayImages(currentQuestion,f"{outputDirectory}\{subjectName}_ms_{currentfilenumber}.jpg")
        MSData.append({"fileName": f"{subjectName}_ms_{currentfilenumber}", "questionNumber":questionNumber, "paperCode":MSpdf})
    with open(jsonfilelocation,'w') as jsonfile: 
        json.dump(MSData,jsonfile,indent=1) #saves the data to the json file

makeQuestionMs("9702_s22_ms_41 .pdf", thissubjectName,mypdfDirectory, myoutputdirectory, myjsonfilelocation) 