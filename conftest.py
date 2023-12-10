import string
import random
import pytest
import yaml

from sshcheckers import ssh_checkout

with open('config.yaml', 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)


@pytest.fixture()
def del_deploy():
    yield
    return ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("passwd")}',
                        f'echo {data.get("user")} | sudo -S dpkg -r {data.get("dpkg")}',
                        'Удаляется')


@pytest.fixture()
def make_folders():
    return ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("passwd")}',
                        f'mkdir -p {data.get("folder_in")} {data.get("folder_out")} {data.get("folder_ext")} '
                        f'{data.get("folder_ext2")}', '')


@pytest.fixture()
def clear_folders():
    return ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("passwd")}',
                        f'rm -rf {data.get("folder_in")}/* {data.get("folder_out")}/* '
                        f'{data.get("folder_ext")}/* {data.get("folder_ext2")}/*', "")


@pytest.fixture()
def del_folders():
    yield
    return ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("passwd")}',
                        f'rm -rf {data.get("folder_in")} {data.get("folder_out")} {data.get("folder_ext")} '
                        f'{data.get("folder_ext2")}', '')


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data.get('count')):
        file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("passwd")}',
                        f'cd {data.get("folder_in")}; dd if=/dev/urandom of={file_name} bs={data.get("bs")} '
                        f'count=1 iflag=fullblock', ''):
            list_of_files.append(file_name)
    return list_of_files
