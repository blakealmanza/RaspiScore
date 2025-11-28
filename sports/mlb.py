import espn_scraper as espn
import methods.getOdds as getOdds
import methods.getBroadcasts as getBroadcasts
import methods.changeTime as changeTime
import methods.getLogo as getLogo

def getData():
    events_data = []
    urls = espn.get_current_scoreboard_urls(league='mlb')

    for scoreboard_url in urls:
        data = espn.get_url(scoreboard_url)

    print("\n" + "-"*40 + "\n")

    for event in data["events"]:
        event_data = {}
        event_data.clear()
        short_detail = event["status"]["type"]["shortDetail"]
        inning_state = short_detail.find('End')

        if short_detail.find("Final") != 0:
            print(getBroadcasts.main(event))
            event_data["broadcasts"] = getBroadcasts.main(event)

            if inning_state == -1:
                print(f"{short_detail}")
                show_outs = True
            else:
                print(f"{short_detail}")
                show_outs = False
        else:
            print(f"{short_detail}")
            show_outs = False
        event_data["short detail"] = f"{short_detail}"
        event_data["show outs"] = show_outs

        print(getOdds.main('baseball', 'mlb', event, short_detail))
        event_data["odds"] = getOdds.main('baseball', 'mlb', event, short_detail)

        if short_detail.find(":") != -1 and (short_detail.find("EDT") != -1 or short_detail.find("EST") != -1):
            print(changeTime.main(short_detail))
            event_data["start time"] = changeTime.main(short_detail)

        for competition in event["competitions"]:
            if short_detail.find("Final") == -1 and short_detail.find(":") == -1:
                firstBase = competition["situation"]["onFirst"]
                event_data["first base"] = firstBase
                secondBase = competition["situation"]["onSecond"]
                event_data["second base"] = secondBase
                thirdBase = competition["situation"]["onThird"]
                event_data["third base"] = thirdBase

                outs = competition["situation"]["outs"]
                event_data["outs"] = outs

                strikes = competition["situation"]["strikes"]
                event_data["strikes"] = strikes
                balls = competition["situation"]["balls"]
                event_data["balls"] = balls

                def print_base(base):
                    if base == 0:
                        return 'o'
                    else:
                        return '*'

                if inning_state == -1:
                    print(f"{outs} outs")
                    print(f"Count: {balls}-{strikes}")
                    print("  " + print_base(secondBase) + "   \n" +
                    print_base(thirdBase) + "   " + print_base(firstBase))
                else:
                    print(end="")

            team_id = 0
            for team in competition["competitors"]:
                team_id += 1
                event_data["logo" + str(team_id)] = getLogo.main(team)

                team_short_name = team["team"]["shortDisplayName"]
                team_score = team["score"]

                if short_detail.find('EDT') == -1:
                    print(f"{team_short_name} - {team_score}")
                else:
                    print(f"{team_short_name}")

                event_data["team" + str(team_id) + " name"] = team_short_name
                event_data["team" + str(team_id) + " score"] = team_score

        print("\n" + "-"*40 + "\n")
        events_data.append(event_data)

    return events_data

if __name__ == "__main__":
    getData()
