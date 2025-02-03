import random
from constants import color_map, duration_map

"""
This class represents a color code and duration that can be displayed on the lights.
"""
class Color:
    def __init__(self, base, intensity_modifier, duration_modifier):
        self.base = base
        self.intensity = intensity_modifier
        self.duration = duration_modifier

    def __str__(self):
        return f"{self.base} {self.intensity} {self.duration}"

    def get_json(self):
        return {
            "code": self._calculate_rgb(),
            "duration": self._calculate_duration()
        }

    def _calculate_rgb(self):
        rgb_range = color_map[self.base][self.intensity]
        rgb = {
            "r": random.randint(rgb_range["r"][0], rgb_range["r"][1]),
            "g": random.randint(rgb_range["g"][0], rgb_range["g"][1]),
            "b": random.randint(rgb_range["b"][0], rgb_range["b"][1])
        }
        return (rgb["r"], rgb["g"], rgb["b"])

    def _calculate_duration(self):
        return duration_map[self.duration]
