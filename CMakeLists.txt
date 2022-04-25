cmake_minimum_required(VERSION 3.14.2)
project(sdk-tools)

enable_language(ASM)

# set global cflags and cxxflags
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fcolor-diagnostics -fPIC -Wno-attributes -std=gnu11")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fcolor-diagnostics -fPIC -Wno-attributes -std=gnu++2a")
# static link
set(CMAKE_EXE_LINKER_FLAGS "-static")

# platform tools version
# see the patches/other/platform_tools_version.h
set(TOOLS_VERSION 33.0.1)
set(SRC ${PROJECT_SOURCE_DIR}/src)

# 64-bit off_t for lseek.
add_definitions(-D_FILE_OFFSET_BITS=64)

# do not use the system's protobuf, as this may have incompatibilities
add_custom_target(aprotoc
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    DEPENDS protobuf::protoc
    COMMENT "generate the protoc executable file"
)

# thrid-party libraries
add_subdirectory(src/boringssl EXCLUDE_FROM_ALL)
add_subdirectory(src/fmtlib EXCLUDE_FROM_ALL)
add_subdirectory(src/pcre EXCLUDE_FROM_ALL)
add_subdirectory(src/libpng EXCLUDE_FROM_ALL)
add_subdirectory(src/expat EXCLUDE_FROM_ALL)
add_subdirectory(src/zopfli EXCLUDE_FROM_ALL)
add_subdirectory(src/jsoncpp EXCLUDE_FROM_ALL)
add_subdirectory(src/zstd/build/cmake EXCLUDE_FROM_ALL)
add_subdirectory(src/lz4/build/cmake EXCLUDE_FROM_ALL)
add_subdirectory(src/brotli EXCLUDE_FROM_ALL)
add_subdirectory(src/abseil-cpp EXCLUDE_FROM_ALL)
add_subdirectory(src/protobuf/cmake EXCLUDE_FROM_ALL)

# building sdk-tools
add_subdirectory(lib)
add_subdirectory(build-tools)
add_subdirectory(platform-tools)

# creating source tarballs
set(CPACK_PACKAGE_DIRECTORY ${PROJECT_SOURCE_DIR}/pack)
set(CPACK_RESOURCE_FILE_LICENSE "${PROJECT_SOURCE_DIR}/LICENSE.txt")
set(CPACK_SOURCE_GENERATOR "TXZ")
set(CPACK_SOURCE_PACKAGE_FILE_NAME "${PROJECT_NAME}-${TOOLS_VERSION}")
set(CPACK_SOURCE_IGNORE_FILES 
    ${PROJECT_SOURCE_DIR}/.git
    ${PROJECT_SOURCE_DIR}/.gitignore
    ${PROJECT_SOURCE_DIR}/.gitmodules
    ${PROJECT_SOURCE_DIR}/build
    ${PROJECT_SOURCE_DIR}/patches
    ${PROJECT_SOURCE_DIR}/pack
)
    
include(CPack)

