import sys
import wave
import librosa
import soundfile as sf
from tempfile import NamedTemporaryFile
import shutil
import os
import warnings
warnings.filterwarnings('ignore')
x,_ = librosa.load(sys.argv[1], sr=16000)
f = NamedTemporaryFile(delete=False,suffix=".wav")
out_filepath = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])),os.path.basename(sys.argv[1]).split(".")[0]+"_converted."+os.path.basename(sys.argv[1]).split(".")[1])
sf.write(f.name, x, 16000)
shutil.move(f.name, out_filepath)
f.close()