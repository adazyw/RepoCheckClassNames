import gc
import os
import cutblock
from pprint import pprint


def remove_suffix_str(processed_string: str, suffix: str):
    # if len(self) <= 0 or len(suffix) <= 0:
    #     return self
    if suffix and processed_string.endswith(suffix):
        return processed_string[:-len(suffix)]
    else:
        return processed_string[:]


# inputPath = r'C:\GIT\Phoenix\Integration\Application\UserInterface\GenieMedical'
inputPath = r'C:\GIT\Phoenix'

# Get all .cs files from given root directory.
allCsFiles = []
for r, d, f in os.walk(inputPath):
    for anyFilePath in f:
        if anyFilePath.endswith('.cs'):
            allCsFiles.append(os.path.join(r, anyFilePath))

# pprint(allCsFiles)
totalCsCount = len(allCsFiles)
print(f'Total number of cs files: {totalCsCount}')

# Build dictionary "className: classPath"
classDic = {}
decode_error_ct = 0
for csFile in allCsFiles:
    # Read file.
    with open(csFile, mode='rt') as oFile:
        try:
            file_lines = oFile.readlines()
        except UnicodeDecodeError:
            decode_error_ct += 1
            print(f'UnicodeDecodeError: {csFile}')

    file_lines = cutblock.remove_block(file_lines, '/*', '*/', csFile)
    file_lines = cutblock.remove_block(file_lines, '[', ']', csFile)
    file_lines = cutblock.remove_block(file_lines, '<', '>', csFile)

    for line in file_lines:
        if line.strip().startswith('//'):
            continue

        expectClassName = False
        classAdded = False
        for word in line.split():
            if expectClassName:
                if word != '':
                    if word.endswith(':'):
                        word = word[:-1]
                    classDic[csFile] = word
                    classAdded = True
                    break
                else:
                    continue
            if word == 'class':
                expectClassName = True

        if classAdded:
            break

    gc.collect()

    # with open(csFile, mode='rt') as oFile:
    #     try:
    #         for line in oFile:
    #             if line.strip().startswith('//'):
    #                 continue
    #
    #             # Note: potential problem - multiline comments /* */
    #
    #             expectClassName = False
    #             classAdded = False
    #             for word in line.split():
    #                 if expectClassName:
    #                     if word != '':
    #                         classDic[word] = csFile
    #                         classAdded = True
    #                         break
    #                     else:
    #                         continue
    #                 if word == 'class':
    #                     expectClassName = True
    #
    #             if classAdded:
    #                 break
    #     except UnicodeDecodeError:
    #         print(f'UnicodeDecodeError: {csFile}')


# pprint(classDic)
print(f'Class dictionary created. Number of entries: {len(classDic)}')


# Check each file if its class name matches the file name.
badNames = {}
for classPath, className in classDic.items():
    fileName = os.path.basename(classPath)
    # print(fileName)
    # fileName, *otherStuff, fileExtension = os.path.splitext(fileName)
    # print(f'{className}, {fileName}')

    # Strip known endings.
    fileName = remove_suffix_str(fileName, '.g.i.cs')
    fileName = remove_suffix_str(fileName, '.xaml.cs')
    fileName = remove_suffix_str(fileName, '.cs')

    # Compare.
    if className != fileName:
        # print(f'{className=} {classPath=} {fileName=} {otherStuff=} {fileExtension=}')
        # print(f'{className=} {classPath=} {fileName=}')
        badNames[className] = classPath

pprint(badNames)
print(f'Total bad names: {len(badNames)}')
print(f'UnicodeDecodeErrors: {decode_error_ct}')
