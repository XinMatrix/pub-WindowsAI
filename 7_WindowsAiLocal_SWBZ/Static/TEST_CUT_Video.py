import subprocess


def cut_video_middle(temp_input_file, temp_start_time, temp_end_time):
    # 指定输出路径
    output_file = r"E:\WindowsAi\7_WindowsAiLocal_SWBZ\临时制作\cut_video.mp4"

    # 构建 ffmpeg 命令：快速裁剪 + 无重新编码
    command = [
        "ffmpeg",
        "-ss", str(temp_start_time),
        "-to", str(temp_end_time),
        "-i", temp_input_file,
        "-c", "copy",  # 复制模式，极快
        output_file,
        "-y"  # 自动覆盖
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_file
    except subprocess.CalledProcessError:
        return None


if __name__ == '__main__':

    # IDEA 秒速啊我草

    input_file = r'/7_WindowsAiLocal_SWBZ/Static/空镜素材.mp4'
    # input_file = r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\临时制作\音频带字幕.mp4'
    start_time = 0
    end_time = 60

    result_path = cut_video_middle(input_file, start_time, end_time)
    if result_path:
        print(f"视频已成功保存到: {result_path}")
    else:
        print("视频处理失败")
