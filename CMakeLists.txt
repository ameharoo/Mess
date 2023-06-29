cmake_minimum_required(VERSION 3.2)

find_package(PythonInterp)
find_package(Python)

if (DEFINED ESP_PLATFORM)
    if(DEFINED MESS_TARGET)
        message("[Mess]: Setting up as Esp Include Cmake")

        add_custom_command(OUTPUT "${MESS_TARGET}"
                DEPENDS "${MESS_SOURCE}"
                PRE_LINK
                COMMAND "${python}"
                "${MESS_DIRECTORY}/mess.py"
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

    if (PYTHON_FOUND)
        add_custom_command(TARGET "mess"
            COMMAND
               ${PYTHON_EXECUTABLE} ${MESS_DIRECTORY}/mess.py ${MESS_TARGET} ${MESS_SOURCE}
    #         OUTPUT
    #            ${MESS_TARGET}
            WORKING_DIRECTORY
                ${MESS_DIRECTORY}
            COMMENT
                "Mess make a magic now"
        )
    endif()
endif ()