# Requires pip install requests

import requests
import os
import re
from urllib.parse import urljoin

# Base URL structure
base_url = "https://edid.tv/edid/"
start_num = 1
end_num = 3350 
# current number of EDIDs on edid.tv = 3349. Change as needed.

# Base directory to save downloaded EDID folders
base_dir = "downloaded_edids"
os.makedirs(base_dir, exist_ok=True)

# Function to extract filename from the content header
def get_filename_from_cd(cd):
    if not cd:
        return None
    # Check if the content-disposition header contains a filename
    filename = None
    if "filename=" in cd:
        filename = cd.split("filename=")[-1].strip('"')
    return filename

# Function to sanitize filenames
def sanitize_filename(filename):
    # Remove or replace invalid characters for Windows filenames
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# Function to download the content of URL
def download_content(url, folder_name):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

        # Try to get the filename from header
        content_disposition = response.headers.get('Content-Disposition')
        filename = get_filename_from_cd(content_disposition)

        # If no filename is found, generate one based on the URL number
        if not filename:
            filename = f"content_{url.split('/')[-2]}.bin"  # Default fallback filename
        
        # Sanitize the filename to remove invalid characters
        filename = sanitize_filename(filename)

        # Create a folder for this specific EDID
        folder_path = os.path.join(base_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # Save the file within its own folder
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        print(f"Downloaded content from {url} and saved as {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download content from {url}: {e}")

# Loop through the numbers and construct the URLs
for num in range(start_num, end_num + 1):
    url = urljoin(base_url, f"{num}/download/")
    folder_name = f"edid_{num}"  # Folder named based on the number from the URL
    download_content(url, folder_name)
