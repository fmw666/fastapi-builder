# 仅在测试包时使用
# 在 fastapi-builder 根目录（即该文件上一级目录）运行

import os


if __name__ == "__main__":
    # 卸载
    os.system("pip uninstall fastapi-builder")

    # 打包文件所在路径
    dist_path = "dist/"

    # 删除 dist 目录下打包文件
    try:
        for fname in os.listdir(dist_path):
            if fname.endswith(".whl"):
                os.remove(os.path.join(dist_path, fname))
                break
    except FileNotFoundError:
        pass

    # 打包并安装
    os.system("python ./setup.py bdist_wheel")
    for fname in os.listdir(dist_path):
        if fname.endswith(".whl"):
            file_path = os.path.join(dist_path, fname)
            os.system(f"pip install {file_path}")
            break
