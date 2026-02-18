from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
import os
import shutil

# DYNAMIC TOOL SEARCH
# This searches the server for 'magick' or 'convert' automatically
magick_path = shutil.which("magick") or shutil.which("convert")
if magick_path:
    os.environ["IMAGEMAGICK_BINARY"] = magick_path
else:
    # Backup common Linux paths
    for path in ["/usr/bin/convert", "/usr/local/bin/convert", "/usr/bin/magick"]:
        if os.path.exists(path):
            os.environ["IMAGEMAGICK_BINARY"] = path
            break

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

app = FastAPI()
engine_status = {"busy": False, "error": None}

def render_task(nifty_support, trigger, target):
    try:
        engine_status["busy"] = True
        video = VideoFileClip("nifty_bg.mp4").subclip(0, 10)
        
        # Using a very basic font to ensure it doesn't crash on font missing
        def make_txt(val, color, pos_y):
            return TextClip(val, fontsize=60, color=color, font='Arial').set_position(('center', pos_y)).set_duration(10)

        txt_s = make_txt(f"Support: {nifty_support}", "white", 400)
        txt_tr = make_txt(f"Trigger: {trigger}", "yellow", 550)
        txt_ta = make_txt(f"Target: {target}", "lightgreen", 700)
        
        final = CompositeVideoClip([video, txt_s, txt_tr, txt_ta])
        final.write_videofile("output.mp4", fps=24, codec="libx264", audio=False, logger=None, threads=4)
        engine_status["busy"] = False
    except Exception as e:
        engine_status["error"] = str(e)
        engine_status["busy"] = False

@app.get("/")
def home():
    return {
        "status": "Ready" if not engine_status["busy"] else "Rendering...",
        "magick_path": os.environ.get("IMAGEMAGICK_BINARY", "NOT FOUND"),
        "last_error": engine_status["error"]
    }

@app.get("/generate")
def start_render(nifty_support: str, trigger: str, target: str, background_tasks: BackgroundTasks):
    if engine_status["busy"]: return {"message": "Busy"}
    background_tasks.add_task(render_task, nifty_support, trigger, target)
    return {"message": "STARTED"}

@app.get("/download")
def download():
    if os.path.exists("output.mp4"):
        return FileResponse("output.mp4", media_type="video/mp4", filename="Nifty_Update.mp4")
    return {"error": "Not found"}
