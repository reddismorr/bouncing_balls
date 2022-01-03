#!/usr/bin/env python
# coding: utf-8

# In[6]:


import sys
import os
import json

def main():
    configuration_file = {}
    with open(sys.argv[1]) as f:
        for i in ['min_radius', 'max_radius',
                  'min_velocity','max_velocity',
                  'min_mass', 'max_mass',
                  'balls_count', 'g',
                  'max_time', 'time_step',
                  'box_x_min', 'box_x_max', 'box_y_min', 'box_y_max', 'box_z_min', 'box_z_max',
                  'x_min_key', 'x_max_key', 'y_min_key', 'y_max_key', 'z_min_key', 'z_max_key']:
            configuration_file[i] = f.readline().split('\n')[0]
    with open('computing_configuration.json', 'w') as f:
        json.dump(configuration_file, f)
    
if __name__ == '__main__':
    main()

