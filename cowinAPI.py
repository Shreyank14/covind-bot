import json
import time

from cowin_api import CoWinAPI
from datetime import date

today = date.today()

#district_id = '269'
date = today.strftime("%d-%m-%Y")  # Optional. Takes today's date by default
# Optional. By default returns centers without filtering by min_age_limit
#min_age_limit = 18
cowin = CoWinAPI()


class vaccine_center(dict):
    def __init__(self, name, address, block_name, fee_type, available_capacity, vaccine, date, age):
        self.name = name
        self.address = address
        self.block_name = block_name
        self.fee_type = fee_type
        self.available_capacity = available_capacity
        self.vaccine = vaccine
        self.date = date
        self.age = age
        # self.slots = slots

    def asdict(self):
        return {'name': self.name, 'address': self.address, 'block_name': self.block_name, 'fee_type': self.fee_type, 'available_capacity': self.available_capacity, 'vaccine': self.vaccine, 'date': self.date, 'age': self.age}

    def __getattr__(self, attr):
        return self[attr]


class cowinapi():
    def call_api(self, min_age_limit, district_id):
        filtered_centers = {'centers': []}
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
                if center['sessions'][0]['available_capacity'] > 0:
                    # print(center)
                    filtered_center = vaccine_center(
                        center['name'], center['address'], center['block_name'], center['fee_type'], center['sessions'][0]['available_capacity'], center['sessions'][0]['vaccine'], center['sessions'][0]['date'], center['sessions'][0]['min_age_limit'])
                    filtered_centers['centers'].append(
                        filtered_center.asdict())
                    print(filtered_centers)
            return filtered_centers


# cowin = cowinapi()
# print(cowin.call_api(45, '269'))
