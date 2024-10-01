import os
import pathlib
import textwrap
from IPython.display import display
from IPython.display import Markdown
import json
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
def json_to_markdown():
    for jsonlocation in os.listdir("D:/GitRepos/TeachmeGCSE/json_files"):
        print(jsonlocation)
        jsonData = json.load(open(f"D:/GitRepos/TeachmeGCSE/json_files/{jsonlocation}","r"))
        for record in jsonData:
            record["ExplanationA"] = to_markdown(record["ExplanationA"])
            print(record["ExplanationA"])
            record["ExplanationB"] = to_markdown(record["ExplanationB"])
            record["ExplanationC"] = to_markdown(record["ExplanationC"])
            record["ExplanationD"] = to_markdown(record["ExplanationD"])
            with open(jsonlocation, "w") as outfile:
                json.dump(jsonData, outfile)


for jsonfile in os.listdir("D:/GitRepos/TeachmeGCSE/json_files"):
    maxChapter = 0
    sortedJson = []
    print(jsonfile)
    jsonData = json.load(open(f"D:/GitRepos/TeachmeGCSE/json_files/{jsonfile}","r"))
    for record in jsonData:
        if int(record["Chapter"])> maxChapter:
            maxChapter = int(record["Chapter"])
    for i in range(1,maxChapter + 1):
        for record in jsonData:
            if int(record["Chapter"]) == i:
                sortedJson.append(record)
    with open(f"D:/GitRepos/TeachmeGCSE/json_files/{jsonfile}","w") as outfile:
        json.dump(sortedJson, outfile)