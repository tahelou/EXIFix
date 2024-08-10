import os
import re
import EXIFix

source_folder = r"C:\Users\ASUS\Desktop\Fix"
destination_folder = r"C:\Users\ASUS\Desktop\Fix\Updated"

# counters
i_WhatsAppIMG = 0
i_WIN_IMG = 0
i_unrecognized = 0

# Define the regular expression pattern for WhatsApp image filenames
pattern_WhatsAppIMG = r"IMG-(\d{4})(\d{2})(\d{2})-WA(\d{4})"    # IMG-20210926-WA0106
pattern_WIN_IMG = r"WIN_(\d{4})(\d{2})(\d{2})_(\d{2})_(\d{2})_(\d{2}).*?"   # WIN_20230206_22_38_57_Pro

# Ensure the destination folder exists
if not os.path.exists(destination_folder):
    print("Destination folder does not exist. It will be created")
    os.makedirs(destination_folder)
# Check if destination_folder is empty
if os.listdir(destination_folder):
    user_response = input("Warning: Destination folder is not empty. Proceed anyway? (Y/N): ")
    if user_response.lower() in ["y","yes","ok","1"]:
        print("Proceeding")
    elif user_response.lower() in ["n","no","nah","0"]:
        print("Aborting")
        exit()
    else:
        print("Invalid input")
        exit()

# Prompt the user if they want to overwrite conflicting files or create copies ie. (0), (1), (2), etc.

# print("Directory:",os.listdir(source_folder)) #test

# Iterate over all files in the specified folder
for filename in os.listdir(source_folder):
    file_path = os.path.join(source_folder, filename)
    
    # Check if the entry is a file (skip if it's a directory)
    if not os.path.isfile(file_path):
        continue
  
    # Match the filename with the pattern for WhatsApp images (check if it's a WhatsApp image file)
    match_WhatsApp = re.match(pattern_WhatsAppIMG, filename)
    if match_WhatsApp:
        EXIFix.fix_WhatsAppIMG(filename, file_path, destination_folder, match_WhatsApp)
        i_WhatsAppIMG += 1
        continue
    # Match the filename with the pattern for WIN images
    match_WIN = re.match(pattern_WIN_IMG, filename)
    if match_WIN:
        EXIFix.fix_WIN_IMG(filename, file_path, destination_folder, match_WIN)
        i_WIN_IMG += 1
        continue
    
    # If no pattern matches, you can log or handle the file differently
    print(f"Unrecognized format: {filename}\n")
    i_unrecognized += 1

total_i = i_WhatsAppIMG + i_WIN_IMG + i_unrecognized
total_i_success = total_i - i_unrecognized
print(f"Script complete. {total_i} files were processed.")
print(f"{total_i_success} images were processed successfully.")
print(f"{i_unrecognized} files were not recognized.")