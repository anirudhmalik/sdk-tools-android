add_executable(split-select
    ${SRC}/base/tools/split-select/Abi.cpp
    ${SRC}/base/tools/split-select/Grouper.cpp
    ${SRC}/base/tools/split-select/Rule.cpp
    ${SRC}/base/tools/split-select/RuleGenerator.cpp
    ${SRC}/base/tools/split-select/SplitDescription.cpp
    ${SRC}/base/tools/split-select/SplitSelector.cpp
    ${SRC}/base/tools/split-select/Main.cpp
)

target_compile_definitions(split-select PRIVATE 
    -D_DARWIN_UNLIMITED_STREAMS
)
target_include_directories(split-select PRIVATE
    ${SRC}/base/libs/androidfw/include
    ${SRC}/core/libutils/include
    ${SRC}/logging/liblog/include
    ${SRC}/core/libsystem/include
    ${SRC}/libbase/include
    ${SRC}/fmtlib/include
    ${SRC}/base/tools
    ${SRC}/incremental_delivery/incfs/util/include 
)
    
target_link_libraries(split-select
    libaapt
    libandroidfw
    libselinux
    libsepol
    libutils
    libcutils
    libincfs
    libbase
    libziparchive
    libpackagelistparser
    libprocessgroup
    liblog
    expat
    crypto
    jsoncpp_static
    png_static
    pcre2-8
    c++_static
    dl
    z
)
    