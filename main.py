from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
import shutil

# DYNAMIC PATH DETECTION
magick_path = shutil.which("magick") or shutil.which("convert")
if magick_path:
    os.environ["IMAGEMAGICK_BINARY"] = magick_path

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Engine Online", "magick": os.environ.get("IMAGEMAGICK_BINARY")}

@app.get("/generate")
def create_video(nifty_support: str, trigger: str, target: str):
    video = VideoFileClip("nifty_bg.mp4").subclip(0, 10)
    
    # Text overlays - Safe Zone Optimized
    def make_txt(val, color, pos_y):
        return TextClip(val, fontsize=60, color=color, font='Arial-Bold').set_position(('center', pos_y)).set_duration(10)

    txt_s = make_txt(f"Support: {nifty_support}", "white", 400)
    txt_tr = make_txt(f"Trigger: {trigger}", "yellow", 550)
    txt_ta = make_txt(f"Target: {target}", "lightgreen", 700)
    
    final = CompositeVideoClip([video, txt_s, txt_tr, txt_ta])
    final.write_videofile("output.mp4", fps=24, codec="libx264", audio=False)
    
    return {"message": "Success", "link": "/download"}

@app.get("/download")
def download():
    return FileResponse("output.mp4", media_type="video/mp4", filename="Nifty_Update.mp4")
