import carla
import random
import time
import os

# 连接 CARLA，获取当前世界和蓝图库
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

world = client.get_world()
blueprint_library = world.get_blueprint_library()

# 生成一辆车并开启自动驾驶
vehicle_blueprints = blueprint_library.filter('vehicle.*')
vehicle_bp = random.choice(vehicle_blueprints)

spawn_points = world.get_map().get_spawn_points()
spawn_point = random.choice(spawn_points)

vehicle = world.spawn_actor(vehicle_bp, spawn_point)
print("Vehicle spawned:", vehicle_bp.id)

vehicle.set_autopilot(True)
print("Autopilot enabled.")

# 配置 RGB 摄像头
camera_bp = blueprint_library.find('sensor.camera.rgb')
camera_bp.set_attribute('image_size_x', '640')
camera_bp.set_attribute('image_size_y', '360')
camera_bp.set_attribute('fov', '90')
camera_bp.set_attribute('sensor_tick', '0.5')

# 将摄像头安装在车辆前上方
camera_transform = carla.Transform(
    carla.Location(x=1.5, z=2.4),
    carla.Rotation(pitch=0)
)

camera = world.spawn_actor(
    camera_bp,
    camera_transform,
    attach_to=vehicle
)

print("Camera sensor attached.")

# 使用相对路径保存采集结果
script_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(script_dir, '..', 'data', 'rgb')

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

print("Images will be saved to:", save_dir)

counter = {'num': 0}
max_images = 30


def save_image(image):
    if counter['num'] < max_images:
        filename = os.path.join(save_dir, '%06d.png' % counter['num'])
        image.save_to_disk(filename)
        print("Saved image:", filename)
        counter['num'] += 1


camera.listen(save_image)
print("Camera is collecting images...")

while counter['num'] < max_images:
    time.sleep(1)

# 停止传感器并清理 actor
camera.stop()
camera.destroy()
vehicle.destroy()

print("Finished collecting images.")
print("Vehicle and camera destroyed.")
