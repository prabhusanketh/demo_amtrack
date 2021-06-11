# Distancematrix     https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins=13.340881,74.742142&destinations=12.915605,74.855965&travelMode=driving&timeUnit=minute&key=AnhOZe_XCLuDlqb6SOYEFFzQ3y_dC2O2xiJHPm4BbHOWDeh5BpMABzzNfPv-CFCM
# BingAPI            AnN_S6vOvSGHcWZ5f6okMnd5iGzc944XAxL4nacb5lWnqDxOptgjOscLXYWFRKdW
# TomTomAPI          CalS1wSGvFTziyjDqzdjr7bEy6QmGHtp

# Importing Libraries
import sys
import json
import re
import urllib.request
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://amtrack-default-rtdb.firebaseio.com/",
})

ref1 = db.reference('Ambulance 1')  # Udupi
ref2 = db.reference('Ambulance 2')  # Surathkal
ref3 = db.reference('Ambulance3')  # NavIC

n = 3
a = []
lat = []
long = []
num = []
stat = []  # 1=Engaged, 0=Vacant
msg = []
atime = []
aatime = []

# x = "13.2303012,74.752326"
y = (sys.argv[1]).split(",")
plat = y[0]
plong = y[1]

b = []
c = []
d = []
f = ref1.get()
g = ref2.get()
h = ref3.get()

for i in f:
    b.append(str(f[i]))
for i in g:
    c.append(str(g[i]))
for i in h:
    d.append(str(h[i]))
a = b + c + d

for i in range(0, 13, 6):
    lat.append(a[i])
for i in range(1, 14, 6):
    long.append(a[i])

ref1.update({
    'lat': float(lat[0]),
    'lng': float(long[0])
})

ref2.update({
    'lat': float(lat[1]),
    'lng': float(long[1])
})

ref3.update({
    'lat': float(lat[2]),
    'lng': float(long[2])
})

for i in range(3, 16, 6):
    num.append(a[i])
for i in range(4, 17, 6):
    stat.append(a[i])
stat1 = []
for i in stat:
    stat1.append(int(i))
statind = []

# print(lat, long, num, stat1)
for i in range(3):
    if stat1[i] == 1:
        statind.append(i)

for i in sorted(statind, reverse=True):
    del stat1[i]
    del lat[i]
    del long[i]
    del num[i]

# print(lat, long, num, stat1)

if len(stat1) == 0:
    print("All our Ambulances are engaged. Please try again after some time.")
else:
    for i in range(0, len(stat1)):
        # Defining Distance Matrix URL
        timeurl = "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins=" + str(lat[i]) + "," + str(long[
                                                                                                                      i]) + "&destinations=" + plat + "," + plong + "&travelMode=driving&timeUnit=minute&key=AnN_S6vOvSGHcWZ5f6okMnd5iGzc944XAxL4nacb5lWnqDxOptgjOscLXYWFRKdW"

        # URL Operation
        request = urllib.request.Request(timeurl)
        response = urllib.request.urlopen(request)

        # Parsing Distance Matrix JSON
        r = response.read().decode(encoding="utf-8")
        data = json.loads(r)
        a = str(data['resourceSets'])

        # Finding values using regular expression
        regex = '\d+\.\d+'
        match = re.findall(regex, a)
        atime.append(match[5])

    # Finding Nearest Ambulance
    for j in atime:
        b = float(j)
        aatime.append(b)

    myindex = aatime.index(min(aatime))

    if num[myindex] == '9108302604':
        ref1.update({
            'stat': 1
        })
    if num[myindex] == '9980253852':
        ref2.update({
            'stat': 1
        })
    if num[myindex] == '9663563745':
        ref3.update({
            'stat': 1
        })

    final = min(aatime)
    #  print("Your Ambulance will reach your place in", final, "mins")

    a1_route = []
    a2_route = []
    route_url = "http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0=" + plat + "," + plong + "&wp.1=" + str(
        lat[myindex]) + "," + str(
        long[myindex]) + "&optmz=timeWithTraffic&key=AnhOZe_XCLuDlqb6SOYEFFzQ3y_dC2O2xiJHPm4BbHOWDeh5BpMABzzNfPv-CFCM"
    request_route = urllib.request.Request(route_url)
    response_route = urllib.request.urlopen(request_route)
    r_route = response_route.read().decode(encoding="utf-8")
    a_route = json.loads(r_route)
    for i_route in a_route["resourceSets"]:
        b_route = i_route["resources"]
    for i_route in b_route:
        c_route = i_route["routeLegs"]
    for i_route in c_route:
        d_route = i_route["itineraryItems"]
    for i_route in d_route:
        a1_route.append(i_route["instruction"])
    for i_route in a1_route:
        a2_route.append(i_route["text"])
    route = ','.join([str(elem) for elem in a2_route])
    # print(route)

    url = "https://www.fast2sms.com/dev/bulk"
    payload = "sender_id=FSTSMS&message=" + "Patient at http://www.google.com/maps/place/" + plat + "," + plong + "  ," + route + "&language=english&route=p&numbers=" + str(
        num[myindex])
    headers = {
        'authorization': "lf2FdhnsMPCbKQzxH76rwW1qJaV0UpBkovRGgtZTXyNEYjS9537AGVBPjZomEguxFf3zsq2a8rKXMnN5",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)

    # print(response.text)

    output = final
    print("Your Ambulance will reach your place in", output, "mins")
