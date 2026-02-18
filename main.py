from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
import os
import shutil

# Tool Detection
os.environ["IMAGEIO_FFMPEG_EXE"] = shutil.which("ffmpeg") or "/usr/bin/ffmpeg"
os.environ["IMAGEMAGICK_BINARY"] = shutil.which("magick") or shutil.which("convert") or "/usr/bin/convert"

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

app = FastAPI()

# Global status to track if the engine is busy
status = {"generating": False, "last_error": None}

def process_video(nifty_support, trigger, target):
    try:
        status["generating"] = True
        video = VideoFileClip("nifty_bg.mp4").subclip(0, 10)
        
        def make_txt(val, color, pos_y):
            return TextClip(val, fontsize=60, color=color, font='Arial').set_position(('center', pos_y)).set_duration(10)

        txt_s = make_txt(f"Support: {nifty_support}", "white", 400)
        txt_tr = make_txt(f"Trigger: {trigger}", "yellow", 550)
        txt_ta = make_txt(f"Target: {target}", "lightgreen", 700)
        
        final = CompositeVideoClip([video, txt_s, txt_tr, txt_ta])
        # Force high speed rendering
        final.write_videofile("output.mp4", fps=24, codec="libx264", audio=False, logger=None, threads=4)
        status["generating"] = False
    except Exception as e:
        status["last_error"] = str(e)
        status["generating"] = False

@app.get("/")
def home():
    msg = "Ready" if not status["generating"] else "Processing Video..."
    return {"status": msg, "error": status["last_error"]}

@app.get("/generate")
def start_generation(nifty_support: str, trigger: str, target: str, background_tasks: BackgroundTasks):
    if status["generating"]:
        return {"message": "Engine is already busy. Wait 1 minute."}
    
    # This starts the render WITHOUT making the browser wait
    background_tasks.add_task(process_video, nifty_support, trigger, target)
    return {"message": "Generation started. Refresh the home page in 60 seconds."}

@app.get("/download")
def download():
    if os.path.exists("output.mp4"):
        return FileResponse("output.mp4", media_type="video/mp4", filename="Nifty_Update.mp4")
    return {"error": "File not found. Generate first."}
