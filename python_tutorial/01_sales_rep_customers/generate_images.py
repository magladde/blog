import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

usa = gpd.read_file('./data/States_shapefile-shp/States_shapefile.shp')
usa.plot(color='black', edgecolor='grey')
circle_1 = plt.Circle((-120, 38), color='red', radius=2, alpha=.5)
circle_2 = plt.Circle((-110, 35), color='red', radius=1.5, alpha=.5)
circle_3 = plt.Circle((-105, 40), color='red', radius=1.3, alpha=.5)
circle_4 = plt.Circle((-123, 41), color='red', radius=.8, alpha=.5)
circle_5 = plt.Circle((-117, 33), color='red', radius=1.1, alpha=.5)
circle_6 = plt.Circle((-118, 36), color='red', radius=.7, alpha=.5)
fig = plt.gcf()
ax = fig.gca()
ax.add_patch(circle_1)
ax.add_patch(circle_2)
ax.add_patch(circle_3)
ax.add_patch(circle_4)
ax.add_patch(circle_5)
ax.add_patch(circle_6)
plt.axis('equal')
plt.xlim(-130, -65)
plt.ylim(25, 50)
plt.savefig('usa.png')