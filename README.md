# Coordinate-Transformation
Functions in python to perform coordinate transformation (cartesian, spherical, and map projection)
ecef_geodetic - to convert from ecef to Latitude-Longitude and height.
geodetic_ecef - to convert from Latitude-Longitude pairs (in degrees)and height to ECEF in metres.
geodetic_utm - convert from latitude-longitude pairs to utm map projection system
utm_geodetic -  convert from utm map projection to geodetic latitude-longitude pairs.

ECEF (acronym for earth-centered, earth-fixed), It represents positions as X, Y, and Z coordinates.
- The origin (0,0,0) is the centre of mass of the earth.
- The positive X axis passes through the Americas at LatLong(0, -90)
- The positive Y axis passes through the South-North pole
- The positive Z axis passes through the prime meridian (0 longitude) at LatLong(0, 0)
