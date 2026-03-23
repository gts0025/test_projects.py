#gif to mp4
import moviepy as mp
import os

os.chdir(os.path.dirname(os.path.abspath(__file__))) 

class Converter:
    def __init__(self,gif_path:str, video_path:str):
        """
        origin: file path for the gif file:
        destiny: file path for the mp4 file:
        
        """
        
        clip = mp.VideoFileClip(gif_path)
        clip.write_videofile(video_path)
        clip.close()
        os.remove(gif_path)

