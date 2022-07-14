import simfile
from __init__ import *
from pathlib import Path

class SimfileRes:
    props = ['simfile', 'jacket']

    def __init__(self, path:Path) -> None:
        self.name = path.name
        self.simfile = self.findSimfile(path)
        self.jacket = self.findJacket(path)
        self.banner = self.findBanner(path)
        self.ssc = self.simfile.suffix == ".ssc"


    def checkNaming(self):
        if not self.simfile:
            LOGGER.error(f"Simfile not found for {self.name}")
            raise RuntimeError
        if not self.jacket:
            LOGGER.error(f"Jacket not found for {self.jacket}.")
            raise RuntimeError

    def to_dict(self):
        return {prop: str(getattr(self, prop).name) for prop in type(self).props}

    def findFile(self, filename:Path) -> Path:
        if filename.exists():
            return filename
        else:
            raise

    def findSimfile(self, foldername:Path) -> Path:
        try:
            return self.findFile(foldername/(self.name+'.sm'))
        except:
            return self.findFile(foldername/(self.name+'.ssc'))

    def findJacket(self, foldername:Path) -> Path:
        try:
            return self.findFile(foldername/(self.name+"-jacket.png"))
        except:
            return Path('')

    def findBanner(self, foldername:Path) -> Path:
        try:
            return self.findFile(foldername/(self.name+".png"))
        except:
            return Path('')