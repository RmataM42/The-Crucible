import pandas as pd
import subprocess

# Load the Excel file
excel_path = '/Users/amatamuadthong/Desktop/467_multi_media/Project/The-Crucible/Thumbnail_with_thumbnails.xlsx'
df = pd.read_excel(excel_path)

# Function to trim video using FFmpeg
def trim_video(input_path, output_path, start_time, end_time):
    ffmpeg_command = [
        'ffmpeg',
        '-y',  # Overwrite output files without asking
        '-i', input_path,
        '-ss', start_time,
        '-to', end_time,
        '-c:v', 'copy',  # Copy the video stream
        '-c:a', 'copy',  # Copy the audio stream
        output_path
    ]
    subprocess.run(ffmpeg_command)

# Function to convert timecode to FFmpeg compatible format considering 24 fps
def convert_timecode(timecode):
    hh, mm, ss, frames = timecode.split(':')
    total_seconds = int(hh) * 3600 + int(mm) * 60 + int(ss) + int(frames) / 24
    return "{:02}:{:02}:{:06.3f}".format(int(total_seconds // 3600), int((total_seconds % 3600) // 60), total_seconds % 60)

# Path to the input video
input_video_path = '/Users/amatamuadthong/Desktop/467_multi_media/Project/The-Crucible/Test #/twitch_nft_demo.mp4'

# Iterate over each row in the dataframe
for index, row in df.iterrows():
    timecode = row['Timecode']
    start_time, end_time = timecode.split(' - ')
    
    # Convert timecodes
    start_time = convert_timecode(start_time)
    end_time = convert_timecode(end_time)
    
    # Skip if the end time is earlier than the start time
    if start_time >= end_time:
        print(f"Skipping invalid time range: {start_time} - {end_time}")
        continue
    
    # Define the output video path
    output_video_path = f'/Users/amatamuadthong/Desktop/467_multi_media/Project/The-Crucible/trim/output_trimmed_{index}.mp4'
    
    # Trim the video
    trim_video(input_video_path, output_video_path, start_time, end_time)

print("Video trimming completed.")
