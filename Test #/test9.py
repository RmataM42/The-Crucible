import pandas as pd
import subprocess
import os
from PIL import Image as PILImage
from openpyxl import load_workbook
from openpyxl.drawing.image import Image

# Paths to the Excel file and MP4 file
file_path = '/Users/amatamuadthong/Desktop/467_multi_media/Project/The-Crucible/Thumbnail.xlsx'
mp4_file_path = '/Users/amatamuadthong/Desktop/467_multi_media/Project/The-Crucible/Reference/twitch_nft_demo.mp4'

# Load the Excel file
excel_data = pd.read_excel(file_path)

# Function to convert timecode from HH:MM:SS:FF to HH:MM:SS
def convert_timecode(timecode):
    parts = timecode.split(':')
    return ':'.join(parts[:3])

# Extract start timecodes from the "Timecode" column and convert them
excel_data['Start_Timecode'] = excel_data['Timecode'].apply(lambda x: x.split(' - ')[0])
excel_data['Converted_Start_Timecode'] = excel_data['Start_Timecode'].apply(convert_timecode)

# Directory to save the temporary thumbnails
thumbnail_dir = '/Users/amatamuadthong/Desktop/467_multi_media/Project/The-Crucible/temp_thumbnails/'
os.makedirs(thumbnail_dir, exist_ok=True)

# Generate thumbnails using FFmpeg for each converted start timecode
for index, row in excel_data.iterrows():
    timecode = row['Converted_Start_Timecode']
    output_thumbnail = f"{thumbnail_dir}thumbnail_{index + 1}.png"
    
    # FFmpeg command to generate thumbnail
    ffmpeg_command = [
        'ffmpeg', '-ss', timecode, '-i', mp4_file_path,
        '-vframes', '1', '-q:v', '2', output_thumbnail
    ]
    
    # Execute the command
    subprocess.run(ffmpeg_command)
    
    # Resize the thumbnail to 96x74 pixels
    img = PILImage.open(output_thumbnail)
    img = img.resize((50, 20), PILImage.LANCZOS)
    img.save(output_thumbnail)

# Load the workbook and select the active worksheet
workbook = load_workbook(file_path)
sheet = workbook.active

# Embed the thumbnails into the Excel file in the 4th column
for index, row in excel_data.iterrows():
    img_path = f"{thumbnail_dir}thumbnail_{index + 1}.png"
    img = Image(img_path)
    
    # Calculate the cell position (openpyxl uses 1-based indexing)
    cell = f'D{index + 2}'
    
    # Add the image to the sheet
    sheet.add_image(img, cell)

# Save the workbook
output_excel_path = '/Users/amatamuadthong/Desktop/467_multi_media/Project/The-Crucible/Thumbnail_with_thumbnails.xlsx'
workbook.save(output_excel_path)

# Clean up temporary thumbnails
for file in os.listdir(thumbnail_dir):
    os.remove(os.path.join(thumbnail_dir, file))

# Print the path to the updated Excel file
print(f"Thumbnails embedded into Excel file: {output_excel_path}")
