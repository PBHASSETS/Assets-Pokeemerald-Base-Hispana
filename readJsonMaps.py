import os
import json

rootPath = "data/maps"

filterParameter =  "MAPSEC_PALLET_TOWN"

def readJson(pathJson):
    with open(pathJson, 'r') as file:
        data = json.load(file)
    return data


def isValidMap(filterParameter, dataJson):
    if filterParameter is None or filterParameter == '':
        return True

    valid_values = [
        dataJson.get("region_map_section"),
        dataJson.get("layout"),
        dataJson.get("map_type")
    ]
    
    return filterParameter in valid_values


arrayData = []

for ruta_directorio, subdirectorios, archivos in os.walk(rootPath):

    if "map.json" in archivos:
        dataJson = readJson(os.path.join(ruta_directorio, "map.json"))

        if isValidMap(filterParameter, dataJson):
            mapData = { 
                "id": dataJson.get("id"), 
                "name": dataJson.get("name"), 
                "layout": dataJson.get("layout") 
            }
            arrayData.append(mapData)

with open('mapData.txt', 'w') as file:
    for map in arrayData:
        file.write(str(map)+"\n")

    