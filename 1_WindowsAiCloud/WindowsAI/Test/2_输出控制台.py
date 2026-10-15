import subprocess
import time


def open_cmd(temp_command_list):
    time.sleep(3)
    cmd_process = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    for command in temp_command_list:
        cmd_process.stdin.write((command + '\n').encode('gbk'))
    cmd_process.stdin.close()
    temp_output, _ = cmd_process.communicate()
    print(temp_output.decode('GBK'))


if __name__ == '__main__':
    print('A')
    open_cmd(['dir'])
    # output_list = open_cmd(['dir'])
    # for output in output_list:
    #     print(output)
    print('B')
