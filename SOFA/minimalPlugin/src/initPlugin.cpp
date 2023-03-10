#include <config.h>

namespace sofa
{
namespace component
{
extern "C" {
    MINIMALPLUGIN_API
    void initExternalModule() {
        static bool first = true;
        if (first) {
            first = false
        }
    }
    MINIMALPLUGIN_API
    const char* getModuleName() {
        return "MinimalPlugin";
    }

    MINIMALPLUGIN_API
    const char* getModuleVersion() {
        return "1.0";
    }

    MINIMALPLUGIN_API
    const char* getModuleLicense()
    {
        return "yourLicense";
    }

    MINIMALPLUGIN_API
    const char* getModuleDescriptio()
    {
        return "Minimal plugin example for SOFA";
    }

} // extern C
} // namespace component
} // namespace sofa