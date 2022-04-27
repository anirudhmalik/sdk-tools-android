#!/usr/bin/env python
#
# Copyright © 2022 Github Lzhiyong
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# pylint: disable=not-callable, line-too-long, no-else-return

import os
import requests
import tarfile
import shutil
import subprocess
from pathlib import Path


def untar(source, target):
    tar = tarfile.open(source)
    names = tar.getnames()
    if os.path.isdir(target):
        pass
    else:
        os.mkdir(target)

    for name in names:
        tar.extract(name, target)
    tar.close()

def download(url, filename, target):
    print("downloading {}".format(filename))
    content = requests.get(url).content
    with open(filename, 'wb') as file:
        file.write(content)
    # extract tar file
    print("extracting {} to {}".format(filename, target))
    untar(filename, target)
    # delete file
    if os.path.exists(filename):
        os.remove(filename)

def patch():
    inc = Path(os.getcwd() + "/src/incremental_delivery/sysprop/include")
    if not inc.exists():
        inc.mkdir()
    shutil.copy2(Path("patches/other/IncrementalProperties.sysprop.h"), inc)
    shutil.copy2(Path("patches/other/IncrementalProperties.sysprop.cpp"), inc.parent)

    shutil.copy2(Path("patches/other/deployagent.inc"), Path("src/adb/fastdeploy/deployagent"))
    shutil.copy2(Path("patches/other/deployagentscript.inc"), Path("src/adb/fastdeploy/deployagent"))

    shutil.copy2(Path("patches/other/platform_tools_version.h"), Path("src/libbuildversion/include"))

def check(command):
    try:
        output = subprocess.check_output("command -v {}".format(command), shell=True)
        print(output.decode("utf-8"))
    except subprocess.CalledProcessError as e:
        print("please install the {} package".format(command))
        exit()


def main():
    # check git
    check("git")
    # branch android-mainline-12.0.0_r32
    # libziparchive
    url = "https://android.googlesource.com/platform/system/libziparchive/+archive/a0b94e44142022e8b6ba86c3dc84b9f2594f9f98.tar.gz"
    download(url, os.path.basename(url), "src/libziparchive")

    # zipalign
    url = "https://android.googlesource.com/platform/build.git/+archive/refs/tags/android-mainline-12.0.0_r32/tools/zipalign.tar.gz"
    download(url, os.path.basename(url), "src/zipalign")

    # etc1tool
    url = "https://android.googlesource.com/platform/development/+archive/refs/tags/android-mainline-12.0.0_r32/tools/etc1tool.tar.gz"
    download(url, os.path.basename(url), "src/etc1tool")

    # libbuildversion
    url = "https://android.googlesource.com/platform/build/soong/+archive/refs/tags/android-mainline-12.0.0_r32/cc/libbuildversion.tar.gz"
    download(url, os.path.basename(url), "src/libbuildversion")

    # git clone submodules
    os.system("git submodule update --depth=1 --init --recursive")
    os.system("git submodule update --depth=1 --remote")
    
    # patch files
    patch()
    
    # check golang
    check("go")
    
    print("download success!!")

if __name__ == "__main__":
    main()
 