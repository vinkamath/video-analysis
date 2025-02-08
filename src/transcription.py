import os
import json
from dotenv import load_dotenv
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

def transcribe_audio(audio_filename: str):
    """
    Transcribes an audio file using the Deepgram API.

    Args:
        audio_filename (str): The path to the audio file to transcribe.
    """
    # Check if the audio file exists
    try:
        if not os.path.exists(audio_filename):
            print(f"Audio file {audio_filename} does not exist.")
            return
    except FileNotFoundError as e:
        print(f"Audio file {audio_filename} does not exist.")
        raise e

    # if transcription exists, do nothing
    if os.path.exists(audio_filename.replace(".mp3", "_transcription.json")):
        print(f"Transcription for {audio_filename} already exists.")
        return

    try:
        # STEP 1 Create a Deepgram client using the API key
        load_dotenv()
        deepgram = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))

        with open(audio_filename, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        #STEP 2: Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            #smart_format=True,
            filler_words=True
        )

        # STEP 3: Call the transcribe_file method with the text payload and options
        response = deepgram.listen.rest.v("1").transcribe_file(payload, options)

        # STEP 4: Extract the transcription from the response
        transcription = response.results.channels[0].alternatives[0]

        # STEP 5: Print the transcription
        output_directory = os.path.dirname(audio_filename)
        input_filename = os.path.basename(audio_filename)
        output_filename = os.path.join(output_directory, input_filename.replace(".mp3", "_transcription.json"))
        with open(output_filename, "w") as f:
            json.dump(response.to_dict(), f, indent=4)
        print(f"Transcription saved to {output_filename}")

    except Exception as e:
        print(f"Exception: {e}")
