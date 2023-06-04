from elevenlabs import clone, generate, play, set_api_key, VOICES_CACHE, voices
from elevenlabs.api import History
import os

os.environ['ELEVENLABS_API_KEY'] = ''

set_api_key(os.environ.get("ELEVENLABS_API_KEY"))


def with_custom_voice(name, description, prompt, file_path):
    audio_path = 'sample.mp3'

    voice = clone(
        name=name,
        description=description,
        files=[file_path,],
    )

    audio = generate(text=prompt, voice=voice)

    play(audio)

    try:
        with open(audio_path, 'wb') as f:
            f.write(audio)

        return audio_path
    
    except Exception as e:
        print(e)
        
        return ""


def with_premade_voice(prompt, voice):
    audio_path = f'{voice}.mp3'

    audio = generate(
        text=prompt,
        voice=voice,
        model="eleven_monolingual_v1"
    )

    play(audio)

    try:
        with open(audio_path, 'wb') as f:
            f.write(audio)

        return audio_path
    
    except Exception as e:
        print(e)

        return ""


def get_voices():
    names = []

    v_list = voices()

    for v in v_list:
        names.append(v.name)

    return names


# usage
# if __name__ == '__main__':
    # print(get_voices())

    # print(with_premade_voice(prompt='Hi! My name is Bella, nice to meet you!', voice='Bella'))
