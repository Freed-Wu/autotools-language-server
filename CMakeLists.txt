cmake_minimum_required(VERSION 3.10)
include(FetchContent)
FetchContent_Declare(
  tree-sitter-make
  GIT_REPOSITORY "https://github.com/alemuller/tree-sitter-make"
  GIT_TAG main)
FetchContent_MakeAvailable(tree-sitter-make)
include_directories(${tree-sitter-make_SOURCE_DIR}/src)
add_library(parser SHARED ${tree-sitter-make_SOURCE_DIR}/src/parser.c)
if(NOT DEFINED SKBUILD_PLATLIB_DIR)
  set(SKBUILD_PLATLIB_DIR ${CMAKE_SOURCE_DIR}/src)
endif()
set(CMAKE_INSTALL_LIBDIR ${SKBUILD_PLATLIB_DIR}/autotools_language_server/data/lib)
install(TARGETS parser RUNTIME)
