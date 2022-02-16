import os
import shutil


# 删除 CliRunner isolated_filesystem 生成的随机目录
def rm_tmp_dir(path: str):
    for fname in os.listdir(path):
        if len(fname) == 11 and fname.startswith("tmp"):
            shutil.rmtree(fname)
