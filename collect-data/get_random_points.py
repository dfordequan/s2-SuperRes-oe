import random
import geopandas as gpd
from shapely import geometry
from tqdm import tqdm
import json

def generate_random(polygon, number, seed):
    random.seed(seed)
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    with tqdm(total=number) as pbar:
        while len(points) < number:
            pnt = geometry.Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
            if polygon.contains(pnt):
                points.append(pnt)
                pbar.update(1)
    return points


countries_polies = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

country = 'United States of America'

country_poly = countries_polies[countries_polies['name'] == country]['geometry'].iloc[0]

random_points = generate_random(country_poly, number=100, seed=42)

print(random_points)

# make a data structure like: ["features"][0]["geometry"]["coordinates"][0][0]
# save the points as list of two numbers
# save the list as a json file

# save the points as list of two numbers

points = [[point.x, point.y] for point in random_points]

# save the list as a json file

import json

with open('./us_points.json', 'w') as f:
    json.dump(points, f)

