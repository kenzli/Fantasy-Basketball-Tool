import requests
import json
import pandas as pd
from stats import *

quit = False

league_id = 1789757869

year = 2021

teamUrl = "https://fantasy.espn.com/apis/v3/games/fba/seasons/" + str(year) + "/segments/0/leagues/" + str(league_id) + "?view=mTeam"
rosterUrl = "https://fantasy.espn.com/apis/v3/games/fba/seasons/" + str(year) + "/segments/0/leagues/" + str(league_id) + "?view=mRoster"
rostResp = requests.get(rosterUrl,
                 cookies={"swid": "{04B8953D-80C0-4866-8A06-4E33E16CAEC1}",
                          "espn_s2": "AEAaVC1FfKwuEkFRsOghRWzbkSyNPFpjfWsIcXgPVGBpVpopLKaaz4%2BxNeGgvuBKYrvuf%2BE8HL1Ydc7Vi9yaMhiA5bP4NHja9wpaqwknr%2FQTntUjb5T00vCmQw2tGF6roASKRT1SzUxfAbNDkBugQjVCp8lHtQq%2FdjHwffThPehXDLCXZNY0kwtYrQ3LYDt4vlH4jeYfBN3FunLncczgqbkh1V4kzF8Qqcz%2FY7ARx2LiFMC%2FDdhtPiv0Vavg91HcVAE7r2TZIcYANpvTCdZvMPDl"})
rostJson = rostResp.json()

teamResp = requests.get(teamUrl,
                 cookies={"swid": "{04B8953D-80C0-4866-8A06-4E33E16CAEC1}",
                          "espn_s2": "AEAaVC1FfKwuEkFRsOghRWzbkSyNPFpjfWsIcXgPVGBpVpopLKaaz4%2BxNeGgvuBKYrvuf%2BE8HL1Ydc7Vi9yaMhiA5bP4NHja9wpaqwknr%2FQTntUjb5T00vCmQw2tGF6roASKRT1SzUxfAbNDkBugQjVCp8lHtQq%2FdjHwffThPehXDLCXZNY0kwtYrQ3LYDt4vlH4jeYfBN3FunLncczgqbkh1V4kzF8Qqcz%2FY7ARx2LiFMC%2FDdhtPiv0Vavg91HcVAE7r2TZIcYANpvTCdZvMPDl"})
teamJson = teamResp.json()

teamDict = {}

print("League Teams:")
for team in teamJson["teams"]:
    teamName = team["location"] + " " + team["nickname"]
    print(teamName)
    teamDict[teamName] = team["id"]

#Ken ID: 7

# Stats: 
# 0: Points
# 1: Blocks
# 2: Steals
# 3: Assists
# 6: Rebounds
# 17: 3PM (3 Points Made)
# 19: FG%
# 20: FT%


