#!/usr/bin/env python
# coding: utf-8

# In[19]:


import sys
import json
import numpy as np
import os

EPS = 1.0e-2
color_names = ['antique_white', 'azure', 'bisque', 'blanched_almond', 'cornsilk', 'eggshell', 'floral_white', 'gainsboro',
                       'ghost_white', 'honeydew', 'ivory', 'lavender', 'lavender_blush', 'lemon_chiffon', 'linen', 'mint_cream',
                       'misty_rose', 'moccasin', 'navajo_white', 'old_lace', 'papaya_whip', 'peach_puff', 'seashell', 'snow',
                       'thistle', 'titanium_white', 'wheat', 'white', 'white_smoke', 'zinc_white','cold_grey', 'dim_grey', 
                       'grey', 'light_grey', 'slate_grey', 'slate_grey_dark', 'slate_grey_light', 'warm_grey', 
                       'black', 'ivory_black', 'lamp_black', 'alizarin_crimson', 'brick', 'cadmium_red_deep', 'coral',
                       'coral_light', 'deep_pink', 'english_red', 'firebrick','geranium_lake', 'hot_pink', 'indian_red', 
                       'light_salmon', 'madder_lake_deep', 'maroon', 'pink', 'pink_light', 'raspberry', 'red', 'rose_madder', 
                       'salmon', 'tomato', 'venetian_red', 'beige', 'brown', 'brown_madder', 'brown_ochre', 'burlywood', 
                       'burnt_sienna', 'burnt_umber', 'chocolate', 'deep_ochre', 'flesh', 'flesh_ochre', 'gold_ochre',
                       'greenish_umber', 'khaki', 'khaki_dark', 'light_beige', 'peru', 'rosy_brown', 'raw_sienna', 'raw_umber', 
                       'sepia', 'sienna', 'saddle_brown', 'sandy_brown', 'tan', 'van_dyke_brown', 'cadmium_orange', 
                       'cadmium_red_light', 'carrot','dark_orange', 'mars_orange', 'mars_yellow', 'orange', 'orange_red', 
                       'yellow_ochre', 'aureoline_yellow', 'banana', 'cadmium_lemon','cadmium_yellow', 'cadmium_yellow_light', 
                       'gold', 'goldenrod', 'goldenrod_dark', 'goldenrod_light', 'goldenrod_pale', 'light_goldenrod', 
                       'melon', 'naples_yellow_deep', 'yellow', 'yellow_light', 'chartreuse', 'chrome_oxide_green', 
                       'cinnabar_green', 'cobalt_green', 'emerald_green', 'forest_green', 'green', 'green_dark', 'green_pale', 
                       'green_yellow', 'lawn_green', 'lime_green', 'mint', 'olive', 'olive_drab', 'olive_green_dark', 
                       'permanent_green', 'sap_green', 'sea_green', 'sea_green_dark', 'sea_green_medium', 'sea_green_light', 
                       'spring_green', 'spring_green_medium', 'terre_verte', 'viridian_light', 'yellow_green', 'aquamarine', 
                       'aquamarine_medium', 'cyan', 'cyan_white', 'turquoise', 'turquoise_dark', 'turquoise_medium',
                       'turquoise_pale', 'alice_blue', 'blue', 'blue_light', 'blue_medium', 'cadet', 'cobalt', 'cornflower', 
                       'cerulean', 'dodger_blue', 'indigo', 'manganese_blue', 'midnight_blue', 'navy', 'peacock', 'powder_blue',
                       'royal_blue', 'slate_blue', 'slate_blue_dark', 'slate_blue_light', 'slate_blue_medium', 'sky_blue', 
                       'sky_blue_deep', 'sky_blue_light', 'steel_blue', 'steel_blue_light', 'turquoise_blue', 'ultramarine', 
                       'blue_violet', 'cobalt_violet_deep', 'magenta', 'orchid', 'orchid_dark', 'orchid_medium',
                       'permanent_red_violet', 'plum', 'purple', 'purple_medium', 'ultramarine_violet', 'violet',
                       'violet_dark', 'violet_red', 'violet_red_medium', 'violet_red_pale'
                  ]

# =============================================================================================================================
# =============================================================================================================================
# =============================================================================================================================
# =============================================================================================================================
# Some stuff for balls position creation 

