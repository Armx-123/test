import whisper_timestamped as whisper


def generate_srt(result, words_per_segment):
    srt_text = ""
    segment_count = 1
    word_buffer = []
    time_start, time_end = None, None

    for rs in result["segments"]:
        for word in rs["words"]:
            if not word_buffer:
                # Initialize the start time for a new segment
                time_start = word["start"]

            word_buffer.append(word["text"])
            time_end = word["end"]  # Update the end time

            # Check if the buffer has reached the desired words per segment
            if len(word_buffer) >= words_per_segment:
                # Format timestamps
                time_start_formatted = "{:02d}:{:02d}:{:06.3f}".format(
                    int(time_start // 3600),
                    int((time_start % 3600) // 60),
                    time_start % 60
                )
                time_end_formatted = "{:02d}:{:02d}:{:06.3f}".format(
                    int(time_end // 3600),
                    int((time_end % 3600) // 60),
                    time_end % 60
                )

                # Create SRT text for the segment
                srt_text += str(segment_count) + "\n"
                srt_text += time_start_formatted.replace('.', ',') + " --> " + time_end_formatted.replace('.', ',') + "\n"
                srt_text += " ".join(word_buffer) + "\n\n"

                segment_count += 1
                word_buffer = []  # Reset the buffer

    # Handle any remaining words in the buffer
    if word_buffer:
        # Format timestamps
        time_start_formatted = "{:02d}:{:02d}:{:06.3f}".format(
            int(time_start // 3600),
            int((time_start % 3600) // 60),
            time_start % 60
        )
        time_end_formatted = "{:02d}:{:02d}:{:06.3f}".format(
            int(time_end // 3600),
            int((time_end % 3600) // 60),
            time_end % 60
        )

        # Create SRT text for the segment
        srt_text += str(segment_count) + "\n"
        srt_text += time_start_formatted.replace('.', ',') + " --> " + time_end_formatted.replace('.', ',') + "\n"
        srt_text += " ".join(word_buffer) + "\n\n"

    return srt_text


# Load and transcribe the audio
audio_path = "lol.mp3"  # Replace with your audio file
audio = whisper.load_audio(audio_path)
model = whisper.load_model("tiny", device="cpu")
result = whisper.transcribe(model, audio, remove_punctuation_from_words=False)

# Specify the number of words per segment
words_per_segment = 1  # Adjust this value as needed

# Generate SRT content
srt_content = generate_srt(result, words_per_segment)

# Write the SRT content to a file
with open("output.srt", "w") as srt_file:
    srt_file.write(srt_content)

print("SRT file generated successfully.")
