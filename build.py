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

import time
import argparse
import subprocess
from pathlib import Path

def format_time(seconds):
    minute, sec = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    if hour > 0:
        return "{}h{:02d}m{:02d.2f}s".format(hour, minute, sec)
    elif minute > 0:
        return "{}m{:02d.2f}s".format(minute, sec)
    else:
        return "{:.2f}s".format(sec)

def build(cc, cxx, args):
    command = ["cmake", "-GNinja", 
      "-B {}".format(args.build), 
      "-DCMAKE_C_COMPILER={}".format(cc), 
      "-DCMAKE_CXX_COMPILER={}".format(cxx), 
      "-DTARGET_ABI={}".format(args.arch),
      "-DCMAKE_BUILD_TYPE=Release"]
    
    if args.protoc is not None and len(str(args.protoc)) > 0:
        command.append("-DPROTOC_PATH={}".format(args.protoc))
    
    result = subprocess.run(command)
    start = time.time()
    if result.returncode == 0:
        if args.target == "all":
            result = subprocess.run(["ninja", "-C", args.build, "-j {}".format(args.job)])
        else:
            result = subprocess.run(["ninja", "-C", args.build, args.target, "-j {}".format(args.job)])

    if result.returncode == 0:
        end = time.time()
        print("\033[1;32mbuild success cost time: {}\033[0m".format(format_time(end - start)))

def configure(args):
    ndk = Path(args.ndk)
    if not ndk.exists() or not ndk.is_dir():
        raise ValueError("cannot find the ndk")

    toolchain = ndk / "toolchains/llvm/prebuilt/linux-x86_64"

    cc: Path = Path()
    cxx: Path = Path()

    if args.arch == "aarch64":
        cc = toolchain / "bin" / "aarch64-linux-android{}-clang".format(args.api)
        cxx = toolchain / "bin" / "aarch64-linux-android{}-clang++".format(args.api)
    elif args.arch == "arm":
        cc = toolchain / "bin" / "armv7a-linux-androideabi{}-clang".format(args.api)
        cxx = toolchain / "bin" / "armv7a-linux-androideabi{}-clang++".format(args.api)
    elif args.arch == "x86":
        cc = toolchain / "bin" / "i686-linux-android{}-clang".format(args.api)
        cxx = toolchain / "bin" / "i686-linux-android{}-clang++".format(args.api)
    else:
        cc = toolchain / "bin" / "x86_64-linux-android{}-clang".format(args.api)
        cxx = toolchain / "bin" / "x86_64-linux-android{}-clang++".format(args.api)
    
    print("cc is {}".format(cc))
    print("cxx is {}".format(cxx))
    
    if not cc.exists() or not cxx.exists():
        raise ValueError("error: cannot find the clang compiler")

    # start building
    build(str(cc), str(cxx), args)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--ndk", required=True, help="set the ndk toolchain path")

    parser.add_argument("--arch", choices=["aarch64", "arm", "x86", "x86_64"], 
      required=True, help="build for the specified architecture")
    
    parser.add_argument("--api", default=30, help="set android platform level, min api is 30")

    parser.add_argument("--build", default="build", help="the build directory")

    parser.add_argument("--job", default=16, help="run N jobs in parallel, default is 16")
    
    parser.add_argument("--target", default="all", help="build specified targets such as aapt2 adb fastboot, etc")
    
    parser.add_argument("--protoc", help="set the host protoc path")
    
    args = parser.parse_args()

    configure(args)

if __name__ == "__main__":
    main()
