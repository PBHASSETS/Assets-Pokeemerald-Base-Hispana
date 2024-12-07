import os
import ast
import shutil
import json

def readJson(pathJson):
    with open(pathJson, 'r') as file:
        data = json.load(file)
    return data


def writeJson(pathJson, data):
    try:
        with open(pathJson, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error al escribir el archivo {pathJson}: {e}")


def deleteFolder(pathFolder):
    try:
        shutil.rmtree(pathFolder)
        print(f"Directorio {pathFolder} eliminado con éxito.")
    except OSError as e:
        print(f"Error al eliminar el directorio: {e}")


def getDataMapDataFile():
    map_data_list = []

    with open("mapData.txt", 'r') as file:
        for linea in file:
            dic = ast.literal_eval(linea.strip())
            map_data_list.append(dic)

    return map_data_list


def deleteMapOfMapGroupsJson(mapGroupsData, mapNameDelete):

    for group in mapGroupsData:
        if isinstance(mapGroupsData[group], list):
            if mapNameDelete in mapGroupsData[group]:
                mapGroupsData[group].remove(mapNameDelete)
                print(f'map_groups.json: Elemento "{mapNameDelete}" eliminado del grupo "{group}"')


    with open(JSON_PATH_MAP_GROUPS, 'w') as file:
        json.dump(mapGroupsData, file, indent=4)
    

def deleteEventScript(mapName):
    pathFile = "data/event_scripts.s"
    pattern = f'include "data/maps/{mapName}/scripts.inc"'

    with open(pathFile, 'r') as file:
        lines = file.readlines()
    
    with open(pathFile, 'w') as file:
        for line in lines:
            if pattern not in line:
                file.write(line)

    print("event_scrips.s: elemento eliminado: "+pattern)

def deleteLayoutReference(idLayoutDelete):
    jsonPath = 'data/layouts/layouts.json'
    dataJson = readJson(jsonPath)

    dataJson["layouts"] = [layout for layout in dataJson.get("layouts", []) if layout.get("id") != idLayoutDelete]
    writeJson(jsonPath, dataJson)


def searchMapReferenceInOtherMapJson(dataJson, keyName, idsMapArray):
    result = []

    if isinstance(dataJson, list):

        for item in dataJson:
            result = [item for item in dataJson if item.get(keyName) not in idsMapArray]

    return result 

######################################################
######################################################
ROOT_PATH_DATA_MAP_FOLDER = "data/maps"
ROOT_PATH_DATA_LAYOUT_FOLDER = "data/layouts"
JSON_PATH_MAP_GROUPS = "data/maps/map_groups.json"


map_data_list = getDataMapDataFile()
mapGroupsData = readJson(JSON_PATH_MAP_GROUPS)

for mapData in map_data_list:
    # delete data/maps
    pathDataMapFolder = os.path.join(ROOT_PATH_DATA_MAP_FOLDER, mapData.get("name"))
    deleteFolder(pathDataMapFolder)
    # #delete data/layout
    pathDataLayoutFolder = os.path.join(ROOT_PATH_DATA_LAYOUT_FOLDER, mapData.get("name"))
    deleteFolder(pathDataLayoutFolder)
    # delte of mapGroups.json
    deleteMapOfMapGroupsJson(mapGroupsData, mapData.get("name"))
    # delete of event_script.s
    deleteEventScript(mapData.get("name"))
    # delete reference layouts.json
    deleteLayoutReference(mapData.get("layout"))

# delete connection with other maps
idsMapArray = [map_item.get('id') for map_item in map_data_list] 

for ruta_directorio, subdirectorios, archivos in os.walk(ROOT_PATH_DATA_MAP_FOLDER):

    modifyFile = False

    if "map.json" in archivos:
        pathJsonFile = os.path.join(ruta_directorio, "map.json")
        dataJson = readJson(pathJsonFile)

        if dataJson:

            filtered_warp_events  = searchMapReferenceInOtherMapJson(dataJson.get("warp_events"), 'dest_map', idsMapArray)
            if filtered_warp_events != dataJson.get("warp_events") and isinstance(dataJson.get("warp_events") , list) :
                dataJson['warp_events'] = None if len(filtered_warp_events) == 0 else filtered_warp_events
                modifyFile = True

            filtered_connections  = searchMapReferenceInOtherMapJson(dataJson.get("connections"), 'map', idsMapArray)
            if filtered_connections != dataJson.get("connections") and isinstance(dataJson.get("connections") , list) :
                dataJson['connections'] = None if len(filtered_connections) == 0 else filtered_connections
                modifyFile = True

            if modifyFile:
                writeJson(pathJsonFile, dataJson)



