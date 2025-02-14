import subprocess

def run_sadtalker():
    # 定义需要执行的命令
    commands = [
        "F:",  # 切换到 F 盘
        "cd F:\\SadTalker\\SadTalker",  # 切换到 SadTalker 目录
        '"F:\\anaconda3\\envs\\sadtalker03\\python.exe" "F:\\SadTalker\\SadTalker\\inference.py" --driven_audio F:\\test_sadtalker\\audio.wav --source_image F:\\test_sadtalker\\Hang2.png --result_dir F:\\test_sadtalker --still --preprocess full --enhancer gfpgan'
    ]

    for cmd in commands:
        # 执行每个命令
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        # 打印命令的输出和错误信息
        print(f"Output of command '{cmd}':\n{stdout.decode()}")
        print(f"Error of command '{cmd}':\n{stderr.decode()}")
        
        if process.returncode != 0:
            print(f"Command '{cmd}' failed with return code {process.returncode}")
            break

if __name__ == "__main__":
    run_sadtalker()
