cmake_minimum_required(VERSION 3.24)
set(CMAKE_CXX_STANDARD 23)

# Low-Level API Testing CMake Target
project(cpp_ll_api_test)

# Include Mess and create target
set(MESS_CPP_HIGHLEVEL_API 1)
set(MESS_DIRECTORY "${CMAKE_SOURCE_DIR}/../..")
set(MESS_SOURCE "${CMAKE_SOURCE_DIR}/messages/test.ini")
set(MESS_TARGET "${CMAKE_SOURCE_DIR}/messages/test_protocol.h")

include(${MESS_DIRECTORY}/CMakeLists.txt)

# Enable testing and includes googletest
enable_testing()
add_subdirectory(googletest)

# Add executable
add_executable(cpp_ll_api_test  main.cpp
                                lowlevel/builtins.cpp
                                lowlevel/vararrays.cpp
                                lowlevel/complex.cpp
                                ${MESS_TARGET})
target_link_libraries(cpp_ll_api_test gtest_main gmock_main pthread)
add_dependencies(cpp_ll_api_test mess)

# Add Mess target directory as include dir
target_include_directories(cpp_ll_api_test PRIVATE "messages/")