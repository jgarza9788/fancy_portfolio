import os
import json5 as json


class portfolio:
    def __init__(self):
        self.DIR = os.path.dirname(os.path.realpath(__file__))
        self.file = os.path.join(self.DIR, 'portfolio.json')
        self.data = self.get_data(self.file)

    def get_data(self,file):
        try:
            with open(file,'r',encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

    def set_data(self,data,file):
        with open(file,'w',encoding='utf-8') as f:
            json.dump(data,f,indent=4)

    def save(self):
        self.set_data(self.data,self.file)


def tag2icon(tag):
    i = {}
    i["icon"] = "mdi-square-rounded"
    i["tooltip"] = tag

    if tag == "Java":
        i["icon"] = "mdi-language-java"
    elif tag == "JavaScript":
        i["icon"] = "mdi-language-javascript"
    elif tag == "CSS":
        i["icon"] = "mdi-language-css3"
    elif tag == "Jupyter Notebook":
        i["icon"] = "mdi-circle"
        i["tooltip"] = "Jupyter Notebook/Lab"
    elif tag == "HTML":
        i["icon"] = "mdi-language-html5"
    elif tag == "Batchfile":
        i["icon"] = "mdi-console"
    elif tag == "PowerShell":
        i["icon"] = "mdi-powershell"
    elif tag == "PowerShell":
        i["icon"] = "mdi-powershell"
    elif tag == "TypeScript":
        i["icon"] = "mdi-language-typescript"
    elif tag == "C#":
        i["icon"] = "mdi-language-csharp"
    elif tag == "Shell":
        i["icon"] = "mdi-console"
    elif tag == "VBScript":
        i["icon"] = "mdi-script"
    elif tag == "Dart":
        i["icon"] = "mdi-bird"
        i["tooltip"] = "Flutter/Dart"
    elif tag == "GLSL":
        i["icon"] = "mdi-gradient-horizontal"
        i["tooltip"] = "GLSL/ShaderLab"
    elif tag == "ShaderLab":
        i["icon"] = "mdi-gradient-horizontal"
        i["tooltip"] = "GLSL/ShaderLab"
    elif tag == "Kotlin":
        i["icon"] = "mdi-language-kotlin"
    elif tag == "Swift":
        i["icon"] = "mdi-language-swift"
    elif tag == "alpha":
        i["icon"] = "mdi-alpha"
        i["tooltip"] = "alpha/abandoned"
    elif tag == "Python":
        i["icon"] = "mdi-language-python"

    return i

def name2description(name):
    desc = "sorry, i haven't writting a description yet."

    if name == "github-scraper":
        desc = "scrapes all my public github projects using python and selenium!"
    elif name == "todo_app_flask_python":
        desc = "A basic todo app, written in python using the flask workflow."
    elif name == "HashTag_Sentiment":
        desc = "Gets the hashtag data from twitter along with the sentiment. Built with Flask, Python, along with APIs for HashTag data and Sentiment."
    elif name == "color_extractor":
        desc = "Extracts the color from an Image. Built with Python and Flask."
    elif name == "AsteroidNavigator_Demo":
        desc = "A cute little game made with Unity and C#."
    elif name == "JelloShot_demo":
        desc = "A cute little game made with Unity and C#."
    elif name == "GaussianBlur_URP_Demo":
        desc = "A screen blur effect for Unity and C#"
    elif name == "VPNTools":
        desc = "just some scripts i use to manage my VPN (NordVPN)"
    elif name == "DataAnalytics_SpaceMissions":
        desc = "Analyzing the data from the Space Missions."
    elif name == "DataAnalytics_PredictEarnings_NLSY97":
        desc = "Analyzing the data for earnings based on the data in the NLSY97 dataset."

    return desc

def add_demo_link(name):
    demolink = None

    if name == "AsteroidNavigator_Demo":
        demolink = "https://jgarza9788.github.io/AsteroidNavigator_Demo/"
    elif name == "GaussianBlur_URP_Demo":
        demolink = "https://jgarza9788.github.io/GaussianBlur_URP_Demo/"
    elif name == "ShockWave_URP_Demo":
        demolink = "https://jgarza9788.github.io/ShockWave_URP_Demo/"

    return demolink

def add_video_link(name):
    video = None

    if name == "AsteroidNavigator_Demo":
        video = "https://www.youtube.com/watch?v=BVzFEV6DejM"
    elif name == "JelloShot_Demo":
        video = "https://www.youtube.com/watch?v=YctU3RsBSFk"
    elif name == "ShockWave_URP_Demo":
        video = "https://www.youtube.com/watch?v=Z_wAd-TFDAY"
    elif name == "NightmareVsNightmare_Demo":
        video = "https://www.youtube.com/watch?v=2ErpXB4t-Ug"
    
    return video


def process_portfolio():
    import re
    pfo = portfolio()
    for p in pfo.data:
        p["demo"] = add_demo_link(p["name"])
        p["video"] = add_video_link(p["name"])

    pfo.save()

if __name__ == "__main__":
    process_portfolio()
