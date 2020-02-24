#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np


def main():
    frames = []
    for city in cities:
        print()
        print(city.upper() + " ---------------------------------")
        print()
        frames.append(get_data(city))
    df = pd.concat(frames)
    df = df.sample(frac=1)
    df.to_csv("data.csv", index=False)



def get_data(city):
    listing = pd.read_csv("data_france/"+city+"/listings.csv")
    calendar = pd.read_csv("data_france/"+city+"/calendar.csv")
    calendar["id"] = calendar["listing_id"]
    listing = listing[cols_listing]
    calendar = calendar[cols_calendar]

    data = pd.merge(listing, calendar, on='id', how='outer')
    data = data[data["price_x"] == data["price_y"]]
    data = data[data["number_of_reviews"]>0]
    data = data[data["square_feet"]>0]
    data = data.dropna()

    values, holidays, prices, months = [], [], [], []

    for index, row in data.iterrows():
        surface, zipcode = int(row["square_feet"]), int(row["zipcode"])
        date = row["date"]
        price = float(row["adjusted_price"].strip("$").replace(',', ''))
        month = int(date.split("-")[1])
        
        values.append(get_value(surface, zipcode))
        holidays.append(is_holiday(date))
        prices.append(dollar_to_euro(price))
        months.append(month)
        
    data["property_value"] = np.array(values)
    data["is_holiday"] = np.array(holidays)
    data["price"] = np.array(prices)
    data["month"] = np.array(months)

    return data[cols]



def is_holiday(date):
    if date in holidays_list:
        return 1
    else:
        return 0

def dollar_to_euro(p):
    return p*0.92

def get_value(square_feet, zipcode):
    r = zip_price_m2[zip_price_m2["zipcode"]==zipcode]
    if r.shape[0] > 0:
        price_m2 = r.iloc[0]['price_m2']
    else:
        r = zip_price_m2[zip_price_m2["zipcode"]//1000==zipcode//1000]
        price_m2 = r.iloc[0]['price_m2']
    return 0.92903 * square_feet * price_m2


if __name__ == "__main__":
    
    holidays_list = ['2019-01-01', '2019-04-21', '2019-04-22', '2019-05-01',
                     '2019-05-08', '2019-05-30', '2019-06-09', '2019-06-10',
                     '2019-07-14', '2019-08-15', '2019-11-01', '2019-11-11',
                     '2019-12-24', '2019-12-25', '2019-12-31', '2020-01-01',
                     '2020-04-12', '2020-04-13', '2020-05-01', '2020-05-08',
                     '2020-05-21', '2020-05-31', '2020-06-01', '2020-07-14',
                     '2020-08-15', '2020-11-01', '2020-11-11', '2020-12-24',
                     '2020-12-25', '2020-12-31']

    cols_listing = ['id', 'zipcode', 'property_type', 'room_type',
                    'accommodates', 'bedrooms', 'square_feet',
                    'price', 'number_of_reviews', 'review_scores_rating']
    cols_calendar = ["id", "date", "price", "adjusted_price"]
    cols = ["month", "is_holiday", "property_type", "room_type", 
            "accommodates", "bedrooms", "square_feet", "property_value", 
            "price"]
    
    zip_price_m2 = pd.read_csv("data_france/price_m2_zip.csv")

    cities = ["bordeaux", "paris", "lyon"]

    main()




