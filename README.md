# depth maixsense a010
[![language](https://img.shields.io/badge/language-c++-239120)](#)
[![OS](https://img.shields.io/badge/OS-Ubuntu_24.04-0078D4)](#)
[![ROS](https://img.shields.io/badge/ROS_Version-Jazzy_Jalisco-0078D4)](#)
[![CPU](https://img.shields.io/badge/CPU-x86%2C%20x64%2C%20ARM%2C%20ARM64-FF8C00)](#)
[![GitHub release](https://img.shields.io/badge/release-v1.0.9-4493f8)](#)
[![GitHub release date](https://img.shields.io/badge/release_date-february_2025-96981c)](#)
[![GitHub last commit](https://img.shields.io/badge/last_commit-june_2025-96981c)](#)

⭐ Star us on GitHub — it motivates us a lot!

## Table of Contents
- [About](#-about)
- [How to Build](#-how-to-build)
- [Display Variant](#-display-variant)
- [udev Rules](#-udev-rules)
- [License](#-license)

## 🚀 About

**depth maixsense a010** is a package for ROS2 Jazzy that allows using the MaixSense A010 depth camera. This package was originally made by [Sipeed](https://github.com/sipeed/MaixSense_ROS/) — all credits to them. We fixed the package for Jazzy compatibility, addressed stability issues on Raspberry Pi 4 (ARM64), and created a launch file to simplify running the camera node with RViz.

## 📝 How to Build

```shell
# Add yourself to the dialout group (required for serial port access)
sudo usermod -a -G dialout $USER

# Go to your workspace src folder
cd ~/dev_ws/src

# Clone the repository
git clone https://github.com/DanielFLopez1620/depth_maixsense_a010.git

# Return to workspace root
cd ~/dev_ws

# Build the package
colcon build --packages-select depth_maixsense_a010

# Source the workspace
source ~/dev_ws/install/setup.bash
```

To launch the camera node with RViz:

```shell
ros2 launch depth_maixsense_a010 maixsense_a010_launch.py
```

## 🖥️ Display Variant

The MaixSense A010 comes in variants **with** and **without** the onboard LCD. The driver tells the camera where to send its output via the `AT+DISP=<n>` command, which is a bitfield of output targets (`bit0 = LCD`, `bit1 = USB`, `bit2 = UART`). The frame stream this driver reads always travels over the **USB** bit, so streaming works on both variants; the only difference is whether the camera also renders to its LCD.

This is controlled by a single compile-time flag at the top of [`src/main.cc`](src/main.cc):

```cpp
#define MAIXSENSE_HAS_DISPLAY 0   // 1 if your unit has the LCD, 0 if it does not
```

- **`1`** → `AT+DISP=3` (LCD + USB). Use this if your unit has the screen.
- **`0`** → `AT+DISP=2` (USB only). Use this for screenless units; it also avoids the camera spending time rendering to a non-existent LCD, which is helpful on the Raspberry Pi 4.

Set the flag to match your hardware and rebuild the package.

> **Note for Raspberry Pi 4 users:** The MaixSense A010 may require more current than a standard RPi4 USB 2.0 port can reliably supply. If the node stops publishing after 30–60 seconds or fails to initialize, use a **powered USB hub** between the RPi4 and the camera.

## 🔌 udev Rules

The MaixSense A010 exposes **two tty devices** when connected over USB:

| Interface | Device    | Role          |
|-----------|-----------|---------------|
| `00`      | `ttyUSB0` | Camera (data) |
| `01`      | `ttyUSB1` | Debugger      |

Both interfaces share the same `idVendor`, `idProduct`, and `manufacturer` attributes, so rules based on those alone can assign the symlink to the wrong interface (usually the debugger). The correct approach combines the physical USB path (`KERNELS`) with the logical interface number (`bInterfaceNumber`).

> Note: If you are using the UART ports and a connection to a serializer, you may only receive one device (the camera data). However, the udev rule may be different at what is shown below as it will depend on the USB serializer you are using.

### Shared device attributes

```text
idVendor        = "0403"
idProduct       = "6010"
manufacturer    = "SIPEED"
bNumInterfaces  = 2
```

### Rule file: `/etc/udev/rules.d/99-orion.rules`

```bash
# MaixSense A010 - Camera
SUBSYSTEM=="tty", KERNELS=="1-1.2:1.0", ATTRS{bInterfaceNumber}=="00", MODE:="0666", SYMLINK+="ttyA010"

# MaixSense A010 - Debugger
SUBSYSTEM=="tty", KERNELS=="1-1.2:1.1", ATTRS{bInterfaceNumber}=="01", MODE:="0666", SYMLINK+="ttyA010_debug"
```

After creating the file, reload the rules:

```shell
sudo udevadm control --reload-rules && sudo udevadm trigger
```

Verify the symlinks were created:

```shell
ls -la /dev/ttyA010*
```

To inspect attributes of a connected device:

```shell
udevadm info --attribute-walk --name=/dev/ttyUSB0
udevadm info --attribute-walk --name=/dev/ttyUSB1
```

> **Warning:** `KERNELS=="1-1.2:x.x"` is tied to the **physical USB port** where the A010 is connected. If the camera is moved to a different port on the Raspberry Pi the rules will stop working and the `KERNELS` value must be updated. Always connect the A010 to the same physical USB port.

## 📃 License

depth_maixsense_a010 is available under the BSD-3-Clause license. See the LICENSE file for more details.
