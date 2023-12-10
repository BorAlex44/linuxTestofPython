import yaml
import pytest

from sshcheckers import upload_files, ssh_checkout

with open('config.yaml', 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)


class TestPositive:

    def test_deploy(self):
        # test deploy
        res = []
        upload_files(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("passwd")}',
                     f'{data.get("local_path")}{data.get("file")}',
                     f'{data.get("remote_path")}{data.get("file")}')
        res.append(ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("passwd")}',
                                f'echo {data.get("user")} | sudo -S dpkg -i {data.get("remote_path")}{data.get("file")}',
                                'Настраивается пакет'))
        res.append(ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("passwd")}',
                                f'echo {data.get("user")} | sudo -S dpkg -s {data.get("dpkg")}',
                                'Status: install ok installed'))
        assert all(res), "test_deploy FAIL"

    def test_step1(self, make_folders, clear_folders, make_files):
        # test1
        res = [ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("passwd")}',
                            f'cd {data["folder_in"]}; 7z a -t{data.get("type")} {data["folder_out"]}/archive_1',
                            'Everything is Ok'),
               ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("passwd")}',
                            f'ls {data["folder_out"]}', f'archive_1.{data.get("type")}')]
        assert all(res), 'test1 FAIL'

    def test_step2(self, clear_folders, make_files):
        # test2
        res = [ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("passwd")}',
                            f'cd {data.get("folder_in")}; 7z a -t{data.get("type")} '
                            f'{data.get("folder_out")}/archive_1', 'Everything is Ok'),
               ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("passwd")}',
                            f'cd {data.get("folder_out")}; 7z e archive_1.{data.get("type")} '
                            f'-o{data.get("folder_ext")} -y', 'Everything is Ok')]
        for item in make_files:
            res.append(ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("passwd")}',
                                    f'ls {data.get("folder_ext")}', item))
        assert all(res), 'test2 Fail'

    def test_step3(self):
        # test3
        assert ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("passwd")}',
                            f'cd {data.get("folder_out")}; 7z t archive_1.{data.get("type")}',
                            "Everything is Ok"), 'test3 FAIL'

    def test_step4(self):
        # test4
        assert ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("passwd")}',
                            f'cd {data.get("folder_out")}; 7z u archive_2.{data.get("type")}',
                            "Everything is Ok"), 'test4 FAIL'

    def test_step5(self, clear_folders, make_files, del_folders, del_deploy):
        # test5
        res = [ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("passwd")}',
                            f'cd {data.get("folder_in")}; 7z a -t{data.get("type")} {data.get("folder_out")}/arx',
                            "Everything is Ok")]
        for i in make_files:
            res.append(ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("passwd")}',
                                    f'cd {data.get("folder_out")}; 7z l arx.{data.get("type")}', i))
        assert all(res), 'test5 FAIL'


if __name__ == '__main__':
    pytest.main(['-vv'])
    