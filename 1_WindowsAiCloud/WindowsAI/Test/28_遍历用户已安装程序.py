import winreg


def get_installed_programs():
    temp_installed_programs = []
    reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_32KEY) as key:
        for i in range(winreg.QueryInfoKey(key)[0]):
            sub_key_name = winreg.EnumKey(key, i)
            with winreg.OpenKey(key, sub_key_name) as sub_key:
                try:
                    program_name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                    temp_installed_programs.append(program_name)
                except FileNotFoundError:
                    continue
    return temp_installed_programs


# 获取已安装程序列表
installed_programs = get_installed_programs()
print('installed_programs len = ', len(installed_programs))

# 打印已安装程序
for program in installed_programs:
    print(program)
