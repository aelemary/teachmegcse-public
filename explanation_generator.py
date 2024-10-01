
import pathlib
import textwrap
import PIL.Image
import google.generativeai as genai
import json
import time
from dotenv import load_dotenv
import os
load_dotenv()
code = "0625"
subject = "physics"
level = "igcse"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
jsonPath = "D:/GitRepos/TeachmeGCSE/json_files/IG_phy_p2_db.json"
questionData = json.load(open(jsonPath, "r"))
imagePath = f"D:/GitRepos/TeachmeGCSE/images/subject_questions//igcse/{code}/p2"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')
answers = ["A", "B", "C", "D"]
for record in questionData:
    file = record["questionName"]
    print(f"***************************{file}********************************")
    img = PIL.Image.open(f"{imagePath}/{file}")
    for answer in answers:
        answerGenerated = False
        if answer == record["Answer"]:
            while not answerGenerated:
                try:
                    response = model.generate_content([img, f"""the answer to the above question is {record["Answer"]}. please give a brief explanation why the answer is {record["Answer"]} in a way that an {level} {subject} ({code} curriculum) student would understand, please try to keep it brief but if you need to write more to get the point across you can go into more detail, please dont address me directly since this is gonna be in an explanation book, and please dont ask me if i have any more questions"""], 
                            safety_settings = {
                                    'HATE': 'BLOCK_NONE',
                                    'HARASSMENT': 'BLOCK_NONE',
                                    'SEXUAL' : 'BLOCK_NONE',
                                    'DANGEROUS' : 'BLOCK_NONE'
                                    })
                    if len(response.text) > 10:
                        answerGenerated = True
                except Exception as e:
                    print(f"""failed, trying again {record["questionName"]} answer {answer} error code: {e}""")
                    time.sleep(0.2)
        else:
            while not answerGenerated:
                try:
                    response = model.generate_content([img, f"""the answer to the above question is {record["Answer"]}. please give a brief explanation why the answer is "{record["Answer"]}" and why its not {answer} in a way that an {level} {subject} ({code} curriculum) student would understand, please try to keep it brief but if you need to write more to get the point across you can go into more detail, please dont address me directly since this is gonna be in an explanation book, and please dont ask me if i have any more questions"""],
                               safety_settings = {
                                    'HATE': 'BLOCK_NONE',
                                    'HARASSMENT': 'BLOCK_NONE',
                                    'SEXUAL' : 'BLOCK_NONE',
                                    'DANGEROUS' : 'BLOCK_NONE'
                                    })
                    if len(response.text) > 10:
                        answerGenerated = True
                except Exception as e:
                    print(f"""failed, trying again {record["questionName"]} answer {answer} error code: {e}""")
                    time.sleep(0.5)
        record.update({f"Explanation{answer}": response.text})
        print(response.text)
        
json.dump(questionData, open(jsonPath, "w"))