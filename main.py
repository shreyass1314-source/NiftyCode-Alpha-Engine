from fastapi import FastAPI
import os

# FORCE PATHS FOR RAILWAY
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
os.environ["IMAGEMAGICK_BINARY"] = "/usr/bin/convert"

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Alpha Engine Active"}

@app.get("/generate")
def create_video(nifty_support: str, trigger: str, target: str):
    # Load background (must be 10 seconds or longer)
    video = VideoFileClip("nifty_bg.mp4").subclip(0, 10)
    
    # Text overlays - Safe Zone Optimized
    txt_support = TextClip(f"Support: {nifty_support}", fontsize=60, color='white', font='Arial-Bold').set_position(('center', 350)).set_duration(10)
    txt_trigger = TextClip(f"Trigger: {trigger}", fontsize=60, color='yellow', font='Arial-Bold').set_position(('center', 500)).set_duration(10)
    txt_target = TextClip(f"Target: {target}", fontsize=60, color='lightgreen', font='Arial-Bold').set_position(('center', 650)).set_duration(10)
    
    # Combine and save locally on the server
    final = CompositeVideoClip([video, txt_support, txt_trigger, txt_target])
    final.write_videofile("output_short.mp4", fps=24, codec="libx264", audio=False)
    
    return {"message": "Success", "link": "/output_short.mp4"}

@app.get("/output_short.mp4")
def download_video():
    from fastapi.responses import FileResponse
    return FileResponse("output_short.mp4", media_type="video/mp4")
