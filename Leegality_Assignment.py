# Leegality Python developer assignment
"""
Assumptions Made:
1. I'm assuming that both the levels have parking spots corresponding to each other,
   which means if a car has to find the nearest parking spot, it will consider both the levels simultaneously.
   If both A1 and B21 are empty, A1 will be preferred over B21.
2. There is only 1 entry point to the parking lot, that is from the side where Parking spots 1 and 21 are reserved.
3. Vehicle Number is a unique string consisting of 5 literals, a character and 4 integers denoting the license plate no.
   It's not a requirement, however, makes easier to keep track of the vehicles parked.
"""
import json


class ParkingLot:
    def __init__(self):
        self.levels = {'A': [None] * 20, 'B': [None] * 20}  # Parking lot structure
        self.parked_vehicles = {}  # To store all the parked vehicles

    def save_structure(self, filename='parking_lot_structure.json'):
        structure = {'levels': self.levels, 'parked_vehicles': self.parked_vehicles}
        with open(filename, 'w') as file:
            json.dump(structure, file)

    def load_structure(self, filename='parking_lot_structure.json'):
        try:
            with open(filename, 'r') as file:
                state = json.load(file)
                self.levels = state.get('levels', {'A': [None] * 20, 'B': [None] * 20})
                self.parked_vehicles = state.get('parked_vehicles', {})
        except FileNotFoundError:
            pass  # No previous structure found, use default

    def get_nearest_parking_spot(self):
        for spot, vehicle in enumerate(zip(self.levels['A'], self.levels['B']), start=1):
            if vehicle[0] is None:
                return {'level': 'A', 'spot': spot}
            elif vehicle[1] is None:
                return {'level': 'B', 'spot': spot + 20}

        return None  # Parking Lot is full

    def assign_parking_spot(self, vehicle_num):
        if vehicle_num in self.parked_vehicles:
            # Vehicle is already parked.
            vehicle_dict = self.retrieve_parking_spot(vehicle_num)
            vehicle_dict['already_exists'] = True
            return vehicle_dict
        vehicle_dict = self.get_nearest_parking_spot()
        if vehicle_dict is not None:
            self.levels[vehicle_dict['level']][vehicle_dict['spot'] - 1 if vehicle_dict['level'] == 'A' else vehicle_dict['spot'] - 21] = vehicle_num
            self.parked_vehicles[vehicle_num] = vehicle_dict
            return vehicle_dict

        return None  # Parking Lot is full

    def unpark_vehicle(self, vehicle_num):
        if vehicle_num in self.parked_vehicles:
            level = self.parked_vehicles[vehicle_num]['level']
            spot = self.parked_vehicles[vehicle_num]['spot']
            self.levels[level][spot - 1 if level == 'A' else spot - 21] = None
            del self.parked_vehicles[vehicle_num]
            return {'level': level, 'spot': spot}

    def retrieve_parking_spot(self, vehicle_number):
        if vehicle_number in self.parked_vehicles:
            return self.parked_vehicles[vehicle_number]
        else:
            return None  # Vehicle not found in the parking lot


def main():
    parking_lot = ParkingLot()
    parking_lot.load_structure()  # Load previous structure if available

    print("<--------Leegality Parking Lot-------->")
    while True:
        print("\n1. Assign Parking Spot")
        print("2. Retrieve Parking Spot")
        print("3. Unpark Vehicle")
        print("4. Get Nearest Parking Spot")
        print("5. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            vehicle_number = input("Enter vehicle number: ")
            result = parking_lot.assign_parking_spot(vehicle_number)
            try:
                if result['already_exists']:
                    print(f"Vehicle is already parked at Level {result['level']}, Spot {result['spot']}")
            except KeyError:
                if result:
                    print(f"Vehicle parked at Level {result['level']}, Spot {result['spot']}")
                else:
                    print("Parking lot is full.")

        elif choice == 2:
            vehicle_number = input("Enter vehicle number: ")
            result = parking_lot.retrieve_parking_spot(vehicle_number)
            if result:
                print(f"Vehicle is parked at Level {result['level']}, Spot {result['spot']}")
            else:
                print("Vehicle not found in the parking lot.")

        elif choice == 3:
            vehicle_number = input("Enter vehicle number: ")
            result = parking_lot.unpark_vehicle(vehicle_number)
            if result:
                print(f"Vehicle unparked from Level {result['level']}, Spot {result['spot']}")
            else:
                print("Vehicle not found in the parking lot.")

        elif choice == 4:
            result = parking_lot.get_nearest_parking_spot()
            if result:
                print(f"The nearest parking spot is at Level {result['level']}, Spot {result['spot']}")
            else:
                print("Parking lot is full.")

        elif choice == 5:
            parking_lot.save_structure()  # Save the current state before exiting
            break


if __name__ == "__main__":
    main()
