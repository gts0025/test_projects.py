import os 
os.chdir(os.path.dirname(os.path.abspath(__file__))) 

files = os.listdir() 
#gif to mp4
import moviepy as mp
for file in files: 
    if file.endswith(".gif"): 
        print(" flie " + file + "found")
        final = file.replace("gif","mp4") 
        
        clip = mp.VideoFileClip(file)
        clip.write_videofile(final)
        clip.close()
       
        os.remove(file)