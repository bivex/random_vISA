cmake_minimum_required(VERSION 3.16)
project(RVV_Custom_ISA_emulator CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -Wall -Wextra")

add_executable(visa_test_runner
    main.cpp
    instructions.cpp
)

target_include_directories(visa_test_runner PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})