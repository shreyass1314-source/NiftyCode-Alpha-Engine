from fastapi import FastAPI
import os

# Tells Python exactly where to find the video software
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
os.environ["IMAGEMAGICK_BINARY"] = "/usr/bin/convert"

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

app = FastAPI()

@app.get("/")
def home():
    return {"status": "NiftyCode Engine Online"}

@app.get("/generate")
def create_video(nifty_support: str, trigger: str, target: str):
    # Load your background
    video = VideoFileClip("nifty_bg.mp4").subclip(0, 10)
    
    # Text overlays - Positioned for YouTube Shorts UI
    txt_s = TextClip(f"Support: {nifty_support}", fontsize=60, color='white', font='Arial-Bold').set_position(('center', 400)).set_duration(10)
    txt_tr = TextClip(f"Trigger: {trigger}", fontsize=60, color='yellow', font='Arial-Bold').set_position(('center', 550)).set_duration(10)
    txt_ta = TextClip(f"Target: {target}", fontsize=60, color='lightgreen', font='Arial-Bold').set_position(('center', 700)).set_duration(10)
    
    final = CompositeVideoClip([video, txt_s, txt_tr, txt_ta])
    
    # High-quality render for YouTube
    final.write_videofile("output.mp4", fps=24, codec="libx264", audio=False)
    
    return {"message": "Success", "download_link": "/download"}

@app.get("/download")
def download():
    from fastapi.responses import FileResponse
    return FileResponse("output.mp4", media_type="video/mp4", filename="NiftyCode_Update.mp4")
