cmake_minimum_required(VERSION 3.20)
project(Client C)

set(CMAKE_C_STANDARD 11)

include_directories(utils)

add_executable(Client utils/cJSON.h utils/cJSON.c utils/SockClient.h utils/SockString.h main.c)
