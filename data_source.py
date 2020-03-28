import json
import requests


class DataSource:
    def __init__(self, config_path):
        self.load_config(config_path)
        self.prev_data = {}
        self.data = {}

    def load_config(self, config_path):
        with open(config_path, "rb") as file:
            config = json.load(file)

        self.sources = config["sources"]
        self.statistics = config["statistics"]

    def refresh_data(self):
        self.prev_data = self.data
        self.data = {}
        for source in self.sources:
            res = requests.get(source["url"])
            data = json.loads(res.text)
            self.data[source["key"]] = data

    def __iter__(self):
        for stat in self.statistics:
            path, announce = stat["path"], stat["announce"]

            curr_value = DataSource._data_by_path(self.data,      path)
            prev_value = DataSource._data_by_path(self.prev_data, path)

            yield curr_value, prev_value, announce

    @staticmethod
    def _data_by_path(data: dict, path: str):
        try:
            for key in path.split("."):
                data = data[key]
            return data
        except Exception as e:
            if data != {}: print("Invalid path:", path)
            return None

