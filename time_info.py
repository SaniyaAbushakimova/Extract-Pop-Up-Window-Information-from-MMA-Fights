import re

################ TIME INFO FUNCTIONS ################

class TIME_ONLY_INFO:

  def __init__(self):
    self.video_time = None
    self.round_num = None
    self.time = None

class TIME_BOXERS_INFO:

  def __init__(self):
    self.video_time = None
    self.boxer1 = None
    self.color1 = None
    self.round_num = None
    self.time = None
    self.color2 = None
    self.boxer2 = None

class ROUND_VIDEO_INFO:

  def __init__(self, round_num):
    self.round_num = round_num
    self.video_time_start = None
    self.video_time_end = None
    self.round_duration = None

class TIME_INFO_POPUPWINDOW:

  def __init__(self, my_json, calc_bb_intersection, global_variables, 
              ocr_text, boxer1_info, boxer2_info, video_time, 
              round1_video_info, round2_video_info, round3_video_info):
    self.my_json = my_json
    self.intersection = calc_bb_intersection
    self.global_variables = global_variables
    self.text = ocr_text
    self.boxer1_info = boxer1_info
    self.boxer2_info = boxer2_info
    self.video_time = video_time
    self.round1_video_info = round1_video_info
    self.round2_video_info = round2_video_info
    self.round3_video_info = round3_video_info
  
  def find_boxers_names(self, bb):
    bb_check = {'x1': bb[0][0], 'x2': bb[2][0],
                'y1': bb[0][1], 'y2': bb[2][1]}

    # bounding boxes where we usually see boxer1 and boxer2 names 
    bb_names_fixed = [{'x1':290, 'x2':520,'y1':650, 'y2':674},
                      {'x1':750, 'x2':970,'y1':650, 'y2':674}]
    
    for i in range(len(bb_names_fixed)):
      if self.intersection(bb_names_fixed[i], bb_check):
        return "boxer{}".format(i+1)
      
  def gather_info(self):

    keywords = []
    boxer1_name = []
    boxer2_name = []
    time_instance = ''
    time_pattern = re.compile("\s*\d{1,2}[;:,. ]*\d{2}\s*")

    # bounding box where we usually see time on video
    bb_time_fixed = {'x1':570, 'x2':700,'y1':638, 'y2':681}
  
    for i in range(len(self.text)):
      bb_check = {'x1': self.text[i][0][0][0], 'x2': self.text[i][0][2][0],
                  'y1': self.text[i][0][0][1], 'y2': self.text[i][0][2][1]}
      
      # if pop-up window with boxers information doesn't exist
      if (self.boxer1_info.name == None) or (self.boxer2_info.record == None):
        
        if self.find_boxers_names(self.text[i][0]) == 'boxer1':
          boxer1_name.append(self.text[i][1])
        elif self.find_boxers_names(self.text[i][0]) == 'boxer2':
          boxer2_name.append(self.text[i][1])

      if (((len(boxer1_name) == 1) and (len(boxer2_name) == 1)) and 
        ((self.boxer1_info.name == None) or (self.boxer2_info.record == None))):
        
        self.boxer1_info.name = boxer1_name[0]
        self.boxer2_info.name = boxer2_name[0]
      
      elif (((len(boxer1_name) > 1) and (len(boxer2_name) > 1)) and 
        ((self.boxer1_info.name == None) or (self.boxer2_info.record == None))):
        
        self.boxer1_info.name = boxer1_name[0] + ' ' + boxer1_name[1]
        self.boxer2_info.name = boxer2_name[0] + ' ' + boxer2_name[1]

      if bool(time_pattern.match(self.text[i][1])) and self.intersection(bb_time_fixed, bb_check):
        
        if self.global_variables.printed == False:
          self.global_variables.printed = True
          self.round1_video_info.video_time_start = self.video_time
          
          print("[INFO] TIME INFORMATION (ROUND {}):".format(self.global_variables.round_num))

        # extracting time instances
        for d in range(len(self.text[i][1])):
          if self.text[i][1][d].isdigit():
            time_instance += self.text[i][1][d]
        
        if len(time_instance) == 4:
          time_instance = '{}:{}'.format(time_instance[:2], time_instance[-2:])
        else:
          time_instance = '{}:{}'.format(time_instance[0], time_instance[-2:])

        # updating rounds
        round_updators_list = ['5:00','05:00','4:59','04:59','4:58','04:58']
        update_turnons = ['4:39','04:39', '4:38', '04:38', '04:37', '4:37']
        
        if ((time_instance in update_turnons) and (self.global_variables.round_num == 1 or 
          self.global_variables.round_num == 2) and (self.global_variables.round_updator == False)):
          
          self.global_variables.round_updator = True

        elif ((time_instance in round_updators_list) and (self.global_variables.round_num == 1) 
          and (self.global_variables.round_updator == True)):
          
          self.global_variables.round_num = 2
          self.global_variables.round_updator = False
          self.round2_video_info.video_time_start = self.video_time
          self.round1_video_info.video_time_end = self.my_json["time_info"][-1]["video_time"]
          
          print("[INFO] TIME INFORMATION (ROUND {}):".format(self.global_variables.round_num))
        
        elif ((time_instance in round_updators_list) and (self.global_variables.round_num == 2) 
          and (self.global_variables.round_updator == True)):
          
          self.global_variables.round_num = 3
          self.round3_video_info.video_time_start = self.video_time
          self.round2_video_info.video_time_end = self.my_json["time_info"][-1]["video_time"]
          
          print("[INFO] TIME INFORMATION (ROUND {}):".format(self.global_variables.round_num))

      keywords.append(self.text[i][1])
      
    if bool(time_pattern.match(time_instance)):

      # pop-up window with time and boxers information
      if (self.boxer1_info.name != None) and (self.boxer2_info.name != None):
        boxer1_surname = self.boxer1_info.name.split(' ')[1]
        boxer2_surname = self.boxer2_info.name.split(' ')[1]
        
        if ((self.boxer1_info.name in keywords or self.boxer2_info.name in keywords) or 
          (boxer1_surname in keywords) or (boxer2_surname in keywords)):
          
          self.time_info = TIME_BOXERS_INFO()

          self.time_info.boxer1 = self.boxer1_info.name
          self.time_info.color1 = self.boxer1_info.color
          self.time_info.round_num = self.global_variables.round_num
          self.time_info.time = time_instance
          self.time_info.color2 = self.boxer2_info.color
          self.time_info.boxer2 = self.boxer2_info.name
          self.time_info.video_time = self.video_time
        
        else:
          self.time_info = TIME_ONLY_INFO()

          self.time_info.round_num = self.global_variables.round_num
          self.time_info.time = time_instance
          self.time_info.video_time = self.video_time  

      # pop-up window with time only
      else:
        self.time_info = TIME_ONLY_INFO()

        self.time_info.round_num = self.global_variables.round_num
        self.time_info.time = time_instance
        self.time_info.video_time = self.video_time        

      print(vars(self.time_info))
      self.my_json["time_info"].append(vars(self.time_info))
