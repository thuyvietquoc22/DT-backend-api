from abc import abstractmethod


class BaseMap4DService:

    @property
    @abstractmethod
    def url(self):
        pass

    def build_url(self, **kwargs):
        return self.url + "?" + "&".join([f"{key}={value}" for key, value in kwargs.items()])
