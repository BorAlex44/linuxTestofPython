import random
import string
from datetime import datetime

import pytest
import yaml
from seminar_3 import check_command, getout

with open('config.yaml', encoding='utf-8') as file:
    data = yaml.safe_load(file)


@pytest.fixture()
def make_folders():
    return check_command(f'mkdir -p {data.get("folder_in")} {data.get("folder_out")} {data.get("folder_ext")} '
                         f'{data.get("folder_ext2")}', '')


@pytest.fixture()
def del_folders():
    yield
    return check_command(f'rm -rf {data.get("folder_in")} {data.get("folder_out")} {data.get("folder_ext")} '
                         f'{data.get("folder_ext2")}', '')


@pytest.fixture()
def clear_folders():
    return check_command(f'rm -rf {data.get("folder_in")}/* {data.get("folder_out")}/* '
                         f'{data.get("folder_ext")}/* {data.get("folder_ext2")}/*', "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data.get('count')):
        file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if check_command(f'cd {data.get("folder_in")}; dd if=/dev/urandom of={file_name} bs={data.get("bs")} '
                         f'count=1 iflag=fullblock', ''):
            list_of_files.append(file_name)
    return list_of_files


@pytest.fixture()
def make_sub_folder():
    test_filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    sub_folder_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not check_command(f'cd {data.get("folder_in")}; mkdir {sub_folder_name}', ""):
        return None, None
    if not check_command(f'cd {data.get("folder_in")}/{sub_folder_name}; '
                         f'dd if=/dev/urandom of={test_filename} bs=1M count=1 iflag=fullblock', ""):
        return sub_folder_name, None
    else:
        return sub_folder_name, test_filename


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print("Finish: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture(autouse=True)
def stat_log():
    yield
    time = datetime.now().strftime("%H:%M:%s.%f")
    stat = getout('cat /proc/loadavg')
    check_command(f"echo 'time:{time} count:{data.get('count')} size:{data.get('bs')} stat:{stat}' >> stat.txt",
                  '')
