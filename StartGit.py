import shlex
import subprocess
from datetime import datetime


def git_repo():
    date_str = datetime.now().strftime('%m月%d日%H时%M分')
    commit_msg = f'自动化更新-{date_str}'
    # commit_msg = f'{date_str}-已改为sj默认GET'
    def run(cmd):
        subprocess.run(shlex.split(cmd),
                       cwd=r'E:\WindowsAi',
                       stdout=subprocess.PIPE,  # 捕获并静默标准输出
                       stderr=subprocess.PIPE,  # 捕获并静默警告
                       check=True)
    run("git add -u")
    try:
        run(f'git commit -m "{commit_msg}"')
    except subprocess.CalledProcessError as e:
        raise
    run("git push")

git_repo()
