import json
from os.path import exists
subjectcode=9702
subjectname="physics"
jsondirectory=f"D:\TeachmeGCSE\json_files\{subjectcode}"
MSjsonDirectory=f"{jsondirectory}\physics_p4_ms_db.json"
QuestionJsonDirectory=f"{jsondirectory}\phy_db_p4.json"
def combineJSON(MSjson,QPjson,jsonName,jsonDirectory):
    totalData=[]
    MSData=json.load(open(MSjson))
    QPData=json.load(open(QPjson))
    if exists(f"{jsonDirectory}\{jsonName}"):
        totalData=json.load(f"{jsonDirectory}\{jsonName}")
    for QPindex in range(len(MSData)):
        MSindex=0
        while MSindex <len(QPData):
            if MSData[MSindex]["questionNumber"]==QPData[QPindex]["questionNum"] and MSData[MSindex]["paperCode"].replace("ms","qp")==QPData[QPindex]["pdfName"]:
                totalData.append({"questionName": QPData[QPindex]["questionName"], "MSName": MSData[MSindex]["fileName"], "questionNumber": MSData[MSindex]["questionNumber"], "pdfName":QPData[MSindex]["pdfName"]})
                break
            MSindex+=1
    with open(f"{jsonDirectory}\{jsonName}",'w') as totalJson:
        totalJson.write(json.dumps(totalData,indent=1))

combineJSON(MSjsonDirectory,QuestionJsonDirectory, "physics_p4_db.json",jsondirectory)