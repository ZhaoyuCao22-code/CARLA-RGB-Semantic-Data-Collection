# CARLA-RGB-Semantic-Data-Collection
CARLA RGB and Semantic Segmentation Data Collection Project

Project Overview

This project focuses on collecting RGB images and semantic segmentation images using the CARLA autonomous driving simulator.

The goal is to build a basic dataset for autonomous driving perception tasks, including camera data acquisition and semantic segmentation data collection.

Environment

* CARLA Version: 0.9.15
* Python Version: 3.7
* Platform: Windows
* Simulator: CARLA Unreal Engine

Project Structure

01_connect_carla.py

Connects to the CARLA server and retrieves basic simulation information.

Functions:

* Connect CARLA client
* Get current simulation world
* Get map information
* Count existing vehicles

02_spawn_vehicle.py

Creates a vehicle inside the CARLA simulation environment.

Functions:

* Load vehicle blueprint
* Select spawn point
* Spawn vehicle actor

03_autopilot_vehicle.py

Enables autonomous driving mode for the vehicle.

Functions:

* Spawn vehicle
* Enable autopilot
* Observe vehicle movement

04_camera_sensor.py

Adds an RGB camera sensor to the vehicle.

Functions:

* Attach RGB camera
* Capture images
* Save RGB images

05_collect_rgb_semantic.py

Collects RGB images and semantic segmentation images simultaneously.

Functions:

* Attach RGB camera
* Attach semantic segmentation camera
* Save paired RGB and semantic images

06_collect_batch_rgb_semantic.py

Tests larger batch data collection.

Functions:

* Collect multiple RGB frames
* Collect multiple semantic frames
* Test dataset generation

07_collect_small_batch.py

Final stable data collection script.

Functions:

* Optimize sensor settings
* Reduce simulation load
* Successfully collect RGB and semantic segmentation data

Dataset

The collected dataset contains:

* 521 RGB images
* 521 semantic segmentation images

RGB images are stored in:

data/rgb

Semantic segmentation images are stored in:

data/semantic

Result

This project demonstrates:

* CARLA Python API usage
* Vehicle spawning and control
* Camera sensor attachment
* RGB image collection
* Semantic segmentation data collection

Future Work

Possible improvements:

* Increase dataset size
* Add more traffic scenarios
* Train perception models using collected data
