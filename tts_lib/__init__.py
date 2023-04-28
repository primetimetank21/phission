import pyttsx3


def tts(text: str, rate: int = 185, voice: str = "english"):
    engine = pyttsx3.init()
    props = {
        "rate": rate,
        "voice": voice,
    }
    for prop, value in props.items():
        engine.setProperty(prop, value)

    engine.say(text)
    engine.runAndWait()
    engine.stop()


# for playing with the API
if __name__ == "__main__":
    talk_rate = int(input("Enter a rate: "))
    tts("Welcome to MorphCast Emotion AI HTML5 SDK", talk_rate)
    tts("New Mobile App", talk_rate)
    tts("Alert! The control point is being captured", talk_rate)
    tts("Security alert", talk_rate)
