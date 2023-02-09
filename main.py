from state_info import *
from boxer_info import *
from time_info import *
from winner_info import *

import easyocr
import cv2
import json
import argparse
import os

#######################################################

class GLOBAL_VARIABLES:

  def __init__(self):
    self.boxer_info_frame = 0
    self.state_info_b1_frame = 0
    self.state_info_b2_frame = 0
    self.round_num = 1
    self.round_updator = False
    self.printed = False

#######################################################

class DETECT_POPUPWINDOW:

  def __init__(self, my_json, global_variables, ocr_text, boxer1_info, boxer2_info, 
              winner_info, calc_bb_intersection, state_info, video_time, 
              round1_video_info, round2_video_info, round3_video_info):
    self.my_json = my_json
    self.global_variables = global_variables
    self.text = ocr_text
    self.boxer1_info = boxer1_info
    self.boxer2_info = boxer2_info
    self.winner_info = winner_info
    self.intersection = calc_bb_intersection
    self.state_info = state_info
    self.video_time = video_time
    self.round1_video_info = round1_video_info
    self.round2_video_info = round2_video_info
    self.round3_video_info = round3_video_info

  def check(self):

    # bounding box where we usually see winner's name on video
    bb_winner_fixed = {'x1':153, 'x2':425,'y1':610, 'y2':650}

    time_pattern = re.compile("\s*\d{1,2}[;:,. ]*\d{2}\s*")
    keywords = []

    # start scanning through all the detected text and get useful information
    for i in range(len(self.text)):

      bb_check = {'x1': self.text[i][0][0][0], 'x2': self.text[i][0][2][0],
                  'y1': self.text[i][0][0][1], 'y2': self.text[i][0][2][1]}

      ########### POP-UP WINDOW: TIME INFORMATION ###########
      
      if bool(time_pattern.match(self.text[i][1])):
        self.processor = TIME_INFO_POPUPWINDOW(self.my_json, self.intersection, self.global_variables, 
                                              self.text, self.boxer1_info, self.boxer2_info, self.video_time, 
                                              self.round1_video_info, self.round2_video_info, self.round3_video_info)
        self.processor.gather_info()

      ########### POP-UP WINDOW: WINNER INFORMATION ###########

      elif ((self.intersection(bb_winner_fixed, bb_check)) and 
        ((self.text[i][1] == self.boxer1_info.name) or 
        (self.text[i][1] == self.boxer2_info.name))):
        
        self.processor = WINNER_INFO_POPUPWINDOW(self.my_json, self.text[i][1], self.winner_info, self.boxer1_info, 
                                                self.boxer2_info, self.round1_video_info, self.round2_video_info, 
                                                self.round3_video_info, self.video_time)
        self.processor.gather_info()
      
      keywords.append(self.text[i][1])

    ########### POP-UP WINDOW: BOXERS INFORMATION ###########
    
    if ('AGE' in keywords) or ('HEIGHT' in keywords) or ('WEIGHT' in keywords):
      self.global_variables.boxer_info_frame += 1
      
      if self.global_variables.boxer_info_frame > 4:
        self.processor = BOXER_INFO_POPUPWINDOW(self.my_json, self.text, self.boxer1_info, self.boxer2_info, 
                                               self.intersection, self.state_info, self.video_time)
        self.processor.gather_info()
    
    ########### POP-UP WINDOW: BOXER'S STATE INFORMATION ###########

    for i in range(len(keywords)):
      if ((re.search(r'\bRECORD\b', self.text[i][1])) and (('AGE' not in keywords) 
        and ('HEIGHT' not in keywords) and ('WEIGHT' not in keywords))):
        
        self.processor = STATE_INFO_POPUPWINDOW(self.text, self.intersection, self.state_info, 
                                               self.global_variables, self.video_time)
        self.processor.gather_info()

#######################################################

class VIDEO_PROCESSOR:

  def __init__(self, video_path, file_path):
    self.video_path = video_path
    self.file_path = file_path
  
  def calc_bb_intersection(self, bb1, bb2):

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1['x1'], bb2['x1'])
    y_top = max(bb1['y1'], bb2['y1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_bottom = min(bb1['y2'], bb2['y2'])

    if x_right < x_left or y_bottom < y_top:
      return False

    intersection_area = (x_right - x_left) * (y_bottom - y_top)
    bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])
    
    if bb2_area == 0.0:
      return False
    else:
      intersection_ratio = intersection_area/float(bb2_area)
      return intersection_ratio > 0.35
  
  def process_frames(self):
    print("[INFO] Initializing easyocr reader...")
    reader = easyocr.Reader(['en'], gpu = True)
    
    print("\n[INFO] Extracting information...")
    cap = cv2.VideoCapture(self.video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_id = 0

    my_json = {"boxer_info": [],
                "time_info": [],
                "rounds_info": []}

    global_variables = GLOBAL_VARIABLES()
    state_info = STATE_INFO()
    boxer1_info = BOXER_INFO(color = 'red')
    boxer2_info = BOXER_INFO(color = 'blue')
    round1_video_info = ROUND_VIDEO_INFO(round_num = '1')
    round2_video_info = ROUND_VIDEO_INFO(round_num = '2')
    round3_video_info = ROUND_VIDEO_INFO(round_num = '3')
    winner_info = WINNER_INFO()
    
    while(cap.isOpened()):
      ret, frame = cap.read()
      
      if (ret != True):
          break
      
      if frame_id % (fps+1) == 0:
        # get current video time
        seconds = round(frame_id/fps)
        video_time = str(datetime.timedelta(seconds=seconds))

        # detect all text in a frame
        ocr_text = reader.readtext(frame)

        # extract useful information from the detected text
        popupwindow_detector = DETECT_POPUPWINDOW(my_json, global_variables, ocr_text, boxer1_info, boxer2_info, 
                                                  winner_info, self.calc_bb_intersection, state_info, video_time, 
                                                  round1_video_info, round2_video_info, round3_video_info)
        popupwindow_detector.check()
      
      frame_id += 1
    cap.release()
    
    with open(self.file_path, 'w') as fp:
      json.dump(my_json, fp, indent=4)


#################### START HERE #########################

parser = argparse.ArgumentParser()
parser.add_argument("--path_video", required=True, help="path to the video")
parser.add_argument("--path_result", required=True, help="path to csv/json file")

args = vars(parser.parse_args())
video_path = args["path_video"]
file_path = args["path_result"]

if os.path.isfile(video_path) and os.path.isfile(file_path):
    processor = VIDEO_PROCESSOR(video_path, file_path)
    processor.process_frames()
    print("[INFO] Information extraction is finished.")
    print("[INFO] Results saved to '{}'.".format(file_path))
else:
    print("[ERROR] Could not find files. Please specify file paths correctly.")

