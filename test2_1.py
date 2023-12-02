import pytest

from seminar2_1 import check_command, find_hash

folder_in = '/home/boralex/folder_in'
folder_out = '/home/boralex/folder_out'
folder_ex = '/home/boralex/folder_ex'


def test_step_1():
    assert check_command(f'cd {folder_in}; 7z a {folder_out}/archive_1',
                         'Everything is Ok')


def test_step_2():
    assert check_command(f'cd {folder_out}; 7z x archive_1.7z -o{folder_ex} ', 'Everything is Ok')


def test_step_3():
    result_1 = check_command(f'cd {folder_out}; 7z l {folder_out}/archive_1.7z', 'file_1.txt')
    result_2 = check_command(f'cd {folder_out}; 7z l {folder_out}/archive_1.7z', 'file_2.txt')
    result_3 = check_command(f'cd {folder_out}; 7z l {folder_out}/archive_1.7z', 'file_3.txt')
    assert result_1 and result_2 and result_3


def test_step_4():
    hash_res_1 = find_hash(f'cd {folder_out}; crc32 archive_1.7z')
    assert check_command(f'cd {folder_out}; 7z h archive_1.7z', hash_res_1)


if __name__ == '__main__':
    pytest.main(['-vv'])
