#main 
import threading
import time
from queue import Queue
from display_logic import initialize_display, update_display
from sensor_simulation import simulate_sensor
from temperature_processing import process_temperatures


def main():
    """Main function to start the simulation and synchronize threads."""
    # Queue for transferring data between threads
    queue = Queue()
    
    # Condition for synchronization between processing and display
    condition = threading.Condition()

    # Initialize display
    initialize_display()

    # Start sensor threads
    sensor_threads = []
    for i in range(3):
        thread = threading.Thread(target=simulate_sensor, args=(i, queue))
        thread.daemon = True
        sensor_threads.append(thread)
        thread.start()

    # Start the processing thread
    processing_thread = threading.Thread(target=process_temperatures, args=(queue, condition))
    processing_thread.daemon = True
    processing_thread.start()

    try:
        while True:
            # Main thread waits for the signal from the processing thread
            with condition:
                condition.wait()  # Wait for the signal to update the display
                update_display()  # Update the display
            time.sleep(1)  # Sleep to avoid rapid looping
    except KeyboardInterrupt:
        print("\nSimulation stopped.")

if __name__ == "__main__":
    main()