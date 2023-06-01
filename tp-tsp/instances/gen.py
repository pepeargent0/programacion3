import random

num_points = 1000
x_range = (0, 10000)
y_range = (0, 10000)

with open('1000_cities.tsp', 'w') as f:
    f.write('NAME : 1000_cities\n')
    f.write('COMMENT : 1000-city problem (randomly generated)\n')
    f.write('TYPE : TSP\n')
    f.write(f'DIMENSION : {num_points}\n')
    f.write('EDGE_WEIGHT_TYPE : EUC_2D\n')
    f.write('NODE_COORD_SECTION\n')

    for i in range(1, num_points+1):
        x = random.uniform(*x_range)
        y = random.uniform(*y_range)
        f.write(f'{i} {x} {y}\n')
    
    f.write('EOF\n')
