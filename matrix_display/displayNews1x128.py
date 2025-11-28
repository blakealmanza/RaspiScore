import time
from RGBMatrixEmulator import graphics
from PIL import Image, ImageEnhance

def display_headline(headline, matrix, config):

    if config["news"]["source"] == 'espn':
        title = headline[0]
        teams = headline[1]
    else:
        title = headline

    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("./matrix_display/fonts/7x13.bdf")
    font_width = 7

    r, g, b = config["other"]["text_color"]
    text_color = graphics.Color(r, g, b)

    r, g, b = config["other"]["outline_color"]
    outline_color = graphics.Color(r, g, b)

    offscreen_canvas.Clear()

    if config["news"]["display_source_logo"]:
        logo = Image.open("./media/news/" + str(config["news"]["source"]) + "_logo.png")
        logo = ImageEnhance.Brightness(logo).enhance(config["news"]["source_logo_opacity"])
        logo.thumbnail((150, 64), Image.Resampling.BOX)
        x_pos = int(matrix.options.cols/2) - int(logo.width/2)
        y_pos = int(matrix.options.rows/2) - int(logo.height/2)
        matrix.SetImage(logo.convert('RGB'), x_pos, y_pos)


    def split_text_by_words(text, n=18):
        words = title.split()
        result = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 > n:
                result.append(current_line.strip())
                current_line = word
            else:
                current_line += " " + word

        if current_line:
            result.append(current_line.strip())

        return result

    new_title = split_text_by_words(title)

    if len(new_title) > 6:
        new_title.pop()
        new_title[5] += '...'

    line_count = 0
    for line in new_title:
        line_count += 1
        height = len(new_title) * 13
        line_spacing = config["news"]["line_spacing"]
        graphics.DrawText(offscreen_canvas, font, calc_center_x_pos(matrix, line, font_width) -1, calc_y_pos(height, line_spacing, line_count) - 1, outline_color, line)
        graphics.DrawText(offscreen_canvas, font, calc_center_x_pos(matrix, line, font_width) +1, calc_y_pos(height, line_spacing, line_count) + 1, outline_color, line)
        graphics.DrawText(offscreen_canvas, font, calc_center_x_pos(matrix, line, font_width) -1, calc_y_pos(height, line_spacing, line_count) + 1, outline_color, line)
        graphics.DrawText(offscreen_canvas, font, calc_center_x_pos(matrix, line, font_width) +1, calc_y_pos(height, line_spacing, line_count) - 1, outline_color, line)

        graphics.DrawText(offscreen_canvas, font, calc_center_x_pos(matrix, line, font_width) -1, calc_y_pos(height, line_spacing, line_count), outline_color, line)
        graphics.DrawText(offscreen_canvas, font, calc_center_x_pos(matrix, line, font_width) +1, calc_y_pos(height, line_spacing, line_count), outline_color, line)
        graphics.DrawText(offscreen_canvas, font, calc_center_x_pos(matrix, line, font_width), calc_y_pos(height, line_spacing, line_count) + 1, outline_color, line)
        graphics.DrawText(offscreen_canvas, font, calc_center_x_pos(matrix, line, font_width), calc_y_pos(height, line_spacing, line_count) - 1, outline_color, line)

        graphics.DrawText(offscreen_canvas, font, calc_center_x_pos(matrix, line, font_width), calc_y_pos(height, line_spacing, line_count), text_color, line)

    # Send the buffer to the matrix
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)


def calc_center_x_pos(matrix, text, font_width):
    x_calculation = (int(matrix.options.cols/2) - ((len(text)*font_width)/2))
    if x_calculation >= 0:
        return x_calculation
    else:
        return 0

def calc_y_pos(height, line_spacing, line_count):
    y_calculation = ((64-height)/2 + (line_spacing*line_count) + 6)
    if y_calculation >= 0:
        return y_calculation
    else:
        return 0

def main(headlines_data, matrix, config):
    try:
        for headline in headlines_data:
            display_headline(headline, matrix, config)
            time.sleep(config["news"]["news_display_time"])
    except KeyboardInterrupt:
        print("Display interrupted")
    finally:
        matrix.Clear()  # Clear matrix on exit


if __name__ == "__main__":
    main()
