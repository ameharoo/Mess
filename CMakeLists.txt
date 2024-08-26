cmake_minimum_required(VERSION 3.20)


if (NOT DEFINED MESS_DIRECTORY)
    set(MESS_DIRECTORY ${CMAKE_SOURCE_DIR})
endif()

if (NOT DEFINED MESS_BACKEND)
    set(MESS_BACKEND "cpp")
endif()

find_package (Python3 COMPONENTS Interpreter)
execute_process (COMMAND "${Python3_EXECUTABLE}" -m venv "${MESS_DIRECTORY}/.venv")

# Here is the trick
## update the environment with VIRTUAL_ENV variable (mimic the activate script)
set (ENV{VIRTUAL_ENV} "${MESS_DIRECTORY}/.venv")
## change the context of the search
set (Python3_FIND_VIRTUALENV FIRST)
## unset Python3_EXECUTABLE because it is also an input variable (see documentation, Artifacts Specification section)
unset (Python3_EXECUTABLE)
## Launch a new search  
find_package (Python3 COMPONENTS Interpreter)

# Install requirements
execute_process(COMMAND "${Python3_EXECUTABLE}" -m pip install --upgrade pip)
execute_process(COMMAND "${Python3_EXECUTABLE}" -m pip install -r "${MESS_DIRECTORY}/requirements.txt")

if (DEFINED ESP_PLATFORM)
    if(DEFINED MESS_TARGET)
        message("[Mess]: Setting up as Esp Include Cmake")

        add_custom_command(OUTPUT "${MESS_TARGET}"
                DEPENDS "${MESS_SOURCE}"
                PRE_LINK
                COMMAND "${Python3_EXECUTABLE}"
                "${MESS_DIRECTORY}/mess.py"
                "${MESS_BACKEND}"
                "${MESS_TARGET}" "${MESS_SOURCE}"
                WORKING_DIRECTORY
                "${MESS_DIRECTORY}")

        add_custom_target(Mess DEPENDS "${MESS_TARGET}")
        add_dependencies(${COMPONENT_LIB} Mess)

        set_property(DIRECTORY "${COMPONENT_DIR}" APPEND PROPERTY
                ADDITIONAL_CLEAN_FILES "${MESS_TARGET}")

        unset(MESS_TARGET)
    else()
        message("[Mess]: Idf.py bypass")
    endif ()

else()
    add_custom_target("mess")

    if (Python3_FOUND)
        add_custom_command(OUTPUT "${MESS_TARGET}"
            DEPENDS 
                "${MESS_SOURCE}"
            PRE_LINK
            COMMAND
               "${Python3_EXECUTABLE}" "${MESS_DIRECTORY}/mess.py"
                "${MESS_BACKEND}" "${MESS_TARGET}" "${MESS_SOURCE}"
            # OUTPUT
            #    ${MESS_TARGET}
            WORKING_DIRECTORY
                "${CMAKE_SOURCE_DIR}"       
            COMMENT
                "Mess make a magic now"
        )
    else()
        message(FATAL_ERROR "Not found python for Mess")
    endif()
endif ()