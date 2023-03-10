# SOFA
 
This file contains information about different applications and implementations for SOFA that I have discovered over the years. For more detailed information on how to start with SOFA, compilation and adding useful plugins follow the instructions in their [tutorial](https://www.sofa-framework.org/community/doc/getting-started/build/linux/). I highly recommend adding the **SofaPython3** plugin as it adds an extra layer to control the simulation and massively simplifies the code.

## Connecting SOFA with ROS
For this task we need SOFA with SofaPython3 plugin. I have tested it with the binaries from [ROS2 Foxy](https://docs.ros.org/en/foxy/Installation.html) and **SOFA v22.06** in Ubuntu 20.04. The binaries from Foxy are built using *Python3.8*, so make sure that the executable used to compile SOFA is the same version. If you are in Ubuntu use the following line for the installation (from the original SOFA documentation).

```
sudo apt install python3.8-dev
sudo apt-get install python3-distutils \
&& curl -L https://bootstrap.pypa.io/pip/get-pip.py --output /tmp/get-pip3.py \
&& python3.8 /tmp/get-pip3.py \
&& python3.8 -m pip install --upgrade pip \
&& python3.8 -m pip install numpy scipy
```

on Windows just install the newest version of Python3.8 from their official webpage. On the CMake GUI just make sure to set the variable **PYTHON_EXECUTABLE** to the path of Python3.8. In the CMake console, you will have printed the used Python version for the compilation, make sure it is 3.8.

## Compiling SOFACuda

Make sure to have cuda and cuda-toolkits install in your system. You can directly install the latest version available in your system (Ubuntu) using `sudo apt install cuda-toolkit cuda`. Make sure the version is *=11.x*, as it won't compile with the newest versions of cuda. If you have multiple versions of CUDA in your computer you can use the *switch-cuda.sh* file in this folder to change from one version to another. The command to use this file is:

```
source /path/to/file/switch-cuda.sh 11.x
Switched to CUDA 11.x.
```
Now we need to make some changes on the compilation variables at the SOFA CMake project. Open the CMake-GUI using the command `cmake-gui`, choose the source and build directory for your SOFA project. Click on *Configure* and in the pop up window choose the option **Specify native compilers**. Here set the C and C++ compiler to gcc-8 or gcc-9, as we can only compile the binaries with this two versions. 

Activate the flag **PLUGIN_SOFACUDA** and click *Configure* again. 

## Minimal plugin example

A minimal SOFA plugin should contain two files inside the *src/pluginName* directory: **config.h** and **initPluginName.cpp**. This two files will load the plugin into SOFA when we initialize the software. 

```cpp
// config.h
#pragma once

#include <sofa/config.h>

#ifdef SOFA_BUILD_YOURPLUGINNAME
    #define YOURPLUGINNAME_API SOFA_EXPORT_DYNAMIC_LIBRARY
#else
    #define YOURPLUGINNAME_API SOFA_IMPORT_DYNAMIC_LIBRARY
#endif
```

```cpp
// inityourPluginName.cpp
#include <yourPluginName/config.h>

namespace sofa
{
namespace component
{
extern "C" {
    
YOURPLUGINAME_API
void initExternalModule()
{
    static bool first = true;
    if (first)
    {
        first=false;
    }
}

YOURPLUGINAME_API
const char* getModuleName()
{
    return "YourPluginName";
}

YOURPLUGINNAME_API
const char* getModuleVersion()
{
    return "1.0";
}

YOURPLUGINNAME_API
const char* getModuleLicense()
{
    return "yourLicense";
}

YOURPLUGINNAME_API
const char* getModuleDescriptio()
{
    return "A short description of your plugin";
}

} // extern C
} // namespace component
} // namespace sofa
```