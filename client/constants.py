base_colors = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "cyan", "white"]

intensities = ["intense", "moderate", "subtle"]

color_map = {
    "red": {
        "intense": {"r": (255, 255), "g": (0, 32), "b": (0, 32)},
        "moderate": {"r": (255, 255), "g": (64, 128), "b": (64, 128)},
        "subtle": {"r": (255, 255), "g": (144, 187), "b": (144, 187)}
    },
    "green": {
        "intense": {"r": (0, 32), "g": (255, 255), "b": (0, 32)},
        "moderate": {"r": (64, 128), "g": (255, 255), "b": (64, 128)},
        "subtle": {"r": (144, 187), "g": (255, 255), "b": (144, 187)}
    },
    "blue": {
        "intense": {"r": (0, 32), "g": (0, 32), "b": (255, 255)},
        "moderate": {"r": (64, 128), "g": (64, 128), "b": (255, 255)},
        "subtle": {"r": (144, 187), "g": (144, 187), "b": (255, 255)}
    },
    "yellow": {
        "intense": {"r": (255, 255), "g": (255, 255), "b": (0, 32)},
        "moderate": {"r": (255, 255), "g": (255, 255), "b": (64, 128)},
        "subtle": {"r": (255, 255), "g": (255, 255), "b": (144, 187)}
    },
    "orange": {
        "intense": {"r": (255, 255), "g": (128, 192), "b": (0, 32)},
        "moderate": {"r": (255, 255), "g": (192, 255), "b": (64, 128)},
        "subtle": {"r": (255, 255), "g": (255, 255), "b": (144, 187)}
    },
    "purple": {
        "intense": {"r": (128, 192), "g": (0, 32), "b": (255, 255)},
        "moderate": {"r": (192, 255), "g": (64, 128), "b": (255, 255)},
        "subtle": {"r": (255, 255), "g": (144, 187), "b": (255, 255)}
    },
    "pink": {
        "intense": {"r": (255, 255), "g": (128, 192), "b": (192, 255)},
        "moderate": {"r": (255, 255), "g": (192, 255), "b": (192, 255)},
        "subtle": {"r": (255, 255), "g": (255, 255), "b": (255, 255)}
    },
    "cyan": {
        "intense": {"r": (0, 32), "g": (255, 255), "b": (255, 255)},
        "moderate": {"r": (64, 128), "g": (255, 255), "b": (255, 255)},
        "subtle": {"r": (144, 187), "g": (255, 255), "b": (255, 255)}
    },
    "white": {
        "intense": {"r": (255, 255), "g": (255, 255), "b": (255, 255)},
        "moderate": {"r": (255, 255), "g": (255, 255), "b": (255, 255)},
        "subtle": {"r": (255, 255), "g": (255, 255), "b": (255, 255)}
    }
}

durations = ["short", "lengthy"]

duration_map = {
    "short": 1,
    "lengthy": 5
}
