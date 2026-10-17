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

site = 'MOB'
product = 'N0B'
start = datetime(2026, 10, 17, 6, 0)
end = start + timedelta(hours=1)

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

    outfile = outdir / f'frame_{i:03d}.png'
    plt.savefig(outfile, bbox_inches='tight')
    plt.close(fig)

