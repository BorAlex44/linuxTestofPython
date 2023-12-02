import subprocess


def check_command(command, text):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = result.stdout
    if result.returncode == 0 and text in out:
        return True
    else:
        return False


def find_hash(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = result.stdout.upper()
    print(out)
    if result.returncode == 0:
        return out
    else:
        return False
