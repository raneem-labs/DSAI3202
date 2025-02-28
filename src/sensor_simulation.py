#task 1 sensor simulation
import threading
import time
import random
from queue import Queue

latest_temperatures = {}
rlock = threading.RLock()

def simulate_sensor(sensor_id, queue): #func takes the id as a parameter which will be given in main
    while True: #infinte loop until user exits
        temperature = random.randint(15,40)
        with rlock: #we use lock here because this is the critical section where updates happen and we dont want the threads to collide 
            latest_temperatures[sensor_id] = temperature
           # print(f"sensor {sensor_id} : {temperature} degree C")
        queue.put((sensor_id, temperature))
        time.sleep(1) #every second a new temp is genertaed 
            


