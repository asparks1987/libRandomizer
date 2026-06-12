cmake_minimum_required(VERSION 3.16)
project(librandomizer_c VERSION 0.1.0 LANGUAGES C)

add_library(librandomizer_c src/librandom.c)
target_include_directories(librandomizer_c PUBLIC include)

if(WIN32)
  target_link_libraries(librandomizer_c PRIVATE bcrypt)
endif()
