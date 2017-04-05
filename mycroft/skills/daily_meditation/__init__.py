# Copyright 2016 Mycroft AI, Inc.
#

#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.


import feedparser
import time
from os.path import dirname
import re

import mycroft.skills.weather as weather
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util import play_mp3
from mycroft.util.log import getLogger

__author__ = 'kfezer'

LOGGER = getLogger(__name__)


class DailyMeditationSkill(MycroftSkill):
    def __init__(self):
        super(DailyMeditationSkill, self).__init__(name="DailyMeditationSkill")
        #self.url_rss = self.config['url_rss']
        self.weather = weather.WeatherSkill()
        self.process = None

    def initialize(self):
        self.load_data_files(dirname(__file__))
        intent = IntentBuilder("DailyMeditationIntent").require(
            "DailyMeditationKeyword").build()
        self.register_intent(intent, self.handle_intent)

	self.weather.bind(self.emitter)
        self.weather.load_data_files(dirname(weather.__file__))

    def handle_intent(self, message):
        try:
            data = feedparser.parse("http://www.themeditationpodcast.com/tmp.xml")
            self.speak_dialog('daily.meditation')
            time.sleep(3)
            self.process = play_mp3(
                re.sub(
                    'https', 'http', data['entries'][0]['enclosures'][0]['href']))

        except Exception as e:
            LOGGER.error("Error: {0}".format(e))

    def stop(self):
        if self.process and self.process.poll() is None:
            self.speak_dialog('daily.meditation.stop')
            self.process.terminate()
            self.process.wait()


def create_skill():
    return DailyMeditationSkill()