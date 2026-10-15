import subprocess

# installed_programs = subprocess.check_output('wmic product get name', shell=True, encoding='utf-8')
installed_programs = subprocess.check_output('wmic product get name', shell=True, encoding='GBK')
print(installed_programs)
print('installed_programs len = ', len(installed_programs))

# subprocess.call('appwiz.cpl', shell=True) # 这个是打开卸载，比系统自带的好用
