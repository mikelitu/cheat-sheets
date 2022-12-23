# TouchX-OpenHaptics

This file contains a brief introduction to the OpenHaptics API to use the TouchX on your projects.

## Install OpenHaptics and setup the device

To set up the TouchX device from [3DSystems](https://www.3dsystems.com/), we will need two different things [OpenHaptics](https://www.3dsystems.com/haptics-devices/openhaptics) and the Touch X device drivers.

### Ubuntu (Focal 20.04)

The installer from the latest version of OpenHaptics for Ubuntu 20.04 can be found in this [link](https://support.3dsystems.com/s/article/OpenHaptics-for-Linux-Developer-Edition-v34?language=en_US). Download the compressed file and run the following commands on the terminal.

```
$ cd /path/to/file
$ tar -zvxf openhaptics_3.4-0-developer-edition-amd64.tar.gz
$ cd openhaptics_3.4-0-developer-edition-amd64
$ sudo ./install
```

This is a short explanation for the code:

> 1. Change to the file directory
> 1. Extract the file and change to the newly extracted directory
> 1. Install OpenHaptics via the install file

The PC will automatically reboot after the installation. Check that *OpenHaptics* is installed into */opt/OpenHaptics*.

Now, we need to install the drivers for the TouchX device. For Linux you can find them on the same webpage as [OpenHaptics](https://support.3dsystems.com/s/article/OpenHaptics-for-Linux-Developer-Edition-v34?language=en_US). Download the files and copy the following commands on the terminal.

```
$ sudo apt-get update
$ sudo apt-get install qt5-default
$ cd /path/to/file
$ tar -zvxf TouchDriver2022_04_04.tar.gz
$ cd TouchDriver2022_04_04
$ sudo cp ./usr/lib/LibPhantomIOLib42.so /usr/lib/
```

Now you can connect the TouchX via the USB port. First, run the command:
```
bash ListUSBHapticDevices
```
This should print the connected device with the following COM name */dev/ttyACM\** where * is any number. To grant permissions to the COM port you could run either

```
$ sudo chmod 777 /dev/ttyACM*
```
or
```
$ sudo adduser YourUserName dialout
```

I recommend using the second as it will grant privilege to every COM port you connect and you do not need to run the command more times even if you log out or reboot the system.

Before finishing with the setup of the device we are going to add a new variable to the environment to let the script know where we want to save the configuration files.

```
$ echo "export GSTDD_HOME = /home/user/.3dsystems" >> ~/.bashrc
```

Now finish the setup running the *./bin/Touch_Setup* and apply and save the necessary changes. I recommend keeping the name to **Default Device** if we only are connecting a single TouchX. You can calibrate the system using the script *./bin/Touch_Diagnostics*.

For a more detailed setup guide click [here](https://s3.amazonaws.com/dl.3dsystems.com/binaries/Sensable/Linux/Installation+Instructions_2022.pdf).

### Windows 10/11

Download the latest version of OpenHaptics, which is currently v3.5.0 from the official [webpage](https://support.3dsystems.com/s/article/OpenHaptics-for-Windows-Developer-Edition-v35?language=en_US). Once it is done, follow the instructions below:

1. Uninstall any previous version of OpenHaptics if any
1. Unzip the file
1. Run .exe file

The installation by default will be at the directory *C:/OpenHaptics*.

For the drivers download the drivers from the same [webpage](https://support.3dsystems.com/s/article/OpenHaptics-for-Windows-Developer-Edition-v35?language=en_US). Execute the file and let the drivers to be installed. Plugged your device in.

## How to use OpenHaptics

OpenHaptics provides an API to read the commands from any haptic device and include them in any of your project. The main library for this is known as **HD** and **HDU**, which includes the data types to retieve the state of the device. Here is a simple explanation on how to use the OpenHaptics library in your project. The complete documentation for the OpenHaptics library can be found [here](https://s3.amazonaws.com/dl.3dsystems.com/binaries/Sensable/OH/3.5/OpenHaptics_Toolkit_ProgrammersGuide.pdf).

### Requirements

#### CMake

To include OpenHaptics in our projects we are going to use CMake to generate the configuration files for it. We are going to need CMake (<=3.1.0) to build the projects. In Ubuntu, open a terminal and type the following command to obtain the latest version of CMake.

```
$ sudo snap install cmake --classic
```

In Windows, download the latest available binary version from the official [CMake download webpage](https://cmake.org/download/). Execute the binary and follow the instructions for the installation.

#### VisualStudio 2015/2017 (Windows)

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

HD contains many functions to initialize and use the device inside your C++ framework. This is just a very short introduction to the most used functions. For a complete reference guide to the latest OpenHaptics library functions refer to the official [webpage](https://s3.amazonaws.com/dl.3dsystems.com/binaries/Sensable/OH/3.5/OpenHaptics_Toolkit_API_Reference_Guide.pdf).

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

The haptic device inside HDAPI is defined with the variable *HHD*. We want to catch any possible error that starting the device may cause.. We want to enable the force display so we need to include the command. Now we initialize the scheduler for the haptic device. Finally, we create an instance of our data structure *TouchState* and call the callback function to run asynchronously during the execution of the program. We will go deeper on how to program a callback function in the next section. Here is a small snippet of a *main.cpp* file code on how to initialize the device.

```cpp
// include headers here

// callback function explained in next section here

int main {
    ///////////////////
    // Init Touch X //
    /////////////////

    HDErrorInfo error; // catch the initialization errors
    HHD hHD = hdInitDevice(HD_DEFAULT_DEVICE); // init device

    // Catch initialization errors
    if (HD_DEVICE_ERROR(error = hdGetError())) {
        hduPrintError(stderr, &error, "Failed to start haptic device");
    }

    // Enable force feedback
    hdEnable(HD_FORCE_OUTPUT);

    // Start the scheduler & catch errors
    hdStartScheduler();
    if (HD_DEVICE_ERROR(error = hdGetError())) {
        hduPrintError(stderr, &error, "Failed to start scheduler");
    }

    HHD_Auto_Calibration();
    // Define the data structure and the callback loop
    TouchState state;
    hdScheduleAsynchronous(touch_state_callback, &state, HD_MAX_SCHEDULER_PRIORITY);
}
```

#### Callback to update device state

