﻿# https://github.com/hflabs/dadata-py
from dadata import Dadata
def adress(pos_s:int, pos_d:int):
    token = """2784d4bfc49fa072b9cb6d5b9653f1d393430127"""
    dadata = Dadata(token)
    result = dadata.geolocate(name="address", lat=pos_s, lon=pos_d, radius_meters=100)
    print(result)
    if result != []:
        return result[0]['value']
    else:
        return f"Не удалось определить, координаты: {pos_s}, {pos_d}"
    