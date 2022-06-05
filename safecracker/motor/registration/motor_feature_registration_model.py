from typing import Union
import asyncio
from collections.abc import Iterable


class Feature:
    def __init__(self):
        pass

    def register(self, motor):
        pass



class FeaturedMotor:
    def __init__(self, motor, features=None):
        self.motor = motor
        self.features = []
        if features:
            for feature in features:
                self.register(feature)


    def register(self, features: Union[Feature, Iterable]):
        if not isinstance(features, Iterable):
            features = [features]
        for feature in features:
            self.features.append(feature)
            feature.register(self)

    def __getattr__(self, name):
        print("here1", name)
        if hasattr(type(self), name):
#        if name in self.__dict__:
            print("here2")
            attribute = object.__getattr__(name)
            print(attribute)
            if not callable(attribute):
                return attribute

            callables = []
            for feature in self.features:
                print(feature)
                if hasattr(feature, f"before_{name}"):
                    callables.append(getattr(feature, f"before_{name}"))
            callables.append(object.__getattribute__(self.motor, name))
            for feature in self.features:
                if hasattr(feature, f"after_{name}"):
                    callables.append(getattr(feature, f"after_{name}"))

            def a(*args, **kwargs):
                for c in callables:
                    c(*args, **kwargs)

            return a
        else:
            for feature in self.features:
                if hasattr(feature, name):
                    return getattr(feature, name)
            return object.__getattribute__(self.motor, name)
