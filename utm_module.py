from math import radians
from math import degrees
from math import cos
from math import cosh
from math import sin
from math import sinh
from math import asinh
from math import atan2
from math import atanh
from math import atan
from math import tan
from math import sqrt

def dms(sdt):
    sdt = abs(sdt)
    d=int(sdt)
    t = (sdt-d)*60
    m = int(t)
    s = (t-m)*60
    return(d,m,s)

def geo_utm(lat,lon):
    a,f = 6378137.0, 1 / 298.257223563 #datum WGS84 and flatening
    ko = 0.9996 # UTM scale factor on the central meridian
    ns = 'N'
    ew = 'E'

    # identifying North or South
    if lat < 0:
        ns = 'S'
        lat = abs(lat)

    # identifying East or West and calculating meridian centre
    if lon < 0:
        bo = int(lon/6)*6 - 3 # for western
        ew = 'W'
    else:
        bo = int(lon/6)*6 + 3 # for eastern

    # Converting to radians  
    λo = radians(bo)
    φ = radians(lat)
    λ = radians(lon)- λo

    #computtion
    e = sqrt(f*(2-f))

    n = f / (2 - f)
    n2 = n*n
    n3 = n2*n
    n4 = n3*n
    n5 = n4*n
    n6 = n5*n
    n7 = n6*n    
    n8 = n7*n
    
    cosλ = cos(λ)
    sinλ = sin(λ)
    tanλ = tan(λ)

    τ = tan(φ)
    σ = sinh(e*atanh(e*τ/sqrt(1+τ*τ)))
    τ1 = τ*sqrt(1+σ*σ) - σ*sqrt(1+τ*τ)
    ξ1 = atan2(τ1, cosλ)
    η1 = asinh(sinλ / sqrt(τ1*τ1 + cosλ*cosλ))

    A = a/(1+n) * (1 + 1/4*n2 + 1/64*n4 + 1/256*n6 + 25/16384*n8)

    α1 = 1/2*n - 2/3*n2 + 5/16*n3 + 41/180*n4 - 127/288*n5 + 7891/37800*n6 + 72161/387072*n7 - 18975107/50803200*n8
    α2 = 13/48*n2 - 3/5*n3 + 557/1440*n4 + 281/630*n5 - 1983433/1935360*n6 + 13769/28800*n7 + 148003883/174182400*n8
    α3 = 61/240*n3 - 103/140*n4 + 15061/26880*n5 + 167603/181440*n6 - 67102379/29030400*n7 + 79682431/79833600*n8
    α4 = 49561/161280*n4 - 179/168*n5 + 6601661/7257600*n6 + 97445/49896*n7 + 40176129013/7664025600*n8
    α5 = 34729/80640*n5 - 3418889/1995840*n6 + 14644087/9123840*n7 + 2605413599/622702080*n8
    α6 = 212378941/319334400*n6 - 30705481/10378368*n7 + 175214326799/58118860800*n8
    α7 = 1522256789/1383782400*n7 - 16759934899/3113510400*n8
    α8 = 1424729850961/743921418240*n8

    ξ = ξ1 + α1*sin(2*ξ1)*cosh(2*η1) + α2*sin(4*ξ1)*cosh(4*η1) + α3*sin(6*ξ1)*cosh(6*η1) + α4*sin(8*ξ1)*cosh(8*η1) + α5*sin(10*ξ1)*cosh(10*η1) + α6*sin(12*ξ1)*cosh(12*η1) + α7*sin(14*ξ1)*cosh(14*η1) + α8*sin(16*ξ1)*cosh(16*η1)
    η = η1 + α1*cos(2*ξ1)*sinh(2*η1) + α2*cos(4*ξ1)*sinh(4*η1) + α3*cos(6*ξ1)*sinh(6*η1) + α4*cos(8*ξ1)*sinh(8*η1) + α5*cos(10*ξ1)*sinh(10*η1) + α6*cos(12*ξ1)*sinh(12*η1) + α7*cos(14*ξ1)*sinh(14*η1) + α8*cos(16*ξ1)*sinh(16*η1)

    # UTM Coordinate
    x = 500000 + ko*A*η
    y = ko*A*ξ
    if(ns=='S'):
        y = 10000000 - y

    # UTM Meridian Convergency
    p1 = 1
    q1 = 0
    p1 = p1 + 2*α1*cos(2*ξ1)*cosh(2*η1) + 4*α2*cos(4*ξ1)*cosh(4*η1) + 6*α3*cos(6*ξ1)*cosh(6*η1) + 8*α4*cos(8*ξ1)*cosh(8*η1) + 10*α5*cos(10*ξ1)*cosh(10*η1) + 12*α6*cos(12*ξ1)*cosh(12*η1)
    q1 = q1 + 2*α1*sin(2*ξ1)*sinh(2*η1) + 4*α2*sin(4*ξ1)*sinh(4*η1) + 6*α3*sin(6*ξ1)*sinh(6*η1) + 8*α4*sin(8*ξ1)*sinh(8*η1) + 10*α5*sin(10*ξ1)*sinh(10*η1) + 12*α6*sin(12*ξ1)*sinh(12*η1)
    γ1 = atan(τ1 / sqrt(1+τ1*τ1)*tanλ)
    γ2 = atan2(q1,p1)
    γ = degrees(γ1 + γ2)
    if((lon<bo and lat>0) or (lon>bo and lat<0)):
        γ = -1*γ

    # UTM Scale Factor
    sinφ = sin(φ)
    k1 = sqrt(1 - e*e*sinφ*sinφ) * sqrt(1 + τ*τ) / sqrt(τ1*τ1 + cosλ*cosλ);
    k2 = A / a * sqrt(p1*p1 + q1*q1)
    k = ko * k1 * k2

    # UTM Zone Number
    zone = round((lon + 180)/6 + 0.5)   

    return(x,y,zone,bo,k,γ)

