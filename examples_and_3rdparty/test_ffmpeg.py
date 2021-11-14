import subprocess
import os
import shutil
import sys

file_name_ = sys.argv[1]
new_file_ = file_name_.replace(" ", "_")
splitted_ = new_file_.split(".")
tmp_ = []
for i_ in range(0, len(splitted_)):
    if i_ < len(splitted_) - 1:
        tmp_.append(splitted_[i_])

sample_rate = 16000
audio_channels = 2

new_name = os.path.join("_".join(tmp_) + "_reencoded-ar16000" + "." + splitted_[len(splitted_) - 1])
cmd_ = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "ffmpeg-4.4.1-full_build",
    "bin", "ffmpeg.exe"
) + \
       " -i " + os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", new_file_) + \
       " -y -f wav -bitexact -acodec pcm_s16le -ar " + str(sample_rate) + \
       " -ac "+str(audio_channels)+" " + new_name

with subprocess.Popen(cmd_, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, cwd="..") as ps:
    err, out = ps.communicate()
    if len(err) != 0:
        for line in out.splitlines():
            print("out: " + line.decode())
    else:
        for line in err.splitlines():
            print("err: " + line.decode())
