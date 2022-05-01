Building platform-tools and build-tools for Android, such as `aapt aapt2 aidl zipalign adb fastboot` ... etc</br>

If you need other tools, please refer to existing tools to add CMake file

Currently only test the aarch64 architecture</br>

I haven't tested other architectures, so I can't guarantee it will work, although I have support for cross-compiling

 **** 
 
### How to build

Method one, download the `release/sdk-tools-source.zip` directly to compile, the source code has been patched

```bash
# arch [arm, aarch64, x86, x86_64]
python build.py \
    --ndk=/path/to/android-ndk-xxx \
    --arch aarch64 
    
# specify the output directory, default is build
python build.py \
    --ndk=/path/to/android-ndk-xxx \
    --arch aarch64 \
    --build build/aarch64
    
# specify the build target, such as aspt2 adb, etc
python build.py \
    --ndk=/path/to/android-ndk-xxx \
    --arch aarch64 \
    --build build/aarch64 \
    --target aapt2
    
# there are also some options, execute python build.py --help to see

```

 **** 
 
Method two, start from scratch，git clone the source code, then patch it manually</br>
Why patch it manually? the main reason is the aosp master branch is updated very quickly,
so the patch files may be incompatible

```bash

# clone the repository
git clone --depth=1 https://github.com/Lzhiyong/sdk-tools

cd sdk-tools

# download the source code
python get_source.py

# note that you need a host protoc before compilation for generating cpp files
# host protoc not target platform protoc
# how to get a host protoc
# cd src/protobuf, use host clang or gcc to compile it, you can get a host protoc
# why not use the system's protobuf? mainly the version incompatibility
# if the protobuf version is too new, you may encounter the following error
# error: this file was generated by a newer version of protoc
python build.py \
    --ndk=/path/to/android-ndk-xxx \
    --arch aarch64 \
    --build build/aarch64 \
    --protoc=/path/to/protoc
    
```

 **** 
 
