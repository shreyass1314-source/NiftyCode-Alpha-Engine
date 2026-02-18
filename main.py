from fastapi import FastAPI
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Alpha Engine Active"}

@app.post("/generate")
def create_video(nifty_support: str, trigger: str, target: str):
    # This script pulls the background and burns your text into the safe zone
    video = VideoFileClip("nifty_bg.mp4").subclip(0, 10)
    
    txt_support = TextClip(f"Support: {nifty_support}", fontsize=70, color='white', font='Arial-Bold').set_position(('center', 400)).set_duration(10)
    txt_trigger = TextClip(f"Trigger: {trigger}", fontsize=70, color='yellow', font='Arial-Bold').set_position(('center', 600)).set_duration(10)
    txt_target = TextClip(f"Target: {target}", fontsize=70, color='lightgreen', font='Arial-Bold').set_position(('center', 800)).set_duration(10)
    
    final = CompositeVideoClip([video, txt_support, txt_trigger, txt_target])
    final.write_videofile("output_short.mp4", fps=24)
    return {"message": "Video Generated Successfully"}
