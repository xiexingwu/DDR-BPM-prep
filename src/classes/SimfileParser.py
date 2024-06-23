import env
import simfile

# from simfile import timing
# from simfile import notes

# from simfile.notes import NoteData, count
# from simfile.notes.timed import time_notes
from simfile.timing import Beat, TimingData
from simfile.timing.engine import TimingEngine


BPM_BUMP_TRIGGER_DIFF = 10
BPM_BUMP_SMOOTH_DIFF = 3
BPM_BUMP_DUR = 2
SHORT_FAST_BPM_DUR = 4.5
MIN_DOMINANT_BPM_DUR = 13
MOST_BPM_DUR = 30


def _sec2beat(sec, bpm):
    return Beat(sec * bpm / 60)


def _fmt(decimal, fmt=".3f"):
    return format(float(decimal), fmt)


def _round(x, nearest=1.0):
    return round(x / nearest) * nearest


def _printBPMs(bpm_times, bpm_vals) -> None:
    print("-----BPM changes-----")
    for st, ed, bpm in zip(bpm_times[:-1], bpm_times[1:], bpm_vals[:-1]):
        print(f"{_fmt(st)} -- {_fmt(ed)}: {_fmt(st-ed)} sec @ {_fmt(bpm)}")


def _printSTOPs(timing_data, timing_eng) -> None:
    print("-----STOPs-----")
    for stop in timing_data.stops:
        # timestamp
        stop_time = timing_eng.time_at(stop.beat)
        # duration in beats
        stop_beats = _sec2beat(stop.value, timing_eng.bpm_at(stop.beat))
        print(
            f"{_fmt(stop_time)} -- {_fmt(stop_time + stop.value)}: {_fmt(stop_beats)}"
        )


