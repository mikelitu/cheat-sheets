#pragma once

#include <sofa/config.h>

#ifdef SOFA_BUILD_MINIMALPLUGIN
    #define MINIMALPLUGIN_API SOFA_EXPORT_DYNAMIC_LIBRARY
#else
    #define MINIMALPLUGIN_API SOFA_IMPORT_DYNAMIC_LIBRARY
#endif