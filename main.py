from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

# Set paths for Railway environment
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
os.environ["IMAGEMAGICK_BINARY"] = "/usr/bin/convert"

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Alpha Engine Online"}

@app.get("/generate")
def create_video(nifty_support: str, trigger: str, target: str):
    # Load background
    video = VideoFileClip("nifty_bg.mp4").subclip(0, 10)
    
    # Using 'Courier' font as it is a default system font on Linux
    def make_txt(val, color, pos_y):
        return TextClip(val, fontsize=70, color=color, font='Courier').set_position(('center', pos_y)).set_duration(10)

    txt_s = make_txt(f"Support: {nifty_support}", "white", 400)
    txt_tr = make_txt(f"Trigger: {trigger}", "yellow", 550)
    txt_ta = make_txt(f"Target: {target}", "lightgreen", 700)
    
    final = CompositeVideoClip([video, txt_s, txt_tr, txt_ta])
    final.write_videofile("output.mp4", fps=24, codec="libx264", audio=False)
    
    return {"message": "Success", "link": "/download"}

@app.get("/download")
def download():
    return FileResponse("output.mp4", media_type="video/mp4", filename="Nifty_Update.mp4")
