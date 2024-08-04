cmake_minimum_required(VERSION 3.24)
project(cpp_example)

set(CMAKE_CXX_STANDARD 17)

set(MESS_DIRECTORY "${CMAKE_SOURCE_DIR}/../..")
set(MESS_SOURCE "test_message.ini")
set(MESS_TARGET "test_message.h")
    
include(${MESS_DIRECTORY}/CMakeLists.txt)


add_executable(cpp_example main.cpp ${MESS_TARGET})
add_dependencies(cpp_example mess)