def make_position(boundary_coord, radius):
    radius += EPS
    return np.array([np.random.uniform(low = (boundary_coord['x_min'] + radius), high = boundary_coord['x_max'] - radius),                      np.random.uniform(low = (boundary_coord['y_min'] + radius), high = boundary_coord['y_max'] - radius),                      np.random.uniform(low = (boundary_coord['z_min'] + radius), high = boundary_coord['z_max'] - radius)])

def make_velocity(min_velocity, max_velocity):
    velocity_norm = np.random.uniform(low = min_velocity, high = max_velocity)
    velocity = np.random.uniform(low = -1.0, high = 1.0, size = 3)
    velocity = velocity / np.sqrt(velocity.dot(velocity)) * velocity_norm
    return velocity

def define_sphere_properties(balls_count, min_radius, max_radius, min_mass, max_mass, min_velocity, max_velocity, boundary_coords):
    positions = [np.array([(boundary_coords['x_max']+boundary_coords['x_min'])/2.0, 
                           (boundary_coords['y_max']+boundary_coords['y_min'])/2.0, 
                           (boundary_coords['z_max']+boundary_coords['z_min'])/2.0])]
    radii = [np.random.uniform(low = min_radius, high = max_radius)]
    masses = [np.random.uniform(low = min_mass, high = max_mass)]
    velocities = [make_velocity(min_velocity, max_velocity)]
    for i in range(balls_count - 1):
        radius = np.random.uniform(low = min_radius, high = max_radius)
        while True:
            pos = make_position(boundary_coords, radius)
                
            ## check for spheres intersection:
            if any(np.linalg.norm(pos - np.array(positions), axis=1) - np.array(radii) + radius <= EPS) is True:
                continue
            break;
        positions.append(pos)
        radii.append(radius)
        masses.append(np.random.uniform(low = min_mass, high = max_mass))
        velocities.append(make_velocity(min_velocity, max_velocity))
    return positions, radii, masses, velocities, # colors

# =============================================================================================================================
# =============================================================================================================================
# =============================================================================================================================
# =============================================================================================================================
# VTK Sphere class extension with mass, velocity and collision checks

class Ball():
    def __init__(self, position, radius, mass, velocity):
        self.Center  = tuple(position)
        self.Radius = abs(radius)
        self.Mass = abs(mass)
        self.Velocity = np.array(velocity)
        self.InBox = True
        
    def still_in_box(self, boundary_coords):
        coords = [(boundary_coords['x_min'], boundary_coords['x_max']), 
                  (boundary_coords['y_min'], boundary_coords['y_max']), 
                  (boundary_coords['z_min'], boundary_coords['z_max'])]
        for i, (min_, max_) in enumerate(coords):
            if (self.Center[i] <= (min_ -self.Radius - EPS)) or (self.Center[i]  >= (max_ + self.Radius + EPS)):
                self.InBox = False
                break

    def check_ball_bounds_collisions(self, boundary_coords, boundary_keys):
        coords = [(boundary_coords['x_min'], boundary_coords['x_max']), 
                  (boundary_coords['y_min'], boundary_coords['y_max']), 
                  (boundary_coords['z_min'], boundary_coords['z_max'])]
        keys = [(boundary_keys['x_min'], boundary_keys['x_max']), 
                (boundary_keys['y_min'], boundary_keys['y_max']), 
                (boundary_keys['z_min'], boundary_keys['z_max'])]
        for i, ((min_, max_), (min_key, max_key)) in enumerate(zip(coords, keys)):
            center = np.array(self.Center)
            if (center[i] <= (min_ + self.Radius) - EPS) and min_key:
                center[i] = (min_ + self.Radius)
                self.Velocity[i] = - self.Velocity[i]
            elif(center[i]  >= (max_ - self.Radius) + EPS) and max_key:
                center[i] = (max_ - self.Radius)
                self.Velocity[i] = - self.Velocity[i]
            self.Center = tuple(center)
            
            
    def check_ball_balls_collisions(self, balls):
        for second_ball in balls.values():
            if second_ball == self:
                continue
            central_vector = np.array(second_ball.Center) - np.array(self.Center) 
            mu = self.Mass/second_ball.Mass
            if (np.sqrt(central_vector.dot(central_vector)) <= (self.Radius + second_ball.Radius) + EPS):
                central_vector = central_vector / np.sqrt(central_vector.dot(central_vector))
                v01 = self.Velocity.dot(central_vector) * central_vector
                v02 = second_ball.Velocity.dot(central_vector) * central_vector
                if(v01.dot(central_vector) < v02.dot(central_vector)):
                    break
                else:
                    v01, v02 = self.Velocity + (((mu-1)*v01 + 2*v02)/(mu+1) - v01),                               second_ball.Velocity + ((2*mu*v01 + (1-mu)*v02)/(mu+1) - v02)
                    self.Velocity = np.array(v01)
                    second_ball.Velocity = np.array(v02)
    
    def gravity_force(self, delta_t, g):
        self.Velocity += delta_t * g
    
    def move(self, delta_t):
        self.Center = tuple(np.array(self.Center) + delta_t * self.Velocity)

