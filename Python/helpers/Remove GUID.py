# importing os module

import os

for root, dirs, files in os.walk(
    "C:/Users/Jack.Ball/Documents/Work/SGSS/Python Test Files/"
):  # Folder path
    for file in files:

        dst = file[9:]  # Number of characters you wish to remove from start of filename

        src = root + "/" + file
        dst = root + "/" + dst

        # rename() function will
        # rename all the files
        os.rename(src, dst)
        print("Renamed: " + src)
        print("To: " + dst)
        print("")
