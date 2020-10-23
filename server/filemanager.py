import re
import pathlib
import os

fileData = str(pathlib.Path(__file__).parent.absolute()) + "/file-data"

def validateDir(dirName):
    pattern = re.compile("\\/?%*:|\"<>")
    result = pattern.search(dirName)
    return result is None

def getPath(pathName):
    if not validateDir(pathName):
        raise Exception("Invalid PathName")
    if not pathName:
        raise Exception("Empty PathName")
    completePath = fileData + "/" + pathName
    p = pathlib.Path(completePath)
    p.mkdir(parents=True, exist_ok=True)
    return