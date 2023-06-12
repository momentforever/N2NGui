import os
import shutil

import PyInstaller.__main__

# 源代码文件
source_file = 'main.py'
project_name = 'N2NGui'
package_dir = ".\\package"
icon_file = ".\\statics\\icon_48.ico"

# 编译选项
options = [
    '-n',
    project_name,
    '--icon={0}'.format(icon_file),
    '--uac-admin',  # 以管理员运行
    '--onefile',  # 生成单个可执行文件
    '--noconsole',  # 不显示控制台窗口
    '--clean',  # 清理临时文件
]

# 使用 PyInstaller 编译脚本为可执行文件
PyInstaller.__main__.run([source_file] + options)

if os.path.exists(package_dir):
    shutil.rmtree(package_dir)
os.mkdir(package_dir, mode=777)

shutil.copytree("statics", os.path.join(package_dir, "statics"))
shutil.copytree("n2n", os.path.join(package_dir, "n2n"))
shutil.copytree("tools", os.path.join(package_dir, "tools"))
shutil.copy(os.path.join(".\\dist", f"{project_name}.exe"), package_dir)

# 删除不需要的中间内容
delete_files = [
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
