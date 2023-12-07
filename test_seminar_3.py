import pytest
import yaml
from seminar_3 import check_command, getout

with open('config.yaml', encoding='utf-8') as file:
    data = yaml.safe_load(file)


class TestPositive:

    def test_step1(self, make_folders, clear_folders, make_files):
        # test1
        res = [check_command(f'cd {data["folder_in"]}; 7z a -t{data.get("type")} {data["folder_out"]}/archive_1',
                             'Everything is Ok'), check_command(f'ls {data["folder_out"]}',
                                                                f'archive_1.{data.get("type")}')]
        assert all(res), 'test1 FAIL'

    def test_step2(self, clear_folders, make_files):
        # test2
        res = [check_command(f'cd {data.get("folder_in")}; 7z a -t{data.get("type")} '
                             f'{data.get("folder_out")}/archive_1', 'Everything is Ok'),
               check_command(f'cd {data.get("folder_out")}; 7z e archive_1.{data.get("type")} '
                             f'-o{data.get("folder_ext")} -y', 'Everything is Ok')]
        for item in make_files:
            res.append(check_command(f'ls {data.get("folder_ext")}', item))
        assert all(res), 'test2 Fail'

    def test_step3(self):
        # test3
        assert check_command(f'cd {data.get("folder_out")}; 7z t archive_1.{data.get("type")}',
                             "Everything is Ok"), 'test3 FAIL'

    def test_step4(self):
        # test4
        assert check_command(f'cd {data.get("folder_in")}; 7z u archive_2.{data.get("type")}',
                             "Everything is Ok"), 'test4 FAIL'

    def test_step5(self, clear_folders, make_files):
        # test5
        res = [check_command(f'cd {data.get("folder_in")}; 7z a -t{data.get("type")} {data.get("folder_out")}/arx',
                             "Everything is Ok")]
        for i in make_files:
            res.append(check_command(f'cd {data.get("folder_out")}; 7z l arx.{data.get("type")}', i))
        assert all(res), 'test5 FAIL'

    def test_step6(self, clear_folders, make_files, make_sub_folder):
        # test6
        res = [check_command(f'cd {data.get("folder_in")}; 7z a -t{data.get("type")} '
                             f'{data.get("folder_out")}/arx', "Everything is Ok"),
               check_command(f'cd {data.get("folder_out")}; 7z x arx.{data.get("type")} '
                             f'-o{data.get("folder_ext2")} -y', "Everything is Ok")]
        for i in make_files:
            res.append(check_command(f'ls {data.get("folder_ext2")}', i))
            res.append(check_command(f'ls {data.get("folder_ext2")}', make_sub_folder[0]))
            res.append(check_command(f'ls {data.get("folder_ext2")}/{make_sub_folder[0]}', make_sub_folder[1]))
        assert all(res), 'test6 FAIL'

    def test_step7(self):
        # test7
        assert check_command(f'cd {data.get("folder_out")}; 7z d arx.{data.get("type")}',
                             "Everything is Ok"), 'test7 FAIL'

    def test_step8(self, clear_folders, make_files, del_folders):
        # test8
        res = []
        for i in make_files:
            res.append(check_command(f'cd {data.get("folder_in")}; 7z h {i}', "Everything is Ok"))
            i_hash = getout(f'cd {data.get("folder_in")}; crc32 {i}').upper()
            res.append(check_command(f'cd {data.get("folder_in")}; 7z h {i}', i_hash))
        assert all(res), 'test8 FAIL'


if __name__ == '__main__':
    pytest.main(['-vv'])
