import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sentinelhub import DataCollection, SHConfig, BBox, CRS, SentinelHubRequest, MimeType, \
bbox_to_dimensions, DownloadRequest

CLIENT_ID = '38f3a25e-448b-4fb7-8d86-12dae7ab0136'
CLIENT_SECRET = '0Gf?B{PBWqV,wUhhb)AGjG6-72_;}l/6f5HE,9:4'

config = SHConfig()
config.sh_client_id = CLIENT_ID
config.sh_client_secret = CLIENT_SECRET

def get_NDRE(box, date, resolution, config=None):
    
    bbox = BBox(box, crs=CRS.WGS84)
    size = bbox_to_dimensions(bbox, resolution=resolution)
    print('pixel size =', size)

    evalscript_true_color = """
    //VERSION=3

    function setup() {
        return {
            input: [{
                bands: ["B05", "B08", "CLM"]
            }],
            output: {
                bands: 3,
            }
        };
    }

    function evaluatePixel(sample) {
        return [(sample.B08-sample.B05)/(sample.B08+sample.B05), sample.CLM];
    }
    """

    if not config:
        CLIENT_ID = '38f3a25e-448b-4fb7-8d86-12dae7ab0136'
        CLIENT_SECRET = '0Gf?B{PBWqV,wUhhb)AGjG6-72_;}l/6f5HE,9:4'
        config = SHConfig()
        config.sh_client_id = CLIENT_ID
        config.sh_client_secret = CLIENT_SECRET

    request = SentinelHubRequest(
        evalscript=evalscript_true_color,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A,
                time_interval=date,
            )
        ],
        responses=[
            SentinelHubRequest.output_response('default', MimeType.PNG)
        ],
        bbox=bbox,
        size=size,
        config=config
    )
    image = request.get_data()[0]
    
    return image


def get_NDVI(box, date, resolution, config=None):
    
    bbox = BBox(box, crs=CRS.WGS84)
    size = bbox_to_dimensions(bbox, resolution=resolution)
    print('pixel size =', size)

    evalscript_true_color = """
    //VERSION=3

    function setup() {
        return {
            input: [{
                bands: ["B04", "B08"]
            }],
            output: {
                bands: 3
            }
        };
    }

    function evaluatePixel(sample) {
        return [(sample.B08-sample.B04)/(sample.B08+sample.B04)];
    }
    """

    if not config:
        CLIENT_ID = '38f3a25e-448b-4fb7-8d86-12dae7ab0136'
        CLIENT_SECRET = '0Gf?B{PBWqV,wUhhb)AGjG6-72_;}l/6f5HE,9:4'
        config = SHConfig()
        config.sh_client_id = CLIENT_ID
        config.sh_client_secret = CLIENT_SECRET

    request = SentinelHubRequest(
        evalscript=evalscript_true_color,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A,
                time_interval=date,
            )
        ],
        responses=[
            SentinelHubRequest.output_response('default', MimeType.PNG)
        ],
        bbox=bbox,
        size=size,
        config=config
    )
    image = request.get_data()[0]
    
    return image

def get_NDRE_coverage(box, date, resolution, config=None):
    
    bbox = BBox(box, crs=CRS.WGS84)
    size = bbox_to_dimensions(bbox, resolution=resolution)
    print('pixel size =', size)


    evalscript_true_color = """
    //VERSION=3
    function setup() {
    return {
        input: ["B02", "B03", "B04", "B05", "B08"],
        output: { bands: 3 }
    }
    }

    function evaluatePixel(sample) {
    if ((sample.B08-sample.B05)/(sample.B08+sample.B05) > 0.55) {
        return [0.75 + sample.B04, sample.B03, sample.B02]
    }
    return [3.5*sample.B04, 3.5*sample.B03, 3.5*sample.B02];
    }
    """

    if not config:
        CLIENT_ID = '38f3a25e-448b-4fb7-8d86-12dae7ab0136'
        CLIENT_SECRET = '0Gf?B{PBWqV,wUhhb)AGjG6-72_;}l/6f5HE,9:4'
        config = SHConfig()
        config.sh_client_id = CLIENT_ID
        config.sh_client_secret = CLIENT_SECRET

    request = SentinelHubRequest(
        evalscript=evalscript_true_color,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A,
                time_interval=date,
            )
        ],
        responses=[
            SentinelHubRequest.output_response('default', MimeType.PNG)
        ],
        bbox=bbox,
        size=size,
        config=config
    )
    image = request.get_data()[0]
    
    return image

