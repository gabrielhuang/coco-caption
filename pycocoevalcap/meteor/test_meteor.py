import subprocess
import os
from time import time

TEST_METEOR = True
USE_COMMUNICATE = False
BUFSIZE=0

if TEST_METEOR:
    meteor_p = subprocess.Popen(['java', '-jar', '-Xmx2G', 'meteor-1.5.jar',
                       '-', '-', '-stdio', '-l', 'en', '-norm'],
                                     cwd=os.path.dirname(os.path.abspath(__file__)),
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,bufsize=BUFSIZE)
else:
    meteor_p = subprocess.Popen(['cat'],
                                 cwd=os.path.dirname(os.path.abspath(__file__)),
                                 stdin=subprocess.PIPE,
                                bufsize=BUFSIZE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE
                                 )

score_line ='SCORE ||| the cat in the hat is black . ||| the black cat is hat is hat'

if USE_COMMUNICATE:
    out, err = meteor_p.communicate('{}\n'.format(score_line).encode())
    print('"{}"'.format(out))
else:
    # This creates a deadlock in Python 3, unless BUFSIZE=0
    # The default value changed between Python 2 and 3.
    # https://docs.python.org/2/library/subprocess.html#subprocess.Popen
    # https://docs.python.org/3/library/subprocess.html#subprocess.Popen
    print('Sending line')
    meteor_p.stdin.write('{}\n'.format(score_line).encode())
    meteor_p.stdin.flush()
    last = time()

    print ('Waiting for answer')
    answer = meteor_p.stdout.readline().decode().strip()

    print ('Answer {}'.format(answer))
