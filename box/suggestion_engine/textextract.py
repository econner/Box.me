import os
from box import constants
import subprocess

def extract_text(filename):
    args = constants.POI_SUBPROCESS_ARGS
    args.append(filename)
    pipe = subprocess.Popen(args, stdout=subprocess.PIPE)
    return pipe.stdout.read().decode('utf-8', 'ignore')