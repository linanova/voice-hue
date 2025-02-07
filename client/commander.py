import logging
import time

import board
import neopixel
import spacy
import speech_recognition as sr
from nltk.corpus import wordnet as wn

from api import Api
from constants import base_colors, intensities, durations
from color import Color


nlp = spacy.load("en_core_web_sm")
pixels = neopixel.NeoPixel(board.D21, 9, pixel_order=neopixel.RGB)
api = Api()
logger = logging.getLogger()


"""
This class is responsible for listening to voice commands and controlling
the lights based on the commands.
"""


class LightCommander():
    def __init__(self):
        self.running = True
        self.pattern = []

    """Controls the lights based on the current pattern."""
    def control_lights(self):
        while self.running:
            time.sleep(1)
            for color_json in self.pattern:
                pixels.fill(color_json["code"])
                pixels.show()
                time.sleep(color_json["duration"])

    """Callback function for the speech recognizer."""
    def listener_callback(self, recognizer, audio):
        try:
            command = recognizer.recognize_google(audio)
            if command.lower() == "stop":
                self.running = False
                self.stop_listening(wait_for_stop=False)
            else:
                new_colors = self.process_command(command)
                if len(new_colors) > 0:
                    self.pattern = new_colors
                    api.post("commands", {"data": self.pattern, "command": command})
        except Exception as e:
            logger.error(f"Error processing command: {e}")

    """Listens for voice commands in the background."""
    def listen_for_commands(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            recognizer.adjust_for_ambient_noise(source)

        self.stop_listening = recognizer.listen_in_background(
            sr.Microphone(), self.listener_callback)

    """Processes a voice command to extract color and duration information."""
    def process_command(self, command):
        doc = nlp(command)

        colors_found = []
        for token in doc:
            if token.text in base_colors:
                modifiers_found = []
                for child in token.children:
                    if child.dep_ == "amod":  # adjective modifying noun
                        modifiers_found.append(child.text)

                color_found = Color(
                    token.text,
                    self.match_modifier(modifiers_found, intensities) or 'moderate',
                    self.match_modifier(modifiers_found, durations) or 'short')
                colors_found.append(color_found)

        return [color.get_json() for color in colors_found]

    """Matches provided modifiers to a list of target words using WordNet synonyms."""
    def match_modifier(self, modifiers, target_list):
        for modifier in modifiers:
            synonyms = self.get_synonyms(modifier)
            for synonym in synonyms:
                if synonym in target_list:
                    return synonym

        return None

    """ Returns a set of synonyms for a given word. """
    def get_synonyms(self, word):
        synsets = wn.synsets(word)

        synonyms = set()
        for synset in synsets:
            for lemma in synset.lemmas():
                synonyms.add(lemma.name())

        return synonyms

    def run(self):
        self.listen_for_commands()
        self.control_lights()
