import matplotlib.pyplot as plt
import shutil
from PIL import Image 
import os 
os.chdir(os.path.dirname(os.path.abspath(__file__))) 

path = os.path.abspath(__file__)
class Selector():
    def __init__(self):
        self.origin = "origin"

    def run(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__))) 

        files = os.listdir() 
        print(files)
        #gif to mp4
        import moviepy as mp
        for file in files: 
            if file.endswith(("png","gif")):
                data = Image.open(file)
                plt.imshow(data)
                plt.show(block = False)
                print("image found, accept image?")
                print("yes: 1, no: 0")
                plt.pause(0.1)
                choice = int(input())
                plt.close()
                
                
                
                if choice == 1:
                    shutil.move(file,"accepted")
                else:
                    shutil.move(file,"declined")

selector = Selector()
selector.run()

               
