Building platform-tools and build-tools for Android, such as `aapt aapt2 aidl zipalign adb fastboot` ... etc</br>

If you need other tools, please refer to existing tools to add CMake file

Currently only test aarch64 architecture</br>

For other architectures you may need to refer to `Android.bp` to modify the corresponding CMake file

If you redownloaded the latest source from the master branch, patch files may be incompatible and you may encounter some new errors

Patch files are not universal since the master branch is updated very quickly

If necessary, you need to patch it by yourself

 **** 
 
### How to build

```bash

# clone the repository
git clone --depth=1 https://github.com/Lzhiyong/sdk-tools

cd sdk-tools

# download the source code
python get_source.py

# note that the above three commands are not necessary
# If you need the latest source code, it is necessary clone this repository and download the source code
# in most cases, you can download the release/sdk-tools-source.zip for direct compilation

mkdir build && cd build

# ==============start build.sh==============
# setup the ndk toolchain
NDK_TOOLCHAIN=/path/to/android-ndk-r24/toolchains/llvm/prebuilt/linux-x86_64

cmake -G 'Ninja' \
    -DCMAKE_C_COMPILER=$NDK_TOOLCHAIN/bin/aarch64-linux-android30-clang \
    -DCMAKE_CXX_COMPILER=$NDK_TOOLCHAIN/bin/aarch64-linux-android30-clang++ \
    -DCMAKE_SYSROOT=$NDK_TOOLCHAIN/sysroot \
    -DCMAKE_BUILD_TYPE=Release \
    ..
# ==============end build.sh===============

# generate the protoc file
ninja aprotoc

# please note that: 
# you need to execute the build.sh again
# use protoc to generate cpp files
bash build.sh

# start building
ninja -j16

```

 **** 
 