def get_NDVI_coverage(box, date, resolution, config=None):
    
    bbox = BBox(box, crs=CRS.WGS84)
    size = bbox_to_dimensions(bbox, resolution=resolution)
    print('pixel size =', size)


    evalscript_true_color = """
    //VERSION=3
    function setup() {
    return {
        input: ["B02", "B03", "B04", "B08"],
        output: { bands: 3 }
    }
    }

    function evaluatePixel(sample) {
    if ((sample.B08-sample.B04)/(sample.B08+sample.B04) > 0.7) {
        return [0.75 + sample.B04, sample.B03, sample.B02]
    }
    return [3.5*sample.B04, 3.5*sample.B03, 3.5*sample.B02];
    }
    """

    if not config:
        CLIENT_ID = '38f3a25e-448b-4fb7-8d86-12dae7ab0136'
        CLIENT_SECRET = '0Gf?B{PBWqV,wUhhb)AGjG6-72_;}l/6f5HE,9:4'
        config = SHConfig()
        config.sh_client_id = CLIENT_ID
        config.sh_client_secret = CLIENT_SECRET

    request = SentinelHubRequest(
        evalscript=evalscript_true_color,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A,
                time_interval=date,
            )
        ],
        responses=[
            SentinelHubRequest.output_response('default', MimeType.PNG)
        ],
        bbox=bbox,
        size=size,
        config=config
    )
    image = request.get_data()[0]
    
    return image

def get_RGB(box, date, resolution, brighten=False, config=None):
    
    bbox = BBox(box, crs=CRS.WGS84)
    size = bbox_to_dimensions(bbox, resolution=resolution)
    print('pixel size =', size)

    if brighten:
        evalscript_true_color = """
        //VERSION=3

        function setup() {
            return {
                input: [{
                    bands: ["B02", "B03", "B04"]
                }],
                output: {
                    bands: 3
                }
            };
        }

        function evaluatePixel(sample) {
            return [3*sample.B04, 3*sample.B03, 3*sample.B02];
        }
        """
    else:
        evalscript_true_color = """
        //VERSION=3

        function setup() {
            return {
                input: [{
                    bands: ["B02", "B03", "B04"]
                }],
                output: {
                    bands: 3
                }
            };
        }

        function evaluatePixel(sample) {
            return [sample.B04, sample.B03, sample.B02];
        }
        """

    # evalscript_true_color = """
    # //VERSION=3
    # function setup() {
    # return {
    #     input: ["B02", "B03", "B04", "CLM"],
    #     output: { bands: 3 }
    # }
    # }

    # function evaluatePixel(sample) {
    # if (sample.CLM == 1) {
    #     return [0.75 + sample.B04, sample.B03, sample.B02]
    # }
    # return [3.5*sample.B04, 3.5*sample.B03, 3.5*sample.B02];
    # }
    # """

    if not config:
        CLIENT_ID = '38f3a25e-448b-4fb7-8d86-12dae7ab0136'
        CLIENT_SECRET = '0Gf?B{PBWqV,wUhhb)AGjG6-72_;}l/6f5HE,9:4'
        config = SHConfig()
        config.sh_client_id = CLIENT_ID
        config.sh_client_secret = CLIENT_SECRET

    request = SentinelHubRequest(
        evalscript=evalscript_true_color,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A,
                time_interval=date,
            )
        ],
        responses=[
            SentinelHubRequest.output_response('default', MimeType.PNG)
        ],
        bbox=bbox,
        size=size,
        config=config
    )
    image = request.get_data()[0]
    
    return image


def get_county_box(county_name, statefp, height=None, width=None, county_df=None):

    if not county_df:
        county_df = pd.read_csv("US_County_Boundaries.csv")

    obj =  county_df[(county_df['NAME'] == county_name) & (county_df['STATEFP'] == statefp)]
    lat, lon = obj['INTPTLAT'].values[0], obj['INTPTLON'].values[0]
    lat_min, lat_max = lat - height/2/110.574, lat + height/2/110.574
    lon_min, lon_max = lon - width/2/111.320/np.cos(lat*np.pi/180), lon + width/2/110.574/np.cos(lat*np.pi/180)

    return [lon_min, lat_min, lon_max, lat_max]



