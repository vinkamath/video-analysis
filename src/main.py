from audio import download_audio_snippet
from transcription import transcribe_audio

def main():
    # Example usage
    youtube_url = 'https://www.youtube.com/watch?v=3uB_kn4HwKc'  
    start_time = None  # Start time (HH:MM:SS or seconds)
    end_time = None  # End time (HH:MM:SS or seconds)

    audio_file = download_audio_snippet(youtube_url, start_time, end_time)
    transcribe_audio(audio_filename=audio_file)


if __name__ == '__main__':
    main()