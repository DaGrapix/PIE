import game
import math
from shapely.geometry import Point, Polygon

# Compute the distance between a drone and a zone
# Return : the distance
def computeDistance(drone, zone) :
    rect = Polygon(zone)
    drone_pos = (drone.position.x, drone.position.y)
    point = Point(drone_pos)
    return rect.distance(point)


# Assigns each drone to a zone
# Return :  - assignment_list : a list of couples (drone, zone assigned)
#           - list(set(drones_list) - set(assigned_drones)) : left drones (if number of drones > number of zones)
#           - zones_list : left zones (if number of zones > number of drones)
def assignment(drones_list, zones_list) :
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
            print("Assignment list append :", drone.position, ", ", zone_min)
            assignment_list.append((drone, zone_min))
    return assignment_list, list(set(drones_list) - set(assigned_drones)), zones_list

def main() :
    drone_1 = game.Drone(0, 0)
    drone_2 = game.Drone(100, 100)
    zone_1 = [[2, 4], [3, 4], [2, 7], [3, 7]]
    zone_2 = [[125, 125], [190, 125], [125, 300], [125, 300]]
    zone_3 = [[300, 300], [400, 300], [300, 500], [300, 500]]
    a, b, c  = assignment([drone_1, drone_2], [zone_2])
    print("\nAssignment list :", a,"\nLeft drones :", b,"\nLeft zones", c)
    
if __name__ == '__main__':
    main()





'''
# Importer les modules nécessaires
import math

# Définir la fonction first_last_waypoint
def first_last_waypoint(trajectories_left, current_position):
    start = current_position
    end = trajectories_left[0][-1]
    total_path_length = math.dist(start, end)
    return [start, 
            total_path_length]

# Initialiser les variables
trajectories_num = len(trajectories_total)
trajectories_assigned = []
trajectories_left = [i for i in range(1, trajectories_num + 1)]

total_path_length = []
current_positions = [0 for i in range(n_drones)]

# Boucle principale
while trajectories_assigned != trajectories_total:
    # Parcourir tous les drones
    for i in range(n_drones):
        # Vérifier si toutes les trajectoires ont été assignées
        if not trajectories_left:
            break
        # Trouver la trajectoire avec la longueur la plus courte
        min_length = min(total_path_length)
        min_index = total_path_length.index(min_length)
        # Assigner la trajectoire au drone correspondant
        drone_index = min_index % n_drones
        trajectory_index = trajectories_left.pop(min_index // n_drones)
        trajectories_assigned.append(trajectory_index)
        current_positions[drone_index] = trajectories_total[trajectory_index - 1][-1]
        # Mettre à jour les longueurs de chemin
        total_path_length.pop(min_index)
        for j in range(len(trajectories_left)):
            start = current_positions[drone_index]
            end = trajectories_total[trajectories_left[j] - 1][-1]
            total_path_length[j] = first_last_waypoint([trajectories_left[j]], start)[1] + math.dist(start, end)
    # Construire ou mettre à jour les trajectoires finales
    # Mettre à jour les positions actuelles des drones
    # Mettre à jour les trajectoires restantes
'''
