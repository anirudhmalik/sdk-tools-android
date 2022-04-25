add_executable(dmtracedump 
    ${SRC}/art/tools/dmtracedump/tracedump.cc
)
target_link_libraries(dmtracedump c++_static dl z)
