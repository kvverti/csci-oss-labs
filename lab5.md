## CMake Tutorial Part 1

CMakeLists:
```
cmake_minimum_required(VERSION 3.3)
project(Tutorial)
set(Tutorial_VERSION_MAJOR 1)
set(Tutorial_VERSION_MINOR 0)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# inject CMake settings into header file
configure_file(
  "${PROJECT_SOURCE_DIR}/TutorialConfig.h.in"
  "${PROJECT_BINARY_DIR}/TutorialConfig.h"
)

# add binary path to the search path
include_directories("${PROJECT_BINARY_DIR}")

add_executable(Tutorial tutorial.cxx)
```
Output:
```
neroc@DESKTOP-NRJLD6E:~/cmake/Tests/Tutorial/Step1$ ./Tutorial 4294967296
The square root of 4.29497e+09 is 65536
neroc@DESKTOP-NRJLD6E:~/cmake/Tests/Tutorial/Step1$ ./Tutorial 10
The square root of 10 is 3.16228
neroc@DESKTOP-NRJLD6E:~/cmake/Tests/Tutorial/Step1$ ./Tutorial
Version: 1.0
Usage: ./Tutorial number
```

### Part 2
CMake:
```
cmake_minimum_required(VERSION 3.3)
project(Tutorial)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# the version number.
set(Tutorial_VERSION_MAJOR 1)
set(Tutorial_VERSION_MINOR 0)

# configure a header file to pass some of the CMake settings
# to the source code
configure_file(
  "${PROJECT_SOURCE_DIR}/TutorialConfig.h.in"
  "${PROJECT_BINARY_DIR}/TutorialConfig.h"
  )

option(USE_MYMATH "Use tutorial provided math implementation" ON)

if(USE_MYMATH)
    add_subdirectory(MathFunctions)
    list(APPEND EXTRA_LIBS MathFunctions)
    list(APPEND EXTRA_INCLUDES "${PROJECT_SOURCE_DIR}/MathFunctions")
endif(USE_MYMATH)

# add the executable
add_executable(Tutorial tutorial.cxx)

target_link_libraries(Tutorial ${EXTRA_LIBS})

# add the binary tree to the search path for include files
# so that we will find TutorialConfig.h
target_include_directories(Tutorial PUBLIC
                           "${PROJECT_BINARY_DIR}"
                           "${EXTRA_INCLUDES}"
                           )
```
Output:
```
$ ./Tutorial 10
The square root of 10 is 3.16228
```

### Part 3
CMake:
```
add_library(MathFunctions mysqrt.cxx)
target_include_directories(MathFunctions INTERFACE ${CMAKE_CURRENT_SOURCE_DIR})
```

### Part 4
CMake:
```
cmake_minimum_required(VERSION 3.3)
project(Tutorial)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# should we use our own math functions
option(USE_MYMATH "Use tutorial provided math implementation" ON)

# the version number.
set(Tutorial_VERSION_MAJOR 1)
set(Tutorial_VERSION_MINOR 0)

# configure a header file to pass some of the CMake settings
# to the source code
configure_file(
  "${PROJECT_SOURCE_DIR}/TutorialConfig.h.in"
  "${PROJECT_BINARY_DIR}/TutorialConfig.h"
  )

# add the MathFunctions library?
if(USE_MYMATH)
  add_subdirectory(MathFunctions)
  list(APPEND EXTRA_LIBS MathFunctions)
endif(USE_MYMATH)

# add the executable
add_executable(Tutorial tutorial.cxx)

install(TARGETS Tutorial DESTINATION bin)
install(FILES "${PROJECT_BINARY_DIR}/TutorialConfig.h" DESTINATION include)

target_link_libraries(Tutorial PUBLIC ${EXTRA_LIBS})

# add the binary tree to the search path for include files
# so that we will find TutorialConfig.h
target_include_directories(Tutorial PUBLIC
                           "${PROJECT_BINARY_DIR}"
                           )
  # enable testing
  enable_testing()

  # does the application run
  add_test(NAME Runs COMMAND Tutorial 25)

  # does the usage message work?
  add_test(NAME Usage COMMAND Tutorial)
  set_tests_properties(Usage
    PROPERTIES PASS_REGULAR_EXPRESSION "Usage:.*number"
    )

  # define a function to simplify adding tests
  function(do_test target arg result)
    add_test(NAME Comp${arg} COMMAND ${target} ${arg})
    set_tests_properties(Comp${arg}
      PROPERTIES PASS_REGULAR_EXPRESSION ${result}
      )
  endfunction(do_test)

  # do a bunch of result based tests
  do_test(Tutorial 25 "25 is 5")
  do_test(Tutorial -25 "-25 is [-nan|nan|0]")
  do_test(Tutorial 0.0001 "0.0001 is 0.01")
```
Output:
```
Test project /home/neroc/cmake/Tests/Tutorial/Step4
  Test #1: Runs
  Test #2: Usage
  Test #3: Comp25
  Test #4: Comp-25
  Test #5: Comp0.0001

Total Tests: 5
```

