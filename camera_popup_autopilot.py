#!/usr/bin/env python
# coding: utf-8

# In[5]:


import carla
import random
import cv2
import numpy as np


# In[6]:


client = carla.Client('localhost', 2000)


# In[7]:


client.load_world('Town02')


# In[17]:


world = client.get_world()
spawn_points = world.get_map().get_spawn_points()


# In[18]:


vehicle_bp = world.get_blueprint_library().filter('*vehicle*')


# In[19]:


start_point = random.choice(spawn_points)
vehicle = world.try_spawn_actor(vehicle_bp[0], start_point)


# In[20]:


spectator = world.get_spectator()
start_point.location.z = start_point.location.z+1
spectator.set_transform(start_point)


# In[12]:


vehicle.set_autopilot(True)


# In[13]:


CAMERA_POS_Z = 1.6
CAMERA_POS_X = 0.9

camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
camera_bp.set_attribute('image_size_x', '640')
camera_bp.set_attribute('image_size_y', '360')
camera_init_trans = carla.Transform(carla.Location(z=CAMERA_POS_Z, x=CAMERA_POS_X))
camera = world.spawn_actor(camera_bp, camera_init_trans, attach_to=vehicle)

def camera_callback(image, data_dict):
    data_dict['image'] = np.reshape(np.copy(image.raw_data),(image.height, image.width, 4))

image_w = camera_bp.get_attribute('image_size_x').as_int()
image_h = camera_bp.get_attribute('image_size_y').as_int()

camera_data = {'image' : np.zeros((image_h, image_w, 4))}
camera.listen(lambda image: camera_callback(image, camera_data))


# In[14]:


img = camera_data['image']
cv2.imshow('RGB Camera', img)
cv2.waitKey(0)


# In[25]:


camera.stop()
for actor in world.get_actors().filter('*vehicle*'):
    actor.destroy()
for sensor in world.get_actors().filter('*sensor*'):
    sensor.destroy()


# In[ ]:





# In[ ]:




