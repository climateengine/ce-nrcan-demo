import datetime
import time

import ee


def init_gee():
    ee.Authenticate()  # Use application default credentials to authenticate to GEE
    ee.Initialize()


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
