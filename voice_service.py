import os
import json
import vosk
import pyaudio


MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "vosk-model",
    "vosk-model-small-en-us-0.15"
)


def main():
    print("SAFEHER BACKGROUND VOICE SERVICE STARTED")

    try:
        model = vosk.Model(MODEL_PATH)

        recognizer = vosk.KaldiRecognizer(
            model,
            16000
        )

        audio = pyaudio.PyAudio()

        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=4000
        )

        stream.start_stream()

        print("SAFEHER: BACKGROUND LISTENING ACTIVE")

        while True:

            data = stream.read(
                4000,
                exception_on_overflow=False
            )

            if recognizer.AcceptWaveform(data):

                result = json.loads(
                    recognizer.Result()
                )

                detected_text = result.get(
                    "text",
                    ""
                ).lower().strip()

                if detected_text:

                    print(
                        "BACKGROUND VOICE:",
                        detected_text
                    )

                if "help" in detected_text:

                    print(
                        "SAFEHER EMERGENCY VOICE DETECTED: HELP"
                    )

    except Exception as error:

        print(
            "BACKGROUND VOICE SERVICE ERROR:",
            error
        )


if __name__ == "__main__":
    main()