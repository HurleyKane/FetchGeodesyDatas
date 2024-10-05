# 该库对C++进行
# 安装 python setup.py bdist_wheel
# pip install dist/InSARlib-0.0.5-py3-none-any.whl
import os, platform, sys
from datetime import datetime
import setuptools
from setuptools.command.install import install

VERSION = '0.0.0'

"""******************************设置包名*************************************"""
# 动态生成包名
package_name = f"FetchLib"

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        print(
            "\nIMPORTANT: This package requires OpenCV, which cannot be installed via pip.\n"
            "Please install OpenCV using conda with the following command:\n"
            "    conda install -c conda-forge opencv\n"
        )

setuptools.setup(
    name=package_name,
    version=VERSION,  # 两个地方都可以
    description="这是一个爬取geodesy数据的库",
    author="chenmingkai",
    author_email="<EMAIL>",
    url="https://github.com/hurleykane/InSAR3DDeformation",
    packages=setuptools.find_packages("."), # 自动找
    install_requires=[
        "selenium == 4.25.0",
        "webdriver_manager == 4.0.2",
        "pandas"
    ],
    classifiers = [
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]

)