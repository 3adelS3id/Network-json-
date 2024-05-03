import os
import math
import matplotlib.pyplot as plt
from ultralytics import YOLO
from roboflow import Roboflow
import google.generativeai as genai
import matplotlib.image as mpimg

# Initialize Roboflow
rf = Roboflow(api_key="gpBJORB7I5m5f5yWUmzk")
project = rf.workspace("floorplan-cvjp0").project("floorplan-9fxye")
version = project.version(1)
dataset = version.download("yolov8")

# Define dataset location
dataset_location = r"C:\Users\GREEN STORE\Downloads\Network-json--master\floorplan-1"
print(dataset_location)

# Read data.yaml content and remove unnecessary prefixes
with open(os.path.join(dataset_location, "data.yaml"), "r") as file:
    data_yaml = file.read()

updated_data_yaml = data_yaml.replace("floorplan-1/", "").replace("../", "")

# Write the updated content back to data.yaml
with open(os.path.join(dataset_location, "data.yaml"), "w") as file:
    file.write(updated_data_yaml)

# Load YOLO model
model1 = YOLO('best.pt')

# Function to get room information using YOLO
def get_rooms_info(image_source: str) -> list[dict]:
    results = model1.predict(image_source, save=False, imgsz=320, conf=0.5)
    rooms_info = []

    for box in results[0].boxes.xywh.cpu():
        x, y, w, h = box
        x_center = (x + w) / 2
        y_center = (y + h) / 2

        rooms_info.append({
            "width": w.item(),
            "height": h.item(),
            "location": (x_center.item(), y_center.item())
        })

    return rooms_info

# Configure Google Generative AI
genai.configure(api_key="AIzaSyDhqVElyxOKHaZ0eCkpvb3Hq_KGZo4tdeM")

# Load Gemini Pro model for text generation
model = genai.GenerativeModel("gemini-pro")

# Get room information from image
image_path = r"C:\Users\GREEN STORE\Downloads\Network-json--master\WhatsApp Image 2024-05-02 at 3.57.12 PM.jpeg"
rooms_info = get_rooms_info(image_path)

# Method to arrange data after the model
def arrange_office_info(rooms_info):
    offices = []
    
    for i, room in enumerate(rooms_info, start=1):
        office_name = f"office {i}"
        office_area = room["width"] * room["height"]
        office_location = room["location"]

        office_info = {
            "name": office_name,
            "area": office_area,
            "location": office_location
        }
        offices.append(office_info)

    return offices

# Get arranged office information
arranged_offices = arrange_office_info(rooms_info)

# Print the arranged office information
for office in arranged_offices:
    print(f"Office {office['name']}: Area={office['area']}, Location={office['location']}")

# Function to calculate Euclidean distance between two points
def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Function to calculate Euclidean distance between two points
def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Function to choose office from JSON data
def choose_office(office_data):
    offices = office_data["offices"]
    selected_office = None
    max_area = 0

    # Find the office with the largest area
    for office in offices:
        if office["area"] > max_area:
            max_area = office["area"]
            selected_office = office

    # Check if IT office is selected
    if selected_office["name"] != "IT":
        # Sort offices by area in descending order
        sorted_offices = sorted(offices, key=lambda x: x["area"], reverse=True)
        
        # Choose the office with the largest area (excluding IT office)
        it_room = sorted_offices[0]["name"]
        print(f"The IT room is {it_room}.")
    else:
        print("The IT office was selected.")

    # Calculate the number of switches needed
    num_offices = len(offices)
    num_switches = math.ceil(num_offices / 5)
    print(f"Number of switches needed: {num_switches}")

    # Determine nearest point to the IT room for each group of 5 offices
    switch_locations = {}
    switch_offices = {}  # Store offices associated with each switch
    for i in range(num_switches):
        # Determine the range of offices for this switch
        start_index = i * 5
        end_index = min((i + 1) * 5, num_offices)
        sorted_offices = sorted(offices, key=lambda x: x["area"], reverse=True)
        offices_subset = sorted_offices[start_index:end_index]

        # Calculate centroid of offices subset
        centroid_x = sum(office["location"][0] for office in offices_subset) / len(offices_subset)
        centroid_y = sum(office["location"][1] for office in offices_subset) / len(offices_subset)

        # Find the nearest point to the IT room
        nearest_point = None
        min_distance = float('inf')
        for office in offices_subset:
            distance = calculate_distance(office["location"], selected_office["location"])
            if distance < min_distance:
                min_distance = distance
                nearest_point = office["location"]

        # Store the coordinates for this switch
        switch_locations[i] = (int(nearest_point[0]), int(nearest_point[1]))  # Convert to integers
        
        # Store the offices for this switch
        switch_offices[i] = offices_subset

        print(f"Switch {i + 1} location: x1={int(nearest_point[0])}, y1={int(nearest_point[1])}")
        print(f"Offices for Switch {i + 1}:")
        for office in offices_subset:
            print(f"Name: {office['name']}, Area: {office['area']}, Location: {office['location']}")

    return switch_locations, switch_offices

# Call the function with the arranged office data
switch_locations, switch_offices = choose_office({"offices": arranged_offices})

# Load the image
image = mpimg.imread(image_path)

# Create a plot
plt.figure()
plt.axis('off')  # Turn off axis labels

# Show the image
plt.imshow(image)

# Plot each switch
for switch_num, (x1, y1) in switch_locations.items():
    plt.scatter(x1, y1, s=160, c='blue', marker='o')  
    # Add text label indicating the switch number
    plt.text(x1 + 10, y1 + 10, f"Switch {switch_num + 1}", fontsize=10, color='black')
     # Plot lines connecting the switch point to its corresponding offices
    for office in switch_offices[switch_num]:
        office_x, office_y = office["location"]
        plt.plot([x1, office_x], [y1, office_y], color='red', linestyle='--')
# Show the plot
plt.show()
