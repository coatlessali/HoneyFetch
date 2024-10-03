if __name__ == '__main__':
    from guizero import App, PushButton, Text, Picture, ButtonGroup
    import platform, subprocess, cpuinfo, os, multiprocessing, sys, cffi
    from cpuinfo import get_cpu_info

    multiprocessing.freeze_support()

    # Lay out some colors.

    bg = "#0a2050"
    normal = "#ffffff"
    warn = "#24b7d6"
    good = "#12c615"
    bad = "#b43421"

    # cpu info stuff.

    ffi = cffi.FFI()
            
    # This part was written by gloria.
    # I didn't ask for this, she just wrote it,
    # and said it was now mine apparently.
    def testVulkan() -> str:
        try:
            import vulkan as vk
        except OSError:
            return "Vulkan runtime could not be found."

        appInfo = vk.VkApplicationInfo(
            pApplicationName="HoneyFetch",
            applicationVersion=1,
            apiVersion=vk.VK_MAKE_VERSION(1, 1, 0)
        )

        flags = None
        extensions: [str] = [ ]

        if sys.platform == "darwin":
            flags.vk.VK_INSTANCE_CREATE_ENUMERATE_PORTABILITY_BIT_KHR
            extensions.append(vk.VK_KHR_PORTABILITY_ENUMERATION_EXTENSION_NAME)
        instanceInfo = vk.VkInstanceCreateInfo(
            flags=flags,
            pApplicationInfo=appInfo,
            enabledExtensionCount=len(extensions),
            ppEnabledExtensionNames=extensions
        )

        try:
            instance: vk.VkInstance = vk.vkCreateInstance(instanceInfo, None)
        except vk.VkErrorIncompatibleDriver:
            return "No compatible vulkan driver was found."

        try:
            devices: [vk.VkPhysicalDevice] = vk.vkEnumeratePhysicalDevices(instance=instance)
        except:
            return "Could not discover Vulkan devices."
            
        if len(devices) == 0:
            return "No Vulkan 1.1 compatible device found."
            
        goodDriverProperties: vk.VkPhysicalDeviceDriverProperties = None
        goodDevProperties: vk.VkPhysicalDeviceProperties = None
            
        for device in devices:
            driverProperties = vk.VkPhysicalDeviceDriverProperties()
            deviceProperties = vk.VkPhysicalDeviceProperties2(pNext=driverProperties)
            
            vk.vkGetPhysicalDeviceProperties2(device, deviceProperties)
            
            if "llvmpipe" in driverProperties.driverName:
                continue
            
            goodDriverProperties = driverProperties
            goodDevProperties = deviceProperties
            break
            
        if goodDriverProperties is None or goodDevProperties is None:
            return "Failed to find a usable device."
            
        return [f"{ffi.string(goodDevProperties.properties.deviceName).decode("utf-8")}", f"{ffi.string(goodDriverProperties.driverName).decode("utf-8")}", f"{ffi.string(goodDriverProperties.driverInfo).decode("utf-8")}", f"v{goodDevProperties.properties.driverVersion}", f"v{goodDevProperties.properties.apiVersion}"]


    print(testVulkan())            

    # Parse color.
    def color_parse_str(field, cont, color, color2):
        try:
            if cont in field:
                return color
            else:
                return color2
        except:
            return color2

    def color_parse_bool(field, color, color2):
        try:
            if field:
                return color
            else:
                return color2
        except:
            return color2

    # Export.
    def export_info():
        if stf_button.value == None:
            app.error("Error!", "Please select a value.")
        x = "\n"
        info = "CPU: " + cpu + x + "AVX: " + str(avx) + x + "AXV2: " + str(avx2) + x + str(arch._text) + x + "OS Type: " + system + x + "GPU: " + deviceName + x + "VK VERSION: " + apiVersion + x + "DRIVER VERSION: " + driverVersion + x + "DRIVER NAME: " + driverName + x + "DRIVER INFO:" + driverInfo + x + "STATUS:" + stf_button.value
        with open('HoneyFetchEXPORT.txt', 'w+') as f:
            f.write(info)
        app.info("Notice", "Exported to HoneyFetchEXPORT.txt! Please send this in #troubleshooting, or to coatlessali for the survey!")

    # System info.
    cpu = get_cpu_info()["brand_raw"]
    avx = "avx" in get_cpu_info()["flags"]
    avx2 = "avx2" in get_cpu_info()["flags"]
    arch = platform.machine()
    system = platform.system()
    deviceName = testVulkan()[0]
    apiVersion = "placeholder"
    driverVersion = testVulkan()[3]
    driverName = testVulkan()[1]
    driverInfo = testVulkan()[2]

    # COLOR DEFS
    cpu_color = normal
    avx_color = color_parse_bool(avx, good, bad)
    avx2_color = color_parse_bool(avx2, good, bad)
    arch_color = color_parse_str(arch, "64", good, bad)
    deviceName_color = color_parse_str(driverName, "llvmpipe", bad, normal) 

    # GUI
    app = App(title="HoneyFetch", bg=bg, width=960, height=720)

    funny = Picture(app, image="gato.png", align="right")

    cput = Text(app, text=f"CPU: {cpu}")
    cput.text_color = normal
    avxt = Text(app, text=f"AVX: {avx}")
    avxt.text_color = avx_color
    avx2t = Text(app, text=f"AVX2: {avx2}")
    avx2t.text_color = avx2_color
    arch = Text(app, text=f"Architecture: {arch}")
    arch.text_color = arch_color
    systemt = Text(app, text=f"OS Type: {system}")
    systemt.text_color = normal
    deviceNamet = Text(app, text=f"GPU: {deviceName}")
    deviceNamet.text_color = deviceName_color
    apiVersiont = Text(app, text=f"Vulkan API: {apiVersion}")
    apiVersiont.text_color = normal
    driverVersiont = Text(app, text=f"Driver Version: {driverVersion}")
    driverVersiont.text_color = normal
    driverNamet = Text(app, text=f"Driver in Use: {driverName}")
    driverNamet.text_color = normal
    driverInfot = Text(app, text=f"Driver info: {driverInfo}")
    driverInfot.text_color = normal

    stf_button = ButtonGroup(app, options=["STF runs perfect!", "STF stutters sometimes.", "STF runs poorly.", "STF crashes."])
    stf_button.text_color = normal

    export_button = PushButton(app, text="Export info...", command=export_info)
    export_button.text_color = warn

    print(cpu)
    if os.path.exists('vulkaninfo.txt'):
        os.remove('vulkaninfo.txt')
        
    app.display()
else:
    exit()
