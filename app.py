#!/usr/bin/env python3
"""Queue and retry FFmpeg jobs with progress tracking."""
import argparse, json, shutil, subprocess, time
from pathlib import Path

def require(x):
    if shutil.which(x) is None: raise SystemExit(f'Missing required binary: {x}')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('queue_json'); p.add_argument('--retries',type=int,default=1)
    a=p.parse_args(); require('ffmpeg')
    jobs=json.loads(Path(a.queue_json).read_text())
    for job in jobs:
        cmd=job['cmd']; attempts=0
        while True:
            attempts += 1; print('Running', cmd, 'attempt', attempts)
            rc=subprocess.call(cmd)
            if rc==0 or attempts>a.retries: break
            time.sleep(2)
if __name__ == '__main__': main()
