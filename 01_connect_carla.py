import carla

# 连接 CARLA，并读取当前仿真环境
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

world = client.get_world()
carla_map = world.get_map()
vehicles = world.get_actors().filter('vehicle.*')

print("CARLA connected successfully.")
print("Current map:", carla_map.name)
print("Number of vehicles:", len(vehicles))
