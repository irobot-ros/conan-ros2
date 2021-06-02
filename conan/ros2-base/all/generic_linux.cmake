set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_VERSION 1)

# Specify the target file system
set(CMAKE_SYSROOT $ENV{SYSROOT})

# Compiler flags
set(CMAKE_C_FLAGS "$ENV{CMAKE_C_FLAGS} $ENV{CFLAGS}" CACHE STRING "" FORCE)
set(CMAKE_CXX_FLAGS "$ENV{CMAKE_CXX_FLAGS} $ENV{CXXFLAGS}" CACHE STRING "" FORCE)

# Where is the target environment
set(CMAKE_FIND_ROOT_PATH $ENV{ROS2_CONAN_WORKSPACE})
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

# This assumes that pthread will be available on the target system
# (this emulates that the return of the TRY_RUN is a return code "0")
set(THREADS_PTHREAD_ARG "0"
    CACHE STRING "Result from TRY_RUN" FORCE)
