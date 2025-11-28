import time
from RGBMatrixEmulator import graphics
from PIL import Image, ImageEnhance, ImageOps
import urllib.request

def display_event(event, matrix, config):
    #broadcasts = event["broadcasts"]
    short_detail = event["short detail"]
    #show_outs = event["show outs"]
    #odds = event["odds"]
    #firstBase = event["first base"]
    #secondBase = event["second base"]
    #thirdBase = event["third base"]
    #outs = event["outs"]
    #strikes = event["strikes"]
    #balls = event["balls"]
    #home_team_name = event["team1 name"]
    home_team_score = event["team1 score"]
    #away_team_name = event["team2 name"]
    away_team_score = event["team2 score"]
    #home_logo_url = event["logo1"]
    #away_logo_url = event["logo2"]
    #home_team_score = '00'
    #away_team_score = '00'

    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("./matrix_display/fonts/ic16x16u.bdf")
    font_width = 12

    r, g, b = config["other"]["text_color"]
    text_color = graphics.Color(r, g, b)

    r, g, b = config["other"]["outline_color"]
    outline_color = graphics.Color(r, g, b)

    offscreen_canvas.Clear()

    i = 0
    while (i < 2):
        i += 1
        logo_url = event["logo" + str(i)]
        logo = urllib.request.urlretrieve(logo_url, "./media/events/team_logo.png")
        logo = Image.open("./media/events/team_logo.png")
        pixels = logo.load()

        # Changes Utah Jazz logo from black to yellow
        if logo_url == 'http://a.espncdn.com/i/teamlogos/nba/500/scoreboard/utah.png':
            yellow_color = (255, 242, 31, 255)
            for y in range(logo.height):
                for x in range(logo.width):
                    r, g, b, a = pixels[x, y]
                    if (r, g, b) == (0, 0, 0) and a > 0:
                        pixels[x, y] = yellow_color

        # Check if any neighboring pixel is transparent
        def has_transparent_neighbor(x, y, width, height, pixels):
            neighbors = [
                (x-1, y),  # left
                (x+1, y),  # right
                (x, y-1),  # up
                (x, y+1),  # down
            ]

            for nx, ny in neighbors:
                if 0 <= nx < width and 0 <= ny < height:
                    r, g, b, a = pixels[nx, ny]
                    if a == 0:
                        return True
            return False

        white_color = (255, 255, 255, 255)

        for y in range(logo.height):
            for x in range(logo.width):
                r, g, b, a = pixels[x, y]

                if (r, g, b) == (0, 0, 0) and a > 0:
                    # Only change if it has a transparent neighbor
                    if has_transparent_neighbor(x, y, logo.width, logo.height, pixels):
                        pixels[x, y] = white_color  # Change black pixel to white

        logo = ImageEnhance.Brightness(logo).enhance(config["events"]["team_logo_opacity"])

        if i == 2 and config["events"]["team_logo_mirrored"]:
            logo = ImageOps.mirror(logo)

        logo.thumbnail((config["events"]["team_logo_size"], config["events"]["team_logo_size"]), Image.Resampling.BOX)

        if i == 1:
            matrix.SetImage(logo.convert('RGB'), -config["events"]["team_logo_offset"], int(matrix.options.rows/2) - int(logo.height/2))
        else:
            matrix.SetImage(logo.convert('RGB'), 128 - config["events"]["team_logo_size"] + config["events"]["team_logo_offset"], int(matrix.options.rows/2) - int(logo.height/2))


    if len(short_detail) > 12:
        short_detail = event["start time"]
    else:
        if (short_detail.find(":") != -1 or short_detail.find(".") != -1) and short_detail.find("EST") == -1:
            time_detail = short_detail.split(" - ")[0]
            short_detail = short_detail.split(" - ")[1]

            graphics.DrawText(offscreen_canvas, font, get_center_pos(matrix, time_detail, font_width) -1,  36-1, outline_color, time_detail)
            graphics.DrawText(offscreen_canvas, font, get_center_pos(matrix, time_detail, font_width) +1,  36+1, outline_color, time_detail)
            graphics.DrawText(offscreen_canvas, font, get_center_pos(matrix, time_detail, font_width) -1,  36+1, outline_color, time_detail)
            graphics.DrawText(offscreen_canvas, font, get_center_pos(matrix, time_detail, font_width) +1,  36-1, outline_color, time_detail)
            graphics.DrawText(offscreen_canvas, font, get_center_pos(matrix, time_detail, font_width),  36, text_color, time_detail)
        elif (short_detail.find("End of ")) != -1:
            short_detail = short_detail[:-2]

        graphics.DrawText(offscreen_canvas, font, config["events"]["score_offset"] - 1,  60-1, outline_color, home_team_score)
        graphics.DrawText(offscreen_canvas, font, config["events"]["score_offset"] + 1,  60+1, outline_color, home_team_score)
        graphics.DrawText(offscreen_canvas, font, config["events"]["score_offset"] - 1,  60+1, outline_color, home_team_score)
        graphics.DrawText(offscreen_canvas, font, config["events"]["score_offset"] + 1,  60-1, outline_color, home_team_score)
        graphics.DrawText(offscreen_canvas, font, config["events"]["score_offset"],  60, text_color, home_team_score)

        graphics.DrawText(offscreen_canvas, font, matrix.options.cols - config["events"]["score_offset"] - (len(away_team_score)*font_width) - 1,  60-1, outline_color, away_team_score)
        graphics.DrawText(offscreen_canvas, font, matrix.options.cols - config["events"]["score_offset"] - (len(away_team_score)*font_width) + 1,  60+1, outline_color, away_team_score)
        graphics.DrawText(offscreen_canvas, font, matrix.options.cols - config["events"]["score_offset"] - (len(away_team_score)*font_width) - 1,  60+1, outline_color, away_team_score)
        graphics.DrawText(offscreen_canvas, font, matrix.options.cols - config["events"]["score_offset"] - (len(away_team_score)*font_width) + 1,  60-1, outline_color, away_team_score)
        graphics.DrawText(offscreen_canvas, font, matrix.options.cols - config["events"]["score_offset"] - (len(away_team_score)*font_width),  60, text_color, away_team_score)

    graphics.DrawText(offscreen_canvas, font, get_center_pos(matrix, short_detail, font_width) - 1,  20-1, outline_color, short_detail)
    graphics.DrawText(offscreen_canvas, font, get_center_pos(matrix, short_detail, font_width) + 1,  20+1, outline_color, short_detail)
    graphics.DrawText(offscreen_canvas, font, get_center_pos(matrix, short_detail, font_width) - 1,  20+1, outline_color, short_detail)
    graphics.DrawText(offscreen_canvas, font, get_center_pos(matrix, short_detail, font_width) + 1,  20-1, outline_color, short_detail)
    graphics.DrawText(offscreen_canvas, font, get_center_pos(matrix, short_detail, font_width),  20, text_color, short_detail)

    # Send the buffer to the matrix
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

def get_center_pos(matrix, text, font_width):
    calculation = (int(matrix.options.cols/2) - ((len(text)*font_width)/2))
    if calculation >= 0:
        return calculation
    else:
        return 0

def main(events_data, matrix, config):
    try:
        for event in events_data:
            display_event(event, matrix, config)
            time.sleep(config["events"]["event_display_time"])
    except KeyboardInterrupt:
        print("Display interrupted")
    finally:
        matrix.Clear()  # Clear matrix on exit


if __name__ == "__main__":
    main()
