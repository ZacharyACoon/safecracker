import json


class Config:
    def __init__(self, d, parent=None):
        self.___raw = d
        self.___parent = parent
        self.__getitem__ = self.___fetch
        self.__getattr__ = self.___fetch

    def ___trace(self):
        parents = []
        parent = self.___parent
        while parent:
            parents.append(parent)
            parent = parent.parent
        return parents[::-1]

    @property
    def ___default(self):
        raise Exception(f"{'.'.join(self.___trace())}")

    def ___fetch(self, key):
        if key in self.___raw:
            v = self.raw[key]
            if v is dict:
                return Config(v)
            return v
        return self.___default



def get_relative_config_json():
    with open("config.json") as f:
        return json.load(f)
