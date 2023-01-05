# SOFA
 
This file contains information on how to build custom SOFA packages. Focusing on the necessary files and functions you need to include to build a successful plugin. In addition, contains the information on how to write your CMake file to create new plugins.

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