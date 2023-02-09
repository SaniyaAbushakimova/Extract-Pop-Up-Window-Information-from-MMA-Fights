
################ STATE INFO FUNCTIONS ################

class STATE_INFO:

  def __init__(self):
    self.boxer1_name = None
    self.boxer1_state = None
    self.boxer1_video_time = None
    self.boxer2_name = None
    self.boxer2_state = None
    self.boxer2_video_time = None

class STATE_INFO_POPUPWINDOW:

  def __init__(self, ocr_text, calc_bb_intersection, state_info, 
              global_variables, video_time):
    self.text = ocr_text
    self.intersection = calc_bb_intersection
    self.state_info = state_info
    self.global_variables = global_variables
    self.video_time = video_time

  def gather_info(self):
    # bounding boxes where we usually see state and boxers' names on video
    bb_state_fixed = {'x1':390, 'x2':513,'y1':645, 'y2':677}
    bb_name_fixed = {'x1':178, 'x2':374,'y1':612, 'y2':680}

    boxer_state_info_temp = []

    # determine to which boxer state belongs
    name = ''
    for i in range(len(self.text)):
      bb_check = {'x1': self.text[i][0][0][0], 'x2': self.text[i][0][2][0],
                  'y1': self.text[i][0][0][1], 'y2': self.text[i][0][2][1]}
      
      if self.intersection(bb_name_fixed, bb_check):
        if name != '':
          name += ' '
        name += self.text[i][1]
      
      elif self.intersection(bb_state_fixed, bb_check):
        state = self.text[i][1]
    
    if self.state_info.boxer2_name == None:
      self.state_info.boxer2_name = name
    else:
      self.global_variables.state_info_b2_frame += 1
    
    # take state from 4th frame of boxer2
    if self.global_variables.state_info_b2_frame == 4:
      self.state_info.boxer2_video_time = self.video_time
      self.state_info.boxer2_state = state
    
    if (self.state_info.boxer1_name == None) and (name != self.state_info.boxer2_name):
      self.state_info.boxer1_name = name
    elif (self.state_info.boxer1_name != None) and (name != self.state_info.boxer2_name):
      self.global_variables.state_info_b1_frame += 1
    
    # take state from 4th frame of boxer1
    if self.global_variables.state_info_b1_frame == 4:
      self.state_info.boxer1_video_time = self.video_time
      self.state_info.boxer1_state = state
      