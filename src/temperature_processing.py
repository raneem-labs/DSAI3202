#3.b process tempretures 
import threading
from queue import Queue
import time
#global dict
latest_tempratures = {}
temperature_averages = {}
rlock = threading.RLock() 
condition = threading.Condition()

#lock 
lock = threading.Lock()


def process_temperatures(queue):
    #create 2 local dict to store the data and the count that we use to calc the avg
    sensor_data = {}
    sensor_counts= {}

    while True: 
        sensor_id , temperature = queue.get()
        #we start updating the dict so need locks
        with rlock:
            if sensor_id not in sensor_data:
                sensor_data[sensor_id] = 0 
                sensor_counts[sensor_id]=0 
            sensor_data[sensor_id] += temperature
            sensor_counts[sensor_id] += 1

            temperature_averages[sensor_id] = sensor_data[sensor_id]/sensor_counts[sensor_id]

            #print(f"average for {sensor_id}: {temperature_averages[sensor_id]: .2f}°C ")
        # Notify the main thread to update the display
        with condition:
            condition.notify()
        queue.task_done()
        time.sleep(5)

            