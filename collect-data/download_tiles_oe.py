import numpy as np
import json
import math
import subprocess
from concurrent.futures import ThreadPoolExecutor
import os
import time



"""
Input Parameters
"""
file_path = '/home/aoqiao/developer_dq/superresolution_oe/collect-data'

# file = 'gadm41_NLD_0.json'
file = 'us_points.json'

output_path = '/home/aoqiao/developer_dq/superresolution_oe/collect-data/tiles'


"""
Default Parameters, mos of them are default from the original code
"""
zoom_level = 16
threads = os.cpu_count()


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return xtile, ytile

def format_string(url, x, y, zoom):
    substituted_string = url.replace('{x}', str(x))
    substituted_string = substituted_string.replace('{y}', str(y))
    substituted_string = substituted_string.replace('{z}', str(zoom))
    return substituted_string


def download_tile(url, tile_path, max_retries=5, retry_delay=2):
    retries = 0
    while retries < max_retries:
        try:
            subprocess.run(["curl", url, '--output', tile_path], check=True)
            return  # Download successful, exit the function
        except subprocess.CalledProcessError as e:
            print(f"Download failed: {e}")
            retries += 1
            if retries < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached, giving up.")


# APIS = {
#     'worldimagery' : 'https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
#     'worldimagery-clarity': 'https://clarity.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
#     'openstreetmap' : 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
#     'ukosgb1888': 'https://api.maptiler.com/tiles/uk-osgb10k1888/{z}/{x}/{y}.jpg?key=MXVhdLdJmHeZ0z5DwjBI'
# }

APIS = {
    'worldimagery' : 'https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'}

coordinates = []

f = open(f'{file_path}/{file}', 'r')
data = json.load(f)


# coordinates = data["features"][0]["geometry"]["coordinates"][0][0] # for gadm41_NLD_0.json only
coordinates = data

print(len(coordinates))

# Create folders for the different image types

for url in APIS:
    if not os.path.exists(f'{output_path}/{url}'):
        os.makedirs(f'{output_path}/{url}')

with ThreadPoolExecutor(max_workers=threads) as executor:

    futures = []

    for coord in coordinates:
        lon, lat = coord[0], coord[1]
        x, y = deg2num(lat, lon, zoom=zoom_level)
                
        for url in APIS:
            tile_url = format_string(APIS[url], x, y, zoom_level)
            tile_path = f'{output_path}/{url}/{zoom_level}_{x}_{y}.png'
            future = executor.submit(download_tile, tile_url, tile_path)
            futures.append(future)
            
            # Wait for all the downloads to complete
            for future in futures:
                future.result()