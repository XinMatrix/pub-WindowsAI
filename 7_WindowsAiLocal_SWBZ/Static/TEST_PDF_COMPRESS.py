import subprocess
import os

def compress_pdf_ghostscript(input_path, output_path, max_size_mb=20):
    """使用 Ghostscript 压缩 PDF"""
    max_size_bytes = max_size_mb * 1024 * 1024

    # 检查输入文件
    if not os.path.exists(input_path):
        print(f"错误: 文件 {input_path} 不存在")
        return False

    original_size = os.path.getsize(input_path)
    print(f"原始文件大小: {original_size / (1024 * 1024):.2f} MB")

    if original_size <= max_size_bytes:
        print("文件已小于目标大小，无需压缩")
        os.replace(input_path, output_path)
        return True

    # 尝试不同压缩级别
    for quality in ["/printer", "/ebook", "/screen"]:  # 从高到低质量
        try:
            subprocess.run([
                "gswin64c" if os.name == 'nt' else "gs",  # Windows 用 gswin64c，其他系统用 gs
                "-sDEVICE=pdfwrite",
                f"-dPDFSETTINGS={quality}",
                "-dNOPAUSE",
                "-dQUIET",
                "-dBATCH",
                f"-sOutputFile={output_path}",
                input_path
            ], check=True)

            compressed_size = os.path.getsize(output_path)
            print(f"压缩级别 {quality} -> 大小: {compressed_size / (1024 * 1024):.2f} MB")

            if compressed_size <= max_size_bytes:
                print(f"成功压缩到 {compressed_size / (1024 * 1024):.2f} MB")
                return True

        except subprocess.CalledProcessError as e:
            print(f"Ghostscript 压缩失败: {e}")
            continue

    print("无法压缩到目标大小以下")
    return False

# 使用示例
if __name__ == "__main__":
    # input_pdf = r"E:\xwechat_files\wxid_z9wrrwcf37tu22_71df\msg\file\2025-05\岐黄宁心——安宁疗护全周期科普志愿服务引领者.pdf"
    input_pdf = r"E:\xwechat_files\wxid_z9wrrwcf37tu22_71df\msg\file\2025-06\PPT：武凡+秋叶静美——安宁疗护全周期科普志愿服务引领者.pdf"
    output_pdf = "compressed.pdf"
    if compress_pdf_ghostscript(input_pdf, output_pdf, max_size_mb=20):
        print("压缩成功！")
    else:
        print("压缩失败")
