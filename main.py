import datetime
import time

import ee
import google.auth
from google.oauth2.credentials import Credentials


def init_gee():

    # Initialize GEE using Application Default Credentials
    auth_scopes = ['https://www.googleapis.com/auth/earthengine',
                   'https://www.googleapis.com/auth/devstorage.full_control']
    credentials, project_id = google.auth.default(scopes=auth_scopes)

    print("Using credentials:")
    print(credentials.to_json())

    ee.Initialize(credentials)


def main():
    landsat_img = ee.Image('LANDSAT/LC8_L1T_TOA/LC81230322014135LGN00').select(['B4', 'B3', 'B2'])
    aoi = ee.Geometry.Rectangle([116.2621, 39.8412, 116.4849, 40.01236])

    file_name = datetime.datetime.now().isoformat(timespec='seconds')

    export_task = ee.batch.Export.image.toCloudStorage(landsat_img,
                                                       f"NRCanExportDemo-{file_name}",
                                                       fileNamePrefix=file_name,
                                                       bucket='ce-nrcan-demo',
                                                       region=aoi)

    print(f"Starting export task for file {file_name}")
    export_task.start()

    print("Waiting for task to finish...")
    while export_task.active():
        time.sleep(2)

    print(export_task.status())


if __name__ == "__main__":
    init_gee()
    main()
