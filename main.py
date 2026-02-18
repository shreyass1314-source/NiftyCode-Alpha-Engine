from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
import shutil

# --- PROJECT MANAGER'S FIX: PATH DETECTION ---
# Automatically find where the server installed the video tools
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
magick_path = shutil.which("magick") or shutil.which("convert")
if magick_path:
    os.environ["IMAGEMAGICK_BINARY"] = magick_path

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

app = FastAPI()

@app.get("/")
def home():
    # Shows if the tool is detected correctly in the logs
    return {
        "status": "Alpha Engine Online", 
        "magick_found": os.environ.get("IMAGEMAGICK_BINARY", "Not Found")
    }

@app.get("/generate")
def create_video(nifty_support: str, trigger: str, target: str):
    try:
        # Determine the absolute path to the background video
        base_path = os.path.dirname(os.path.abspath(__file__))
        video_path = os.path.join(base_path, "nifty_bg.mp4")
        
        if not os.path.exists(video_path):
            return {"error": f"Video file not found. Ensure 'nifty_bg.mp4' is in your GitHub repo."}

        # Load background and clip to 10 seconds
        video = VideoFileClip(video_path).subclip(0, 10)
        
        # Text Generation with standard 'Arial' font for stability
        def make_txt(val, color, pos_y):
            return TextClip(val, fontsize=65, color=color, font='Arial-Bold').set_position(('center', pos_y)).set_duration(10)

        txt_s = make_txt(f"Support: {nifty_support}", "white", 400)
        txt_tr = make_txt(f"Trigger: {trigger}", "yellow", 550)
        txt_ta = make_txt(f"Target: {target}", "lightgreen", 700)
        
        # Combine layers
        final = CompositeVideoClip([video, txt_s, txt_tr, txt_ta])
        
        # Render the final file
        output_filename = "output.mp4"
        output_path = os.path.join(base_path, output_filename)
        final.write_videofile(output_path, fps=24, codec="libx264", audio=False)
        
        return {"message": "Success", "download_link": "/download"}
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/download")
def download():
    # Provides the file directly to your phone's browser
    base_path = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(base_path, "output.mp4")
    if os.path.exists(output_path):
        return FileResponse(output_path, media_type="video/mp4", filename="Nifty_Update.mp4")
    return {"error": "Video not generated yet. Run /generate first."}
