from os import listdir, getcwd, mkdir
from os.path import join

import subprocess

COMPASS_EXECUTABLE = "..\\..\\Compass(trunk)\\source\\com.proteinsimple.compass.e4.product\\target\\products\\compass\\win32\\win32\\x86_64\\Compass for SW.exe"
# COMPASS_EXECUTABLE = "C:\\Program Files\\Compass for SW\\Compass for SW.exe"
TEST_SUTIE_PATH = join(getcwd(), "compass-script-test-suite")

def runScripts():
    '''Takes in the directory of the test and run the tests in it'''

    tests = getTestSuite()
    for test in tests:
        runScript(tests[test])

def getTestSuite():
    tests = {}
    for test in listdir(TEST_SUTIE_PATH):
        testAbsPath = join(TEST_SUTIE_PATH, test)
        tests[test] = testAbsPath
    return tests

def runScript(testDirectory):
    '''Run a test script'''
    mkdir(join(testDirectory, "export"))
    tempScriptFile = getTempScriptFile(testDirectory)

    # Get the export by opening compass and run the script
    openCompassWithScriptFile(tempScriptFile.name)

def getTempScriptFile(testDirectory):
    '''Gets the run file, the export reference, and the script file for the test'''

    runFile, scriptFile = None, None
    for file in listdir(testDirectory):
        if file.endswith(".cbz"):
            runFile = join(testDirectory, file)
        elif file.endswith(".txt"):
            scriptFile = join(testDirectory, file)
            
    tempScriptFile = createTempScriptFile(testDirectory, runFile, scriptFile)
    return tempScriptFile

def createTempScriptFile(testDir, runFile, scriptFile):
    '''Create the temporary script test file'''
    rawScript = None
    with open(scriptFile, "r") as script:
        rawScript = script.read()
    rawScript = rawScript.format(RunFile=runFile, ExportDir=join(testDir, "export"))

    tempScriptPath = join(testDir, "temp.txt")
    with open(tempScriptPath, "w") as tempScript:
        tempScript.write(rawScript)
    return tempScript

def openCompassWithScriptFile(scriptPath):
    '''Open Compass with the test script file'''
    subprocess.call([COMPASS_EXECUTABLE, "-scriptfile", scriptPath])

runScripts()


