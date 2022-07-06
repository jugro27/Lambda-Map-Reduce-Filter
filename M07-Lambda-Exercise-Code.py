import csv
import json
from functools import reduce

# PART 1

cFSF = open('911_Calls_For_Service_(Last_30_Days).csv', 'r')
callsForServiceDict = csv.DictReader(cFSF)

filteredDictList = list(filter(lambda row: row["zip_code"] != "" and row["neighborhood"] != "" and row["totalresponsetime"] != "" and row["dispatchtime"] != "" and row["totaltime"] != "", callsForServiceDict))

totalResponseTime = reduce(lambda tRT1, dict: tRT1 + float(dict["totalresponsetime"]), filteredDictList, 0)
averageTotalResponseTime = (totalResponseTime/len(filteredDictList))
print(f"Average Total Response Time: {averageTotalResponseTime}")

totalDispatchTime = reduce(lambda tDT1, dict: tDT1 + float(dict["dispatchtime"]), filteredDictList, 0)
averageTotalDispatchTime = (totalDispatchTime/len(filteredDictList))
print(f"Average Total Dispatch Time: {averageTotalDispatchTime}")

totalTime = reduce(lambda tTT1, dict: tTT1 + float(dict["totaltime"]), filteredDictList, 0)
averageTotalTime = (totalTime/len(filteredDictList))
print(f"Average Total Time: {averageTotalTime}")


# PART 2

neighborhoods = []

for i in filteredDictList:
    if i["neighborhood"] not in neighborhoods:
        neighborhoods.append(i["neighborhood"])

jsonOut = []
for i in neighborhoods:

    currentNeighborhood = list(filter(lambda row: row["neighborhood"] == i, filteredDictList))
    #print(currentNeighborhood)

    nhTotalResponseTime = reduce(lambda nTRT, dict: nTRT + float(dict["totalresponsetime"]), currentNeighborhood, 0)
    nhAverageResponseTime = (nhTotalResponseTime/len(currentNeighborhood))
    #print(f"{currentNeighborhood}'s average response time: {nhAverageResponseTime}")

    nhTotalDispatchTime = reduce(lambda nTDT, dict: nTDT + float(dict["dispatchtime"]), currentNeighborhood, 0)
    nhAverageDispatchTime = (nhTotalDispatchTime/len(currentNeighborhood))
    #print(f"{currentNeighborhood}'s average dispatch time: {nhAverageDispatchTime}")

    nhTotalTime = reduce(lambda nTTT, dict: nTTT + float(dict["totaltime"]), currentNeighborhood, 0)
    nhAverageTotalTime = (nhTotalTime/len(currentNeighborhood))
    #print(f"{currentNeighborhood}'s average total time: {nhAverageTotalTime}")


    # PART 3
    # Was not sure how to get the neighborhood times assigned to each neighborhood
    # It grouped them up instead, so need to ask question about that


    jsonOut.append({"Neighborhoods": neighborhoods, "Average Total Response Time": nhTotalResponseTime, 
                "Average Total Dispatch Time": nhAverageDispatchTime, "Average Total Time": nhAverageTotalTime})

jsonOut.append({"Neighborhoods": "Overall", "Average Total Response Time": averageTotalResponseTime, 
                "Average Total Dispatch Time": averageTotalDispatchTime, "Average Total Time": averageTotalTime})

with open("callsForServiceOut.json", "w") as outfile:
    json.dump(jsonOut, outfile)


cFSF.close()