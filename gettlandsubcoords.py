from pykml import parser

def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

def gettlcoords():
    kml_file = "Buslocs/texastlkml.kml"
    with open(kml_file) as f:
        doc = parser.parse(f)

    root = doc.getroot()

    placemarks = root.Document.Folder.Placemark
    lines = []
    busfounds = []

    for line in placemarks:
        buses = []
        for data in line.ExtendedData.Data:
            if data.attrib['name'] == "BusNumFrom" or data.attrib['name'] == "BusNumTo":
                buses.append(int(data.value.text))
        busfounds.append([min(buses), max(buses)]) #do it like this to avoid both way sequencing issues
        lonlats = []
        for point in line.MultiGeometry.Point:
            locdata = point.coordinates.text
            locdata = locdata.split(',')
            lonlats.append(list(map(float, locdata[0:2])))
        sameconnection = busfounds.count([min(buses), max(buses)])
        lines.append({'busfrom' : buses[0], 'busto' : buses[1], 'from' : lonlats[0], 'to' : lonlats[1], 'connumber' : sameconnection})
    return lines





def getsubcoords():
    kml_file = "Buslocs/texaskml.kml"
    with open(kml_file) as f:
        doc = parser.parse(f)

    root = doc.getroot()
    placemarks = root.Document.Folder.Placemark
    substations = []
    for substation in placemarks:
        buses = []
        text = substation.description.text #do .text to convert string element class to a "real" string
        locs = findOccurrences(text, '(') #all buses are preceded by a (
        for loc in locs: #jus get the entire set of numbers before the closing bracket
            added = 2
            while True:
                if text[loc+added] == ')':
                    break
                added += 1
            buses.append(int(text[loc+1:loc+added])) #append the number to the list
        for data in substation.ExtendedData.Data:
            if data.attrib['name'] == "Number":
                subid = int(data.value.text)
        locdata = substation.Point.coordinates.text
        locdata = locdata.split(',')
        lonlat = list(map(float, locdata[0:2]))
        substations.append({'subid' : subid, 'buses' : buses, 'loc': lonlat})
    
    return substations
