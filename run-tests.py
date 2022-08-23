import pytest
import csv
from os import getcwd, listdir
from os.path import join

TEST_SUTIE_PATH = join(getcwd(), "compass-script-test-suite")

def createTests():
    tests = {}
    
    testSuite = getTestsSuite()
    for test in testSuite:
        tests[test] = getTablePair(testSuite[test])

    return tests

def getTestsSuite():
    testSuite = {}
    for test in listdir(TEST_SUTIE_PATH):
        testAbsPath = join(TEST_SUTIE_PATH, test)
        testSuite[test] = testAbsPath
    return testSuite

def getTablePair(test):
    exportTable = getExportTable(test)
    refTable = getRefTable(test)
    return (exportTable, refTable)


def getExportTable(test):
    exportDirectory = join(test, "export")
    exportTables = listdir(exportDirectory)
    exportTable = exportTables[0]
    return join(exportDirectory, exportTable)  

def getRefTable(test):
    for file in listdir(test):
        if file.endswith("_REF"):
            return join(test, file)

def compareExports(refTable, exportTable):
    '''Compares the new exported tables with the reference'''
    exportRefTables = listdir(refTable)
    newExportTables = listdir(exportTable)

    log = str()

    for table in exportRefTables:
        if table in newExportTables:
            exportRefTablePath = join(refTable, table)
            newExportTablePath = join(exportTable, table)
            msg = compareTables(exportRefTablePath, newExportTablePath)
            if msg:
                log += table + ": " + msg + "\n"

    return log

def compareTables(refTable, exportTable):
    '''Compares the tables'''

    refTableContent = getTableContent(refTable)
    exportTableContent = getTableContent(exportTable)

    return compareTableContent(refTableContent, exportTableContent)

def getTableContent(table):
    '''Get the table content'''

    content = []

    with open(table) as t:
        c = csv.reader(t, delimiter='\t')
        for line in c:
            content.append(line)

    return content

def compareTableContent(refContent, exportContent):
    '''Compares data in each table'''
    msg = str()

    if len(refContent) != len(exportContent):
        msg += "NUMBER OF COLUMNS DOES NOT MATCH"
    elif len(refContent[0]) != len(exportContent[0]):
        msg += "NUMBER OF COLUMNS DOES NOT MATCH"
    else:
        for i in range(len(refContent)):
            for j in range(len(refContent[0])):
                if refContent[i][j] != exportContent[i][j]:
                    msg += "DIFFERENCE FOUND IN ROW " + str(i) + " COLUMN " + str(j)
    return msg

tests = createTests()

@pytest.mark.parametrize("test", tests)
def test_tables(test):
    exportTable = tests[test][0]
    refTable = tests[test][1]
    log = compareExports(refTable, exportTable)
    tableDiff = bool(log)
    assert not tableDiff, "*In " + test + "*\n" + log