import time
from PIL import Image

def display_league(league, matrix, config):

    offscreen_canvas = matrix.CreateFrameCanvas()
    offscreen_canvas.Clear()

    logo_file = str("./media/leagues/" + str(league) + ".png")
    logo = Image.open(logo_file).convert('RGBA')
    logo.thumbnail((config["leagues"]["league_logo_size"], config["leagues"]["league_logo_size"]), Image.Resampling.BOX)
    x_pos = int(matrix.options.cols/2) - int(logo.width/2)
    y_pos = int(matrix.options.rows/2) - int(logo.height/2)
    matrix.SetImage(logo.convert('RGB'), x_pos, y_pos)

    # Send the buffer to the matrix
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)


def main(league, matrix, config):
    try:
        display_league(league, matrix, config)
        time.sleep(config["leagues"]["league_display_time"])
    except KeyboardInterrupt:
        print("Display interrupted")
    finally:
        matrix.Clear()  # Clear matrix on exit


if __name__ == "__main__":
    main()
