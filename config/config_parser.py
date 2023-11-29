import configparser
import os


class Config:
    def __init__(self, path):
        self.config = configparser.ConfigParser()
        self.config.read(path)

    def get(self, section, option, fallback=None):
        if self.config.has_option(section, option):
            return self.config.get(section, option)
        return fallback

    def getboolean(self, section, option, fallback=None):
        return self.config.getboolean(section, option, fallback=fallback)

    def getint(self, section, option, fallback=None):
        return self.config.getint(section, option, fallback=fallback)


# get config.ini
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')

# create app_config for global usage
app_config = Config(config_path)
