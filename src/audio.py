import os
from dotenv import load_dotenv
import youtube_dl
import subprocess
import os

OUTPUT_PATH = "data/output"
def download_audio_snippet(youtube_url, start_time=None, end_time=None):
    """
    Downloads a snippet of audio from a YouTube video and saves it as an MP3 file.

    Args:
        youtube_url: The URL of the YouTube video.
        start_time: The start time of the snippet in seconds (or a string like "00:01:30").
        end_time: The end time of the snippet in seconds (or a string like "00:02:00").
    
    Returns:
        str: The file path of the downloaded audio snippet.
    """

    try:
        # Convert start and end times to seconds if they are strings
        if isinstance(start_time, str):
            start_time = time_string_to_seconds(start_time)
        if isinstance(end_time, str):
            end_time = time_string_to_seconds(end_time)

        # Ensure start_time and end_time are valid (if provided)
        if start_time is not None and (not isinstance(start_time, (int, float)) or start_time < 0):
            raise ValueError("start_time must be a non-negative integer, float, or string in HH:MM:SS format, or None.")
        if end_time is not None and (not isinstance(end_time, (int, float)) or end_time < 0):
            raise ValueError("end_time must be a non-negative integer, float, or string in HH:MM:SS format, or None.")
        if start_time is not None and end_time is not None and start_time >= end_time:
            raise ValueError("start_time must be less than end_time.")

        # Use video ID from the URL as temporary audio filename
        video_id = youtube_url.split('v=')[-1]
        output_directory = os.path.join(OUTPUT_PATH, video_id)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        temp_audio_filename = os.path.join(output_directory, "full_audio.mp4")

        # Check if the file already exists
        if os.path.exists(temp_audio_filename):
            print(f"File {temp_audio_filename} already exists. Skipping download.")
        else:
            # Create youtube_dl options
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': temp_audio_filename,
                'noplaylist': True,  # Prevent downloading entire playlists
            }

            # Download the audio using youtube_dl
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])

        # Use ffmpeg to extract the audio snippet and convert to MP3
        command = ['ffmpeg']
        suffix = ""

        if start_time is not None:
            command.extend(['-ss', str(start_time)])
            suffix += f"_{start_time}"
        else:
            suffix += "_0"
        if end_time is not None:
            command.extend(['-to', str(end_time)])
            suffix += f"_{end_time}"
        else:
            suffix += "_end"
        output_filename = os.path.join(output_directory, "audio_snippet" + suffix + ".mp3")

        command.extend(['-i', temp_audio_filename,
                         '-vn',  # Disable video processing
                         '-acodec', 'libmp3lame',  # Use MP3 encoder
                         '-ab', '128k',  # Set audio bitrate (optional)
                         '-n', # Do not overwrite output files
                         output_filename])

        subprocess.run(command, check=True) # Raises exception on failure

        print(f"Audio snippet saved to {output_filename}")

        return output_filename

    except youtube_dl.utils.DownloadError as e:
        print(f"Error downloading video: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing audio with ffmpeg: {e}")
    except FileNotFoundError:
        print("Error: ffmpeg not found.  Please install ffmpeg (e.g., 'apt install ffmpeg' or 'brew install ffmpeg').")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def time_string_to_seconds(time_string):
    """Converts a time string in HH:MM:SS format to seconds."""
    hours, minutes, seconds = map(float, time_string.split(':'))
    return hours * 3600 + minutes * 60 + seconds


if __name__ == '__main__':
    # Example usage
    youtube_url = 'https://www.youtube.com/watch?v=3uB_kn4HwKc'  
    start_time = None  # Start time (HH:MM:SS or seconds)
    end_time = None  # End time (HH:MM:SS or seconds)

    download_audio_snippet(youtube_url, start_time, end_time)