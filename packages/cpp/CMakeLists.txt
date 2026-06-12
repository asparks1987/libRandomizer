cmake_minimum_required(VERSION 3.16)
project(librandomizer_cpp VERSION 0.1.0 LANGUAGES CXX)

add_library(librandomizer_cpp INTERFACE)
target_include_directories(librandomizer_cpp INTERFACE include)
target_compile_features(librandomizer_cpp INTERFACE cxx_std_17)

if(WIN32)
  target_link_libraries(librandomizer_cpp INTERFACE bcrypt)
endif()

add_executable(librandomizer_cpp_smoke tests/smoke.cpp)
target_link_libraries(librandomizer_cpp_smoke PRIVATE librandomizer_cpp)
