import os
import shutil
from src.common.const import N2NGUI_VERSION
import PyInstaller.__main__

import zipfile


def compress_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历文件夹中的所有文件和子文件夹
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # 构建文件的绝对路径
                file_path = os.path.join(root, file)
                # 计算文件在 ZIP 文件中的相对路径
                relative_path = os.path.relpath(file_path, folder_path)
                # 将文件写入 ZIP 文件中
                zipf.write(file_path, arcname=relative_path)

# 源代码文件
worker_dir = os.getcwd()
source_file = 'main.py'
project_name = 'N2NGui'
package_dir = ".\\N2NGui"
zip_path = f".\\N2NGui_{N2NGUI_VERSION}.zip"
icon_file = ".\\statics\\icon_48.ico"

options = [
    '-n',
    project_name,
    '--icon={0}'.format(icon_file),
    # '--uac-admin',  # 以管理员运行
    '--onefile',  # 生成单个可执行文件
    '--noconsole',  # 不显示控制台窗口
    '--clean',  # 清理临时文件
]

# 使用 PyInstaller 编译脚本为可执行文件
PyInstaller.__main__.run([source_file] + options)

if os.path.exists(package_dir):
    shutil.rmtree(package_dir)
os.mkdir(package_dir)

# 拷贝文件
shutil.copytree("statics", os.path.join(package_dir, "statics"))
shutil.copytree("tools", os.path.join(package_dir, "tools"))
shutil.copy(os.path.join(".\\dist", f"{project_name}.exe"), package_dir)

# 压缩文件
compress_folder(package_dir, zip_path)

# 删除不需要的中间内容
delete_files = [
    package_dir,
    f'.\\{project_name}.spec',  # 生成的 .spec 文件
    '.\\build',  # 生成的 build 目录
    '.\\dist',  # 生成的 dist 目录
]

for file in delete_files:
    try:
        if os.path.isfile(file):
            os.remove(file)
            print(f'已删除文件：{file}')
        elif os.path.isdir(file):
            shutil.rmtree(file)
            print(f'已删除目录：{file}')
    except Exception as e:
        print(f'删除文件或目录 {file} 时发生错误：{str(e)}')
