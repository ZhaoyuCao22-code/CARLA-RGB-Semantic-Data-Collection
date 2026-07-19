import carla
import random
import time

# 连接 CARLA，获取当前世界和蓝图库
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

world = client.get_world()
blueprint_library = world.get_blueprint_library()

# 随机生成一辆车
vehicle_blueprints = blueprint_library.filter('vehicle.*')
vehicle_bp = random.choice(vehicle_blueprints)

spawn_points = world.get_map().get_spawn_points()
spawn_point = random.choice(spawn_points)

vehicle = world.spawn_actor(vehicle_bp, spawn_point)

print("Vehicle spawned successfully.")
print("Vehicle type:", vehicle_bp.id)
print("Vehicle id:", vehicle.id)

# 开启自动驾驶
vehicle.set_autopilot(True)
print("Autopilot enabled. Vehicle will drive for 30 seconds.")

# 让观察视角跟随车辆，便于观察行驶过程
spectator = world.get_spectator()

for i in range(30):
    transform = vehicle.get_transform()
    location = transform.location

    spectator.set_transform(
        carla.Transform(
            location + carla.Location(x=-8, z=5),
            carla.Rotation(pitch=-20, yaw=transform.rotation.yaw)
        )
    )

    print("Time:", i + 1, "seconds")
    time.sleep(1)

vehicle.set_autopilot(False)
vehicle.destroy()

print("Vehicle destroyed.")
