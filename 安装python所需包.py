import subprocess
import sys

# 定义要安装的包列表
#packages = ["requests", "numpy", "pandas"]

# 定义要安装的包列表
packages = ["moviepy"]

# 安装每个包
for package in packages:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
