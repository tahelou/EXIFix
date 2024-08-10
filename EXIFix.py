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
        
        new_filename = f"{year}{month}{day}_{file_mod_time_concat}_WA{wa_code}{os.path.splitext(filename)[1]}" # [1] to get the extension .jpg
        print("New filename:",new_filename)
        # Save the image with updated EXIF data
        destination_path = os.path.join(destination_folder, new_filename)
        exif_bytes = piexif.dump(exif_data)
        image.save(destination_path, "jpeg", exif=exif_bytes)
        # Set date modified of new file
        new_time = datetime(int(year),int(month),int(day),int(file_mod_time_concat[0:2]),int(file_mod_time_concat[2:4]),int(file_mod_time_concat[4:]))
        timestamp = new_time.timestamp()
        os.utime(destination_path, (timestamp, timestamp))
        print("File saved successfully!\n")
    
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
        # Save the image with updated EXIF data
        destination_path = os.path.join(destination_folder, new_filename)
        exif_bytes = piexif.dump(exif_data)
        image.save(destination_path, "jpeg", exif=exif_bytes)
        # Set date modified of new file
        new_time = datetime(int(year),int(month),int(day),int(file_mod_time_concat[0:2]),int(file_mod_time_concat[2:4]),int(file_mod_time_concat[4:]))
        timestamp = new_time.timestamp()
        os.utime(destination_path, (timestamp, timestamp))
        print("File saved successfully!\n")

def fix_WIN_IMG(filename,file_path,destination_folder,match):
    print("Match found (Windows IMG):",filename) # test
    print("WIP\n")
            
            
            
            #new_filename = f"{year}{month}{day}_WA{wa_code}{os.path.splitext(filename)[1]}" # [1] to get the extension .jpg
            
            # # Open the image file
            # image = Image.open(file_path)
            

    
            # # Load EXIF data or initialize if not available
            # try:
            #     exif_data = piexif.load(image.info["exif"])
            # except KeyError:
            #     exif_data = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
            
            # # Extract date taken from EXIF data
            # date_taken = exif_data["Exif"].get(piexif.ExifIFD.DateTimeOriginal, None)
            # if date_taken is None:
            #     date_taken = exif_data["Exif"].get(piexif.ImageIFD.DateTime, None)
            #     if date_taken is None:
            #         date_taken = exif_data["0th"].get(piexif.ImageIFD.DateTime, None)
            #         if date_taken is None: print("No metadata")
            #         else: print("0th-ImageIFD-DateTime")
            #     else: print("Exif-ImageIFD-DateTime")
            # else: print("Exif-ExifIFD-DateTimeOriginal")
            
            
            # if date_taken == filename_date:
            #     # Date taken matches date in filename
            #     # Set date modified and created to date taken
            #     exif_data["0th"][piexif.ImageIFD.DateTime] = date_taken
            #     exif_data["Exif"][piexif.ExifIFD.DateTimeOriginal] = date_taken
            #     exif_data["Exif"][piexif.ExifIFD.DateTimeDigitized] = date_taken
                
            #     # Copy the original image to the destination with a new name
            #     destination_path = os.path.join(destination_folder, new_filename)
            #     copy2(file_path, destination_path)
            # else:
            #     # Date taken is wrong, use date from filename
            #     # Set time to 12 AM with seconds/minutes based on WA code
            #     new_time = datetime(int(year), int(month), int(day), 0, 0, int(wa_code) % 60)
            #     new_date = new_time.strftime("%Y:%m:%d %H:%M:%S")
                
            #     exif_data["0th"][piexif.ImageIFD.DateTime] = new_date
            #     exif_data["Exif"][piexif.ExifIFD.DateTimeOriginal] = new_date
            #     exif_data["Exif"][piexif.ExifIFD.DateTimeDigitized] = new_date
                
            #     # Save the image with updated EXIF data to the destination folder
            #     destination_path = os.path.join(destination_folder, new_filename)
            #     exif_bytes = piexif.dump(exif_data)
            #     image.save(destination_path, exif=exif_bytes)
            
            # print(f"Processed: {filename} to {new_filename}")

# Example usage:
