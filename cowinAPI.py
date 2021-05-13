from datetime import datetime, timezone
import json
import time

from cowin_api import CoWinAPI
from datetime import date

today = date.today()


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def aslocaltimestr(utc_dt):
    return utc_to_local(utc_dt).strftime("%d-%m-%Y")


cowin = CoWinAPI()


class vaccine_center(dict):
    def __init__(self, name, address, block_name, fee_type, available_capacity, vaccine, date, age, pincode):
        self.name = name
        self.address = address
        self.block_name = block_name
        self.fee_type = fee_type
        self.available_capacity = available_capacity
        self.vaccine = vaccine
        self.date = date
        self.age = age
        self.pincode = pincode

    def asdict(self):
        return {'name': self.name, 'address': self.address, 'block_name': self.block_name, 'fee_type': self.fee_type, 'available_capacity': self.available_capacity, 'vaccine': self.vaccine, 'date': self.date, 'age': self.age, 'pincode': self.pincode}

    def __getattr__(self, attr):
        return self[attr]


class cowinapi():
    def call_api(self, min_age_limit, district_id):
        filtered_centers = {'centers': []}
        date = aslocaltimestr(datetime.utcnow())
        try:
            print("Calling API")
            available_centers = cowin.get_availability_by_district(
                district_id, date, min_age_limit)
            print("API Executed")
        except:
            print(
                "API is not responding currently, will wait for some time and try again")
            return None
        else:
            for center in available_centers['centers']:
                for slot in center['sessions']:
                    if slot['available_capacity'] > 0:
                        # print(center)
                        filtered_center = vaccine_center(
                            center['name'], center['address'], center['block_name'], center['fee_type'], slot['available_capacity'], slot['vaccine'], slot['date'], slot['min_age_limit'], center['pincode'])
                        filtered_centers['centers'].append(
                            filtered_center.asdict())
                        print(filtered_centers)
            return filtered_centers
