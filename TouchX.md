# TouchX

This file contains information on how to setup the TouchX haptic device in both Linux and Windows. Additionally, it contains a brief introduction to the OpenHaptics API to use the TouchX on your projects.

## Setup the device



## OpenHaptics

OpenHaptics provides an API to read the commands from any haptic device and include them in any of your project. The main library for this is known as **HD** and **HDU**, which includes the data types to retieve the state of the device. Here is a simple explanation on how to use the OpenHaptics library in your project.

### Requirements

#### CMake

To include OpenHaptics in our projects we are going to use CMake to generate the configuration files for it. We are going to need CMake (<=3.1.0) to build the projects. In Ubuntu, open a terminal and type the following command to obtain the latest version of CMake.

```
$ sudo snap install cmake --classic
```

In Windows, download the latest available binary version from the official [CMake download webpage](https://cmake.org/download/). Execute the binary and follow the instructions for the installation.

#### VisualStudio (Windows)

In Windows, I recommend using VisualStudio to build the binaries of your project. Install the latest version from [VisualStudio download webpage](https://visualstudio.microsoft.com/downloads/).

### Including OpenHaptics in your own project

#### CMake File

I recommend using at least C++17 as it has more functionalities built in to manipulate system files. A minimal CMake file to include the OpenHaptics library can be found below.

```cmake
cmake_minimum_required(VERSION 3.1.0)
#set project
project(my_project)

#find openhaptics
find_path(OPENHAPTICS_INCLUDE_DIR NAMES HD/hd.h HL.hl.h HDU/hdu.h)

#check if openhaptics is available
if (NOT OPENHAPTICS_INCLUDE_DIR)
    set(OPENHAPTICS_MESSAGE "OPENHAPTICS was not found. You will not be able to use the Touch X")
    message(STATUS "${OPENHAPTICS_MESSAGE}")
    return()
endif(NOT OPENHAPTICS_INCLUDE_DIR)

#add the source files
aux_source_directory(${CMAKE_CURRENT_SOURCE_DIR}/src/ DIR_SRC)

#set properties
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

#add libraries
include directories(${OPENHAPTICS_INCLUDE_DIR})

#link the source files to an executable
add_executable(${PROJECT_NAME} ${DIR_SRCS})

#target OpenHaptics library
target_link_libraries(HD HDU HL)
```

To build the project in Linux open a terminal and type the following commands on the root directory of the project.
```
$ mkdir -p build && cd build
$ cmake ../ -DCMAKE_BUILD_TYPE=release && make
```

In Windows, open the CMake GUI and set your src directory to your root directory on the project and the build directory to the created *build* directory. Assign the **Release** build type and generate the solution. Find the Solution and use [VisualStudio](https://visualstudio.microsoft.com/) to build the executable.

#### Which files to include?
To read the encoders from the robot you need to include the header files from OpenHaptics include library.

```cpp
#include <HD/hd.h> // haptic device functions
// OpenHaptics data types libraries
#include <HDU/hduError.h>
#include <HDU/hduVector.h>
#include <HDU/hduMatrix.h>
#include <HDU/hduQuaternion.h>
```

### API functions

#### How to handle the data

This is my recommendation and how most of the people handle the data from the Haptic device to facilitate acess to data from different applications inside your project. Defining a data structure with all the information from the device its an interesting approach, here you have an example of how to build the structure and which data type to assign to each entrance.

```cpp
struct TouchState {
    hduVector3Dd position; // 3x1 vector of the position
    hduVector3Dd pre_position; // keep the previous position
    hduQuaternion rot; // quaternion expression of the tool rotation
    hduQuaternion pre_rot; // keep the previous rotation
    hduVector3Dd joints; // Joint position vector
    hduVector3Dd force; // 3 element force feedback
    int buttons[1]; // button state
    int buttons_prev[1]; // previous button state
}
```

#### Initialize device



#### Callback to update device state

