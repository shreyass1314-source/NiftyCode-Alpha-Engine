from fastapi import FastAPI
import os

# DO NOT REMOVE: Force-linking the video tools for Railway/Linux
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
os.environ["IMAGEMAGICK_BINARY"] = "/usr/bin/convert"

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

app = FastAPI()

@app.get("/")
def home():
    return {"status": "NiftyCode Engine Active"}

@app.get("/generate")
def create_video(nifty_support: str, trigger: str, target: str):
    # Load the background video
    video = VideoFileClip("nifty_bg.mp4").subclip(0, 10)
    
    # Text overlays - Safe Zone Optimized
    txt_s = TextClip(f"Support: {nifty_support}", fontsize=60, color='white', font='Arial-Bold').set_position(('center', 350)).set_duration(10)
    txt_tr = TextClip(f"Trigger: {trigger}", fontsize=60, color='yellow', font='Arial-Bold').set_position(('center', 500)).set_duration(10)
    txt_ta = TextClip(f"Target: {target}", fontsize=60, color='lightgreen', font='Arial-Bold').set_position(('center', 650)).set_duration(10)
    
    # Combine and save locally on the server
    final = CompositeVideoClip([video, txt_s, txt_tr, txt_ta])
    final.write_videofile("output.mp4", fps=24, codec="libx264", audio=False)
    
    return {"message": "Success", "download_link": "/download"}

@app.get("/download")
def download():
    from fastapi.responses import FileResponse
    return FileResponse("output.mp4", media_type="video/mp4", filename="NiftyCode_Update.mp4")
