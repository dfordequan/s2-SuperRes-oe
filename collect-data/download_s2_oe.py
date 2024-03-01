from sentinelhub import SHConfig, BBox, CRS, SentinelHubRequest, DataCollection, MimeType, bbox_to_dimensions, SentinelHubCatalog, MosaickingOrder
from geopy.distance import distance
from shapely import geometry
import mercantile
import math
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os


CLIENT_ID = '4233abe2-b007-4a70-9778-0087219bdcbe'
CLIENT_SECRET = '01jdg5RZ8blbe3dfLfkxVuTV4xUOK74E'

date_list = ['2023-04-01', '2023-09-30']

config = SHConfig()

if CLIENT_ID and CLIENT_SECRET:
    config.sh_client_id = CLIENT_ID
    config.sh_client_secret = CLIENT_SECRET


def tile_box_num(x, y, zoom_level=18):
    return geometry.Polygon.from_bounds(*mercantile.bounds(x, y, zoom_level))

def get_s2_l2a(s2_bbox, s2_date, config):
    """ author: Alessandro """
    evalscript_l2a = """//VERSION=3
        function setup() {
            return {
                input: [{
                    bands: ["B02","B03","B04"],
                }],
                output: {
                    bands: 3,
                }
            };
        }

        function evaluatePixel(sample) {
            return [sample.B04,
                    sample.B03,
                    sample.B02];
        }
    """

    request2 = SentinelHubRequest(
        evalscript=evalscript_l2a,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C,
                time_interval=s2_date,
                #time_interval=("2020-06-01", "2020-06-30"),
                #other_args={"processing": {"harmonizeValues": True}}
                mosaicking_order=MosaickingOrder.LEAST_CC,
            )
        ],
        responses=[
            SentinelHubRequest.output_response('default', MimeType.TIFF),
            #SentinelHubRequest.output_response("userdata", MimeType.JSON),
        ],
        bbox=s2_bbox,
        size=bbox_to_dimensions(s2_bbox, 10),
        config=config
    )

    return request2.get_data()[0]


file_path = './tiles/worldimagery'

files = os.listdir(file_path)

for file in files:
    zoom_level = file.split('_')[0]
    point_x = file.split('_')[1]
    point_y = file.split('_')[2][:-4]

    bbox = tile_box_num(int(point_x), int(point_y), int(zoom_level))

    bbox = BBox(bbox.bounds, crs=CRS.WGS84)


    s2_reference_date = date_list[0]
    # bbox = BBox(region.bounds, crs=CRS.WGS84)
    s2_l2a_mst = get_s2_l2a(bbox, s2_reference_date, config)

    # plt.show()


    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    # plot irt with factor = 3.5/255
    # ax.imshow(s2_l2a_mst)




    # plt.show()


    # take the center 32x32 pixels
    size_x = s2_l2a_mst.shape[0]
    size_y = s2_l2a_mst.shape[1]
        
    image = s2_l2a_mst[int(size_x/2)-16:int(size_x/2)+16, int(size_y/2)-16:int(size_y/2)+16, :]

    images = image

    im_ = Image.fromarray(images)
    im_.save(f'./s2/worldimagery/{zoom_level}_{point_x}_{point_y}_s2.png')
