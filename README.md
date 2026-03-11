# ConvertPPT

将图片型 `PDF`、图片型 `PPT/PPTX` 转成可继续编辑的 `PPTX`。

项目当前基于 `PaddleOCR + python-pptx + OpenCV` 运行，默认适配 `Anaconda + CPU` 环境；如果本机 `Torch/LaMa` 可用，也可以手动开启 LaMa 修复模式。

## 功能概览

- 支持输入：`PDF`、`PPT`、`PPTX`
- 支持输出：可编辑的 `PPTX`
- 自动 OCR 提取文本并重建文本框
- 自动清理图片中的水印区域与文本遮挡区域
- 默认使用 `OpenCV` 做图像修复，避免 `Torch` 环境问题导致程序无法启动
- 支持 GUI、CLI、脚本三种入口

## 当前项目结构

```text
converter_core.py   核心转换逻辑
ui.py               Tkinter 图形界面入口
ppt2ppt.py          命令行入口
main2.py            简单示例入口
ui.spec             PyInstaller 打包配置
requirements.txt    Python 依赖
```

## 运行环境

推荐环境：

- Windows
- Python 3.9+
- Anaconda / Miniconda
- CPU 模式即可运行

核心依赖见 `requirements.txt`，当前代码默认优先保证：

- `paddleocr`
- `paddlepaddle`
- `python-pptx`
- `opencv-python`
- `pdf2image`
- `Pillow`
- `numpy<2`

## 安装

### 1. 安装 Python 依赖

在项目目录执行：

```powershell
python -m pip install -r requirements.txt
```

如果你使用的是 Anaconda，也可以先激活自己的环境再安装：

```powershell
conda activate your-env
python -m pip install -r requirements.txt
```

### 2. 安装 Poppler

处理 `PDF` 时需要 `Poppler`。

程序会按以下顺序寻找 `Poppler`：

1. 系统环境变量中的 `pdftoppm`
2. 代码里的 `POPPLER_PATH`
3. 项目目录下的：
   - `poppler/Library/bin`
   - `poppler/bin`

如果没有安装 `Poppler`，转换 PDF 时会报错：

```text
PDF conversion requires Poppler. Please install Poppler or set POPPLER_PATH.
```

## 怎么运行

### GUI

最简单的方式：

```powershell
python ui.py
```

界面支持：

- 选择输入文件
- 自动生成输出名
- 显示运行日志
- 弹窗提示成功或失败

默认输出文件名格式：

```text
原文件名_AI_REPAIRED.pptx
```

### 命令行

```powershell
python ppt2ppt.py input.pdf
python ppt2ppt.py input.pptx
python ppt2ppt.py input.pdf output.pptx
```

### 示例脚本

如果你只是想快速试一下，可以先把输入文件放在项目目录，再运行：

```powershell
python main2.py
```

`main2.py` 默认读取：

- 输入：`test.pdf`
- 输出：`final_clean_kmeans.pptx`

## 当前默认行为

### 图像修复后端

当前代码默认使用 `OpenCV` 修复图片，不强依赖 `Torch`：

- 这样在 `Anaconda base` 或 `Torch DLL` 有问题时，`ui.py` 仍然可以正常启动
- 如果后续你修好了 `Torch + simple-lama-inpainting`，可以手动启用 LaMa

PowerShell 下启用 LaMa：

```powershell
$env:CONVERTPPT_USE_LAMA='1'
python ui.py
```

如果没有设置这个环境变量，程序会保持 OpenCV 模式。

### OCR 模式

程序默认：

- 使用 CPU
- 启用角度分类
- 使用较保守的 PaddleOCR 参数
- 在 OCR 结果为空时，会自动尝试缩放图像后重试一次

## 支持的输入说明

### PDF

- 每页会先转成图片
- 再做 OCR、背景清理、文本框重建
- 输出为整份可编辑 PPTX

### PPT / PPTX

- 当前主要处理幻灯片中的图片形状
- 原有文本形状不会主动重写
- 适合“整页是截图 / 导出的图片型幻灯片”的场景

## 常见问题

### 1. `ui.py` 启动时报 Torch DLL 错误

如果你遇到类似：

```text
Error loading ... torch\lib\shm.dll
```

现在代码会自动回退到 `OpenCV`，一般不影响程序启动。

### 2. 转换 PDF 时提示缺少 Poppler

请先安装 `Poppler`，并确保：

- `pdftoppm` 已加入系统 `PATH`
- 或手动设置 `POPPLER_PATH`

### 3. 识别结果不够理想

可以尝试：

- 提高原始 PDF / 图片清晰度
- 调整 `converter_core.py` 中的 `SCAN_DPI`
- 调整 `WATERMARK_KEYWORDS`
- 调整 `FORCED_ERASE_REGIONS`

## 打包

如果你要生成可执行文件：

```powershell
pyinstaller ui.spec
```

建议不要把 `build/`、`dist/` 产物提交到 Git 仓库。

## 开发说明

当前主要入口：

- `converter_core.py`：核心处理逻辑
- `ui.py`：桌面界面
- `ppt2ppt.py`：命令行

如果你要继续整理项目，建议优先做：

- 增加配置文件而不是直接改常量
- 增加日志级别控制
- 为核心转换逻辑补一组小样本测试

## License

本项目主要用于学习、实验和个人工作流整理，请按相关依赖库协议使用。
