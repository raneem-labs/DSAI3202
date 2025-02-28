
# lab4 part1 
1) Which synchronization metric did you use for each of the tasks?

For the task of simulating sensor data, I used RLock to synchronize access to shared data, particularly the latest_temperatures dictionary. I placed the lock inside the loop because the critical section, where the shared data is modified, occurs within it. This ensures that only one thread can update the shared resource at a time. By doing this inside the loop, I avoid locking the entire function, which would include unnecessary parts such as the time.sleep() and the print statement, potentially causing other threads to be blocked and leading to delays in execution.

For controlling when the display is updated, I used Condition to synchronize the display thread with the processing thread. This allows the processing thread to signal when the averages are updated, and the main thread waits for this signal before calling update_display().



2) Why did the professor not ask you to compute metrics?

The professor did not ask us to compute performance metrics because the focus of this lab was on understanding and implementing the correct synchronization mechanisms rather than measuring the performance or efficiency of the program. The primary goal was to ensure that the threads work properly together without causing data inconsistencies or race conditions, which is why we concentrated on using locks like RLock and managing thread synchronization using Condition. Metrics, such as time taken for each operation or memory usage, were not the main concern here since the task was to simulate sensor data and calculate averages, with a particular emphasis on managing concurrent threads efficiently.
