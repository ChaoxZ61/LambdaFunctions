import csv
import json
from functools import reduce

with open("Detroit_police_Report.csv","r") as file:
    report = csv.DictReader(file)
    listCsv = list(report)

listFiltered = list(filter(lambda x: x["zip_code"] != "" and x["totalresponsetime"] != "" and x["neighborhood"] != "" and x["totaltime"] != ""\
     and x["dispatchtime"] != "",listCsv))

avgResponseTime = reduce(lambda total, x: total + float(x["totalresponsetime"]), listFiltered,0.0)/len(listFiltered)
print(f"The average of total response time is {avgResponseTime:.2f} minutes.")

avgDispatchTime = reduce(lambda total, x: total + float(x["dispatchtime"]), listFiltered,0.0)/len(listFiltered)
print(f"The average of dispatch time is {avgDispatchTime:.2f} minutes.")

avgTotalTime = reduce(lambda total, x: total + float(x["totaltime"]), listFiltered,0.0)/len(listFiltered)
print(f"The average of total time is {avgTotalTime:.2f} minutes.")

neighbor = []
jsonList = []
trtList = []
dtList = []
ttList = []

for i in listFiltered:
    if i["neighborhood"] not in neighbor:
        neighbor.append(i["neighborhood"])
        
# neighbor = reduce(lambda aList, x: aList.append(x) if (x not in aList) else aList, listFiltered,[])

for i in neighbor:
    current = list(filter(lambda x: x["neighborhood"] == i, listFiltered))

    currentAvgTotalResponseTime = reduce(lambda total, x: total + float(x["totalresponsetime"]), current,0.0)/len(current)
    trtList.append(currentAvgTotalResponseTime)

    currentAvgDispatchTime = reduce(lambda total, x: total + float(x["dispatchtime"]), current,0.0)/len(current)
    dtList.append(currentAvgDispatchTime)

    currentAvgTotalTime = reduce(lambda total, x: total + float(x["totaltime"]), current,0.0)/len(current)
    ttList.append(currentAvgTotalTime)

    jsonList.append({"Neighborhood": neighbor, "Average Total Response Time": currentAvgTotalResponseTime,\
        "Average Total Dispatch Time": currentAvgDispatchTime, "Average Total Time": currentAvgTotalTime})

def avg(aList):
    return sum(aList)/len(aList)

jsonList.append({"Neighborhood": "Detroit", "Average Total Response Time": avg(trtList),\
    "Average Total Dispatch Time": avg(dtList), "Average Total Time": avg(ttList)})

with open("DetroitServices.json","w") as jsonOut:
    json.dump(jsonList,jsonOut)
