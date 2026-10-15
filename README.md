# WindowsAi

> 一个想让电脑「像人一样自己干活」的 AI —— 作者 XinMatrix（YOUR_NAME）的失败项目归档。

这是我在大三（2024 年）做的一个方向：不让程序员一行行写代码，而是让程序学会**自己看屏幕、点鼠标、敲键盘**，像一个人那样把活儿干完——比如替用户一键配好开发环境、处理 Excel、改图、剪视频。当时大模型还不会自己看屏幕、点按钮，我想抢在前面做一个。

**结果：没做成，卖不出去，0 收入。** 死因有两条：① 没有壁垒——后来大模型能力一上来，「AI 自己操作电脑」被做成了模型内建能力，我再用截图识别+模拟点击去拼就没有优势；② 付费点始终没想明白，技术铺了一大摊，没人为此付过一分钱。

按照我「无论成败全部公开」的原则，把源码原样（含当时引用的第三方 OCR 框架）开源在这里，供学习、参考、考古。配套的失败复盘在 [xinmatrix.top 台账](https://xinmatrix.top/#/ledger/grave-windows-ai)。

---

## 目录结构（四个版本的演进）

| 目录 | 说明 |
|---|---|
| `1_WindowsAiCloud/` | 云端版 WindowsAI Cloud / WindowsAi Magic：识别与决策放服务器，客户端很薄，靠网络来回传 |
| `2_WindowsAiLocal/` | 本地版 WindowsAi Local / 蓝鲸定制版：整套能力塞进用户电脑，用 CPU 跑、不依赖网络，可双击运行 |
| `3_Res/` | 资源与样例（YOLOv8 样例工程源码） |
| `5_Yolov8/` | YOLOv8 界面元素识别模型的训练代码与工程 |
| `6_OtherFiles/` | 零散资料 |
| `7_WindowsAiLocal_SWBZ/` | 本地版的一个延伸变体（含自动化流程） |

> 子目录里保留了当时的 `README.md` / `PROJECT_INFO.md` / `PROJECT_TODO.md`，是原始开发记录，未做润色。

---

## 它是怎么干活的（核心思路）

1. **「眼睛」**：用 PaddleOCR 识别屏幕上的文字、用 YOLOv8 自训模型识别界面按钮/图标位置；
2. **「手」**：拿到坐标后模拟鼠标点击、键盘输入、窗口操作；
3. **「脑」**：把「装软件、配环境、处理 Office/视频」这类流程写成可复用的自动化步骤；
4. **聊天版 Magic**：不走「录流程自动跑」，改成「跟 AI 说一句话，它去截图识别+模拟点击落地」。

---

## 获取模型权重 / 二进制依赖（本仓库未纳入）

因为 GitHub 对单文件有 **100MB** 的硬限制，下面这些二进制没有进仓库，需要你自行准备：

- **YOLOv8 权重**（`*.pt` / `*.onnx`）：从 [Ultralytics](https://github.com/ultralytics/ultralytics) 下载预训练权重，或按 `5_Yolov8/` 里的训练代码自己训；
- **PaddleOCR 运行环境**：本仓库**未包含** Baidu 的 PaddleOCR 源码（体积过大，已排除）；`1_WindowsAiCloud/MyOCR` 里保留的是作者自己的 MyOCR 封装层。运行时请按官方文档另行安装 PaddlePaddle + PaddleOCR，再跑本仓库代码；
- **ffmpeg**：视频相关功能需要 ffmpeg，请自行从 [ffmpeg.org](https://ffmpeg.org) 安装并加入 PATH；
- **演示视频 / 空镜素材**（`*.mp4`）：属于演示录屏，不影响代码阅读，未纳入。

---

## 依赖（大致）

不同子目录的年代和写法不一样，下面是主干依赖，具体以各目录 README / requirements 为准：

- Python 3.8+
- `opencv-python`、`numpy`、`pyautogui`（模拟键鼠）、`Pillow`
- `paddleocr` / `paddlepaddle`（屏幕文字识别）
- `ultralytics`（YOLOv8 界面元素识别）
- `openai`（聊天版 Magic 调用大模型，需要你自己的 API Key）
- `pyinstaller` + `pyarmor`（打包成可双击运行的独立程序）

> ⚠️ 代码里涉及 API Key、个人路径、联系方式的位置**已做脱敏处理**（统一替换为 `YOUR_OPENAI_API_KEY` / `C:\Users\USER` / `YOUR_PHONE` / `YOUR_NAME` / `YOUR_EMAIL` 等占位符）。运行前请替换成你自己的配置，**切勿把真实密钥提交回本仓库**。

---

## 许可证

[MIT](./LICENSE) —— 随便看、随便学、随便改，作者不对可用性负责，风险自负。

---

## 相关链接

- 作者官网 / 公开台账：[xinmatrix.top](https://xinmatrix.top)
- 本项目复盘：[xinmatrix.top/#/ledger/grave-windows-ai](https://xinmatrix.top/#/ledger/grave-windows-ai)
- 另一个已开源的做成的项目（TODOL 悬浮窗记事 App）：[github.com/XinMatrix/pub-todol](https://github.com/XinMatrix/pub-todol)
