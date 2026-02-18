from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
import shutil

# --- PROJECT MANAGER'S DYNAMIC DETECTION ---
# This finds the tools automatically regardless of the folder
os.environ["IMAGEIO_FFMPEG_EXE"] = shutil.which("ffmpeg") or "/usr/bin/ffmpeg"
os.environ["IMAGEMAGICK_BINARY"] = shutil.which("magick") or shutil.which("convert") or "/usr/bin/convert"

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

app = FastAPI()

@app.get("/")
def home():
    return {
        "status": "Alpha Engine Online", 
        "ffmpeg": os.environ.get("IMAGEIO_FFMPEG_EXE"),
        "magick": os.environ.get("IMAGEMAGICK_BINARY")
    }

@app.get("/generate")
def create_video(nifty_support: str, trigger: str, target: str):
    try:
        video = VideoFileClip("nifty_bg.mp4").subclip(0, 10)
        
        def make_txt(val, color, pos_y):
            # Using 'Arial' for maximum server compatibility
            return TextClip(val, fontsize=65, color=color, font='Arial').set_position(('center', pos_y)).set_duration(10)

        txt_s = make_txt(f"Support: {nifty_support}", "white", 400)
        txt_tr = make_txt(f"Trigger: {trigger}", "yellow", 550)
        txt_ta = make_txt(f"Target: {target}", "lightgreen", 700)
        
        final = CompositeVideoClip([video, txt_s, txt_tr, txt_ta])
        final.write_videofile("output.mp4", fps=24, codec="libx264", audio=False)
        
        return {"message": "Success", "link": "/download"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/download")
def download():
    if os.path.exists("output.mp4"):
        return FileResponse("output.mp4", media_type="video/mp4", filename="Nifty_Update.mp4")
    return {"error": "File not found. Generate it first."}
