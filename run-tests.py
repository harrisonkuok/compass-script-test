def getExportTable(testDirectory):
    '''Gets the directory of the new export'''
    exportDirectory = join(testDirectory, "export")
    exportTables = listdir(exportDirectory)
    exportTable = exportTables[0]
    return join(exportDirectory, exportTable)  

def compareExports(exportRef, exportTable):
    '''Compares the new exported tables with the reference'''
    exportRefTables = listdir(exportRef)
    newExportTables = listdir(exportTable)

    log = str()

    for table in exportRefTables:
        if table in newExportTables:
            exportRefTablePath = join(exportRef, table)
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