Part 5:
CMake:
```
add_library(MathFunctions mysqrt.cxx)

# state that anybody linking to us needs to include the current source dir
# to find MathFunctions.h, while we don't.
target_include_directories(MathFunctions
          INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
          PRIVATE ${Tutorial_BINARY_CIR}
          )

install(TARGETS MathFunctions DESTINATION lib)
install(FILES MathFunctions.h DESTINATION include)
```
Output:
```
$ ./Tutorial 10
Computing sqrt of 10 to be 3.16228 using log
The square root of 10 is 3.16228
```

## Repo code

### Makefile
```
.RECIPEPREFIX = @

static: block.a program.o
@   cc -o static_block program.o block.a

dynamic: block.so program.o
@   cc -o dynamic_block program.o -L. -l:block.so -Wl,-rpath="."

block.so: source/block.c
@   cc -shared -fPIC -o block.so source/block.c

block.a: block.o
@   ar rcs block.a block.o

block.o: source/block.c headers/block.h
@   cc -c -Iheaders -o block.o source/block.c

program.o: program.c headers/block.h
@   cc -c -Iheaders -o program.o program.c
```

### CMakeLists.txt
```
cmake_minimum_required(VERSION 3.5)
project(LabExample)

include_directories("${PROJECT_BINARY_DIR}/headers")
include_directories("${PROJECT_BINARY_DIR}/source")

add_library(blocka STATIC source/block.c)
add_library(blocks SHARED source/block.c)

add_executable(dynamic_block program.c)
target_link_libraries(dynamic_block blocks)

add_executable(static_block program.c)
target_link_libraries(static_block blocka)
```

