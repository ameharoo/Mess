cmake_minimum_required(VERSION 3.2)

find_package(PythonInterp)
find_package(Python)


add_custom_target("mess")

if (PYTHON_FOUND)
    add_custom_command(TARGET "mess"
        COMMAND
           ${PYTHON_EXECUTABLE} ${MESS_DIRECTORY}/mess.py ${CMAKE_SOURCE_DIR}/${MESS_TARGET} ${CMAKE_SOURCE_DIR}/${MESS_SOURCE}
#         OUTPUT
#            ${MESS_TARGET}
        WORKING_DIRECTORY
            ${MESS_DIRECTORY}
        COMMENT
            "Mess make a magic now"
    )
endif()