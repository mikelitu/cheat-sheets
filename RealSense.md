# RealSense

This file contains a short summary on how to set up a C++ project to use a RealSense camera, using CMake. This tutorial is expected to be used with *Ubuntu20.04*.

## Install *librealsense2*

This is a small explanation on how to install librealsense, for a more detailed you can refer to the original tutorial for [pre-built-packages](https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md) or [building from source](https://github.com/IntelRealSense/librealsense/blob/master/doc/installation.md). Here we will cover the pre-built-package installation.

* Register the server's publick key:
  ```console
  sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE
  ```
  In case the key cannot be retrieved follow the instructions on the original tutorial.

* Add the server to the list of repositories:
  ```console
  sudo add-apt-repository "deb https://librealsense.intel.com/Debian/apt-repo $(lsb_release -cs) main" -u
  ```
* Install the libraries:
  ```console
  sudo apt-get install librealsense2-dkms
  sudo apt-get install librealsense2-utils
  ```
* Optionally install the developer and debug packages
  ```console
  sudo apt-get install librealsense2-dev
  sudo apt-get install librealsense2-dbg
  ```
  With `dev`, we can compile an application with librealsense.

Reconnect the IntelRealSense depth camera and run: `realsense-viewer` to verify the installation.

Verify that the kernel is updated:
`modinfo uvcvideo | grep "version:"` should include `realsense` string.

## Create the project file

If you are not familiar with the C++ project folder ordering, this is just a very simple example on how to order your folder.

* root
  * build
  * src
    * main.cpp
  * CMakeLists.txt

My recommendation is for you to first write the CMakeLists.txt file in order to have the *IntelliSense* autocomplete and documentation for the functions in the *librealsense2* library. If you are using an IDE such as **VSCode** when you write this file it will know how to find the functions.

## CMake file

To include *librealsense2* in your project we will use a CMake file. The *CMakeLists.txt* file generates standard Make files that will contain the intsructions describing the projects source files and dependecies. This is an example of a minimal *CMakeLists.txt* file to include *librealsense2* in your custom project. You can find more information on the original *librealsense2* github [repo](https://github.com/IntelRealSense/librealsense/tree/master/examples/cmake).

```cmake
cmake_minimum_required(VERSION 3.1.0)

project(your_project_name)

#Find the librealsense2 installed package
find_package(realsense2 REQUIRED)

#Enable C++11 standard application
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

#Add the application sources to the target
add_executable(${PROJECT} src/main.cpp)

#Link librealsense2 to the target
target_link_libraries(${PROJECT_NAME} ${realsense2_LIBRARY})
```

## C++ source file

In this example, we will look into the most basic *librealsense2* function, which is `rs2::pipeline`. The pipeline is a top-level API for streaming and processing the frames. To execute the pipeline we will use `start()` method. Here you can find a very simple example on how to measure the distance to an object using this function.

```cpp
#include <librealsense2/rs.hpp>
#include <iostream>

int main(int argc, char * argv[]) try
{
    // Create a pipeline
    rs2::pipeline p;

    // Configure and start the pipeline
    p.start();

    while (true)
    {
        // Block program until the next set of frames arrive
        rs2::frameset frames = p.wait_for_frames();

        // Try to get the depth image
        rs2::depth_frame depth = frames.get_depth_frame();

        // Get the depth frame's dimension
        auto width = depth.get_width();
        auto height = depth.get_height();

        // Query the distance from the camera to the object in the center of the image
        float dist_to_center = depth.get_distance(width / 2, height / 2);

        // Print the distance
        std::cout << "The camera is facing an object " << dist_to_center << " meters away \r";
    }

    return EXIT_SUCCESS;
}
catch (const rs2::error & e)
{
    std::cerr << "RealSense error calling " << e.get_failed_function() << "(" << e.get_failed_args() << "):\n" << e.what() << std::endl;
    return EXIT_FAILURE;
}
catch (const std::exception& e)
{
    std::cerr << e.what() << std::endl;
    return EXIT_FAILURE;
}
```

If you want to display the images from the camera I recommend using [OpenCV](https://opencv.org/). You can see a more detailed tutorial on how to use OpenCV to display rgb frames and depth frames in their github [repo](https://github.com/IntelRealSense/librealsense/tree/master/wrappers/opencv/imshow). You will need to update the *CMakeLists.txt* file to include OpenCV on our project.