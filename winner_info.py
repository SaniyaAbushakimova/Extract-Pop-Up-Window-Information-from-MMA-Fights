import datetime

################ WINNER INFO FUNCTIONS ################

class WINNER_INFO:
  
  def __init__(self):
    self.video_time = None
    self.name = None
    self.round_num = None
    self.round_time = None

class WINNER_INFO_POPUPWINDOW:
  
  def __init__(self, my_json, winner_text, winner_info, boxer1_info, boxer2_info, 
              round1_video_info, round2_video_info, round3_video_info, video_time):
    self.my_json = my_json
    self.winner_text = winner_text
    self.winner_info = winner_info
    self.boxer1_info = boxer1_info
    self.boxer2_info = boxer2_info
    self.round1_video_info = round1_video_info
    self.round2_video_info = round2_video_info
    self.round3_video_info = round3_video_info
    self.video_time = video_time
  
  def gather_info(self):

    # updating information about rounds and their video time
    if ((self.round1_video_info.video_time_end == None) and 
      (self.my_json["time_info"][-1]["round_num"] == 1)):
      
      self.round1_video_info.video_time_end = self.my_json["time_info"][-1]["video_time"]
      
      r1_video_time_end = datetime.datetime.strptime(self.round1_video_info.video_time_end, '%H:%M:%S')
      r1_video_time_start = datetime.datetime.strptime(self.round1_video_info.video_time_start, '%H:%M:%S')
      self.round1_video_info.round_duration = str(r1_video_time_end - r1_video_time_start)
      
      self.my_json["rounds_info"].append(vars(self.round1_video_info))
      print("[INFO] ROUNDS INFORMATION:")
      print(vars(self.round1_video_info))
    
    elif ((self.round2_video_info.video_time_end == None) and 
      (self.my_json["time_info"][-1]["round_num"] == 2)):
      
      r1_video_time_end = datetime.datetime.strptime(self.round1_video_info.video_time_end, '%H:%M:%S')
      r1_video_time_start = datetime.datetime.strptime(self.round1_video_info.video_time_start, '%H:%M:%S')
      self.round1_video_info.round_duration = str(r1_video_time_end - r1_video_time_start)

      self.round2_video_info.video_time_end = self.my_json["time_info"][-1]["video_time"]
      r2_video_time_end = datetime.datetime.strptime(self.round2_video_info.video_time_end, '%H:%M:%S')
      r2_video_time_start = datetime.datetime.strptime(self.round2_video_info.video_time_start, '%H:%M:%S')
      self.round2_video_info.round_duration = str(r2_video_time_end - r2_video_time_start)
      
      self.my_json["rounds_info"].append(vars(self.round1_video_info))
      self.my_json["rounds_info"].append(vars(self.round2_video_info))
      print("[INFO] ROUNDS INFORMATION:")
      print(vars(self.round1_video_info))
      print(vars(self.round2_video_info))
    
    elif ((self.round3_video_info.video_time_end == None) and 
      (self.my_json["time_info"][-1]["round_num"] == 3)):

      r1_video_time_end = datetime.datetime.strptime(self.round1_video_info.video_time_end, '%H:%M:%S')
      r1_video_time_start = datetime.datetime.strptime(self.round1_video_info.video_time_start, '%H:%M:%S')
      self.round1_video_info.round_duration = str(r1_video_time_end - r1_video_time_start)

      r2_video_time_end = datetime.datetime.strptime(self.round2_video_info.video_time_end, '%H:%M:%S')
      r2_video_time_start = datetime.datetime.strptime(self.round2_video_info.video_time_start, '%H:%M:%S')
      self.round2_video_info.round_duration = str(r2_video_time_end - r2_video_time_start)

      self.round3_video_info.video_time_end = self.my_json["time_info"][-1]["video_time"]
      r3_video_time_end = datetime.datetime.strptime(self.round3_video_info.video_time_end, '%H:%M:%S')
      r3_video_time_start = datetime.datetime.strptime(self.round3_video_info.video_time_start, '%H:%M:%S')
      self.round3_video_info.round_duration = str(r3_video_time_end - r3_video_time_start)

      self.my_json["rounds_info"].append(vars(self.round1_video_info))
      self.my_json["rounds_info"].append(vars(self.round2_video_info))
      self.my_json["rounds_info"].append(vars(self.round3_video_info))

      print("[INFO] ROUNDS INFORMATION:")
      print(vars(self.round1_video_info))
      print(vars(self.round2_video_info))
      print(vars(self.round3_video_info))

    # updating information about winner
    if (self.winner_text == self.boxer1_info.name) and (self.winner_info.name == None):
      self.my_json["winner_info"] = []
      self.winner_info.name = self.boxer1_info.name
      self.winner_info.round_num = self.my_json["time_info"][-1]["round_num"]
      self.winner_info.round_time = self.my_json["time_info"][-1]["time"]
      self.winner_info.video_time = self.video_time
      
      print("[INFO] WINNER INFORMATION:")
      print((vars(self.winner_info)))
      
      self.my_json["winner_info"].append(vars(self.winner_info))
    
    elif (self.winner_text == self.boxer2_info.name) and (self.winner_info.name == None):
      self.my_json["winner_info"] = []
      self.winner_info.name = self.boxer2_info.name
      self.winner_info.round_num = self.my_json["time_info"][-1]["round_num"]
      self.winner_info.round_time = self.my_json["time_info"][-1]["time"]
      self.winner_info.video_time = self.video_time
      
      print("[INFO] WINNER INFORMATION:")
      print(vars(self.winner_info))
      
      self.my_json["winner_info"].append(vars(self.winner_info))
