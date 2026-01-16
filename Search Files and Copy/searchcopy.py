import os, os.path, shutil
from datetime import date
from pathlib import Path

# First, create a list and populate it with the files
# you want to find (1 file per row in fileslist.txt)
filesList = 'fileslist.txt'
file_exists = os.path.exists(filesList)
print(os.path.abspath(filesList), "EXISTS :", file_exists)

files_to_find = []
with open(filesList) as fh:
    for row in fh:
        files_to_find.append(row.rstrip('\n'))
    print("\nFILES TO FIND & COPY :")
    print(files_to_find)

# Then we recursively traverse through each folder
# and match each file against our list of files to find.
def searchC():
    # Parent Directory path
    parent_dir = "C:/"
    # Directory name
    some_date = date.today()
    format_code = '%Y%m%d'
    directoryName = "SearchResultsForC [" + some_date.strftime(format_code) + "]"
    # Make Directory
    path = os.path.join(parent_dir, directoryName)
    os.mkdir(path)
    print("\nDirectory '% s' created!" % path)
    print("\n[IMPORTANT] WAITING TIME DEPENDS ON THE # OF FILES & SIZE OF THE DRIVE!")
    print("[IMPORTANT] PLEASE WAIT FOR THE PROCESS TO FINISH!\n")

    for root, dirs, files in os.walk('C:\\'):
        for _file in files:
            if _file in files_to_find:
                # If we find it, notify us about it and copy it it to C:\NewPath\
                print('Found file in: ' + str(root))
                shutil.copy(os.path.abspath(root + '/' + _file), path)

def searchD():
    # Parent Directory path
    parent_dir = "D:/"
    # Directory name
    some_date = date.today()
    format_code = '%Y%m%d'
    directoryName = "SearchResultsForD [" + some_date.strftime(format_code) + "]"
    # Make Directory
    path = os.path.join(parent_dir, directoryName)
    os.mkdir(path)
    print("\nDirectory '% s' created!" % path)
    print("\n[IMPORTANT] WAITING TIME DEPENDS ON THE # OF FILES & SIZE OF THE DRIVE!")
    print("[IMPORTANT] PLEASE WAIT FOR THE PROCESS TO FINISH!\n")

    for root, dirs, files in os.walk('D:\\'):
        for _file in files:
            if _file in files_to_find:
                # If we find it, notify us about it and copy it it to D:\NewPath\
                print('Found file in: ' + str(root))
                shutil.copy(os.path.abspath(root + '/' + _file), path)

def searchCustom():
    customDriveLetter = input("Enter Drive letter: ").upper()
    # Parent Directory path
    parent_dir = "".join([customDriveLetter, ':/'])
    # Directory name
    some_date = date.today()
    format_code = '%Y%m%d'
    directoryName = "SearchResultsFor{} [".format(customDriveLetter) + some_date.strftime(format_code) + "]"
    # Make Directory
    path = os.path.join(parent_dir, directoryName)
    os.mkdir(path)
    parent_dir2 = ''.join([customDriveLetter, ':\\'])
    print("\nDirectory '% s' created!" % path)
    print("\n[IMPORTANT] WAITING TIME DEPENDS ON THE # OF FILES & SIZE OF THE DRIVE!")
    print("[IMPORTANT] PLEASE WAIT FOR THE PROCESS TO FINISH!\n")

    for root, dirs, files in os.walk(parent_dir2):
        for _file in files:
            if _file in files_to_find:
                # If we find it, notify us about it and copy it it to [?]:\NewPath\
                print('Found file in: ' + str(root))
                shutil.copy(os.path.abspath(root + '/' + _file), path)

try:
    choice = str(input("""\nChoose where to locate files: 
            c Drive C:
            d Drive D:
            e Custom Drive:
            x. Exit
    Choice: """))
    if choice.lower() == 'c':
        searchC()
        print("\nPROCESS FINISHED")
    elif choice.lower() == 'd':
        searchD()
        print("\nPROCESS FINISHED")
    elif choice.lower() == 'e':
        searchCustom()
        print("\nPROCESS FINISHED")
    elif choice.lower() == 'x':
        quit()
    else:
        raise Exception

except Exception:
    print("""\n[DISCLAIMER] for POSSIBLE CAUSE OF LAPSES OF THE PROGRAM:
    -[COMMON] Invalid input
    -[COMMON] Drive locked or non-existent
    -File corrupted
    -fileslist.txt is missing or not placed in the same directory of executable
    -fileslist.txt contain invalid characters
    -[COMMON] fileslist.txt does not contain file extensions
    -[COMMON] Operation was cancelled unexpectedly
    -[COMMON] Delete/Rename the previous generated folder to retry the search
RESTART THE PROGRAM TO RETRY.

PROGRAM FINISHED
    """)