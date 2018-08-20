# -*- coding: UTF-8 -*-
import sys
import os

folderPath = sys.path[0]
suiteName = os.path.realpath(sys.argv[0]).replace(folderPath, "")[1:-3]
batPath = folderPath + "/" + suiteName + ".bat"
outputFile = open(batPath, "w")
outputFile.truncate()

list = os.listdir(sys.path[0])
outputFile.write("python ")
# outputFile.write("py.test ")
g = os.walk(folderPath)

fileName = None
folderName = None

for path, d, filelist in g:
    for filePath in filelist:
        if filePath.endswith(".py") and filePath.startswith("test_") and not filePath.__contains__(
                "__init__") and not filePath.__contains__("Suite"):
            outputFile.write(os.path.join(path, filePath).replace(os.getcwd(), "..").replace("\\", "/") + " ")

outputFile.write("--html=../report.html ")
outputFile.close()
