#!/usr/bin/env python
# coding: utf-8

# In[2]:


import carla
import random
import cv2
import numpy as np


# In[3]:


client = carla.Client('localhost', 2000)


# In[4]:


client.load_world('Town02')


# In[5]:


world = client.get_world()
spawn_points = world.get_map().get_spawn_points()


# In[ ]:


vehicle_bp = world.get_blueprint_library().filter('*vehicle*')


# In[ ]:


start_point = random.choice(spawn_points)
vehicle = world.try_spawn_actor(vehicle_bp[0], start_point)


# In[ ]:


spectator = world.get_spectator()
start_point.location.z = start_point.location.z+1
spectator.set_transform(start_point)


# In[ ]:


vehicle.set_autopilot(True)


# In[ ]:


camera.stop()
for actor in world.get_actors().filter('*vehicle*'):
    actor.destroy()
for sensor in world.get_actors().filter('*sensor*'):
    sensor.destroy()

