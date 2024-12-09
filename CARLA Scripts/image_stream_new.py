import carla
import random
import time
import os

# Connect to the CARLA server and load the desired world
client = carla.Client('localhost', 2000)
client.load_world('Town02')
world = client.get_world()

# Set up vehicle spawn
spawn_points = world.get_map().get_spawn_points()
vehicle_bp = world.get_blueprint_library().filter('*vehicle*')
start_point = random.choice(spawn_points)
ego_vehicle = world.try_spawn_actor(vehicle_bp[0], start_point)

# Ensure the vehicle was spawned
if not ego_vehicle:
    raise RuntimeError("Failed to spawn ego vehicle.")

# Set spectator view
spectator = world.get_spectator()
start_point.location.z += 1
spectator.set_transform(start_point)

# Enable autopilot
ego_vehicle.set_autopilot(True)

# Camera configuration
camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
camera_bp.set_attribute('image_size_x', '640')
camera_bp.set_attribute('image_size_y', '640')
camera_init_trans = carla.Transform(carla.Location(z=2))  # Camera 2 meters above the car

# Attach camera to vehicle
camera = world.try_spawn_actor(camera_bp, camera_init_trans, attach_to=ego_vehicle)

# Check if the camera was successfully created
if not camera:
    print("Failed to spawn camera.")
    # Clean up the vehicle before exiting
    ego_vehicle.destroy()
    exit(1)

# Ensure output folder exists
output_folder = "out"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Start listening to the camera and save images
camera.listen(lambda image: image.save_to_disk(os.path.join(output_folder, '%06d.png' % image.frame)))

# Run the simulation for a limited time to capture images
try:
    time.sleep(80)  # Adjust the duration as needed
finally:
    # Clean up actors
    if camera:  # Only stop and destroy if the camera was successfully created
        camera.stop()
        camera.destroy()
    if ego_vehicle:  # Ensure vehicle is destroyed
        ego_vehicle.destroy()
    print("Simulation ended and actors cleaned up.")
