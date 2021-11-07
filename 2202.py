from exif import Image
import os
import csv
from geopy.geocoders import Nominatim
import gmplot

# convert coordinates to decimal degrees
def dms_coordinates_to_dd_coordinates(coordinates, coordinates_ref):
    decimal_degrees = coordinates[0] + \
                      coordinates[1] / 60 + \
                      coordinates[2] / 3600

    if coordinates_ref == "S" or coordinates_ref == "W":
        decimal_degrees = -decimal_degrees

    return decimal_degrees


# pulling metadata from the images and saving it to a list
def metaToCSV(images):
    imgInfo = []
    geolocator = Nominatim(user_agent="coordinateconverter")
    for index, image in enumerate(images):
        # check if image has metadata
        if image.has_exif:
            decimal_latitude = dms_coordinates_to_dd_coordinates(image.gps_latitude, image.gps_latitude_ref)
            decimal_longitude = dms_coordinates_to_dd_coordinates(image.gps_longitude, image.gps_longitude_ref)
            url = "https://www.google.com/maps?q="+str(decimal_latitude)+","+str(decimal_longitude)
            loc=decimal_latitude,decimal_longitude
            location = geolocator.reverse(loc)
            status = "contains EXIF (version "+image.exif_version+") information."
            latitude_list.append(decimal_latitude)
            longitude_list.append(decimal_longitude)
            print(index, status)
            print(image.make)
            print(image.model)
            print(image.datetime)
            print(image.datetime_original)
            print(decimal_latitude)
            print(decimal_longitude)
            print(location.address)
            print("\n")

            imgInfo.append([image.make, image.model, image.datetime, image.datetime_original,
                            dms_coordinates_to_dd_coordinates(image.gps_latitude, image.gps_latitude_ref),
                            dms_coordinates_to_dd_coordinates(image.gps_longitude, image.gps_longitude_ref), url,
                            location.address])

        else:
            status = "Image does not contain GPS info."
            print(index, status)
    return imgInfo


def printExifMembers(image_members):
    for index, image_member_list in enumerate(image_members):
        print(index,len(image_member_list))
        print(image_member_list)
        print("\n")


images = []
image_members = []
latitude_list=[]
longitude_list=[]
for filename in os.listdir("/home/deeplearning/sus"):

    with open("/home/deeplearning/sus/" + filename, "rb") as filename:
        filename = Image(filename)
    images.append(filename)
    image_members.append(dir(filename))

data = metaToCSV(images)
printExifMembers(image_members)

header = ['make', 'model', 'date time', 'date time original', 'latitude', 'longitude', 'GMap Url', 'address']
with open('exitf.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)

gmap3 = gmplot.GoogleMapPlotter(1.360347,
                                103.827800, 13)

gmap3.scatter(latitude_list, longitude_list,
              size=100, marker=False)

gmap3.plot(latitude_list, longitude_list,
           'cornflowerblue', edge_width=2.5)
gmap3.draw( "gmplot.html" )
