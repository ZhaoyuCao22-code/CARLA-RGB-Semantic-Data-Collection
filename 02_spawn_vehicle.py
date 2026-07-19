import carla
import random
import time

# 连接 CARLA，获取当前世界和蓝图库
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

world = client.get_world()
blueprint_library = world.get_blueprint_library()

# 随机选择车辆和出生点
vehicle_blueprints = blueprint_library.filter('vehicle.*')
vehicle_bp = random.choice(vehicle_blueprints)

spawn_points = world.get_map().get_spawn_points()
spawn_point = random.choice(spawn_points)

vehicle = world.spawn_actor(vehicle_bp, spawn_point)

print("Vehicle spawned successfully.")
print("Vehicle type:", vehicle_bp.id)
print("Vehicle id:", vehicle.id)

# 将观察视角放到车辆上方，方便查看生成结果
spectator = world.get_spectator()
spectator.set_transform(
    carla.Transform(
        spawn_point.location + carla.Location(z=30),
        carla.Rotation(pitch=-90)
    )
)

time.sleep(20)

# 结束后销毁车辆，避免 actor 残留
vehicle.destroy()
print("Vehicle destroyed.")
