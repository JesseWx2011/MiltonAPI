# 100% Written without AI.
# ©2026 windowclean.net Team. All rights reserved.

from goes2go.data import goes_latest, goes_nearesttime
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from metpy.plots import USCOUNTIES
from dateutil import tz
from datetime import datetime

utc_time = tz.tzutc()
local_time = tz.gettz("America/Chicago")

year = datetime.today().year
print(year)

g = goes_latest(satellite="goes19", product="ABI", return_as="xarray")
# g = goes_latest(satellite="goes19", product="ABI", return_as="xarray")

extent = [-91.021729, -83.309326, 27.223260, 34.052817]

ax = plt.subplot(projection=g.rgb.crs)
ax.set_extent(extent)
ax.imshow(g.rgb.TrueColor(), **g.rgb.imshow_kwargs)
ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='white')
ax.add_feature(USCOUNTIES.with_scale('5m'), linewidth=0.4, edgecolor='white')
ax.coastlines()

goes_timestamp = g.t.dt.strftime('%H:%M UTC %m/%d/%Y').item()

plt.title(f"{goes_timestamp}", fontsize=10, loc="right")
plt.title(f"Latest Satellite Image \n ©2023-{year} windowclean.net", fontsize=9, loc="left")
plt.show()
