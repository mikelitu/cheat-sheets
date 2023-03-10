cmake_minimum_required(VERSION 3.12)
project(MinimalPlugin VERSION 1.0 LANGUAGES CXX)

# Find and load CMake configuration of packages containing this plugin's dependencies
## Mandatory dependencies
find_package(SofaBase REQUIRED)

## Optional dependencies
find_package(SofaPython3)

# List all the files
set (MINIMAL_PLUGIN_SRC_DIR src)

set (HEADER_FILES
    ${MINIMAL_PLUGIN_SRC_DIR}/config.h
)

set(SOURCE_FILES
    ${MINIMAL_PLUGIN_SRC_DIR}/initPlugin.cpp
)

add_library(${PROJECT_NAME} SHARED ${HEADER_FILES} ${SOURCE_FILES})

# Link the plugin library to its dependencies
target_link_libraries(${PROJECT_NAME} SofaBase)

# Create package Config, Version & Target files.
# Deploy the headers, resources, scenes & examples.
# Set the plugin 'relocatable' if built within SOFA.
# --> see SofaMacros.cmake
sofa_create_package_with_targets(
    PACKAGE_NAME ${PROJECT_NAME}
    PACKAGE_VERSION ${PROJECT_VERSION}
    TARGETS ${PROJECT_NAME} AUTO_SET_TARGET_PROPERTIES
    INCLUDE_SOURCE_DIR "src"
    INCLUDE_INSTALL_DIR ${PROJECT_NAME}
    RELOCATABLE "plugins"
)
