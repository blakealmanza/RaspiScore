import json

# Load configuration from main_config.json
def load_config(config_file='./config/main_config.json'):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

def main(short_detail, config=load_config()):
    _strings = short_detail.split(":")
    strings = _strings[0].split("- ")

    strings[1] = int(strings[1]) + config["other"]["time_correction"]
    if strings[1] <= 0:
        strings[1] = 12 + strings[1]
        if strings[1] != 12:
            _strings[1] = _strings[1].replace("PM", "AM")

    _strings[1] = _strings[1].replace("EST", "")
    _strings[1] = _strings[1].replace("EDT", "")
    fixed_time = f"{strings[1]}:{_strings[1]}"

    return fixed_time

if __name__ == "__main__":
    main()