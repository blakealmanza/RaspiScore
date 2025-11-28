import espn_scraper as espn
import json
import methods.getOdds as getOdds
import methods.getBroadcasts as getBroadcasts
import methods.changeTime as changeTime
import methods.getLogo as getLogo

def getData(conferenceID):
    events_data = []
    urls = espn.get_current_scoreboard_urls(league='ncf')

    for scoreboard_url in urls:
        if conferenceID != 0:
            data = espn.get_url(scoreboard_url + "&groups=" + str(conferenceID))
        else:
            data = espn.get_url(scoreboard_url)

    print("\n" + "-"*40 + "\n")

    for event in data["events"]:
        event_data = {}
        event_data.clear()
        short_detail = event["status"]["type"]["shortDetail"]
        event_data["short detail"] = f"{short_detail}"

        if short_detail.find("Final") != 0:
            print(getBroadcasts.main(event))
            event_data["broadcasts"] = getBroadcasts.main(event)

        print(getOdds.main('football', 'college-football', event, short_detail))
        event_data["odds"] = getOdds.main('football', 'college-football', event, short_detail)

        if short_detail.find(":") != -1 and (short_detail.find("EDT") != -1 or short_detail.find("EST") != -1):
            print(changeTime.main(short_detail))
            event_data["start time"] = changeTime.main(short_detail)

        for competition in event["competitions"]:

            down_distance_text = str(competition.get("situation", {}).get("downDistanceText"))
            possession_id = competition.get("situation", {}).get("possession")

            if down_distance_text == 'None':
                pass
            else:
                print(down_distance_text)
                event_data["down and distance"] = down_distance_text

            team_id = 0
            for team in competition["competitors"]:
                team_id += 1

                team_abbreviation = team["team"]["shortDisplayName"]
                rank = team["curatedRank"].get("current", "NR")
                team_score = team["score"]

                event_data["logo" + str(team_id)] = getLogo.main(team)

                possession_marker = "*" if team["id"] == possession_id else ""

                event_data["team" + str(team_id) + " name"] = team_abbreviation
                event_data["team" + str(team_id) + " score"] = team_score

                if short_detail.find('EDT') == -1:
                    if rank < 26:
                        print(f"#{rank:<2} {team_abbreviation} - {team_score}  {possession_marker}")
                    else:
                        print(f"    {team_abbreviation} - {team_score}  {possession_marker}")
                else:
                    print(f"{team_abbreviation}")

        events_data.append(event_data)
        print("\n" + "-"*40 + "\n")

    return events_data


if __name__ == "__main__":
    getData()