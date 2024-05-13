from argparse import ArgumentParser
from pymongo import MongoClient
import os
import csv
import sys
import pandas as pd
import subprocess

# Argparse setup
parser = ArgumentParser(description='It does frame IO... stuff..')

parser.add_argument("--baselight", metavar='', help="Baselight stuff")
parser.add_argument("--xytech", metavar='', help="Xytech stuff")
parser.add_argument('--process', required=True, help='Path to the video file')
parser.add_argument("--output", metavar='', help="Output stuff")
# debug: argparse
parser.add_argument("--timecode", metavar='', type=int, help="Frame to timecode; must follow by an integer to calcualte")
# debug: baselight & xytech from project 1
parser.add_argument("-bx", action='store_true', help="From Project 1: Create csv with location and frame to fix")
# debug: matches frame to fix with timecode
parser.add_argument("--frame-timecode", action='store_true', help="Write csv: matches frame to fix with time code")

args = parser.parse_args()                       

# File path
Xytech_file_path = "baselight_xytech/Sample_Xytech.txt"
Baselight_file_path = "baselight_xytech/Sample_Baselight_export.txt"

# DB setup
# Connect to MongoDB locally
client = MongoClient("mongodb://localhost:27017/")
# Get the crucicle database
db = client["crucible"]
final = db["Baselight_Xytech"]

# Modified project 1: written to csv file instead of console output
def baselight_xytech_csv():
    xytech_folders = []
    try:
        with open(Xytech_file_path, 'r') as read_xytech_file:
            for line in read_xytech_file:
                if "/" in line:
                    xytech_folders.append(line.strip())
    except FileNotFoundError:
        print("File not found.")
        return
    except PermissionError:
        print("Permission denied.")
        return

    try:
        with open(Baselight_file_path, 'r') as baselight_file, open("baselight_xytech.csv", "w", newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['location', 'Frames to fix'])

            for line in baselight_file:
                line_split = line.split(" ")
                line_pop = line_split.pop(0)
                line_replace = line_pop.replace("/baselightfilesystem1","")
                new_file_path = ""
                for xytech_check in xytech_folders:
                    if line_replace in xytech_check:
                        new_file_path = xytech_check.strip()

                head = ""
                curr = ""
                last = ""
                for frame in line_split:
                    stripped_frame = frame.strip()
                    if not stripped_frame.isnumeric():
                        continue
                    if head == "":
                        head = int(stripped_frame)
                        curr = head
                        continue

                    if int(stripped_frame) == (curr+1):
                        curr = int(stripped_frame)
                        continue
                    else:
                        last = curr
                        if head == last:
                            writer.writerow([new_file_path, str(head)])
                        else:
                            writer.writerow([new_file_path, str(head) + '-' + str(last)])
                        head= int(stripped_frame)
                        curr=head
                        last="" 
                last = curr
                if head != "":
                    if head == last:
                        writer.writerow([new_file_path, str(head)])
                    else:
                        writer.writerow([new_file_path, str(head) + '-' + str(last)])
            print("Create baselight_xytech.csv successfully")
    except FileNotFoundError:
        print("Baselight_export.txt file not found.")
        return
    except PermissionError:
        print("Permission denied.")
        return

# convert frame to time code
def calculate_frame_to_timecode(frame, fps=24):
    hours = frame // (3600 * fps)
    frame %= 3600 * fps
    minutes = frame // (60 * fps)
    frame %= 60 * fps
    seconds = frame // fps
    frame %= fps
    return "{:02d}:{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds, frame)

def retrieve_frame_data():
    try:
        frame_data = []
        for x in final.find({}, {"Frames to fix": 1, "_id": 0}):  # Retrieve only 'frame' field, exclude '_id'
            frame_data.append(x["Frames to fix"])
        return frame_data
    except Exception as e:
        print("Error:", e)

def output_frame_to_timecode():
    frame_data = retrieve_frame_data()
    timecode_list = []
    for frame_range in frame_data:
        frames = str(frame_range).split('-')
        start_frame = int(frames[0])
        end_frame = int(frames[-1]) if len(frames) > 1 else start_frame
        start_timecode = calculate_frame_to_timecode(start_frame)
        end_timecode = calculate_frame_to_timecode(end_frame)
        if start_frame != end_frame:
            timecode_range = f"{start_timecode} - {end_timecode}"
        else:
            timecode_range = start_timecode
        timecode_list.append(timecode_range)
    
    # Read the existing CSV file
    df = pd.read_csv('baselight_xytech.csv')
    
    # Add the timecodes to the DataFrame
    df['Timecode'] = timecode_list
    
    # Write the updated DataFrame back to the CSV file
    df.to_csv('baselight_xytech.csv', index=False)
    
    print("Timecodes added to baselight_xytech.csv successfully!")

def extract_timecode(file_path):
    try:
        command = [
            'ffmpeg',
            '-i', file_path,
            '-vf', 'showinfo',
            '-f', 'null', 
            '-'
        ]

        result = subprocess.run(command, stderr=subprocess.PIPE, text=True, check=True)
        
        timecodes = []
        for line in result.stderr.split('\n'):
            if 'showinfo' in line and 'pts_time:' in line:
                parts = line.split('pts_time:')
                if len(parts) > 1:
                    timecode = float(parts[1].split(' ')[0])
                    timecodes.append(timecode)
        
        return timecodes

    except subprocess.CalledProcessError as e:
        print(f"ffmpeg command failed with error: {e.stderr}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def convert_seconds_to_timecode(seconds, fps=24):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    frames = int((seconds - int(seconds)) * fps)
    
    return "{:02d}:{:02d}:{:02d}:{:02d}".format(hours, minutes, secs, frames)

def timecode_to_seconds(timecode, fps=24):
    parts = timecode.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2])
    frames = int(parts[3])
    
    total_seconds = hours * 3600 + minutes * 60 + seconds + frames / fps
    return total_seconds

def output_final_file():

    # Example usage
    mp4_file_path = args.process
    timecodes = extract_timecode(mp4_file_path)

    # Convert timecodes to HH:MM:SS:FF format
    formatted_timecodes = [convert_seconds_to_timecode(tc) for tc in timecodes]

    # Read the CSV file
    csv_file_path = '/Users/amatamuadthong/Desktop/467_multi_media/Project/The-Crucible/baselight_xytech.csv'
    df = pd.read_csv(csv_file_path)

    # Filter rows where the Timecode column matches the extracted timecodes
    matching_rows = []
    for index, row in df.iterrows():
        timecode_range = row.iloc[2]
        if ' - ' in timecode_range:
            start_timecode, end_timecode = timecode_range.split(' - ')
            start_seconds = timecode_to_seconds(start_timecode)
            end_seconds = timecode_to_seconds(end_timecode)
        
            for tc in timecodes:
                if start_seconds <= tc <= end_seconds:
                    matching_rows.append(row)
                    break

    filtered_df = pd.DataFrame(matching_rows)

    # Get the current working directory
    current_directory = os.getcwd()

    # Construct the file path
    output_file_path = os.path.join(current_directory, 'Thumbnail.xlsx')
    filtered_df.to_excel(output_file_path, index=False, engine='openpyxl')

    print(f"Filtered data has been written to {output_file_path}")


if args.timecode:
    print(f"Frame {args.frame_timecode} is {calculate_frame_to_timecode(args.frame_timecode)} at 24 fps")
if args.bx:
    baselight_xytech_csv()
if args.frame_timecode:
    output_frame_to_timecode()
if args.process:
    output_final_file()
