#display logic
import sys 
latest_temperatures = {}
temperature_averages = {}

def initialize_display():
    print("Current Temperatures: ")
    print("Latest Tempretures: ")

    for i in range(3):
        print(f" Sensor{i} : --°C")
    
    print("\nAverages:")
    for i in range(3):
        print(f"Sensor {i} Average: --°C")

#update display without deleting counsle 
def update_display():
    sys.stdout.write("\033[7A") 
    sys.stdout.flush()

    for i in range(3):
        sys.stdout.write(f" Sensor {i} : {latest_temperatures.get(i, '--')} C\n")
    sys.stdout.write("\n")

    for i in range(3):
        sys.stdout.write(f"Sensor {i} Average: {temperature_averages.get(i, '--')}}°C\n")

    sys.stdout.flush()