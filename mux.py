import subprocess

def combine(video_id, keyword):
    cmd = 'avconv -v debug -i downloads/' + video_id + '.mp3 -i downloads/' + keyword + video_id + '.mp4 -c:a libmp3lame -qscale 20 -shortest -y downloads/output' + video_id + '.mov'
    subprocess.call(cmd, shell=True) # "Muxing Done
    cmd = 'avconv -i downloads/output' + video_id + '.mov -c:v libx264 downloads/output' + video_id + '.mp4'
    subprocess.call(cmd, shell=True)
    print('Muxing Done')