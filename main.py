from argparse import ArgumentParser

parser = ArgumentParser(description='It does frame IO... stuff..')

parser.add_argument("--baselight", help="Baselight stuff")
parser.add_argument("--xytech", help="Xytech stuff")
parser.add_argument("--process", help="Process stuff")
parser.add_argument("--output", help="Output stuff")
# debug, argparse
parser.add_argument("--frame-timecode", type=int, help="Frame to timecode")

args = parser.parse_args()

# convert frame to timestamp
def frame_to_timecode(frame, fps=24):
    hours = frame // (3600 * fps)
    frame %= 3600 * fps
    minutes = frame // (60 * fps)
    frame %= 60 * fps
    seconds = frame // fps
    frame %= fps
    return "{:02d}:{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds, frame)

if args.frame_timecode:
    # print(frame_to_timecode(args.frame_timecode))
    print(f"Frame {args.frame_timecode} is {frame_to_timecode(args.frame_timecode)} at 24 fps")