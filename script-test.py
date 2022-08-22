from os import listdir
from os.path import join, getctime
from shutil import rmtree

import sys
import csv
import subprocess

COMPASS_EXECUTABLE = "C:\\Program Files\\Compass for SW\\Compass for SW.exe"

def runTests(testSuiteDir):
    '''Takes in the directory of the test and run the tests in it'''

    log = str()

    tests = getTestSuite(testSuiteDir)
    for test in tests:
        log += "RUNNING TEST: " + test + "\n"
        log += runTest(tests[test])
    print(log)

def getTestSuite(testSuiteDir):
    '''Gets the tests from the testSuiteDir'''
    tests = {}
    for test in listdir(testSuiteDir):
        testAbsPath = join(testSuiteDir, test)
        tests[test] = testAbsPath
    return tests

def runTest(testDir):
    '''Takes in a test testDir, compare the exports and remove the new export'''

    runFile, exportRef, scriptFile = getTestContext(testDir)

    # Get the export by opening compass and run the script
    tempScriptFile = getTempScriptFile(testDir, runFile, scriptFile)
    openCompassWithScriptFile(tempScriptFile.name)
    newExport = join(testDir, getExportDir(testDir))

    log = compareExports(exportRef, newExport)

    # Remove the exported report
    rmtree(newExport)
    return log



def getTestContext(testDir):
    '''Gets the run file, the export reference, and the script file for the test'''

    runFile, exportRef, scriptFile = None, None, None
    for file in listdir(testDir):
        if file.endswith(".cbz"):
            runFile = join(testDir, file)
        elif file.endswith("_REF"):
            exportRef = join(testDir, file)
        elif file.endswith(".txt"):
            scriptFile = join(testDir, file)
    return runFile, exportRef, scriptFile

def getTempScriptFile(testDir, runFile, scriptFile):
    '''Create the temporary script test file'''
    rawScript = None
    with open(scriptFile, "r") as script:
        rawScript = script.read()
    rawScript = rawScript.format(RunFile=runFile, ExportDir=testDir)

    tempScriptPath = testDir + "\\temp.txt"
    with open(tempScriptPath, "w") as tempScript:
        tempScript.write(rawScript)
    return tempScript

def openCompassWithScriptFile(scriptPath):
    '''Open Compass with the test script file'''
    subprocess.call([COMPASS_EXECUTABLE, "-scriptfile", scriptPath])

def getExportDir(testDir):
    '''Gets the directory of the new export'''
    return max(listdir(testDir), key=lambda f: getctime(join(testDir, f)))

def compareExports(exportRef, newExport):
    '''Compares the new exported tables with the reference'''
    exportRefTables = listdir(exportRef)
    newExportTables = listdir(newExport)

    log = str()

    for table in exportRefTables:
        if table in newExportTables:
            exportRefTablePath = join(exportRef, table)
            newExportTablePath = join(newExport, table)
            msg = compareTables(exportRefTablePath, newExportTablePath)
            if msg:
                log += table + ": " + msg + "\n"
    
    if not log:
        log += "PASS\n"

    return log

def compareTables(refTable, newTable):
    '''Compares the tables'''

    refTableContent = getTableContent(refTable)
    newTableContent = getTableContent(newTable)

    return compareTableContent(refTableContent, newTableContent)

def getTableContent(table):
    '''Get the table content'''

    content = []

    with open(table) as t:
        c = csv.reader(t, delimiter='\t')
        for line in c:
            content.append(line)

    return content

def compareTableContent(refContent, newContent):
    '''Compares data in each table'''
    msg = str()

    if len(refContent) != len(newContent):
        msg += "NUMBER OF COLUMNS DOES NOT MATCH"
    elif len(refContent[0]) != len(newContent[0]):
        msg += "NUMBER OF COLUMNS DOES NOT MATCH"
    else:
        for i in range(len(refContent)):
            for j in range(len(refContent[0])):
                if refContent[i][j] != newContent[i][j]:
                    msg += "DIFFERENCE FOUND IN ROW " + str(i) + " COLUMN " + str(j)
    return msg

testSuiteArg = sys.argv[1]
runTests(testSuiteArg)


