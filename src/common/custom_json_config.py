import json
import os.path


class CustomJSONConfig:
    IS_QS = False

    LOG_LEVEL = "INFO"
    IS_STARTUP = False

    SUPERNODE = ""
    EDGE_IP = ""
    EDGE_COMMUNITY = ""
    EDGE_COMMUNITY_PASSWORD = ""
    EDGE_PACKAGE_SIZE = "1386"
    EDGE_DESCRIPTION = ""
    EDGE_ETC_ARGS = ""

    IS_UNLESS_STOP = False

    def __init__(self, path):
        if not os.path.exists(path):
            self._write_to_config(path)
        self._read_from_config(path)

    def _read_from_config(self, path):
        with open(path, 'r', encoding='utf-8') as config_file:
            config_data = json.load(config_file)

        if 'CustomConfig' in config_data:
            config_section = config_data['CustomConfig']
            for attr in CustomJSONConfig.__dict__:
                if attr.isupper() and not attr.startswith('__') and not attr.startswith('_'):
                    if attr.startswith("IS_"):
                        setattr(CustomJSONConfig, attr, config_section.get(attr, getattr(self, attr)))
                    else:
                        setattr(CustomJSONConfig, attr, str(config_section.get(attr, getattr(self, attr))))

    def _write_to_config(self, path):
        config_data = {}
        config_data['CustomConfig'] = {}
        config_section = config_data['CustomConfig']

        for attr in CustomJSONConfig.__dict__:
            if attr.isupper() and not attr.startswith('__') and not attr.startswith('_'):
                config_section[attr] = getattr(self, attr)

        with open(path, 'w', encoding='utf-8') as config_file:
            json.dump(config_data, config_file, indent=4, ensure_ascii=False)
