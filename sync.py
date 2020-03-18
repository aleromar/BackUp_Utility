import os
import shutil
import datetime

FOLDER_ORIGIN = r'D:'
FOLDER_BACKUP = os.getcwd()
FOLDERS_TO_SYNC = ['alejandro','Documents']

def findDifferences(fError,pathOrigin, pathDest, fileList,folderList):
    createNewPath = lambda path,name: path+'\\'+name
    try:
        for name in os.listdir(pathOrigin):
            if os.path.isdir(createNewPath(pathOrigin,name)):
                if name in os.listdir(pathDest):
                    findDifferences(fError,createNewPath(pathOrigin,name),createNewPath(pathDest,name), fileList,folderList)
                else:
                    folderList.append(createNewPath(pathOrigin,name))
            else:
                if name not in os.listdir(pathDest):
                    fileList.append(createNewPath(pathOrigin,name))
                try:
                    fileSize = os.stat(createNewPath(pathOrigin,name)).st_size
                    if  fileSize != os.stat(createNewPath(pathDest,name)).st_size:
                        fError.write('File size is different for {}\n'.format(createNewPath(pathDest,name)))
                except:
                    fError.write('Problems when getting file size for file {}\n'.format(createNewPath(pathDest,name)))
    except:
        fError.write('\n')
        fError.write('ERROR occurred while trying to work on path {}\n'.format(pathOrigin))
        fError.write('\n')

def CreateResultFile(f,misFoldO,misFileO,misFoldB,misFileB,orPath,bckPath):
    fcPrefix = '    '
    def printList(thisList,filehandler,prefix):
        for item in thisList:
            filehandler.write(fcPrefix+prefix+item+'\n')

    def templateCode(f,keyWord, thisList, isBackUp):
        backupstring = lambda isBackUp : 'back-up' if isBackUp else 'origin'
        if(len(thisList) == 0):
            f.write('{}    There are no detected new {} in {}. {} are in SYNC!\n'.format(fcPrefix,keyWord,backupstring(not isBackUp),keyWord.title()))
        else:
            f.write('{}    There are a total of {} new {} NOT present in the {}\n'.format(fcPrefix,len(thisList),keyWord,backupstring(isBackUp)))
            printList(thisList,f,'    - ')
            f.write('\n')
    isBackUp = True
    isOrigin = False
    f.write('{}The following will need to be COPIED from {} to the backup drive: {}\n'.format(fcPrefix,orPath,bckPath))
    templateCode(f,'folders',misFoldB,isBackUp)
    templateCode(f,'files',misFileB,isBackUp)
    f.write('\n\n')
    f.write('{}The following will need to be REMOVED in the backup drive: {}\n'.format(fcPrefix,bckPath))
    templateCode(f,'folders',misFoldO,isOrigin)
    templateCode(f,'files',misFileO,isOrigin)

with open('errorLog.txt','w') as fError:
    enterTime = lambda handle: handle.write('Sync script run on {}\n\n'.format(datetime.datetime.now()))
    with open('results.txt','w') as f:
        enterTime(f)
        enterTime(fError)
        for foldertosync in FOLDERS_TO_SYNC:
            f.write('**************************************\n')
            f.write('Results {}\n'.format(foldertosync.upper()))
            f.write('**************************************\n')
            missingFilesInO = []
            missingFoldersInO = []
            missingFilesInB = []
            missingFoldersInB = []
            createNewPath = lambda path: path+'\\'+foldertosync
            findDifferences(fError,createNewPath(FOLDER_ORIGIN),createNewPath(FOLDER_BACKUP),missingFilesInB,missingFoldersInB)
            findDifferences(fError,createNewPath(FOLDER_BACKUP),createNewPath(FOLDER_ORIGIN),missingFilesInO,missingFoldersInO)
            CreateResultFile(f,missingFoldersInO,missingFilesInO,missingFoldersInB,missingFilesInB,createNewPath(FOLDER_ORIGIN),createNewPath(FOLDER_BACKUP))
            f.write('\n\n')