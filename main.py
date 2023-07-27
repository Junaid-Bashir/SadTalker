import subprocess
from fastapi import FastAPI
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
app = FastAPI()

def run_inference(driven_audio_path, source_image_path, result_dir='./static'):
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

def save_uploaded_file(upload_file: UploadFile, save_path: str):
    with open(save_path, "wb") as f:
        f.write(upload_file.file.read())

@app.get("/run_inference/")
async def call_run_inference(driven_audio: UploadFile = File(...), source_image: UploadFile = File(...)):
    try:
        # Save the uploaded files to a temporary directory
        temp_dir = "temp_files"
        os.makedirs(temp_dir, exist_ok=True)
        driven_audio_path = os.path.join(temp_dir, driven_audio.filename)
        source_image_path = os.path.join(temp_dir, source_image.filename)
        
        save_uploaded_file(driven_audio, driven_audio_path)
        save_uploaded_file(source_image, source_image_path)

        response = run_inference(driven_audio_path, source_image_path, result_dir)

        if response is not None:
            return {"response": response.strip().split("\n")[-1].split(":")[-1]}
        else:
            return {"error": "An error occurred during inference or no non-empty lines in the response."}
    except Exception as e:
        return {"error": str(e)}