from math import cos
from math import sin
from math import atan
from math import sqrt
from math import pi
from math import radians

def geodetic2xyz(latitude,longitude,h):

    a = 6378137.0
    b = 6356752.314245
    
    lat = radians(latitude)
    lon = radians(longitude)
    e2 = 1 - (b/a)**2
    n = a/sqrt(1-e2*sin(lat)**2)
    
    x = (h + n)*cos(lat)*cos(lon)
    y = (h + n)*cos(lat)*sin(lon)
    z = (h + n - e2*n)*sin(lat)
    return(x,y,z)

def xyz2geodetic(x,y,z):
    
    a = 6378137.0
    b = 6356752.314245
    e2 = 1 - (b/a)**2
    e = sqrt(e2)  #eccentricity

    lon = atan(y/x) #geodetic longitude
    r = sqrt(x**2 + y**2 + z**2) #Physical radius
    p = sqrt(x**2 + y**2) #radius in xy plane

    lat_c = atan(p/z) #geocentric latitude
    lat = lat_c
    count = 0
    while (count < 6):
        Rn = a/sqrt(1 - e2*sin(lat)**2)
        h = p/cos(lat) - Rn
        tmp = 1.0/(1-e2*(Rn/(Rn+h)))
        lat = atan((z/p)*tmp)
        count = count + 1
    #end of looping
    lon_deg = lon*180/pi + 180
    lat_deg = lat*180/pi
    height = h
    return(lat_deg,lon_deg,height)

def dms(degree):
    d = int(degree)
    ms =(degree - d)*60.0
    m = int(ms)
    s = (ms-m)* 60.0
    return(d,m,s)