# =============================================================================================================================
# =============================================================================================================================
# =============================================================================================================================
# =============================================================================================================================
            
def main():
    configuration_parameters = {}
    with open('computing_configuration.json') as f:
#     with open(sys.argv[1]) as f:
        data = f.read()
        configuration_parameters = json.loads(data)
    
    min_radius = float(configuration_parameters['min_radius'])
    max_radius = float(configuration_parameters['max_radius'])
    
    min_velocity = float(configuration_parameters['min_velocity'])
    max_velocity = float(configuration_parameters['max_velocity'])
    
    min_mass = float(configuration_parameters['min_mass'])
    max_mass = float(configuration_parameters['max_mass'])
    
    balls_count = int(configuration_parameters['balls_count'])
    g = np.array([0.0, 0.0, float(configuration_parameters['g'])])
    max_time = float(configuration_parameters['max_time'])
    time_step = float(configuration_parameters['time_step'])
    
    boundary_coords = {}
    boundary_keys = {}
    for key in ['x_min', 'x_max', 'y_min', 'y_max', 'z_min', 'z_max']:
        boundary_coords[key] = float(configuration_parameters['box_' + key])
        boundary_keys[key] = (configuration_parameters[key + '_key'] == 'True')


# ==================
#     Create a set of spheres

    balls = {}
    colors = {}
    positions, radii, masses, velocities = define_sphere_properties(balls_count, 
                                                                    min_radius, max_radius,
                                                                    min_mass, max_mass,
                                                                    min_velocity, max_velocity,
                                                                    boundary_coords)
    for i in range(balls_count):
        balls[i] = Ball(positions[i], radii[i], masses[i], velocities[i])
        colors[i] = np.random.choice(color_names)
    
    curr_time = 0.0
    n = 1
    
    truncated_metadata = {}
    truncated_metadata['balls_count'] = balls_count
    truncated_metadata['boundary_coords'] = json.dumps(boundary_coords)
    truncated_metadata['boundary_keys'] = json.dumps(boundary_keys)
    truncated_metadata['max_time'] = max_time
    for i, ball in balls.items():
                truncated_metadata['ball_id_' + str(i)] = {
                    'initial_center_position' : list(ball.Center),
                    'radius' : ball.Radius,
                    'color' : colors[i],
                }
    with open(
        os.path.join('OutDir', 'metadata.json'), 'w') as f:
            json.dump(truncated_metadata, f)
    
    while curr_time < max_time:
        delta_t = min(radii)/np.sqrt(max([np.dot(x.Velocity, x.Velocity) for x in balls.values()]))
        indices_to_delete = []
        for _, ball in balls.items():
            ball.check_ball_balls_collisions(balls)
            ball.check_ball_bounds_collisions(boundary_coords, boundary_keys)
            ball.gravity_force(delta_t, g)
            ball.move(delta_t)
            ball.still_in_box(boundary_coords)
            if not ball.InBox:
                indices_to_delete.append(_)
        for i in indices_to_delete:
            del(balls[i])
        del(indices_to_delete)
        if (curr_time >= n*time_step):
            stored_data = {}
            stored_data['metadata'] = {
                'current_time' : curr_time,
            }
            for i, ball in balls.items():
                stored_data[f'ball_id_{i}' ] = {
                    'position' : list(ball.Center),
                    'velocity' : list(ball.Velocity),
                }
                    
            file_name = os.path.join('OutDir','data_'+ f'{n}'.zfill(10) + '.json')
            with open(file_name, 'w') as f:
                json.dump(stored_data, f)
            n += 1
        curr_time += delta_t
    
if __name__ == '__main__':
    main()

