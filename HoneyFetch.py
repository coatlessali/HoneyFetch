# This guards all of the code from creating a fork bomb on Windows when frozen with pyinstaller.
# Do not touch this. Put everything in the if statement.
if __name__ == '__main__':
    from guizero import App, PushButton, Text, Picture, ButtonGroup
    import platform, subprocess, cpuinfo, os, multiprocessing, sys, cffi
    from cpuinfo import get_cpu_info

    # This also prevents the fork bomb, and is the reason we need to import multiprocessing.
    multiprocessing.freeze_support()

    # These are the colors used by the UI.
    # They are ripped directly from Sonic the Fighters' HD UI.

    bg = "#0a2050"
    normal = "#ffffff"
    warn = "#24b7d6"
    good = "#12c615"
    bad = "#b43421"
            
    # This part was written by @yeah-its-gloria.
    # I didn't ask for this, she just wrote it,
    # and said it was now mine apparently.
    # I have made minimal edits to it.
    # Please don't ask me how it works, I genuinely
    # have no idea.
    ffi = cffi.FFI()

    def testVulkan() -> str:
        try:
            import vulkan as vk
        except OSError:
            return ["Vulkan runtime could not be found.", "None", "None"]

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
            return ["No compatible vulkan driver was found.", "None", "None", bad]

        try:
            devices: [vk.VkPhysicalDevice] = vk.vkEnumeratePhysicalDevices(instance=instance)
        except:
            return ["Could not discover Vulkan devices.", "None", "None", bad]
            
        if len(devices) == 0:
            return ["No Vulkan 1.1 compatible device found.", "None", "None", bad]
            
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
            return ["Failed to find a usable device.", "None", "None", bad]
            
        return [f"{ffi.string(goodDevProperties.properties.deviceName).decode("utf-8")}", f"{ffi.string(goodDriverProperties.driverName).decode("utf-8")}", f"{ffi.string(goodDriverProperties.driverInfo).decode("utf-8")}", good]

    # This part was also partially refactored by @yeah-its-gloria.
    # Again, I didn't ask her to do this. She just did it and handed it to me.
    # You can ask me about this, I actually know what this is doing.
    def testProcessor() -> str:
        # cpu_warning_color is separated because warnings are separate from stats
        cpu_warnings = []
        cpu_colors = [good, good, good, good]
        cpu_data = cpuinfo.get_cpu_info()
        avx = "AVX Unsupported."
        cpu_warning_color = good

        # check for amd64 or arm
        if cpu_data["arch"].lower() != "x86_64" and cpu_data["arch"].lower() != "amd64" and cpu_data["arch"].lower() != "arm_8":
            cpu_warnings.append(f"Unsupported architecture {cpu_data["arch"]}. Emulation will be required.")
            cpu_colors[0] = warn

        # check for anything64
        if cpu_data["bits"] < 64:
            cpu_warnings.append("CPU is not 64 bit.")        
            cpu_colors[1] = bad

        # check for amd64, because AVX doesn't exist outside of it
        if cpu_data["arch"].lower() == "x86_64" or cpu_data["arch"].lower() == "amd64":
            # check for AVX
            if not "avx" in cpu_data["flags"]:
                cpu_warnings.append("AVX unsupported.")
                cpu_colors[2] = bad
            else:
                cpu_colors[2] = warn
                avx = "AVX"

            # check for AVX2
            if not "avx2" in cpu_data["flags"]:
                cpu_warnings.append("AVX2 unsupported.")
                # if you at least have AVX, you can probably get the game to boot
                # but without AVX2 you shouldn't expect it to be playable
            else:
                avx = "AVX2"
                cpu_colors[2] = good
            
        if not cpu_warnings:
            cpu_warnings.append("None!")
        else:
            # if one of the warnings was tripped, you're probably not playing the game tbh
            cpu_warning_color = bad
            if warn in cpu_colors:
                cpu_colors[3] = warn
            if bad in cpu_colors:
                cpu_colors[3] = bad 

        # in order, return:
        # arch, arch color, bits, bits color, avx, avx color, cpu warnings, cpu warning color, raw brand name 
        return [cpu_data["arch"], cpu_colors[0], cpu_data["bits"], cpu_colors[1], avx, cpu_colors[2], cpu_warnings, cpu_warning_color, cpu_data["brand_raw"], cpu_colors[3]]            

    # Export a log.
    def export_info():
        if stf_button.value == None:
            app.error("Error!", "Please select a value.")
        x = "\n"
        #info = "CPU: " + cpu + x + "AVX: " + str(avx) + x + "AXV2: " + str(avx2) + x + str(arch._text) + x + "OS Type: " + system + x + "GPU: " + deviceName + x + "VK VERSION: " + apiVersion + x + "DRIVER VERSION: " + driverVersion + x + "DRIVER NAME: " + driverName + x + "DRIVER INFO:" + driverInfo + x + "STATUS:" + stf_button.value
        info = f"CPU: {cpu_stats}, GPU: {vulkan_stats}"
        with open('HoneyFetchEXPORT.txt', 'w+') as f:
            f.write(info)
        app.info("Notice", "Exported to HoneyFetchEXPORT.txt! Please send this in #troubleshooting, or to coatlessali for the survey!")

    # System info.
    cpu_stats = testProcessor()
    vulkan_stats = testVulkan()

    # GUI
    app = App(title="HoneyFetch", bg=bg, width=960, height=720)

    funny = Picture(app, image="gato.png", align="right")

    cput = Text(app, text=f"CPU: {cpu_stats[8]}")
    cput.text_color = normal
    bitst = Text(app, text=f"{cpu_stats[2]}-bit")
    bitst.text_color = cpu_stats[3]
    avxt = Text(app, text=f"{cpu_stats[4]}")
    avxt.text_color = cpu_stats[5]
    arch = Text(app, text=f"Architecture: {cpu_stats[0]}")
    arch.text_color = cpu_stats[1]
    cpuwarnings = Text(app, text=f"CPU Warnings: {', '.join(cpu_stats[6])}")
    cpuwarnings.text_color = cpu_stats[7]
    system = Text(app, text=f"OS Type: {platform.system()}")
    system.text_color = normal
    deviceName = Text(app, text=f"GPU: {vulkan_stats[0]}")
    deviceName.text_color = testVulkan()[3]
    driverNamet = Text(app, text=f"Driver in Use: {vulkan_stats[1]}")
    driverNamet.text_color = testVulkan()[3]
    driverInfot = Text(app, text=f"Driver info: {vulkan_stats[2]}")
    driverInfot.text_color = testVulkan()[3]

    stf_button = ButtonGroup(app, options=["STF runs perfect!", "STF stutters sometimes.", "STF runs poorly.", "STF crashes."])
    stf_button.text_color = normal

    export_button = PushButton(app, text="Export info...", command=export_info)
    export_button.text_color = warn

    if os.path.exists('vulkaninfo.txt'):
        os.remove('vulkaninfo.txt')
        
    app.display()
else:
    exit()
