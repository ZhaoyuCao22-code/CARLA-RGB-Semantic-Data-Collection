import carla
import random
import time
import os

# 采集参数
MAX_FRAMES = 1000
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 360
SENSOR_TICK = 0.5

# 连接 CARLA
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

world = client.get_world()
blueprint_library = world.get_blueprint_library()

# 创建 RGB 和语义分割图像的保存目录
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')

rgb_dir = os.path.join(data_dir, 'rgb')
semantic_dir = os.path.join(data_dir, 'semantic')

if not os.path.exists(rgb_dir):
    os.makedirs(rgb_dir)

if not os.path.exists(semantic_dir):
    os.makedirs(semantic_dir)

print("RGB images will be saved to:", rgb_dir)
print("Semantic images will be saved to:", semantic_dir)

# 生成车辆并开启自动驾驶
vehicle_bp = random.choice(blueprint_library.filter('vehicle.*'))
spawn_points = world.get_map().get_spawn_points()
spawn_point = random.choice(spawn_points)

vehicle = world.spawn_actor(vehicle_bp, spawn_point)
vehicle.set_autopilot(True)

print("Vehicle spawned:", vehicle_bp.id)
print("Autopilot enabled.")

# 两个摄像头使用相同安装位置，方便图像一一对应
camera_transform = carla.Transform(
    carla.Location(x=1.5, z=2.4),
    carla.Rotation(pitch=0)
)

rgb_bp = blueprint_library.find('sensor.camera.rgb')
rgb_bp.set_attribute('image_size_x', str(IMAGE_WIDTH))
rgb_bp.set_attribute('image_size_y', str(IMAGE_HEIGHT))
rgb_bp.set_attribute('fov', '90')
rgb_bp.set_attribute('sensor_tick', str(SENSOR_TICK))

rgb_camera = world.spawn_actor(
    rgb_bp,
    camera_transform,
    attach_to=vehicle
)

print("RGB camera attached.")

semantic_bp = blueprint_library.find('sensor.camera.semantic_segmentation')
semantic_bp.set_attribute('image_size_x', str(IMAGE_WIDTH))
semantic_bp.set_attribute('image_size_y', str(IMAGE_HEIGHT))
semantic_bp.set_attribute('fov', '90')
semantic_bp.set_attribute('sensor_tick', str(SENSOR_TICK))

semantic_camera = world.spawn_actor(
    semantic_bp,
    camera_transform,
    attach_to=vehicle
)

print("Semantic segmentation camera attached.")

counter = {'rgb': 0, 'semantic': 0}


def save_rgb(image):
    if counter['rgb'] < MAX_FRAMES:
        filename = os.path.join(rgb_dir, '%06d.png' % counter['rgb'])
        image.save_to_disk(filename)

        if counter['rgb'] % 50 == 0:
            print("Saved RGB frame:", counter['rgb'])

        counter['rgb'] += 1


def save_semantic(image):
    if counter['semantic'] < MAX_FRAMES:
        filename = os.path.join(semantic_dir, '%06d.png' % counter['semantic'])
        image.save_to_disk(filename, carla.ColorConverter.CityScapesPalette)

        if counter['semantic'] % 50 == 0:
            print("Saved Semantic frame:", counter['semantic'])

        counter['semantic'] += 1


# 传感器每生成一帧，就调用对应保存函数
rgb_camera.listen(save_rgb)
semantic_camera.listen(save_semantic)

print("Collecting RGB and semantic images...")

while counter['rgb'] < MAX_FRAMES or counter['semantic'] < MAX_FRAMES:
    time.sleep(1)

rgb_camera.stop()
semantic_camera.stop()

rgb_camera.destroy()
semantic_camera.destroy()
vehicle.destroy()

print("Finished collecting dataset.")
print("Vehicle and sensors destroyed.")
print("RGB frames:", counter['rgb'])
print("Semantic frames:", counter['semantic'])
