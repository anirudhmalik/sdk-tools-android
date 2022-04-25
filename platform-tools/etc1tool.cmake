add_executable(etc1tool 
    ${SRC}/etc1tool/etc1tool.cpp
    ${SRC}/native/opengl/libs/ETC1/etc1.cpp
)
target_include_directories(etc1tool PRIVATE
    ${SRC}/libpng
    ${SRC}/native/opengl/include
)
target_link_libraries(etc1tool png_static c++_static dl z)
