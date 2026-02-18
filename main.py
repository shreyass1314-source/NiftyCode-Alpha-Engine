from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
import shutil

# DYNAMIC TOOL DETECTION
os.environ["IMAGEIO_FFMPEG_EXE"] = shutil.which("ffmpeg") or "/usr/bin/ffmpeg"
os.environ["IMAGEMAGICK_BINARY"] = shutil.which("magick") or shutil.which("convert") or "/usr/bin/convert"

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Alpha Engine Online", "magick": os.environ.get("IMAGEMAGICK_BINARY")}

@app.get("/generate")
def create_video(nifty_support: str, trigger: str, target: str):
    try:
        # Load and subclip
        video = VideoFileClip("nifty_bg.mp4").subclip(0, 10)
        
        # Optimized Text Generation
        def make_txt(val, color, pos_y):
            return TextClip(val, fontsize=60, color=color, font='Arial').set_position(('center', pos_y)).set_duration(10)

        txt_s = make_txt(f"Support: {nifty_support}", "white", 400)
        txt_tr = make_txt(f"Trigger: {trigger}", "yellow", 550)
        txt_ta = make_txt(f"Target: {target}", "lightgreen", 700)
        
        final = CompositeVideoClip([video, txt_s, txt_tr, txt_ta])
        
        # SPEED OPTIMIZATION: threads=4 and no progress bar logging
        final.write_videofile("output.mp4", fps=24, codec="libx264", audio=False, logger=None, threads=4)
        
        return {"message": "Success", "link": "/download"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/download")
def download():
    return FileResponse("output.mp4", media_type="video/mp4", filename="Nifty_Update.mp4")
