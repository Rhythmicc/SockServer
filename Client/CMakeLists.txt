cmake_minimum_required(VERSION 3.20)
project(Client C)

set(CMAKE_C_STANDARD 11)

include_directories(include)
aux_source_directory(src/ SRC)

add_executable(Client ${SRC})
