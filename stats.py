import requests
import json
import math
import pandas as pd

# This module interacts with the balldontlie API
def findPlayerId(name):
    lastName = name.split()[-1]
    firstName = name.split()[0]
    url = "https://www.balldontlie.io/api/v1/players?per_page=100&search=" + firstName + "_" + lastName
    response = requests.get(url)
    jsonResp = response.json()

    if len(jsonResp["data"]) == 0:
        return "Null"
    else:
        return jsonResp["data"][0]["id"]


def getPlayerStats(id):
    url = "https://www.balldontlie.io/api/v1/stats?seasons[]=2019&per_page=100&player_ids[]=" + str(id)
    response = requests.get(url)
    jsonResp = response.json()
    return jsonResp["data"]

def getSeasonAvg(id):
    url = "https://www.balldontlie.io/api/v1/season_averages?season=2019&player_ids[]=" + str(id)
    response = requests.get(url)
    jsonResp = response.json()
    return jsonResp["data"]

def calcStdDev(data, avg, name):
    if len(avg) > 0:
        gameNum = avg[0]["games_played"]
        ptsAvg = avg[0]["pts"]
        blkAvg = avg[0]["blk"]
        stlAvg = avg[0]["stl"]
        astAvg = avg[0]["ast"]
        rebAvg = avg[0]["reb"]
        tpmAvg = avg[0]["fg3m"]
        fgAvg = avg[0]["fg_pct"]
        ftAvg = avg[0]["ft_pct"]

        ptsStd = 0
        blkStd = 0
        stlStd = 0
        astStd = 0
        rebStd = 0
        tpmStd = 0
        fgStd = 0
        ftStd = 0

        for game in data:
            ptsStd += (int(game["pts"]) - int(ptsAvg))**2
            blkStd += (game["blk"] - blkAvg)**2
            stlStd += (game["stl"] - stlAvg)**2
            astStd += (game["ast"] - astAvg)**2
            rebStd += (game["reb"] - rebAvg)**2
            tpmStd += (game["fg3m"] - tpmAvg)**2
            fgStd += (game["fg_pct"]/100 - fgAvg)**2
            ftStd += (game["ft_pct"]/100 - ftAvg)**2

        ptsStd = round(math.sqrt(ptsStd/gameNum), 2)
        blkStd = round(math.sqrt(blkStd/gameNum), 2)
        stlStd = round(math.sqrt(stlStd/gameNum), 2)
        astStd = round(math.sqrt(astStd/gameNum), 2)
        rebStd = round(math.sqrt(rebStd/gameNum), 2)
        tpmStd = round(math.sqrt(tpmStd/gameNum), 3)
        fgStd = round(math.sqrt(fgStd/gameNum), 3)
        ftStd = round(math.sqrt(ftStd/gameNum), 3)
    else: 
        ptsStd = blkStd = stlStd = astStd = rebStd = tpmStd = fgStd = ftStd = ptsAvg = blkAvg = stlAvg = astAvg = rebAvg = tpmAvg = fgAvg = ftAvg = math.nan

    stdDevDict = {
        "Player": name,
        "pts": ptsStd,
        "blk": blkStd,
        "stl": stlStd,
        "ast": astStd,
        "reb": rebStd,
        "tpm": tpmStd,
        "fg": fgStd,
        "ft": ftStd,
        "avgpts": ptsAvg,
        "avgblk": blkAvg,
        "avgstl": stlAvg,
        "avgast": astAvg,
        "avgreb": rebAvg,
        "avgtpm": tpmAvg,
        "avgfg": fgAvg,
        "avgft": ftAvg,
    }
    return stdDevDict


#print(findPlayerId("Jaylen Brown"))
#id = findPlayerId("Jaylen Brown")
#print(calcStdDev(getPlayerStats(id), getSeasonAvg(id), "Jaylen Brown"))
