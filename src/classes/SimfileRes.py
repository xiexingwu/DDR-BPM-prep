from __init__ import *
from pathlib import Path

class SimfileRes:
    def __init__(self, foldername:Path) -> None:
        self.name = foldername.name
        self.simfile = self.findSimfile(foldername)
        self.jacket = self.findJacket(foldername)
        self.banner = self.findBanner(foldername)

    def to_dict(self):
        # props = ['simfile', 'jacket', 'banner']
        props = ['simfile', 'jacket']
        return {prop: str(getattr(self, prop).name) for prop in props}

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