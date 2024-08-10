### EXIFix v0.2.0

import os
import time
import re
from PIL import Image
import piexif
from datetime import datetime
from shutil import copy2

# Define the regular expression pattern for WhatsApp image filenames
pattern_WhatsAppIMG = r"IMG-(\d{4})(\d{2})(\d{2})-WA(\d{4})"

# Define date modified dictionary
date_mod_dict = {'Jan':"01",'Feb':"02",'Mar':"03",'Apr':"04",'May':"05",'Jun':"06",'Jul':"07",'Aug':"08",'Sep':"09",'Oct':"10",'Nov':"11",'Dec':"12"}

def fix_WhatsAppIMG(filename,file_path,destination_folder,match):
    print("Match found (WhatsApp IMG):",filename) # test
    year, month, day, wa_code = match.groups() # Extract filename contents
    filename_date = f"{year}:{month}:{day}"
    print("Filename date:",filename_date)
    
    # Get the file's last modified time (in seconds since the epoch) and convert to a human-readable format
    file_date_modified = os.path.getmtime(file_path)
    file_date_modified_readable = time.ctime(file_date_modified)    #output: Fri Sep  9 13:07:38 2022
    file_mod_day = file_date_modified_readable[8:10].lstrip()
    if len(file_mod_day) == 1: file_mod_day = "0" + file_mod_day
    file_mod_date = f"{file_date_modified_readable[-4:]}:{date_mod_dict[file_date_modified_readable[4:7]]}:{file_mod_day}"
    file_mod_time = file_date_modified_readable[11:19]  # output 13:07:38
    file_mod_time_concat = file_mod_time.replace(':','')    # output 130738
    file_mod_date_time = f"{file_mod_date} {file_mod_time}"
    print("Date & time modified:",file_mod_date_time)
    
    # Compare filename date to date modified
    if filename_date == file_mod_date:
        dateCheck = 1
        print("Date modified matches filename")
    else:
        dateCheck = 0
        print("Date modified does not match filename")
    # print(dateCheck) #test
    
    # Open the image file. Load EXIF data or initialize if not available
    image = Image.open(file_path)
    try:
        exif_data = piexif.load(image.info["exif"])
    except KeyError:
        exif_data = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
    
    # if dateCheck == 0, update date modified and metadata to match the filename date
    # if dateCheck == 1, update the metadata to match the date modified
    
    if dateCheck == 1: # update the metadata to match the date modified
        date_taken_from_mod = file_mod_date_time.encode('utf-8') # date in bytes, compatible with EXIF data
        
        # print("Old EXIF data:",exif_data)
        exif_data["0th"][piexif.ImageIFD.DateTime] = date_taken_from_mod
        exif_data["Exif"][piexif.ExifIFD.DateTimeOriginal] = date_taken_from_mod
        exif_data["Exif"][piexif.ExifIFD.DateTimeDigitized] = date_taken_from_mod
        # print("New EXIF data:",exif_data)
              
    if dateCheck == 0: #update date modified and metadata to match the filename date
        # use date from filename and time from file_mod_time
        filename_date_time_mod = f"{filename_date} {file_mod_time}"
        print("New date from filename w/ time modified:",filename_date_time_mod)
        date_taken_from_filename = filename_date_time_mod.encode('utf-8') # date in bytes, compatible with EXIF data
                    
        # print("Old EXIF data:",exif_data)
        exif_data["0th"][piexif.ImageIFD.DateTime] = date_taken_from_filename
        exif_data["Exif"][piexif.ExifIFD.DateTimeOriginal] = date_taken_from_filename
        exif_data["Exif"][piexif.ExifIFD.DateTimeDigitized] = date_taken_from_filename
        # print("New EXIF data:",exif_data)
        
    new_filename = f"{year}{month}{day}_{file_mod_time_concat}_WA{wa_code}{os.path.splitext(filename)[1]}" # [1] to get the extension .jpg
    print("New filename:",new_filename)
    # Create a copy of the file
    destination_path = os.path.join(destination_folder, new_filename)
    copy2(file_path, destination_path)
    print(f"Copied {filename} to {destination_path} and renamed to {new_filename}")
    
    # Insert updated EXIF data to the copied image
    exif_bytes = piexif.dump(exif_data) # Dump EXIF data to bytes
    piexif.insert(exif_bytes, destination_path)    
    # image.save(destination_path, "jpeg", exif=exif_bytes)
    
    # Set date modified of new file
    new_time = datetime(int(year),int(month),int(day),int(file_mod_time_concat[0:2]),int(file_mod_time_concat[2:4]),int(file_mod_time_concat[4:]))
    timestamp = new_time.timestamp()
    os.utime(destination_path, (timestamp, timestamp))
    print("File saved successfully!\n")

def fix_WIN_IMG(filename,file_path,destination_folder,match):
    print("Match found (Windows IMG):",filename) # test
    print("WIP\n")