class SimfileParser:
    def __init__(self, simfile_path):
        self.simfile = simfile.open(simfile_path)
        self.charts = self.simfile.charts
        self.per_chart = self.isPerChart()

        self.measures = sum(c == "," for c in self.charts[0].notes)
        self.song_length = self.getSongLength()

        self.parseData()

    def parseData(self):
        title = self.simfile.title
        title_translit = self.simfile.titletranslit

        self.song_data = {
            "title": title,
            "titletranslit": title_translit or title,
            "song_length": float(_fmt(self.song_length)),
            "per_chart": self.per_chart,
        }
        self.levels_data = self.parseLevels()
        self.chart_data = self.parseCharts()

    def isPerChart(self):
        # per_chart if any chart has its own BPM/stops data
        for chart in self.charts:
            if hasattr(chart, "stops") or hasattr(chart, "bpms"):
                return True
        return False

    def getSongLength(self):
        chart = self.charts[0]
        timing_data = TimingData(self.simfile, chart)
        timing_eng = TimingEngine(timing_data)
        song_length = timing_eng.time_at(Beat(4 * self.measures))
        return song_length

    def parseLevels(self):
        sp_levels = {}
        dp_levels = {}
        for chart in self.charts:
            if chart.stepstype == "dance-double":
                dp_levels[chart.difficulty.lower()] = int(chart.meter)
            elif chart.stepstype == "dance-single":
                sp_levels[chart.difficulty.lower()] = int(chart.meter)
        return {"sp": sp_levels, "dp": dp_levels}

    def parseCharts(self):
        data = []
        if not self.per_chart:
            return self.parseChart(self.charts[0])

        diffs = ""
        for chart in self.charts:
            if chart.difficulty[0] not in diffs:
                diffs += chart.difficulty[0]
                data += self.parseChart(chart)
        # check difficulties are in order from Beginner to Challenge
        order = "BEMHC"
        assert diffs in order
        return data

    def parseChart(self, chart):
        timing_data = TimingData(self.simfile, chart)
        timing_eng = TimingEngine(timing_data)

        bpm_timestamps = [timing_eng.time_at(bpm.beat) for bpm in timing_data.bpms]
        bpm_timestamps.append(self.song_length)
        bpm_vals = [bpm.value for bpm in timing_data.bpms]
        bpm_vals.append(bpm_vals[-1])

        # displaybpm = self.simfile.displaybpm # some songs dont have displaybpm field. e.g. illegal function call
        data = self.parseBpm(bpm_timestamps, bpm_vals)

        data["stops"] = [
            self.processStop(timing_eng, stop) for stop in timing_data.stops
        ]

        return [data]

    """
    TODO - calculate beats @ pre/post-bpms. If one of them is close to a nice number (1/3, 1/2, 1), then use it.
    Examples to consider: 
        Pluto - .48s (1 beat @ 125 bpm, 1.04 beat @ 130 bpm)
        out of focus - 1st stop/slowdown (1.75 beats @ 167 bpm, .875 beats @ 84 bpm)
        Max.(period) - 1st stop (6.646 beats @ 300 bpm to 4 beats @ 180 bpm)
    """

    def processStop(self, timing_eng, stop):
        stop_time = timing_eng.time_at(stop.beat)
        bpm_pre = round(timing_eng.bpm_at(stop.beat - 1))
        bpm_post = round(timing_eng.bpm_at(stop.beat + 1))

        convert = lambda bpm: float(_fmt(_sec2beat(stop.value, bpm)))
        beats_pre = convert(bpm_pre)
        beats_post = convert(bpm_post)

        def _niceness(x):
            to_third = abs(x - _round(x, nearest=1 / 3))
            to_quarter = abs(x - _round(x, nearest=1 / 4))
            return (to_third, 1 / 3) if to_third < to_quarter else (to_quarter, 1 / 4)

        nice_pre, denom_pre = _niceness(beats_pre)
        nice_post, denom_post = _niceness(beats_post)

        if nice_pre <= nice_post and nice_pre <= 0.05:
            beats = [{"bpm": bpm_pre, "val": _round(beats_pre, nearest=denom_pre)}]
        elif nice_post <= 0.05:
            beats = [{"bpm": bpm_post, "val": _round(beats_post, nearest=denom_post)}]
        else:
            env.logger.debug(self.simfile.title + "\n\t" + "no nice stop bpm found")
            # TODO - something?
            beats = [
                {"bpm": bpm_pre, "val": convert(bpm_pre)},
                {"bpm": bpm_post, "val": convert(bpm_post)},
            ]

        return {
            "st": float(_fmt(stop_time)),
            "dur": float(_fmt(stop.value)),
            "beats": beats,
        }

    def parseBpm(self, bpm_times, bpm_vals):
        bpms = [
            {"st": float(_fmt(st)), "ed": float(_fmt(ed)), "val": round(val)}
            for st, ed, val in zip(bpm_times[:-1], bpm_times[1:], bpm_vals[:-1])
        ]

        bpms = self.cleanBPM(bpms)

        d = {}
        dominant_bpm, dominant_dur = self.dominantBPM(bpms)
        d["dominant_bpm"] = dominant_bpm

        # Get actual min/max bpm, actual meaning the bpm must last a significant amount of duration
        # true_min/max is instantaneous min/max bpm
        durs = list(map(lambda x: x["ed"] - x["st"], bpms))
        vals = list(map(lambda x: x["val"], bpms))
        d["true_min"] = _max = min(vals)
        d["true_max"] = _min = max(vals)
        for dur, val in zip(durs, vals):
            if dur < SHORT_FAST_BPM_DUR and dominant_dur > MIN_DOMINANT_BPM_DUR:
                continue
            if val < _min:
                _min = val
            if val > _max:
                _max = val

        d["bpm_range"] = (
            f"{_min}~{dominant_bpm}~{_max}" if _min != _max else f"{_min}"
        )
        d["bpms"] = bpms
        return d

    def cleanBPM(self, bpms):
        """
        smoothen bpm bumps & merge consecutive sections with equal bpm
        """

        # skip
        if self.simfile.titletranslit == "deltaMAX":
            return bpms

        new = [bpms.pop(0)]
        while bpms:
            b2 = bpms.pop(0)
            st, ed, val = new[-1].values()
            st2, ed2, val2 = b2.values()

            # false bpm bump?
            if abs(val2 - val) <= BPM_BUMP_TRIGGER_DIFF:
                if abs(val2 - val) <= BPM_BUMP_SMOOTH_DIFF and (ed - st) < BPM_BUMP_DUR:
                    new[-1]["val"] = val2 if (ed2 - st2) > (ed - st) else val
                    new[-1]["ed"] = ed2
                    env.logger.info(
                        self.simfile.title
                        + "\n\t"
                        + f'bpm bump {st}~{ed}~{ed2} @ {val}~{val2} -> {st}~{ed2} @ {new[-1]["val"]}'
                    )
                else:
                    env.logger.debug(
                        self.simfile.title
                        + "\n\t"
                        + f"bpm bump {st}~{ed}~{ed2} @ {val}~{val2}"
                    )
                    new.append(b2)
                    continue

            # check for matching bpm, noting new[-1] may have changed
            st, ed, val = new[-1].values()
            if val == val2:
                new[-1]["ed"] = ed2
            else:
                new.append(b2)
                continue

        return new

    def dominantBPM(self, bpms):
        # compute dominant BPM of song
        d = {}
        for bpm in bpms:
            st, ed, val = bpm.values()
            val = int(val)
            st = float(st)
            ed = float(ed)

            if val in d.keys():
                d[val] += ed - st  # / self.song_length
            else:
                d[val] = ed - st  # / self.song_length

        dominant_bpm = max(d, key=d.get)
        dominant_dur = d[dominant_bpm]
        for k, v in d.items():
            if k > dominant_bpm and (
                v > MOST_BPM_DUR or dominant_dur < MIN_DOMINANT_BPM_DUR
            ):
                dominant_bpm = k
                dominant_dur = v

        return dominant_bpm, dominant_dur
