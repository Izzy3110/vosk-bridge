import sys
from pydub import AudioSegment
import os


def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

out_filepath = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])),os.path.basename(sys.argv[1]).split(".")[0]+"_converted."+ os.path.basename(sys.argv[1]).split(".")[1])

mod_ = float(sys.argv[2])
sound = AudioSegment.from_file(sys.argv[1], "wav")
normalized_sound = match_target_amplitude(sound, mod_)
normalized_sound.export(out_filepath, format="wav")



