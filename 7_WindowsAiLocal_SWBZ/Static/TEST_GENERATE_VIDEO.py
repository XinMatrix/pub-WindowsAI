import subprocess
import os


def create_final_video():
    cover_image_path = r"E:\WindowsAi\7_WindowsAiLocal_SWBZ\临时制作\封面.png"
    silent_video_path = r"E:\WindowsAi\7_WindowsAiLocal_SWBZ\临时制作\已裁剪空镜视频.mp4"
    audio_video_path = r"E:\WindowsAi\7_WindowsAiLocal_SWBZ\临时制作\音频带字幕.mp4"
    final_output = r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\临时制作\最终成品.mp4'

    temp_overlay = "temp_overlay.mp4"
    temp_cover = "temp_cover.mp4"
    concat_list = "temp_concat_list.txt"

    try:
        # 步骤1：黑色背景去除 + 叠加
        subprocess.run([
            "ffmpeg", "-y",
            "-i", audio_video_path,
            "-i", silent_video_path,
            "-filter_complex",
            "[0:v]scale=iw*1.1:ih*1.1,colorkey=black:0.3:0.2[fg];"
            "[1:v][fg]overlay=x=(W-w)/2:y=(H-h)/2:format=auto",
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",
            "-map", "0:a?",  # 保留原音频（如果有）
            temp_overlay
        ], check=True)

        # 步骤2：创建封面视频（3秒静音）
        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", cover_image_path,
            "-f", "lavfi", "-t", "3",
            "-i", "anullsrc=r=44100:cl=stereo",
            "-shortest",
            "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-pix_fmt", "yuv420p",
            temp_cover
        ], check=True)

        # 步骤3：写入拼接列表
        with open(concat_list, "w", encoding="utf-8") as f:
            f.write(f"file '{os.path.abspath(temp_cover)}'\n")
            f.write(f"file '{os.path.abspath(temp_overlay)}'\n")

        # 步骤4：拼接封面视频和合成视频（同时拼接音频）
        subprocess.run([
            "ffmpeg", "-y",
            "-i", temp_cover,
            "-i", temp_overlay,
            "-filter_complex",
            "[0:v:0][0:a:0][1:v:0][1:a:0]concat=n=2:v=1:a=1[outv][outa]",
            "-map", "[outv]",
            "-map", "[outa]",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-pix_fmt", "yuv420p",
            final_output
        ], check=True)

        print(f"✅ 完整视频生成成功，路径: {final_output}")

    finally:
        # 清理临时文件
        for file in [temp_overlay, temp_cover, concat_list]:
            if os.path.exists(file):
                os.remove(file)
        print("🧹 临时文件已清理。")


# 示例调用
if __name__ == '__main__':
    create_final_video()