while not quit:
    print("Which team would you like analyzed? (Enter 'q' to quit)")
    x = input()
    if (x == "q"): quit = True
    elif x not in teamDict:
        print("That is an invalid team name")
    else: 
        teamId = teamDict[x]
        playerArr = []
        ptsArr = []
        blkArr = []
        stlArr = []
        astArr = []
        rebArr = []
        tpmArr = []
        fgArr = []
        ftArr = []

        stdPtsArr = []
        stdBlkArr = []
        stdStlArr = []
        stdAstArr = []
        stdRebArr = []
        stdTpmArr = []
        stdFgArr = []
        stdFtArr = []

        avgPtsArr = []
        avgBlkArr = []
        avgStlArr = []
        avgAstArr = []
        avgRebArr = []
        avgTpmArr = []
        avgFgArr = []
        avgFtArr = []

        for player in rostJson["teams"][teamId - 1]["roster"]["entries"]:
            name = player["playerPoolEntry"]["player"]["fullName"]
            playerArr.append(name)
            print(name)
            #if (name == "Alec Burks" or name == "Terry Rozier"): print(player["playerPoolEntry"]["player"]["stats"])
            try:
                ptsArr.append(round(player["playerPoolEntry"]["player"]["stats"][0]["averageStats"]["0"], 2))
                blkArr.append(round(player["playerPoolEntry"]["player"]["stats"][0]["averageStats"]["1"], 2))
                stlArr.append(round(player["playerPoolEntry"]["player"]["stats"][0]["averageStats"]["2"], 2))
                astArr.append(round(player["playerPoolEntry"]["player"]["stats"][0]["averageStats"]["3"], 2))
                rebArr.append(round(player["playerPoolEntry"]["player"]["stats"][0]["averageStats"]["6"], 2))
                tpmArr.append(round(player["playerPoolEntry"]["player"]["stats"][0]["averageStats"]["17"], 2))
                fgArr.append(round(player["playerPoolEntry"]["player"]["stats"][0]["averageStats"]["19"], 2))
                ftArr.append(round(player["playerPoolEntry"]["player"]["stats"][0]["averageStats"]["20"], 2))
            except:
                ptsArr.append(math.nan)
                blkArr.append(math.nan)
                stlArr.append(math.nan)
                astArr.append(math.nan)
                rebArr.append(math.nan)
                tpmArr.append(math.nan)
                fgArr.append(math.nan)
                ftArr.append(math.nan)

            id = findPlayerId(name)
            stdDevDict = calcStdDev(getPlayerStats(id), getSeasonAvg(id), name)
            stdPtsArr.append(stdDevDict["pts"])
            stdBlkArr.append(stdDevDict["blk"])
            stdStlArr.append(stdDevDict["stl"])
            stdAstArr.append(stdDevDict["ast"])
            stdRebArr.append(stdDevDict["reb"])
            stdTpmArr.append(stdDevDict["tpm"])
            stdFgArr.append(stdDevDict["fg"])
            stdFtArr.append(stdDevDict["ft"])

            avgPtsArr.append(stdDevDict["avgpts"])
            avgBlkArr.append(stdDevDict["avgblk"])
            avgStlArr.append(stdDevDict["avgstl"])
            avgAstArr.append(stdDevDict["avgast"])
            avgRebArr.append(stdDevDict["avgreb"])
            avgTpmArr.append(stdDevDict["avgtpm"])
            avgFgArr.append(stdDevDict["avgfg"])
            avgFtArr.append(stdDevDict["avgft"])

        #print(playerArr)

        df = pd.DataFrame(
            {
                "Player": playerArr,
                "Pts": ptsArr,
                "Blk": blkArr,
                "Stl": stlArr,
                "Ast": astArr,
                "Reb": rebArr,
                "3PM": tpmArr,
                "FG%":fgArr,
                "FT%": ftArr,
                "AvgPts": avgPtsArr,
                "AvgBlk": avgBlkArr,
                "AvgStl": avgStlArr,
                "AvgAst": avgAstArr,
                "AvgReb": avgRebArr,
                "Avg3PM": avgTpmArr,
                "AvgFG%": avgFgArr,
                "AvgFT%": avgFtArr,
                "StdPts": stdPtsArr,
                "StdBlk": stdBlkArr,
                "StdStl": stdStlArr,
                "StdAst": stdAstArr,
                "StdReb": stdRebArr,
                "Std3PM": stdTpmArr,
                "StdFG%": stdFgArr,
                "StdFT%": stdFtArr,
            }
        )

        df["Perf"] = ((df["Pts"] - df["AvgPts"]) / df["StdPts"] +
                        (df["Blk"] - df["AvgBlk"]) / df["StdBlk"] +
                        (df["Stl"] - df["AvgStl"]) / df["StdStl"] +
                        (df["Ast"] - df["AvgAst"]) / df["StdAst"] +
                        (df["Reb"] - df["AvgReb"]) / df["StdReb"] +
                        (df["3PM"] - df["Avg3PM"]) / df["Std3PM"] +
                        (df["FG%"] - df["AvgFG%"]) / df["StdFG%"] +
                        (df["FT%"] - df["AvgFT%"]) / df["StdFT%"])


        print(df)
