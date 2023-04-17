import game
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point, LineString




def divide_ring_zone(center, inner_radius, outer_radius, nb_zones):
    '''Divides a ring zone into multiple sub zones
    
    Args:
         center (tuple): center of the ring
         inner_radius (float): radius of the inner circle of the ring
         outer_radius (float): radius of the outer cirlce of the ring
         nb_zones (int)
    Returns:
         sub_zones (3 dimension float list): list of sub zones outline coordinates
    '''
    center = Point(center[0], center[1])
    inner_circle = center.buffer(inner_radius)
    outer_circle = center.buffer(outer_radius)

    # Divide inner and outer circle in nb_zones near equal parts
    sub_arrays_inner = np.array_split(inner_circle.exterior.coords, nb_zones)
    sub_arrays_outer = np.array_split(outer_circle.exterior.coords, nb_zones)
    # Add connection points to sub arrays 
    for i in range(nb_zones) :
        sub_arrays_inner[i] = np.concatenate((sub_arrays_inner[i], [sub_arrays_inner[(i+1)%nb_zones][0]]), axis=0)
        sub_arrays_outer[i] = np.concatenate((sub_arrays_outer[i], [sub_arrays_outer[(i+1)%nb_zones][0]]), axis=0)
        
    # Sub zones creation
    sub_zones = []
    for i in range(nb_zones):
        # Concatenate outer circle part with the corresponding inner circle part to create the sub zone
        concat = np.concatenate((np.flip(sub_arrays_inner[i], axis=0), sub_arrays_outer[i]))
        sub_zone = Polygon(concat)
        # Coords of sub zone
        zone_coords = []
        for coord in sub_zone.exterior.coords:
            zone_coords.append([coord[0], coord[1]])
        sub_zones.append(zone_coords)
    return sub_zones




def computeDistance(drone, zone) :
    '''Computes the distance between a drone and a zone

    Args:
          drone (Drone): a drone
          zone (2 dimension float list): list of zone outline coordinates
    
    Returns:
          rect.distance(point) (float): min distance between drone and zone
    '''
    rect = Polygon(zone)
    drone_pos = (drone.position.x, drone.position.y)
    point = Point(drone_pos)
    return rect.distance(point)




def assignment(drones_list, zones_list) :
    '''Assigns each drone to a zone

    Args:
          drones_list (Drone list): list of drones
          zones_list (3 dimension float list): list of zones outline coordinates

    Returns:
          assignment_list (tuple (Drone, 2 dimension float list)): list of couples (drone, zone assigned)
          list(set(drones_list) - set(assigned_drones)) (2 dimension Drone list): list of unassigned drones (if number of drones > number of zones)
          zones_list (3 dimension float list): list of unassigned zones outline coordinates (if number of zones > number of drones)
    '''
    if not drones_list or not zones_list :
        print("No drone or no zone for assignment")
    assignment_list = []
    assigned_drones = []
    for drone in drones_list :
        if zones_list : 
            d_min = computeDistance(drone, zones_list[0])
            zone_min = zones_list[0]
            for zone in zones_list :
                d = computeDistance(drone, zone)
                if d < d_min :
                    d_min = d
                    zone_min = zone
            zones_list.remove(zone_min)
            assigned_drones.append(drone)
            assignment_list.append((drone, zone_min))
    return assignment_list, list(set(drones_list) - set(assigned_drones)), zones_list




def print_assignment(assignment_list, left_drones_list, left_zones_list) :
    '''Prints the result of the assignement

    Args:
         assignment_list (tuple (Drone, 2 dimension list)): list of couples (drone, zone assigned)
         left_drones_list (2 dimension float list): list of unassigned drones (if number of drones > number of zones)
         left_zones_list (3 dimension float list): list of unassigned zones outline coordinates (if number of zones > number of drones)

    Returns:
    '''
    no_of_colors = len(assignment_list)
    color = ["#"+''.join([random.choice('123456789ABCDEF') for i in range(6)]) for j in range(no_of_colors)]
    for i, (drone, zone) in enumerate(assignment_list) :
        print(i)
        plt.plot(drone.position.x, drone.position.y, marker ='1', c=color[i])
        x_coords = []
        y_coords = []
        for (x, y) in zone :
            x_coords.append(x)
            y_coords.append(y)
        plt.plot(x_coords, y_coords, c=color[i])
    for drone in left_drones_list :
        plt.scatter(drone.position.x, drone.position.y, marker='1', c='black')
    for zone in left_zones_list :
        x_coords = []
        y_coords = []
        for (x, y) in zone :
            x_coords.append(x)
            y_coords.append(y)
        plt.plot(x_coords, y_coords, c='black')
    plt.show()


    

def main() :
    
    drone_1 = game.Drone(0, 0)
    drone_2 = game.Drone(10, 10)
    drone_3 = game.Drone(0, 20)
    zone_1 = [[2, 4], [3, 4], [2, 7], [3, 7]]
    zone_2 = [[125, 125], [190, 125], [125, 300], [125, 300]]
    zone_3 = [[300, 300], [400, 300], [300, 500], [300, 500]]
    zone_list = divide_ring_zone((0.,0.), 3., 5., 2)
    a, b, c  = assignment([drone_1, drone_2, drone_3], zone_list)
    #print("\nAssignment list :", a,"\nLeft drones :", b,"\nLeft zones", c)
    print_assignment(a, b, c)
    
    
    
if __name__ == '__main__':
    main()



