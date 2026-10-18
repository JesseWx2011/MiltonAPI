# script was originally written in jupyter notebook

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

from metpy.calc import azimuth_range_to_lat_lon
from metpy.cbook import get_test_data
from metpy.io import Level3File
from metpy.plots import add_metpy_logo, add_timestamp, colortables, USCOUNTIES
from metpy.units import units

import numpy as np

from datetime import datetime, timedelta
from pathlib import Path
from metpy.calc import azimuth_range_to_lat_lon
from metpy.io import Level3File
from metpy.plots import USCOUNTIES, add_timestamp, colortables
from metpy.remote import NEXRADLevel3Archive
from metpy.units import units

import os
from PIL import Image
import shutil

site = 'MOB'
product = 'N0B'
start = datetime.now()
end = start + timedelta(hours=2)

products = list(NEXRADLevel3Archive().get_range(site, product, start, end))
print(f"{len(products)} radar scans were found from radar site {site}")
totalscans = len(products)

outdir = Path("radar_images")
outdir.mkdir(exist_ok=True) # Check if the directory does or doesn't exist

extent = [-89.736328, -85.858154, 29.667313, 31.877162]
norm, cmap = colortables.get_with_steps('NWSStormClearReflectivity', -20, 0.5)

for i, prod in enumerate(products):
    scanscompleted = (i+1)
    percentcomplete = round((scanscompleted / totalscans) * 100)
    print(f"Processing radar scan {i+1}/{totalscans}. {percentcomplete}% complete")

    nex = prod.access()

    datadict = nex.sym_block[0][0]
    data = nex.map_data(datadict['data'])
    data = np.ma.masked_invalid(data)

    az = (datadict['start_az'] + [datadict['end_az'][-1]]) * units.degrees
    rng = np.linspace(0, nex.max_range, data.shape[-1] + 1) * units.km

    lon, lat = azimuth_range_to_lat_lon(az, rng, nex.lon, nex.lat)

    fig = plt.figure(figsize=(9,8))

    ax = plt.axes(projection=ccrs.LambertConformal(central_longitude=nex.lon, central_latitude=nex.lat))

    ax.set_extent(extent, ccrs.PlateCarree())
    ax.add_feature(USCOUNTIES.with_scale('5m'), linewidth=0.4)
        
    mesh = ax.pcolormesh(lon, lat, data, cmap=cmap, norm=norm, transform=ccrs.PlateCarree())

    cbar = plt.colorbar(mesh, ax=ax, pad=0.02, shrink=0.9)
    cbar.set_label('Reflectivity (dBZ)')

    plt.title("Radar Loop | Latest", fontname='Rubik', fontweight='bold', loc='left')
    plt.title(f"Time: {nex.metadata['prod_time']}Z", fontname='Rubik', loc='right')

    outfile = outdir / f'frame_{i:03d}.png'
    plt.savefig(outfile, bbox_inches='tight')
    plt.close(fig)

def create_gif_from_images(image_folder, output_path, duration=500):
    """
    Converts a list of images in a folder into a GIF animation and saves it.
    Args:
        image_folder (str): Path to the folder containing the images.
        output_path (str): Path where the GIF will be saved.
        duration (int): Duration of each frame in the GIF in milliseconds (default is 500 ms).
    """

    # Step 1: Get a list of all image files in the specified folder
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('png', 'jpg', 'jpeg', 'bmp'))]

    # Check if there are any images in the folder
    if not image_files:
        print("No images found in the specified folder.")
        return

    # Step 2: Sort the images by name to ensure they are in the correct order
    image_files.sort()

    # Step 3: Load the images into a list using PIL
    images = [Image.open(os.path.join(image_folder, image_file)) for image_file in image_files]

    # Step 4: Convert the images to RGB format (necessary for GIF creation)
    rgb_images = [img.convert('RGB') for img in images]

    # Step 5: Create the GIF animation using the first image as the base and appending the rest
    rgb_images[0].save(
        output_path, 
        save_all=True, 
        append_images=rgb_images[1:], 
        duration=duration, 
        loop=0
    )

    print(f"GIF animation saved at: {output_path}")


create_gif_from_images('./radar_images/', 'radar_anim.gif', duration=250)
shutil.rmtree("./radar_images")
print("radar_images folder was removed.")
