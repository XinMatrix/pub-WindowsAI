import subprocess
import wmi


def check_nvidia_gpu_windows():
    try:
        w = wmi.WMI()
        gpus = w.Win32_VideoController()
        for gpu in gpus:
            if "NVIDIA" in gpu.Name:
                print(f"检测到NVIDIA GPU: {gpu.Name}")
                return True
        print("系统没有检测到NVIDIA GPU。")
        return False
    except ImportError:
        print("请先安装wmi模块: pip install wmi")
        return False


def check_nvidia_gpu_linux():
    try:
        # 使用lspci命令检测NVIDIA GPU
        result = subprocess.run(['lspci'], capture_output=True, text=True)
        if 'NVIDIA' in result.stdout:
            print("检测到NVIDIA GPU:")
            print([line for line in result.stdout.split('\n') if 'NVIDIA' in line])
            return True
        else:
            print("系统没有检测到NVIDIA GPU。")
            return False
    except FileNotFoundError:
        print("未找到lspci工具，无法检测GPU。请确保lspci已安装。")
        return False


if __name__ == "__main__":
    has_gpu = check_nvidia_gpu_windows()
    if has_gpu:
        print("系统检测到支持CUDA的NVIDIA GPU。")
    else:
        print("系统未检测到NVIDIA GPU，无法进行CUDA开发。")
