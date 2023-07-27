import subprocess
from fastapi import FastAPI
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from gtts import gTTS
from io import BytesIO
app = FastAPI()

async def run_inference(driven_audio_path, source_image_path, result_dir='static'):
    try:
        command = f"python inference.py --driven_audio {driven_audio_path} \
                   --source_image {source_image_path} \
                   --result_dir {result_dir} --still --preprocess full --enhancer gfpgan"

        # Run the command and capture the response
        response = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

        # Decode the response bytes to a string
        response_str = response.decode('utf-8')

        return response_str
    except subprocess.CalledProcessError as e:
        # If there is an error, you can handle it here
        print("Error occurred:", e)
        return None
app.mount("/static", StaticFiles(directory="static"), name="static")

def text_to_audio(text, audio_path):
    tts = gTTS(text=text, lang="en")
    tts.save(audio_path)

@app.get("/run_inference/")
async def call_run_inference(text:str, image: UploadFile = File(...)):
    
    # # Save the uploaded files to a temporary directory
    # name = image.filename
    # contents = image.file.read()
    # with open("static/"+name,'wb') as data:
    #     data.write(contents)
    #     data.close()
    # text_to_audio(text, "static/test.mp3")

    response = await run_inference("static/test.mp3", "static/"+name, result_dir='static')

    if response is not None:
        return {"response": response.strip().split("\n")[-1].split(":")[-1]}
    else:
        return {"error": "An error occurred during inference or no non-empty lines in the response."}
