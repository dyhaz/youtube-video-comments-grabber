import subprocess

def combine(video_id):
    cmd = 'avconv -v debug -i downloads/' + video_id + '.mp3 -i downloads/dance' + video_id + '.mp4 -c:a libmp3lame -qscale 20 -shortest downloads/output' + video_id + '.mov'
    subprocess.call(cmd, shell=True) # "Muxing Done
    cmd = 'avconv -i downloads/output' + video_id + '.mov -c:v libx264 downloads/output' + video_id + '.mp4'
    subprocess.call(cmd, shell=True)
    print('Muxing Done')