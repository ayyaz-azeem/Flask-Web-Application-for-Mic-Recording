from flask import Flask, render_template, request
import os
from display_colors import *
import requests
import pyaudio
import wave
from werkzeug.utils import secure_filename

import subprocess

app = Flask(__name__)
app.debug = True

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
app.config['SECRET_KEY'] = '33a91b0baa57048c9e7b45f282d8a4c8'

UPLOAD_FOLDER_PATH = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_PATH

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'wav'}

def wav_file_content(filepath):
    """
    Reads content of wav file.

    Parameters:
    - filepath (.wav file): The path to the wav file.

    Returns:
    - str: The text content of the wav file.
    """
    print()
    print(f'{Cyan}point 901: in utils.py > wav_file_content(filepath) function START{Color_Off}')
    print(f'{Cyan}point 905: filepath: {filepath}{Color_Off}')
    api_url = 'http://192.168.2.202:1111/predict'
    # file_name = 'voice1.wav'
    files = {'file': ('temp.wav', open(filepath, 'rb'), 'audio/x-wav')}

    headers = {'accept': 'application/json'}

    response = requests.post(api_url, files = files, headers = headers)

    print(f'{Cyan}point 902: response status_code: {response.status_code}{Color_Off}' )
    result = str(response.text).replace('"',"")
    print(f'{Cyan}point 903: result: {result}{Color_Off}')
    print(f'{Cyan}point 904: in utils.py > wav_file_content(filepath) function END{Color_Off}')
    return result

def allowed_file(filename):
    print(f'{Orange}point 800: in allowed_file{Color_Off}')
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def homepage():
	return render_template('index.html')


# @app.route('/upload_audio', methods=['POST'])
# def upload_audio():
#     print('in upload_audio function start')

#     if 'audioFile' not in request.files:
#         print('in first if')
#         return {'message': 'No file part'}, 400

#     file = request.files['audioFile']

#     if file.filename == '':
#         print('in 2nd if')
#         return {'message': 'No selected file'}, 400

#     if file:
#         print('in 3rd if')
#         created_filename = 'recording.wav'
#         print(f'point 2k2A: created_filename: {created_filename}')
#         print(f'point 2k2B: created_filename: {secure_filename(created_filename)}')
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(created_filename))
#         file.save(file_path)

#         text1 = ''
#         text2 = ''

#         the_downloaded_file_directory = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],)
#         print(f'{On_IBlue}{BYellow}point 110: {the_downloaded_file_directory}{Color_Off}')

#         the_downloaded_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'], secure_filename(created_filename))
#         print(f'{On_IBlue}{BYellow}point 111: {the_downloaded_file_path}{Color_Off}')

#         if created_filename.endswith('.wav'):
#             print(f'{On_IBlue}{BYellow}point 2k2C: in .wav if loop {Color_Off}')
#             # text1 = wav_file_content(created_filename)
#             # print('2k2F')
#             text1 = wav_file_content(the_downloaded_file_directory+f"/{secure_filename(created_filename)}")
#             text2 = wav_file_content(the_downloaded_file_path)
#             print('2k2G')
        
#         print(f'2k2D: text: {text1}')
#         print(f'2k2E: text2: {text2}')

#         return {'message': 'File successfully uploaded'}, 200

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    print('in upload_audio function start')

    if 'audioFile' not in request.files:
        print('in first if')
        return {'message': 'No file part'}, 400

    file = request.files['audioFile']

    if file.filename == '':
        print('in 2nd if')
        return {'message': 'No selected file'}, 400

    if file  and allowed_file(file.filename):
        print('in 3rd if')
        created_filename = 'recording.wav'
        print(f'point 2k2A: created_filename: {created_filename}')
        print(f'point 2k2B: created_filename: {secure_filename(created_filename)}')
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(created_filename))

        input_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_recording.webm')
        output_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'recording.wav')
        file.save(input_filename)

        # Using FFmpeg to convert the audio
        command = [
            'ffmpeg',
            '-i', input_filename,
            '-acodec', 'pcm_s16le',  # PCM 16 bits, little-endian
            '-ac', '1',  # Number of audio channels
            '-ar', '44100',  # Sampling rate
            output_filename
        ]
        subprocess.run(command, check=True)

        # Optionally, remove the temporary file
        os.remove(input_filename)

        # file.save(file_path)

        text1 = ''
        text2 = ''

        the_downloaded_file_directory = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],)
        print(f'{On_IBlue}{BYellow}point 110: {the_downloaded_file_directory}{Color_Off}')

        the_downloaded_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'], secure_filename(created_filename))
        print(f'{On_IBlue}{BYellow}point 111: {the_downloaded_file_path}{Color_Off}')

        if created_filename.endswith('.wav'):
            print(f'{On_IBlue}{BYellow}point 2k2C: in .wav if loop {Color_Off}')
            # text1 = wav_file_content(created_filename)
            # print('2k2F')
            text1 = wav_file_content(the_downloaded_file_directory+f"/{secure_filename(created_filename)}")
            text2 = wav_file_content(the_downloaded_file_path)
            print('2k2G')

        print(f'2k2D: text: {text1}')
        print(f'2k2E: text2: {text2}')

        # Optionally, remove the temporary file
        os.remove(output_filename)
        return {'message': 'File successfully uploaded'}, 200


if __name__=='__main__':
	app.run(port=5205)
