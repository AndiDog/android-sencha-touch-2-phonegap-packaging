import os
import subprocess
import sys

def contains_errors(s):
    return '[ERROR]' in s

def get_errors(s):
    ret = ''
    for line in s.splitlines():
        if contains_errors(line):
            ret += line + '\n'
    return ret

print('Running Sencha command...')
proc = subprocess.Popen(['sencha.bat' if os.name == 'nt' else 'sencha'] + list(sys.argv[1:]),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
stdout, stderr = proc.communicate()

if proc.returncode != 0 or contains_errors(stdout) or contains_errors(stderr):
    return_code = proc.returncode or 1
    sys.stderr.write('Command failed\n')
else:
    return_code = 0

sys.stdout.write(stdout)
sys.stderr.write(stderr)

# Eclipse does not seem to stop the build even for return codes != 1, so let's be a bit more cruel
with open(os.path.join('android', 'AndroidManifest.xml'), 'r+t') as f:
    MAGIC = 'SENCHA BUILD FAILED, PLEASE CHECK FOR ERRORS AND RE-RUN BUILD (THIS LINE IS REMOVED AUTOMATICALLY IF SENCHA BUILD SUCCEEDS)'
    content = f.read()

    magicPosition = content.find(MAGIC)
    if magicPosition != -1:
        content = content[:magicPosition].strip()

    if return_code != 0:
        content += '\n' + MAGIC + '\n' + get_errors(stdout + '\n' + stderr)

    f.seek(0)
    f.write(content)
    f.truncate()

exit(return_code)