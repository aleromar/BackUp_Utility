import os
import shutil

#FOLDER_ORIGIN = r'C:\Users\alero\Documents\Viajes'
#FOLDER_DEST   = r'C:\Users\alero\Documents\Viajes2'
FOLDER_ORIGIN = r'D:'
FOLDER_BACKUP = r'E:'

def findDifferences(pathOrigin, pathDest, fileList,folderList):
    createNewPath = lambda path,name: path+'\\'+name
    try:
        for name in os.listdir(pathOrigin):
            if os.path.isdir(createNewPath(pathOrigin,name)):
                if name in os.listdir(pathDest):
                    findDifferences(createNewPath(pathOrigin,name),createNewPath(pathDest,name), fileList,folderList)
                else:
                    folderList.append(createNewPath(pathOrigin,name))
            else:
                if name not in os.listdir(pathDest):
                    fileList.append(createNewPath(pathOrigin,name))
                try:
                    fileSize = os.stat(createNewPath(pathOrigin,name)).st_size
                    if  fileSize != os.stat(createNewPath(pathDest,name)).st_size:
                        print('File size is different for {}'.format(createNewPath(pathDest,name)))
                except:
                    print('Problems when getting file size for file {}'.format(createNewPath(pathDest,name)))
    except:
        print('\n')
        print('***ERROR occurred while trying to work on path {}'.format(pathOrigin))
        print('\n')

def CreateResultFile(misFoldO,misFileO,misFoldB,misFileB):
    def printList(thisList,filehandler,prefix):
        for item in thisList:
            filehandler.write(prefix+item+'\n')
    with open('results.txt','w') as f:
        def templateCode(f,keyWord, thisList, isBackUp):
            backupstring = lambda isBackUp : 'back-up' if isBackUp else 'origin'
            if(len(thisList) == 0):
                f.write('There are no detected new {} in {}. {} are in SYNC!\n'.format(keyWord,backupstring(not isBackUp),keyWord.title()))
            else:
                f.write('There are a total of {} new {} NOT present in the {}\n'.format(len(thisList),keyWord,backupstring(isBackUp)))
                printList(thisList,f,'    - ')
                f.write('\n')
        isBackUp = True
        isOrigin = False
        f.write('**************************************\n')
        f.write('The following will need to be COPIED from {} to the backup drive: {}\n'.format(FOLDER_ORIGIN,FOLDER_BACKUP))
        f.write('**************************************\n')
        templateCode(f,'folders',misFoldB,isBackUp)
        templateCode(f,'files',misFileB,isBackUp)
        f.write('\n\n**************************************\n')
        f.write('The following will need to be REMOVED in the backup drive: {}\n'.format(FOLDER_BACKUP))
        f.write('**************************************\n')
        templateCode(f,'folders',misFoldO,isOrigin)
        templateCode(f,'files',misFileO,isOrigin)


missingFilesInO = []
missingFoldersInO = []
missingFilesInB = []
missingFoldersInB = []

findDifferences(FOLDER_ORIGIN,FOLDER_BACKUP,missingFilesInB,missingFoldersInB)
findDifferences(FOLDER_BACKUP,FOLDER_ORIGIN,missingFilesInO,missingFoldersInO)

CreateResultFile(missingFoldersInO,missingFilesInO,missingFoldersInB,missingFilesInB)