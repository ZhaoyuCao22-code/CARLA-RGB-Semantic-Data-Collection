import carla
import random
import time
import os

# 最终使用的小批量采集参数
BATCH_FRAMES = 50
IMAGE_WIDTH = 320
IMAGE_HEIGHT = 180
SENSOR_TICK = 2.0   # 每 2 秒采 1 帧，降低 CARLA 运行压力

client = carla.Client('localhost', 2000)
client.set_timeout(20.0)

world = client.get_world()
blueprint_library = world.get_blueprint_library()

# 数据保存路径
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')

rgb_dir = os.path.join(data_dir, 'rgb')
semantic_dir = os.path.join(data_dir, 'semantic')

os.makedirs(rgb_dir, exist_ok=True)
os.makedirs(semantic_dir, exist_ok=True)

# 从两个文件夹共同拥有的编号继续采集，保持 RGB 和 semantic 配对
rgb_files = [f for f in os.listdir(rgb_dir) if f.endswith('.png')]
semantic_files = [f for f in os.listdir(semantic_dir) if f.endswith('.png')]

start_index = min(len(rgb_files), len(semantic_files))
end_index = start_index + BATCH_FRAMES

print("Current RGB frames:", len(rgb_files))
print("Current Semantic frames:", len(semantic_files))
print("Start index:", start_index)
print("This batch will collect:", start_index, "to", end_index - 1)

# 优先选择普通乘用车，避免随机生成摩托车
vehicle_candidates = blueprint_library.filter('vehicle.toyota.prius')

if len(vehicle_candidates) == 0:
    vehicle_candidates = blueprint_library.filter('vehicle.tesla.model3')

if len(vehicle_candidates) == 0:
    vehicle_candidates = blueprint_library.filter('vehicle.*')

vehicle_bp = vehicle_candidates[0]

spawn_points = world.get_map().get_spawn_points()
spawn_point = random.choice(spawn_points)

vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)

if vehicle is None:
    print("Failed to spawn vehicle.")
    exit()

vehicle.set_autopilot(True)

print("Vehicle spawned:", vehicle_bp.id)
print("Autopilot enabled.")

# RGB 和 semantic 摄像头使用相同位置
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

print("Semantic camera attached.")

counter = {
    'rgb': start_index,
    'semantic': start_index
}


def save_rgb(image):
    if counter['rgb'] < end_index:
        filename = os.path.join(rgb_dir, '%06d.png' % counter['rgb'])
        image.save_to_disk(filename)

        print("Saved RGB frame:", counter['rgb'])
        counter['rgb'] += 1


def save_semantic(image):
    if counter['semantic'] < end_index:
        filename = os.path.join(semantic_dir, '%06d.png' % counter['semantic'])
        image.save_to_disk(filename, carla.ColorConverter.CityScapesPalette)

        print("Saved Semantic frame:", counter['semantic'])
        counter['semantic'] += 1


rgb_camera.listen(save_rgb)
semantic_camera.listen(save_semantic)

print("Collecting small batch...")

while counter['rgb'] < end_index or counter['semantic'] < end_index:
    time.sleep(1)

# 停止传感器后稍等片刻，再销毁相关 actor
rgb_camera.stop()
semantic_camera.stop()

time.sleep(2)

rgb_camera.destroy()
semantic_camera.destroy()
vehicle.destroy()

print("Finished one small batch.")
print("Vehicle and sensors destroyed.")
print("RGB frames now:", counter['rgb'])
print("Semantic frames now:", counter['semantic'])
