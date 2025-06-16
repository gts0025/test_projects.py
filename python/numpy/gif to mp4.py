#gif to mp4
import moviepy as mp
gif_path = 'C:/Users/gts00/OneDrive/Área de Trabalho/data/python/improved_black_dodge.gif'
video_path = 'C:/Users/gts00/OneDrive/Área de Trabalho/data/python/improved_black_dodge.mp4'
clip = mp.VideoFileClip(gif_path)
clip.write_videofile(video_path)

