from guizero import App, PushButton, Text, Picture, ButtonGroup
import platform
import subprocess
import cpuinfo
import os
from cpuinfo import get_cpu_info

# Lay out some colors.

bg = "#0a2050"
normal = "#ffffff"
warn = "#24b7d6"
good = "#12c615"
bad = "#b43421"

# cpu info stuff.

# Subprocess to get vulkaninfo output.
try:
    vulkaninfostrchk = subprocess.check_output(["vulkaninfo", "--summary"], shell=False, text=True)
    vulkaninfostr = str(vulkaninfostrchk)
except:
    vulkaninfostr = "yikes"
finally:
    with open("vulkaninfo.txt", "w+") as vulkaninfotxt:
        vulkaninfotxt.write(vulkaninfostr)

# Parse vulkaninfo.
def vk_parse(vkstring):
    with open('vulkaninfo.txt', 'rt') as f:
        vulkaninfo = f.readlines()
    for line in vulkaninfo:
        if vkstring in line:
            finalvkstring = line.split("= ",1)[1]
            return finalvkstring

# Parse color.
def color_parse_str(field, cont, color, color2):
    if cont in field:
        return color
    else:
        return color2

def color_parse_bool(field, color, color2):
    if field:
        return color
    else:
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
deviceName = vk_parse("deviceName")
apiVersion = vk_parse("apiVersion")
driverVersion = vk_parse("driverVersion")
driverName = vk_parse("driverName")
driverInfo = vk_parse("driverInfo")

# COLOR DEFS
cpu_color = normal
avx_color = color_parse_bool(avx, good, bad)
avx2_color = color_parse_bool(avx2, good, bad)
arch_color = color_parse_str(arch, "x86_64", good, bad)
deviceName_color = color_parse_str(driverName, "llvmpipe", bad, normal) 

# GUI
app = App(title="HoneyFetch", bg=bg)

funny = Picture(app, image="gato.webp", align="right")

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

stf_button = ButtonGroup(app, options=["STF runs perfect!", "STF stutter sometimes.", "STF runs poorly.", "STF crashes."])
stf_button.text_color = normal

export_button = PushButton(app, text="Export info...", command=export_info)
export_button.text_color = warn

print(cpu)
if os.path.exists('vulkaninfo.txt'):
    os.remove('vulkaninfo.txt')
    
app.display()