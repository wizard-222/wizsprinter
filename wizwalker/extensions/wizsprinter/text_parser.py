import os
import json
pathDict = {}
gateDict = {}
npc_dict = {}

def parseFile(fileName):
    file = open(fileName)
    lines = file.readlines()
    return lines

def parseWorlds():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    lines = parseFile(dir_path + "/traversalData/zoneMap.txt")
    lines = iter(lines)
    for line in lines:
        line = line.strip()
        if 'END' in line:
            continue
        elif 'ZONEDOOR' in line:
            zone = line.rsplit(';', 1)[-1].lower()
            pathDict[zone] = "ZONEDOOR"
        else:
            zone = line.rsplit(';', 1)[-1].lower()
            subzone = line.rsplit(';', 1)[0].lower()
            pathDict[zone] = subzone
    return

def parseGates():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    lines = parseFile(dir_path + "/traversalData/gates_list.txt")
    lines = iter(lines)
    for line in lines:
        line = line.strip()
        parsedLines = line.split(';')
        if len(parsedLines) == 6:
            type = parsedLines[0]
            x = float(parsedLines[1])
            y = float(parsedLines[2])
            z = float(parsedLines[3])
            currentZone = parsedLines[4].lower()
            destinationZone = parsedLines[5].lower()
            if currentZone in gateDict:
                gateDict[currentZone][destinationZone] = {"x": x, "y": y, "z": z, "type": type}
            else:
                gateDict[currentZone] = {}
                gateDict[currentZone][destinationZone] = {"x": x,"y": y, "z": z, "type": type}

def parseUniqueObjectLocations():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    lines = parseFile(dir_path + "/traversalData/uniqueObjectLocations.txt")
    lines = iter(lines)
    for line in lines:
        line = line.strip()
        parsedLines = line.split(';')
        if len(parsedLines) == 5:
            npc_name = parsedLines[0].lower()
            x = float(parsedLines[1])
            y = float(parsedLines[2])
            z = float(parsedLines[3])
            zone = parsedLines[4].lower()
            if zone in npc_dict:
                npc_dict[zone][npc_name] =  {"x": x, "y": y, "z": z, "type": "standard"}
            else:
                npc_dict[zone] = {}
                npc_dict[zone][npc_name] =  {"x": x, "y": y, "z": z, "type": "standard"}
#
def recursiveGetPath(currentZone, return_dict):
        newZone = pathDict[currentZone]
        newPath = gateDict[currentZone]
        if (newZone == 'ZONEDOOR'):
            return_dict['zonedoor'] = npc_dict[currentZone]['zonedoor']
            return return_dict
        else:
            return_dict[newZone] = newPath[newZone]
            return recursiveGetPath(newZone, return_dict)

def getPathToZoneDoor(currentZone):
    return_dict = {}
    return recursiveGetPath(currentZone, return_dict)

def recursiveGetPathToZone(currentZone, endZone, return_dict):
        if currentZone == endZone:
            return return_dict
        newPath = gateDict[currentZone]
        if endZone in newPath:
            return_dict[endZone] = newPath[endZone]
            return return_dict
        else:
            newZone = pathDict[currentZone]
            return_dict[newZone] = newPath[newZone]
            return recursiveGetPathToZone(newZone, endZone, return_dict)

def getPathToZone(currentZone, endZone):
    return_dict = {}
    return recursiveGetPathToZone(currentZone, endZone, return_dict)

def recursiveBackTrack(currentZone, end_zone, return_dict):
        if (currentZone == "ZONEDOOR"):
            return return_dict
        return_dict[end_zone] = gateDict[currentZone][end_zone]
        traversePath = pathDict[currentZone]
        return recursiveBackTrack(traversePath, currentZone, return_dict)

def backTrackZone(startZone, end_zone):
    return_dict = {}
    return dict(reversed(recursiveBackTrack(startZone, end_zone, return_dict).items()))

# Returns dict and bool indicating if resulting path was found
def getPath(currentWorld, destinationWorld):
    destinationWorld = destinationWorld.lower()
    currentWorld = currentWorld.lower()
    return_dict = {}
    append_dict = {}
    if (destinationWorld not in pathDict):
        return {}
    if currentWorld.split('/', 1)[0].lower() != destinationWorld.split('/', 1)[0].lower():
        return_dict = getPathToZoneDoor(currentWorld)
        append_dict = backTrackZone(pathDict[destinationWorld], destinationWorld)
    else:
        append_dict = getPathToZone(currentWorld, destinationWorld)
    return_dict.update(append_dict)
    return return_dict

def init():
    parseWorlds()
    parseGates()
    parseUniqueObjectLocations()

def main():
    parseWorlds()
    parseGates()
    parseUniqueObjectLocations()
    path = getPath("WizardCity/Interiors/WC_SchoolDeath", 'WizardCity/WC_Golem_Tower')
    # print(json.dumps(path, indent=4))

if __name__ == "__main__":
    main()