### CMake Generated Makefile
```
# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.5

# Default target executed when no arguments are given to make.
default_target: all

.PHONY : default_target

# Allow only one "make -f Makefile2" at a time, but pass parallelism.
.NOTPARALLEL:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/neroc/oss/Modules/BuildSystems/Lab-Example

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/neroc/oss/Modules/BuildSystems/Lab-Example/build

#=============================================================================
# Targets provided globally by CMake.

# Special rule for the target edit_cache
edit_cache:
        @$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --cyan "No interactive CMake dialog available..."
        /usr/bin/cmake -E echo No\ interactive\ CMake\ dialog\ available.
.PHONY : edit_cache

# Special rule for the target edit_cache
edit_cache/fast: edit_cache

.PHONY : edit_cache/fast

# Special rule for the target rebuild_cache
rebuild_cache:
        @$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --cyan "Running CMake to regenerate build system..."
        /usr/bin/cmake -H$(CMAKE_SOURCE_DIR) -B$(CMAKE_BINARY_DIR)
.PHONY : rebuild_cache

# Special rule for the target rebuild_cache
rebuild_cache/fast: rebuild_cache

.PHONY : rebuild_cache/fast

# The main all target
all: cmake_check_build_system
        $(CMAKE_COMMAND) -E cmake_progress_start /home/neroc/oss/Modules/BuildSystems/Lab-Example/build/CMakeFiles /home/neroc/oss/Modules/BuildSystems/Lab-Example/build/CMakeFiles/progress.marks
        $(MAKE) -f CMakeFiles/Makefile2 all
        $(CMAKE_COMMAND) -E cmake_progress_start /home/neroc/oss/Modules/BuildSystems/Lab-Example/build/CMakeFiles 0
.PHONY : all

# The main clean target
clean:
        $(MAKE) -f CMakeFiles/Makefile2 clean
.PHONY : clean

# The main clean target
clean/fast: clean

.PHONY : clean/fast

# Prepare targets for installation.
preinstall: all
        $(MAKE) -f CMakeFiles/Makefile2 preinstall
.PHONY : preinstall

# Prepare targets for installation.
preinstall/fast:
        $(MAKE) -f CMakeFiles/Makefile2 preinstall
.PHONY : preinstall/fast

# clear depends
depend:
        $(CMAKE_COMMAND) -H$(CMAKE_SOURCE_DIR) -B$(CMAKE_BINARY_DIR) --check-build-system CMakeFiles/Makefile.cmake 1
.PHONY : depend

#=============================================================================
# Target rules for targets named static_block

# Build rule for target.
static_block: cmake_check_build_system
        $(MAKE) -f CMakeFiles/Makefile2 static_block
.PHONY : static_block

# fast build rule for target.
static_block/fast:
        $(MAKE) -f CMakeFiles/static_block.dir/build.make CMakeFiles/static_block.dir/build
.PHONY : static_block/fast

#=============================================================================
# Target rules for targets named dynamic_block

# Build rule for target.
dynamic_block: cmake_check_build_system
        $(MAKE) -f CMakeFiles/Makefile2 dynamic_block
.PHONY : dynamic_block

# fast build rule for target.
dynamic_block/fast:
        $(MAKE) -f CMakeFiles/dynamic_block.dir/build.make CMakeFiles/dynamic_block.dir/build
.PHONY : dynamic_block/fast

#=============================================================================
# Target rules for targets named blocka

# Build rule for target.
blocka: cmake_check_build_system
        $(MAKE) -f CMakeFiles/Makefile2 blocka
.PHONY : blocka

# fast build rule for target.
blocka/fast:
        $(MAKE) -f CMakeFiles/blocka.dir/build.make CMakeFiles/blocka.dir/build
.PHONY : blocka/fast

#=============================================================================
# Target rules for targets named blocks

# Build rule for target.
blocks: cmake_check_build_system
        $(MAKE) -f CMakeFiles/Makefile2 blocks
.PHONY : blocks

# fast build rule for target.
blocks/fast:
        $(MAKE) -f CMakeFiles/blocks.dir/build.make CMakeFiles/blocks.dir/build
.PHONY : blocks/fast

program.o: program.c.o

.PHONY : program.o

# target to build an object file
program.c.o:
        $(MAKE) -f CMakeFiles/static_block.dir/build.make CMakeFiles/static_block.dir/program.c.o
        $(MAKE) -f CMakeFiles/dynamic_block.dir/build.make CMakeFiles/dynamic_block.dir/program.c.o
.PHONY : program.c.o

program.i: program.c.i

.PHONY : program.i

# target to preprocess a source file
program.c.i:
        $(MAKE) -f CMakeFiles/static_block.dir/build.make CMakeFiles/static_block.dir/program.c.i
        $(MAKE) -f CMakeFiles/dynamic_block.dir/build.make CMakeFiles/dynamic_block.dir/program.c.i
.PHONY : program.c.i

program.s: program.c.s

.PHONY : program.s

# target to generate assembly for a file
program.c.s:
        $(MAKE) -f CMakeFiles/static_block.dir/build.make CMakeFiles/static_block.dir/program.c.s
        $(MAKE) -f CMakeFiles/dynamic_block.dir/build.make CMakeFiles/dynamic_block.dir/program.c.s
.PHONY : program.c.s

source/block.o: source/block.c.o

.PHONY : source/block.o

# target to build an object file
source/block.c.o:
        $(MAKE) -f CMakeFiles/blocka.dir/build.make CMakeFiles/blocka.dir/source/block.c.o
        $(MAKE) -f CMakeFiles/blocks.dir/build.make CMakeFiles/blocks.dir/source/block.c.o
.PHONY : source/block.c.o

source/block.i: source/block.c.i

.PHONY : source/block.i

# target to preprocess a source file
source/block.c.i:
        $(MAKE) -f CMakeFiles/blocka.dir/build.make CMakeFiles/blocka.dir/source/block.c.i
        $(MAKE) -f CMakeFiles/blocks.dir/build.make CMakeFiles/blocks.dir/source/block.c.i
.PHONY : source/block.c.i

source/block.s: source/block.c.s

.PHONY : source/block.s

# target to generate assembly for a file
source/block.c.s:
        $(MAKE) -f CMakeFiles/blocka.dir/build.make CMakeFiles/blocka.dir/source/block.c.s
        $(MAKE) -f CMakeFiles/blocks.dir/build.make CMakeFiles/blocks.dir/source/block.c.s
.PHONY : source/block.c.s

# Help Target
help:
        @echo "The following are some of the valid targets for this Makefile:"
        @echo "... all (the default if no target is provided)"
        @echo "... clean"
        @echo "... depend"
        @echo "... static_block"
        @echo "... edit_cache"
        @echo "... dynamic_block"
        @echo "... blocka"
        @echo "... rebuild_cache"
        @echo "... blocks"
        @echo "... program.o"
        @echo "... program.i"
        @echo "... program.s"
        @echo "... source/block.o"
        @echo "... source/block.i"
        @echo "... source/block.s"
.PHONY : help



#=============================================================================
# Special targets to cleanup operation of make.

# Special rule to run CMake to check the build system integrity.
# No rule that depends on this can have commands that come from listfiles
# because they might be regenerated.
cmake_check_build_system:
        $(CMAKE_COMMAND) -H$(CMAKE_SOURCE_DIR) -B$(CMAKE_BINARY_DIR) --check-build-system CMakeFiles/Makefile.cmake 0
.PHONY : cmake_check_build_system
```

### Relative Sizes
```
... 8600 ... dynamic_block
... 8784 ... static_block
```
