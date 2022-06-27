# load libraries
import pandas as pd
from geopy.geocoders import Nominatim
import time
from tqdm import tqdm
import logging
from math import radians, cos, sin, asin, sqrt


# set up logging file
logging.basicConfig(filename='log_file.log', level=logging.DEBUG)

# load addresses for customers and sales reps
customers = pd.read_csv('data/customers.csv')
sales_reps = pd.read_csv('data/sales_rep.csv')

def lookup_lat_long(df):
    # lookup latitude and longitude for each customer and sales rep using geopy
    # geolocator object is used to look up lat/lon, user agent is requested for large numbers of requests
    working_address = []
    geolocator = Nominatim(user_agent="my_request", timeout=4)
    df['full_addr'] = df['address1'] + ', ' + df['city'] + ', ' + df['state'] + ', ' + df['postalCode'].astype(str)
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        try:
            customer_address = row['full_addr']
            location = geolocator.geocode(customer_address)
            to_append = row.to_dict()
            to_append['lat'] = location.latitude
            to_append['lon'] = location.longitude
            working_address.append(to_append)
            #time.sleep(3)
        except AttributeError:
            logging.exception('error: failed to retrieve lat/lon')
    df_return = pd.DataFrame(working_address)
    return df_return

#customer_lat_lon = lookup_lat_long(customers)
#customer_lat_lon.to_csv('customer_lat_lon.csv', index=False)

#sales_reps_lat_lon = lookup_lat_long(sales_reps)
#sales_reps_lat_lon.to_csv('sales_rep_lat_long.csv', index=False)

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in miles between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956 # Radius of earth in miles. Use 6371 for kilometers. Determines return value units.
    return c * r

def calc_distance_to_cust():
    customers = pd.read_csv('customer_lat_lon.csv')
    sales_reps = pd.read_csv('sales_rep_lat_long.csv')

    return_df = []

    for s_index, s_row in tqdm(sales_reps.iterrows(), total=sales_reps.shape[0]):
        sale_lat = s_row['lat']
        sale_lon = s_row['lon']
        for c_index, c_row in customers.iterrows():
            cust_lat = c_row['lat']
            cust_lon = c_row['lon']
            distance = haversine(sale_lon, sale_lat, cust_lon, cust_lat)
            results = {'sales_rep': s_row['Sales rep'], 'customer': c_row['account_number'], 'distance': distance}
            return_df.append(results)

    return_df = pd.DataFrame(return_df)
    return return_df
#x = calc_distance_to_cust()
#x.to_csv('distance_calc.csv', index=False)

df = pd.read_csv('distance_calc.csv')
below_25 = df[df['distance'] < 25]
unique_customers = below_25['customer'].unique()

above_25 = df[df['distance'] > 25]