def utm_geo(East,North,zone):
    a,f,ko = 6378137.0, 1 / 298.257223563, 0.9996
    FalseEasting,FalseNorthing = 500e3,10000e3
    x = East-FalseEasting
    y = North
    z = int(zone[0:2]) #UTM Zone number
    bo = radians((z-1)*6 - 180 + 3) 

    e = sqrt(f*(2-f))
    n = f / (2 - f)
    n2 = n*n
    n3 = n2*n
    n4 = n3*n
    n5 = n4*n
    n6 = n5*n

    A = a/(1+n)*(1 + (1/4)*n2 + (1/64)*n4 + (1/256)*n6)

    η = x/(ko*A)
    ξ = y/(ko*A)

    β1 = 1/2*n - 2/3*n2 + 37/96*n3 - 1/360*n4 - 81/512*n5 + 96199/604800*n6
    β2 = 1/48*n2 + 1/15*n3 - 437/1440*n4 + 46/105*n5 - 1118711/3870720*n6
    β3 = 17/480*n3 - 37/840*n4 - 209/4480*n5 + 5569/90720*n6
    β4 = 4397/161280*n4 - 11/504*n5 - 830251/7257600*n6
    β5 = 4583/161280*n5 - 108847/3991680*n6
    β6 = 20648693/638668800*n6 

    ξ1 = ξ - β1*sin(2*ξ)*cosh(2*η) - β2*sin(4*ξ)*cosh(4*η) - β3*sin(6*ξ)*cosh(6*η) - β4*sin(8*ξ)*cosh(8*η) - β5*sin(10*ξ)*cosh(10*η) - β6*sin(12*ξ)*cosh(12*η)
    η1 = η - β1*cos(2*ξ)*sinh(2*η) - β2*cos(4*ξ)*sinh(4*η) - β3*cos(6*ξ)*sinh(6*η) - β4*cos(8*ξ)*sinh(8*η) - β5*cos(10*ξ)*sinh(10*η) - β6*cos(12*ξ)*sinh(12*η)

    sinh1 = sinh(η1)
    sinξ1 = sin(ξ1)
    cosξ1 = cos(ξ1)
    τ1 = sinξ1 / sqrt(sinh1*sinh1 + cosξ1*cosξ1)

    δτi = 1
    τi = τ1
    while(abs(δτi)> 1e-12):
        σi = sinh(e*atanh(e*τi/sqrt(1+τi*τi)))
        τi1 = τi*sqrt(1+σi*σi) - σi*sqrt(1+τi*τi)
        δτi = (τ1-τi1)/sqrt(1+τi1*τi1)*(1 + (1-e*e)*τi*τi) / ((1-e*e)*sqrt(1+τi*τi));
        τi += δτi;
    τ = τi
    φ = degrees(atan(τ))
    λ = degrees(bo + atan2(sinh1,cosξ1))
    return(φ,λ)

