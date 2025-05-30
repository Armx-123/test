import os
import sys
import shutil
import librosa
import numpy as np
import moviepy.editor as mp
import soundfile as sf
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import noisereduce as nr

def preprocess_audio(file_path, target_sr=16000):
    """Load and preprocess audio: normalize, reduce noise, clean NaNs and Infs."""
    y, sr = librosa.load(file_path, sr=target_sr)
    if y is None or len(y) == 0:
        raise ValueError("Loaded audio is empty or corrupted")

    y = librosa.util.normalize(y)
    y = nr.reduce_noise(y=y, sr=target_sr, prop_decrease=0.8)

    y = np.nan_to_num(y)
    y[np.isinf(y)] = 0
    if not np.all(np.isfinite(y)):
        raise ValueError("Audio buffer contains non-finite values after cleaning")

    return y, target_sr

def extract_last_audio_from_video(video_path, duration, target_sr=16000):
    """Extract and preprocess the last `duration` seconds of audio from a video."""
    video = mp.VideoFileClip(video_path)
    start_time = max(video.duration - duration, 0)
    audio = video.audio.subclip(start_time, video.duration)

    temp_audio_path = "temp_audio.wav"
    audio.write_audiofile(temp_audio_path, codec='pcm_s16le')

    debug_audio(temp_audio_path)
    return preprocess_audio(temp_audio_path, target_sr)

def debug_audio(file_path):
    """Print basic info about an audio file and validate its content."""
    with sf.SoundFile(file_path) as f:
        print(f"Audio info: {file_path} - {f.samplerate} Hz, {f.channels} channels, {f.frames} frames")
        if f.frames == 0:
            raise ValueError("Extracted audio is empty.")

def process_single_video(music_folder, video_file, output_folder, threshold=5000):
    """Process a single video by checking for music match and trimming it."""
    output_path = os.path.join(output_folder, f"trimmed_{os.path.basename(video_file)}")

    try:
        video = mp.VideoFileClip(video_file)

        for music_file in os.listdir(music_folder):
            if music_file.endswith('.wav'):
                music_path = os.path.join(music_folder, music_file)

                # Load and process both audio sources
                y1, sr1 = preprocess_audio(music_path)
                audio_duration = librosa.get_duration(y=y1, sr=sr1)
                y2, sr2 = extract_last_audio_from_video(video_file, audio_duration)

                # Compare using MFCC + DTW
                mfcc1 = librosa.feature.mfcc(y=y1, sr=sr1, n_mfcc=40)
                mfcc2 = librosa.feature.mfcc(y=y2, sr=sr2, n_mfcc=40)
                distance, _ = fastdtw(mfcc1.T, mfcc2.T, dist=euclidean)

                print(f"[{os.path.basename(video_file)}] vs [{music_file}] -> DTW Distance: {distance}")

                # If match found, trim the video and return
                if distance < threshold:
                    print(f"Match found with '{music_file}'. Trimming video...")
                    trim_end = max(video.duration - audio_duration - 0.01, 0)
                    trimmed_video = video.subclip(0, trim_end)
                    trimmed_video.write_videofile(output_path, codec='libx264')
                    print(f"Trimmed video saved to: {output_path}")
                    return

        # No match found, save original video
        print(f"No match found. Saving original video to: {output_path}")
        video.write_videofile(output_path, codec='libx264')

    except Exception as e:
        print(f"\nError processing '{video_file}': {e}")
        print("Copying original video as fallback...")
        try:
            shutil.copy2(video_file, output_path)
            print(f"Copied original video to: {output_path}")
        except Exception as copy_error:
            print(f"Failed to copy video: {copy_error}")

def process_all_videos(music_folder, video_folder, output_folder, video_extensions=None):
    """Process all videos in a folder and save results to the output folder."""
    if video_extensions is None:
        video_extensions = ['.mp4', '.mov', '.avi', '.mkv']

    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(video_folder):
        if any(filename.lower().endswith(ext) for ext in video_extensions):
            video_path = os.path.join(video_folder, filename)
            print(f"\n=== Processing: {filename} ===")
            process_single_video(music_folder, video_path, output_folder)

# --- Example usage ---
if __name__ == "__main__":
    music_folder = os.path.join('assets', 'music')
    video_folder = os.path.join('folder')
    output_folder = os.path.join('Final')  # Folder to save output

    process_all_videos(music_folder, video_folder, output_folder)
