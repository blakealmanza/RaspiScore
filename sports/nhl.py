import espn_scraper as espn
import methods.getOdds as getOdds
import methods.getBroadcasts as getBroadcasts
import methods.changeTime as changeTime
import methods.getLogo as getLogo


def getData():
    events_data = []
    urls = espn.get_current_scoreboard_urls(league='nhl')

    for scoreboard_url in urls:
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

        print(getOdds.main('hockey', 'nhl', event, short_detail))
        event_data["odds"] = getOdds.main('hockey', 'nhl', event, short_detail)

        if short_detail.find(":") != -1 and (short_detail.find("EDT") != -1 or short_detail.find("EST") != -1):
            print(changeTime.main(short_detail))
            event_data["start time"] = changeTime.main(short_detail)


        for competition in event["competitions"]:

            team_id = 0
            for team in competition["competitors"]:
                team_id += 1

                team_abbreviation = team["team"]["shortDisplayName"]
                team_score = team["score"]

                event_data["logo" + str(team_id)] = getLogo.main(team)

                if short_detail.find('EST') == -1:
                    print(f"{team_abbreviation} - {team_score}")
                else:
                    print(f"{team_abbreviation}")

                event_data["team" + str(team_id) + " name"] = team_abbreviation
                event_data["team" + str(team_id) + " score"] = team_score

        events_data.append(event_data)
        print("\n" + "-"*40 + "\n")

    return events_data


if __name__ == "__main__":
    getData()