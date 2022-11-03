# 仅在测试包时使用

import os


if __name__ == "__main__":
    # 卸载
    os.system("pip uninstall fastapi-builder")
    
    # 删除 dist 目录下打包文件
    try:
        for fname in os.listdir("./dist"):
            if fname.endswith(".whl"):
                os.remove(".\dist\\" + fname)
                break
    except:
        pass

    # 打包并安装
    os.system("python .\setup.py bdist_wheel")
    for fname in os.listdir("./dist"):
        if fname.endswith(".whl"):
            os.system("pip install .\dist\\" + fname)
            break
