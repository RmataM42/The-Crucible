from argparse import ArgumentParser
from pymongo import MongoClient
import os
import csv
import subprocess

# Argparse setup
parser = ArgumentParser(description='It does frame IO... stuff..')

parser.add_argument("--baselight", metavar='', help="Baselight stuff")
parser.add_argument("--xytech", metavar='', help="Xytech stuff")
parser.add_argument("--process", metavar='', help="Process stuff")
parser.add_argument("--output", metavar='', help="Output stuff")
# debug: argparse
parser.add_argument("--frame-timecode", metavar='', type=int, help="Frame to timecode; must follow by an integer to calcualte")
# debug baselight xytech from project 1
parser.add_argument("-bx", action='store_true', help="Project 1: output baselight+xytech w/ frame range")
args = parser.parse_args()

# File path
Xytech_file_path = "baselight_xytech/Sample_Xytech.txt"
Baselight_file_path = "baselight_xytech/Sample_Baselight_export.txt"

# DB setup
# Connect to MongoDB locally
client = MongoClient("mongodb://localhost:27017/")
# Get the reckoning database
db = client["crucicle"]
baselight = db["Baselight"]
xytech = db["Xytech"]

# convert frame to time code
def frame_to_timecode(frame, fps=24):
    hours = frame // (3600 * fps)
    frame %= 3600 * fps
    minutes = frame // (60 * fps)
    frame %= 60 * fps
    seconds = frame // fps
    frame %= fps
    return "{:02d}:{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds, frame)

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
            writer = csv.writer(csvfile, delimiter=' ')
            writer.writerow(['location', 'Frames to fix', 'Timecode', 'Thumbnail'])

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
    except FileNotFoundError:
        print("Baselight_export.txt file not found.")
        return
    except PermissionError:
        print("Permission denied.")
        return

if args.frame_timecode:
    print(f"Frame {args.frame_timecode} is {frame_to_timecode(args.frame_timecode)} at 24 fps")
if args.bx:
    baselight_xytech_csv()