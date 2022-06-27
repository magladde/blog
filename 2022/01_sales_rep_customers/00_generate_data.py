import json
import pandas as pd
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
import random
from tqdm import tqdm
from geopy import geocoders
import time

def create_custmer_data():
    # create customer data files
    with open('data/addresses-us-all.json') as json_file:
        data = json.load(json_file)
    # load data into dataframe
    df = pd.DataFrame(data['addresses'])
    df_sub = df[df['state'].isin(['CA', 'CO', 'AZ'])]
    df_sub = df_sub[['address1', 'city', 'state', 'postalCode']]
    account_numbers = [random.randint(1000000, 9999999) for i in range(df_sub.shape[0])]
    df_sub['account_number'] = account_numbers
    df_sub.to_csv('customers.csv', index=False)

create_custmer_data()
def create_plot(lat_long):
    # create a plot of customers on a map for visualization purposes, probably not provided by the client
    from geopandas import GeoDataFrame as gdf
    import geopandas as gpd

    world = gpd.read_file('data/tl_2020_us_state.zip')
    points = gdf(lat_long, geometry=gpd.points_from_xy(lat_long.lng, lat_long.lat))
    points.plot(ax=world.plot(), color='red', markersize=15)
    plt.xlim(-130, -60)
    plt.ylim(20, 55)
    plt.savefig('customers.png')

