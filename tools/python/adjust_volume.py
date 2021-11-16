import wave, audioop

factor = 0.5

with wave.open('input.wav', 'rb') as wav:
    p = wav.getparams()
    with wave.open('output.wav', 'wb') as audio:
        audio.setparams(p)
        frames = wav.readframes(p.nframes)
        audio.writeframesraw( audioop.mul(frames, p.sampwidth, factor))