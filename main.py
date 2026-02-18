from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
import os
import shutil

# Dynamic Tool Detection
os.environ["IMAGEIO_FFMPEG_EXE"] = shutil.which("ffmpeg") or "/usr/bin/ffmpeg"
os.environ["IMAGEMAGICK_BINARY"] = shutil.which("magick") or shutil.which("convert") or "/usr/bin/convert"

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

app = FastAPI()

# Track if the engine is busy
engine_status = {"busy": False, "error": None}

def render_task(nifty_support, trigger, target):
    try:
        engine_status["busy"] = True
        video = VideoFileClip("nifty_bg.mp4").subclip(0, 10)
        
        def make_txt(val, color, pos_y):
            return TextClip(val, fontsize=60, color=color, font='Arial').set_position(('center', pos_y)).set_duration(10)

        txt_s = make_txt(f"Support: {nifty_support}", "white", 400)
        txt_tr = make_txt(f"Trigger: {trigger}", "yellow", 550)
        txt_ta = make_txt(f"Target: {target}", "lightgreen", 700)
        
        final = CompositeVideoClip([video, txt_s, txt_tr, txt_ta])
        # Threads=4 speeds up the render significantly
        final.write_videofile("output.mp4", fps=24, codec="libx264", audio=False, logger=None, threads=4)
        engine_status["busy"] = False
    except Exception as e:
        engine_status["error"] = str(e)
        engine_status["busy"] = False

@app.get("/")
def home():
    status_msg = "Engine Ready" if not engine_status["busy"] else "Engine is currently rendering video..."
    return {"status": status_msg, "error": engine_status["error"]}

@app.get("/generate")
def start_render(nifty_support: str, trigger: str, target: str, background_tasks: BackgroundTasks):
    if engine_status["busy"]:
        return {"message": "Engine is currently busy. Please wait 1 minute."}
    
    # This starts the render in the background immediately
    background_tasks.add_task(render_task, nifty_support, trigger, target)
    return {"message": "Video generation STARTED. Refresh home page in 60 seconds to check status."}

@app.get("/download")
def download():
    if os.path.exists("output.mp4"):
        return FileResponse("output.mp4", media_type="video/mp4", filename="Nifty_Update.mp4")
    return {"error": "Video not found. Please run /generate first."}
