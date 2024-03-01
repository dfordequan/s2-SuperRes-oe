from sentinelhub import SHConfig, BBox, CRS, SentinelHubRequest, DataCollection, MimeType, bbox_to_dimensions, SentinelHubCatalog

import shapely
from shapely.geometry import Polygon
from shapely.wkt import loads


lon1, lat1 = 52.015774, 4.375342
lon2, lat2 = 52.01605122608524, 4.383102473453196
lon3, lat3 = 52.012723, 4.383517
lon4, lat4 = 52.012619, 4.376376

region  = loads(f'POLYGON (({lat1} {lon1}, {lat2} {lon2}, {lat3} {lon3}, {lat4} {lon4}, {lat1} {lon1}))')

regions = [region]

# randomly generated four other regions in the netherlands with similar area
# region 1
lon1, lat1 = 52.015774, 4.375342
lon2, lat2 = 52.01605122608524, 4.383102473453196
lon3, lat3 = 52.012723, 4.383517
lon4, lat4 = 52.012619, 4.376376


