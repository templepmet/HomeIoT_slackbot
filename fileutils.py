import subprocess
import datetime

def capture():
    dt = datetime.datetime.now()
    filename = dt.strftime('%Y%m%dT%H%M%S') + '.jpg'
    subprocess.call('raspistill -o {} -w 640 -h 480 -t 500'.format(filename), shell=True)
    return filename

def remove(filename):
    subprocess.call("rm {}".format(filename), shell=True)