import librosa
import numpy as np
import moviepy.editor as mp
import os
import subprocess
import sys
import soundfile as sf
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import noisereduce as nr

def preprocess_audio(file_path, target_sr=16000):
    try:
        y, sr = librosa.load(file_path, sr=target_sr)
        if y is None or len(y) == 0:
            raise ValueError("Loaded audio is empty or corrupted")

        y = librosa.util.normalize(y)
        y = nr.reduce_noise(y=y, sr=target_sr, prop_decrease=0.8)

        y = np.nan_to_num(y)
        y[np.isinf(y)] = 0
        if not np.all(np.isfinite(y)):
            raise ValueError("Audio buffer is not finite everywhere after cleaning")

        return y, target_sr
    except Exception as e:
        handle_error(e)
        raise

def extract_last_audio_from_video(video_path, duration, target_sr=16000):
    try:
        video = mp.VideoFileClip(video_path)
        audio = video.audio.subclip(max(video.duration - duration, 0), video.duration)

        audio_path = "temp_audio.wav"
        audio.write_audiofile(audio_path, codec='pcm_s16le')

        debug_audio(audio_path)
        return preprocess_audio(audio_path, target_sr)
    except Exception as e:
        handle_error(e)
        raise

def debug_audio(file_path):
    try:
        with sf.SoundFile(file_path) as f:
            print(f"Audio file {file_path} info: {f.samplerate} Hz, {f.channels} channels, {f.frames} frames")
            if f.frames == 0:
                raise ValueError("Extracted audio is empty.")
    except Exception as e:
        print(f"Error reading audio file: {e}")
        raise

def handle_error(error):
    print(f"Error encountered: {error}\nRunning recovery scripts...")
    with open("error.txt", "w") as error_file:
        error_file.write(str(error))
    subprocess.run([sys.executable, "Python Files/sorter/download.py"], check=True)
    print("Recovery scripts executed. Retrying processing...")

def process_single_video(music_folder, video_file, output_folder, threshold=5000):
    try:
        video = mp.VideoFileClip(video_file)

        for filename in os.listdir(music_folder):
            if filename.endswith('.wav'):
                audio_file = os.path.join(music_folder, filename)
                y1, sr1 = preprocess_audio(audio_file)
                audio_duration = librosa.get_duration(y=y1, sr=sr1)
                y2, sr2 = extract_last_audio_from_video(video_file, audio_duration)

                mfcc1 = librosa.feature.mfcc(y=y1, sr=sr1, n_mfcc=40)
                mfcc2 = librosa.feature.mfcc(y=y2, sr=sr2, n_mfcc=40)

                distance, _ = fastdtw(mfcc1.T, mfcc2.T, dist=euclidean)
                print(f"Comparing {os.path.basename(video_file)} with {filename}, DTW Distance: {distance}")

                output_path = os.path.join(output_folder, f"trimmed_{os.path.basename(video_file)}")
                if distance < threshold:
                    print(f"Match found with {filename}. Trimming video...")
                    trim_end = max(video.duration - audio_duration - 0.01, 0)
                    trimmed_video = video.subclip(0, trim_end)
                    trimmed_video.write_videofile(output_path, codec='libx264')
                    print(f"Trimmed video saved as {output_path}")
                    return

        print(f"No matching audio found for {os.path.basename(video_file)}. Saving the original video.")
        output_path = os.path.join(output_folder, f"trimmed_{os.path.basename(video_file)}")
        video.write_videofile(output_path, codec='libx264')
        print(f"Video saved as {output_path}")
    except Exception as e:
        handle_error(e)
        print(f"Skipping video {video_file} due to error: {e}")

def process_all_videos(music_folder, video_folder, output_folder, video_extensions=None):
    if video_extensions is None:
        video_extensions = ['.mp4', '.mov', '.avi', '.mkv']

    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(video_folder):
        if any(filename.lower().endswith(ext) for ext in video_extensions):
            video_path = os.path.join(video_folder, filename)
            print(f"\nProcessing video: {filename}")
            process_single_video(music_folder, video_path, output_folder)

# Example usage
music_folder = os.path.join('assets', 'music')
video_folder = os.path.join('folder')
output_folder = os.path.join('Final')  # New folder to store output

process_all_videos(music_folder, video_folder, output_folder)
