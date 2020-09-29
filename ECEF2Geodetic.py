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

def user_input():
    str1 = 'S 03 26 20.75675'
    str2 = 'E 102 11 38.87299'
    h = 164.0179
    print(str1, '  ',str2, '  ',h)
    ls = str1.split(' ')
    bs = str2.split(' ')

    ns = ls[0]
    ew = bs[0]
    lat = float(ls[1]) + float(ls[2])/60 + float(ls[3])/3600
    lon = float(bs[1]) + float(bs[2])/60 + float(bs[3])/3600
    if ns == 'S' or ns == 's':
        lat = -1*lat
    if ew == 'W' or ew == 'w':
        lon = -1 * lon
      
    return(lat,lon,h)

def main():
    latlon = user_input()
    lat = latlon[0]
    lon = latlon[1]
    height = latlon[2]
    print(lat,lon)

    xyz = geodetic2xyz(lat,lon,height)
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]

    print(x,y,z)

    lb = xyz2geodetic(x,y,z)
    l = lb[0]
    b = lb[1]
    h = lb[2]

    lintang = dms(l)
    bujur = dms(b)
    height = h

    print(lintang,'   ',bujur, '  ', height)
    
