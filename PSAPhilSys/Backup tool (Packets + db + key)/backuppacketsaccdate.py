import os, shutil, time, traceback, datetime
from datetime import datetime
from future.backports.datetime import timedelta

def dateRange(createdDate, startDate, endDate):
    # determines if date is in range
    createdDate = datetime.strptime(createdDate, '%a %b %d %H:%M:%S %Y')
    startDate = datetime.strptime(startDate, '%Y-%m-%d')
    endDate = datetime.strptime(endDate, '%Y-%m-%d')
    return startDate < createdDate < endDate

def searchCustom():
    source_packets = input("""
[SAMPLE] C:\PhilSys_20210713\Reg-client.1.4.4_012122\packet\packet-manager
    Enter path\directory of packet-manager: """)
    date_created = input("""
[SAMPLE] yyyy-mm-dd -> 2022-05-31
    Enter START date range: """)
    date_end = input("""
[SAMPLE] yyyy-mm-dd -> 2022-06-12
    Enter END date range: """)

    date_end_raw = datetime.strptime(date_end, '%Y-%m-%d') + timedelta(days=1)
    date_end_format = str(date_end_raw).replace(" 00:00:00", "")

    source_db = input("""
[SAMPLE] C:\PhilSys_20210713\Reg-client.1.4.4_012122\Reg-client.1.4.4_012122\db
    Enter path\directory of db: """)

    source_mosipkeys = input("""
[SAMPLE] C:\ProfileUser\PhilSys\.mosipkeys
    Enter path\directory of mosipkeys: """)

    # Parent Directory path
    parent_dir = "".join(['D', ':/'])
    # Directory name
    directoryName = "packets (" + date_created.replace('-', '') + "-" + date_end.replace('-', '') + ")"
    subFolderName = "packet-manager"
    # Make Directory
    new_dir = os.path.join(parent_dir, directoryName)
    new_dir2 = os.path.join(new_dir, subFolderName)
    os.mkdir(new_dir)
    os.mkdir(new_dir2)
    print("\nDirectory '% s' created!" % new_dir)
    print("\nDirectory '% s' created!" % new_dir2)
    print("\n[IMPORTANT] WAITING TIME DEPENDS ON THE # OF FILES!")
    print("[IMPORTANT] PLEASE WAIT FOR THE PROCESS TO FINISH!\n")

    #Copy db content
    new_dir_format = ''.join([new_dir, '\\db'])
    shutil.copytree(source_db, new_dir_format, symlinks=False, ignore=None, ignore_dangling_symlinks=False,
                    dirs_exist_ok=False)

    #Copy .mosipkeys content
    new_dir_format = ''.join([new_dir, '\\.mosipkeys'])
    shutil.copytree(source_mosipkeys, new_dir_format, symlinks=False, ignore=None, ignore_dangling_symlinks=False,
                    dirs_exist_ok=False)

    #Copy specified packets
    source_dir_format = ''.join([source_packets, '\\'])

    for filename in os.listdir(source_dir_format):
        created = time.ctime(os.path.getmtime(source_dir_format + filename))
        if filename.endswith('.html') and dateRange(created, date_created, date_end_format):
            shutil.copy(source_dir_format + filename, new_dir2)
            print("[+] File copied " + filename + " " + created)
        else:
            print("[x] File not included " + filename + " " + created)

        if filename.endswith('.zip') and dateRange(created, date_created, date_end_format):
            shutil.copy(source_dir_format + filename, new_dir2)
            print("[+] File copied " + filename + " " + created)
        else:
            print("[x] File not included " + filename + " " + created)

    print("[!] Transfer complete")


# try:
choice = str(input("""\n
====================NOTICE======================
MAKE SURE YOU TRIED UPLOADING ALL YOUR PACKETS!
PLEASE CLOSE THE REGCLIENT UPON USING THIS TOOL!
PLEASE COORDINATE WITH YOUR I.S.A UPON USE!
====================NOTICE======================

Choose an option: 
        Y Start
        N Exit
Choice: """))
if choice.lower() == 'y':
    searchCustom()
    print("\nPROCESS FINISHED")
elif choice.lower() == 'n':
    quit()
else:
    traceback.print_exc()

# except Exception:
#     print(f"""\n[DISCLAIMER] for POSSIBLE CAUSE OF LAPSES OF THE PROGRAM:
#     -[COMMON] Invalid input
#     -[COMMON] Drive locked or non-existent
#     -[COMMON] Operation was cancelled unexpectedly
#     -[COMMON] Delete/Rename the previous generated folder to retry the search
# RESTART THE PROGRAM TO RETRY.
#
# PROGRAM FINISHED with exit code {traceback.print_exc()}
#     """)
