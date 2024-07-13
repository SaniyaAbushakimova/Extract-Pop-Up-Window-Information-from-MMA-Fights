Project completed on January 29, 2023.
 
## Project description
- Given a video of an MMA fight, extract information from all pop-up windows that appear anywhere in the video. Save result to `file_res.json` file;
- Image to text recognition was done with [easyocr](https://github.com/JaidedAI/EasyOCR);
- Videos were processed one frame per second (usually fps = 25).

## Video materials
• [Playlist 1](https://youtube.com/playlist?list=PLukHrO2gJzOoWizPv3Rx5lk46ehXjPZUk) • [Playlist 2](https://youtube.com/playlist?list=PLukHrO2gJzOqzGP6qQd6ziqZTazm078IK) • [Playlist 3](https://youtube.com/playlist?list=PLukHrO2gJzOq5X1iaK3scyRhWlOnylu6d) • [Playlist 4](https://youtube.com/playlist?list=PLukHrO2gJzOrSRlPjeq_KX06kLUe-S-gD) • [Playlist 5](https://youtube.com/playlist?list=PLukHrO2gJzOrhaUcULTA2JpQVuHRCxzUx) • [Playlist 6](https://youtube.com/playlist?list=PLukHrO2gJzOrGCOruMsry6APdOMMbtz16) 

## Pop-up window types
The above-mentioned videos contain the following types of pop-up windows:
### 1. `state_info`:
- At the beginning of the video, a pop-up window with a brief information about each fighter appears. 
- The window contains *full name*, *record* (highlighted in red) and *country*. 

![state_info](https://user-images.githubusercontent.com/81459892/217808050-465f012a-ac0c-47a7-8297-6ebd21ef0c63.png)

### 2. `boxer_info`:
- Next in the video, we see a pop-up window with information about each of the fighters. 
- The window contains *color*, *full name*, *country*, *record*, *age*, *height* and *weight*.

![boxer_info](https://user-images.githubusercontent.com/81459892/217809363-194084b7-eda6-4b8a-b9d5-44c22a9cea2b.png)

### 3. `time_info`:
- When the figth starts, a pop-up window with the *current round time* and *round number* appear. The number of white circles above time indicate current round number. In MMA each round lasts for 5 minutes at most. There are two types of such pop-up windows:
  - **Time only** - information about the *current round time* and *round number* (appears at the beginning and towards the end of the battle).

  ![time_only_info](https://user-images.githubusercontent.com/81459892/217810290-efca14bb-47a9-4d5c-962d-5ce0bf493271.png)
  
  - **Time and Boxers-info** -  information about the *current round time*, *round number*, *fighters' full names* and their respective *colors* (appears the rest of the time).

  ![time_boxers_info](https://user-images.githubusercontent.com/81459892/217810669-a772e1df-404c-4974-b64a-91fedcda44e8.png)

### 4. `winner_info`:
- At the end of the video, a pop-up window with the full name of the winner appears.

![winner_info](https://user-images.githubusercontent.com/81459892/217811748-3f218a17-edb4-4cad-8f2b-d3aaf6c488d1.png)

### Note
There are videos in which some of the above types of pop-up windows are missing. For example:

- [Playlist 1](https://youtube.com/playlist?list=PLukHrO2gJzOoWizPv3Rx5lk46ehXjPZUk) - no `state_info`
- [Playlist 1: video 6](https://colab.research.google.com/drive/1UXZP_SAvMIiKXdHSvvdEow3qEAm6VjaZ?authuser=1#scrollTo=iz4WepcC4ZX0:~:text=%2D%20%D0%BD%D0%B5%D1%82%20state_info-,Playlist%201%3A%20video%206,-%2D%20%D0%BD%D0%B5%D1%82%20winner_info) - no `winner_info`
- [Playlist 2: video 1](https://colab.research.google.com/drive/1UXZP_SAvMIiKXdHSvvdEow3qEAm6VjaZ?authuser=1#scrollTo=iz4WepcC4ZX0:~:text=%2D%20%D0%BD%D0%B5%D1%82%20winner_info-,Playlist%202%3A%20video%201,-%2D%20%D0%BD%D0%B5%D1%82%20state_info%20%D0%B8) - no `state_info` and `boxer_info`
- [Playlist 2: video 2](https://colab.research.google.com/drive/1UXZP_SAvMIiKXdHSvvdEow3qEAm6VjaZ?authuser=1#scrollTo=iz4WepcC4ZX0:~:text=state_info%20%D0%B8%20boxer_info-,Playlist%202%3A%20video%202,-%2D%20%D0%BD%D0%B5%D1%82%20state_info) - no `state_info`
- [Playlist 6: video 2](https://www.youtube.com/watch?v=Bf-BlSKDeuc&list=PLukHrO2gJzOrGCOruMsry6APdOMMbtz16&index=2) - no `winner_info`

## The structure of file_res.json
- `boxer_info` (if present) : \
    &emsp;`video_time_state` ---  `state_info` pop-up window timecode (if present) \
    &emsp;`video_time_info` ---  `boxer_info` pop-up window timecode  \
    &emsp;`color` ---  fighter's color \
    &emsp;`record` ---  fighter's record \
    &emsp;`age` ---  fighter's age \
    &emsp;`height` ---  fighter's height \
    &emsp;`weight` ---  fighter's weight \
    &emsp;`name` ---  fighter's full name \
    &emsp;`country` ---  fighter's country \
    &emsp;`state` ---  fighter's state (if present)

- `time_info` : \
  &emsp;`video_time_state` ---  `time_info` pop-up window timecode \
  &emsp;`boxer1` ---   **the first fighter's** full name (if present) \
  &emsp;`color1` ---  **the first fighter's** color (if present) \
  &emsp;`round_num` ---  round number \
  &emsp;`time` ---  round current time \
  &emsp;`color2` ---  **the second fighter's** color (if present)  \
  &emsp;`boxer2` ---  **the second fighter's** full name (if present) 

- `rounds_info` : \
  &emsp;`round_num` --- round number \
  &emsp;`video_time_start` --- round beginning timecode \
  &emsp;`video_time_end` --- round ending timecode \
  &emsp;`round_duration` --- round duration 

- `winner_info` (if present) : \
  &emsp;`video_time` --- `winner_info` pop-up window timecode \
  &emsp;`name` --- winner's full name \
  &emsp;`round_num` --- winning round number \
  &emsp;`round_num` --- winning round time 
 
## Launch the script
````
1. pip install -r requirements.txt
````
````
2. python main.py --path_video ./test.mp4 –path_result file_res.json
````
