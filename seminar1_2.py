import string
import subprocess


def subprocess_file(directory: str, find_name: str, find_word='Yes'):
    result = subprocess.run(directory, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = result.stdout
    if result.returncode == 0:
        lst = out.split("\n")
        if find_name in lst:
            for elem in find_name:
                if elem in string.punctuation:
                    find_name = find_name.replace(elem, " ")
            if find_word in find_name:
                print('Find')
            else:
                print('No find')
            return True
        return False
    return False


if __name__ == '__main__':
    print(subprocess_file('cat /etc/os-release',
                          'VERSION="22.04.3 LTS (Jammy Jellyfish)"', '04'))
    