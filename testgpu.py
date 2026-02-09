import torch
import paddle

print("------ 显卡检测报告 ------")

# 1. 检查 PyTorch (LaMa 用)
print(f"PyTorch 版本: {torch.__version__}")
if torch.cuda.is_available():
    print(f"✅ PyTorch GPU: 可用! ({torch.cuda.get_device_name(0)})")
else:
    print("❌ PyTorch GPU: 不可用 (依然是 CPU)")

print("-" * 20)

# 2. 检查 Paddle (OCR 用)
print(f"Paddle 版本: {paddle.__version__}")
if paddle.device.is_compiled_with_cuda():
    print(f"✅ Paddle GPU: 可用!")
else:
    print("❌ Paddle GPU: 不可用")

print("------------------------")