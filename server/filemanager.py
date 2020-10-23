import re
import pathlib
import os

fileData = str(pathlib.Path(__file__).parent.absolute()) + "/file-data"

def validateDir(dirName):
    if not dirName:
        raise Exception("Empty Name")
    pattern = re.compile("\\/?%*:|\"<>")
    result = pattern.search(dirName)
    if result is not None:
        raise Exception("Invalid Name")
    return

def getPath(pathName):
    print('pathName: ' + pathName)
    try:
        validateDir(pathName)
    except Exception as e:
        raise e
    completePath = fileData + "/" + pathName
    p = pathlib.Path(completePath)
    p.mkdir(parents=True, exist_ok=True)
    return

def createBucket(pathName, bucketName):
    try:
        validateDir(pathName)
        validateDir(bucketName)
    except Exception as e:
        raise e
    completePath = fileData + "/" + pathName
    p = pathlib.Path(completePath)
    if not p.exists():
        raise Exception("Path doesn't exists")
    completePath += "/" + bucketName
    p = pathlib.Path(completePath)
    if p.exists():
        raise Exception('Bucket already exists')
    p.mkdir(parents=True, exist_ok=True)