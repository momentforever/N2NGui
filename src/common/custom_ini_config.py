import configparser
import os.path


class CustomINIConfig:
    DEBUG_LEVEL = "ERROR"
    IS_BOOT_UP = False

    SUPERNODE = None
    EDGE_IP = None
    EDGE_COMMUNITY = None
    EDGE_COMMUNITY_PASSWORD = None
    EDGE_PACKAGE_SIZE = "1386"

    def __init__(self, path):
        if not os.path.exists(path):
            self._write_to_config(path)
        self._read_from_config(path)

    @classmethod
    def _read_from_config(self, path):
        config = configparser.ConfigParser()
        config.read(path)

        if 'CustomConfig' in config:
            config_section = config['CustomConfig']
            for attr in CustomINIConfig.__dict__:
                if attr.isupper() and not attr.startswith('__') and not attr.startswith('_'):
                    if attr.startswith("IS_"):
                        setattr(CustomINIConfig, attr, config_section.getboolean(attr, getattr(self, attr)))
                    else:
                        setattr(CustomINIConfig, attr, config_section.get(attr, getattr(self, attr)))

    def _write_to_config(self, path):
        config = configparser.ConfigParser()
        config['CustomConfig'] = {}
        config_section = config['CustomConfig']

        for attr in CustomINIConfig.__dict__:
            if attr.isupper() and not attr.startswith('__') and not attr.startswith('_'):
                config_section[attr] = str(getattr(self, attr))

        with open(path, 'w', encoding='utf-8') as config_file:
            config.write(config_file)
