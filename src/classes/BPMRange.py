class BPMRange:
    def __init__(self, *args):
        # input displaybpm str -> call again after parsing
        if len(args) == 1 and isinstance(args[0], str):
            bpms = [int(float(bpm)) for bpm in args[0].split(':')] # DDR X/SABER WING has bpm 74.000:222.000
            return self.__init__(*bpms)

        # input ints -> list of bpms
        if len(args) != 1 and len(args) != 2:
            raise
        self.value = args

    def __str__(self, value=None) -> str:
        if value is None:
            value = self.value
        return '~'.join(map(str, value))

    @classmethod
    def from_TimingData(cls, timing_data):
        bpms = list(map(lambda x: x.value, timing_data.bpms))
        if len(bpms) == 1:
            bpm = int(bpms[0])
            return cls(bpm)
        else:
            _min = min(bpms)
            _max = max(bpms)
            return cls(int(_min), int(_max))

    def printValue(self, value):
        return self.__str__(value)

    def Mult(self, mult=1):
        return [round(v*mult) for v in self.value]

    def readSpeeds(self):
        mults = [
            0.25, 0.5, 0.75, 1,
            1.25, 1.5, 1.75, 2,
            2.25, 2.5, 2.75, 3,
            3.25, 3.5, 3.75, 4,
                  4.5,       5,
                  5.5,       6,
                  6.5,       7,
                  7.5,       8
            ]
        return {m:self.Mult(m) for m in mults}
