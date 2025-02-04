import os
import shutil
import subprocess

# 设定 Chrome 浏览器原始路径以及新程序安装目录
chrome_src_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # 原始 Chrome 程序路径
chrome_dst_dir = "/Applications"  # 新程序将复制到的位置
base_user_data_dir = "/Users/vc/google_chrome"  # 用户数据目录的基路径
counter_file = "/Users/vc/google_chrome/chrome_instance_counter.txt"  # 存储当前实例编号的文件路径
sh_folder = os.path.join(base_user_data_dir, "sh")  # 启动脚本存放目录

# 确保 sh 文件夹存在
if not os.path.exists(sh_folder):
    os.makedirs(sh_folder)

def get_current_instance_number():
    """
    获取当前实例编号，文件不存在时返回 1
    """
    if os.path.exists(counter_file):
        with open(counter_file, "r") as f:
            try:
                return int(f.read().strip())  # 读取文件中的编号
            except ValueError:
                return 1  # 如果文件内容无效，则从1开始
    else:
        return 1  # 如果文件不存在，则从1开始


def update_instance_number(new_number):
    """
    更新实例编号到文件中
    """
    with open(counter_file, "w") as f:
        f.write(str(new_number))  # 更新文件中的实例编号


def copy_chrome_and_generate_script():
    """
    复制 Chrome 程序，并为每个实例创建一个新的用户数据目录，
    同时生成一个启动该实例的 .sh 脚本。
    """
    current_instance = get_current_instance_number()  # 获取当前实例编号

    if not os.path.exists(base_user_data_dir):
        os.makedirs(base_user_data_dir)  # 创建用户数据存储根目录

    # 复制 Chrome 浏览器程序并生成新实例
    while True:
        # 复制 Chrome 浏览器程序到新目录
        new_chrome_path = os.path.join(chrome_dst_dir, f"google{current_instance}.app")
        if os.path.exists(new_chrome_path):
            print(f"错误: {new_chrome_path} 已经存在！")
            current_instance += 1  # 增加实例编号，避免重名
            continue  # 继续循环，检查下一个编号
        else:
            shutil.copytree("/Applications/Google Chrome.app", new_chrome_path)  # 复制 Chrome 程序
            break  # 一旦成功复制，就跳出循环

    # 创建一个新的 user-data-dir 目录
    user_data_dir = os.path.join(base_user_data_dir, f"google{current_instance}")
    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir)

    # 生成启动脚本 .sh
    script_path = os.path.join(sh_folder, f"google{current_instance}_start.sh")
    with open(script_path, "w") as script_file:
        script_content = f"""#!/bin/bash
sudo "{new_chrome_path}/Contents/MacOS/Google Chrome" --user-data-dir="{user_data_dir}" --remote-debugging-port={9222 + current_instance} --incognito
"""
        script_file.write(script_content)

    # 修改脚本权限，使其可执行
    subprocess.run(["chmod", "+x", script_path])

    print(f"Chrome 实例 {current_instance} 已复制到: {new_chrome_path}")
    print(f"启动脚本已生成: {script_path}")

    # 更新实例编号
    update_instance_number(current_instance + 1)


if __name__ == "__main__":
    copy_chrome_and_generate_script()  # 生成一个新的 Chrome 实例
