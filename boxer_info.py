from matplotlib.backend_bases import NonGuiException

################ BOXER INFO FUNCTIONS ################

class BOXER_INFO:

  def __init__(self, color):
    self.video_time_state = 'No state info'
    self.video_time_info = 'None'
    self.color = color
    self.record = None
    self.age = None
    self.height = None
    self.weight = None
    self.name = None
    self.country = None

class BOXER_INFO_POPUPWINDOW:

  def __init__(self, my_json, ocr_text, boxer1_info, boxer2_info, 
               calc_bb_intersection, state_info, video_time):
    self.my_json = my_json
    self.text = ocr_text
    self.boxer1_info = boxer1_info
    self.boxer2_info = boxer2_info
    self.intersection = calc_bb_intersection
    self.state_info = state_info
    self.video_time = video_time

  def find_name_country(self, bb):
    bb_check = {'x1': bb[0][0], 'x2': bb[2][0],
                'y1': bb[0][1], 'y2': bb[2][1]}

    # bounding boxes where we usually see boxer1's and boxer2's name and country on video
    bb_name_fixed = [{'x1':250, 'x2':470,'y1':465, 'y2':590},
                     {'x1':811, 'x2':1060,'y1':457, 'y2':590}]
    
    bb_country_fixed = [{'x1':370, 'x2':460,'y1':590, 'y2':620},
                        {'x1':816, 'x2':904,'y1':592, 'y2':620}]

    for i in range(len(bb_name_fixed)):
      if self.intersection(bb_name_fixed[i], bb_check):
        return "boxer{}".format(i+1)
    
    for i in range(len(bb_country_fixed)):
      if self.intersection(bb_country_fixed[i], bb_check):
        return "boxer{}".format(i+1)

  def gather_info(self):

    boxer1_info_temp = []
    boxer2_info_temp = []
    active_idx = 1000

    for i in range(len(self.text)):
      if (self.text[i][1] == '') or (self.text[i][1] == ' '):
        continue

      elif (self.text[i][1] == 'RECORD') and (self.boxer1_info.record == None):
        self.boxer1_info.record = self.text[i-1][1]
        self.boxer2_info.record = self.text[i+1][1]

      elif (self.text[i][1] == 'AGE') and (self.boxer1_info.age == None):
        self.boxer1_info.age = self.text[i-1][1]
        self.boxer2_info.age = self.text[i+1][1]

      elif (self.text[i][1] == 'HEIGHT') and ((self.boxer1_info.height == None)):
        self.boxer1_info.height = self.text[i-1][1]
        self.boxer2_info.height = self.text[i+1][1]

      elif (self.text[i][1] == 'WEIGHT') and (self.boxer1_info.weight == None):
        self.boxer1_info.weight = self.text[i-1][1]
        self.boxer2_info.weight = self.text[i+1][1]

        # idx after which easyocr detects boxers' names and countries
        active_idx = i+1
      
      # finding boxers' names and countries
      elif ((i > active_idx) and ((self.boxer1_info.name == None) or 
        (self.boxer2_info.record == None))):

        if self.find_name_country(self.text[i][0]) == 'boxer1':
          boxer1_info_temp.append(self.text[i][1])
        elif self.find_name_country(self.text[i][0]) == 'boxer2':
          boxer2_info_temp.append(self.text[i][1])

    # adding information to boxer1_info and boxer2_info
    if ((len(boxer1_info_temp) != 0) and (len(boxer2_info_temp) != 0) and 
      ((self.boxer1_info.name == None) or (self.boxer2_info.record == None))):
      
      # add boxer's name
      self.boxer1_info.name = boxer1_info_temp[0] + ' ' + boxer1_info_temp[1]
      self.boxer1_info.country = boxer1_info_temp[2]

      self.boxer2_info.name = boxer2_info_temp[0] + ' ' + boxer2_info_temp[1]
      self.boxer2_info.country = boxer2_info_temp[2]

      # add boxer's state based on name
      if self.boxer1_info.name == self.state_info.boxer1_name:
        self.boxer1_info.state = self.state_info.boxer1_state
        self.boxer1_info.video_time_state = self.state_info.boxer1_video_time

      if self.boxer2_info.name == self.state_info.boxer2_name:
        self.boxer2_info.state = self.state_info.boxer2_state
        self.boxer2_info.video_time_state = self.state_info.boxer2_video_time

    if ((None not in list(vars(self.boxer1_info).values())) and 
      (len(self.my_json["boxer_info"]) == 0)):

      self.boxer1_info.video_time_info = self.video_time
      self.boxer2_info.video_time_info = self.video_time
      
      print("[INFO] BOXERS INFORMATION:")
      print(vars(self.boxer1_info))
      print(vars(self.boxer2_info))

      self.my_json["boxer_info"].append(vars(self.boxer1_info))
      self.my_json["boxer_info"].append(vars(self.boxer2_info))
