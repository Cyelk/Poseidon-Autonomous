autopilot.py<br />
Simple CARLA code to spawn desired city, random vehicle in random place in the map (after positioning spectator's viewpoint in the same place) and set the vehicle on a simple autopilot course.

camera_popup_autopilot.py<br />
Videos used to set up Carla and its components as well as run the first Simulation. In Town02, a vehicle is spawned on a random spawn point on the map and the spectator is spawned on top of it. A camera is set
on the car and a function is implemented where the car can snap a screenshot of what it sees at any given moment on command (Button R on keyboard), image popping up in a new window as it does. The car follows 
along the roads on the map, set on autopilot.<br />
References:<br />
https://youtu.be/jIK9sanumuU?si=yo2jnGU-uBDmStN8<br />
https://youtu.be/zZ8s_qrKYGE?si=SEPAg7VhxovqVnzF<br />
https://youtu.be/ATNNdKCqHPA?si=bB_g6Z-iDu1L8aZ7<br />

image_stream_autopilot.py<br />
In Town02, the spectator can spawn on any random point on the map every execution, and the vehicle will spawn upon them in the same way as the previous codes. From there, a camera is attached to the
vehicle that takes input from what the car sees in real time as the car travels in autopilot, and saves the input in png form in the specified folder in the disk.<br />
References:<br />
https://carla.readthedocs.io/en/latest/tuto_first_steps/<br />
