#!/usr/bin/env python
# coding: utf-8

# In[33]:


import carla
import random

client = carla.Client('localhost', 2000)
world = client.get_world()


# In[62]:


client.load_world('Town02')


# In[85]:


spawn_points = world.get_map().get_spawn_points()
start_point = random.choice(spawn_points)
spectator = world.get_spectator()
spectator.set_transform(start_point)


# In[86]:


vehicle_blueprints = world.get_blueprint_library().filter('*vehicle*')
ego_vehicle = world.try_spawn_actor(random.choice(vehicle_blueprints), start_point)


# In[88]:


camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
camera_init_trans = carla.Transform(carla.Location(z=1.5))
camera = world.spawn_actor(camera_bp, camera_init_trans, attach_to=ego_vehicle)
#camera.listen(lambda image: image.save_to_disk('out/%06d.png' % image.frame))


# In[54]:


ego_vehicle.set_autopilot(True)


# In[89]:


camera.stop()
for actor in world.get_actors().filter('*vehicle*'):
    actor.destroy()
for sensor in world.get_actors().filter('*sensor*'):
    sensor.destroy()


# In[ ]:




