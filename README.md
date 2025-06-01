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
- [Demostration](#-demostration)
- [How to Build](#-how-to-build)
- [License](#-license)

## 🚀 About

**depth maixsense a010** is a package for ROS2 Jazzy that allow us to use MaixSense A010 depth camera. This package was originally made by <a href="https://github.com/sipeed/MaixSense_ROS/">Sipeed</a> so all credits to them, we only fixed the package to be compatible with jazzy as it had errors, and created a launch file to simplify launched the camera node with rviz.

## 🎥 Demostration
https://github.com/user-attachments/assets/b3696c4a-1d94-4272-9a09-7452982fdfef



## 📝 How to Build

To build the packages, follow these steps:

```shell
# Add yourself to dialout group if you haven't yet
sudo usermod -a -G dialout $USER

# Go to your workspace/src folder
cd ~/ros2_ws/src

# Clone the repository
git https://github.com/Tesis-ORION/Depth_ydlidar_os30a

# Return to workspace folder
cd ~/ros2_ws

# Compile the package
colcon build --packages-select depth_maixsense_a010

# Source your workspace
source ~/ros2_ws/install/setup.bash

```

## 📃 License

depth_maixsense_a010 is available under the BSD-3-Clause license. See the LICENSE file for more details.
