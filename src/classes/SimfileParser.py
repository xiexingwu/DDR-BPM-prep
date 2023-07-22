from __init__ import *

import simfile
# from simfile import timing
# from simfile import notes

# from simfile.notes import NoteData, count
# from simfile.notes.timed import time_notes
from simfile.timing import Beat, TimingData
from simfile.timing.engine import TimingEngine

import pdb

BPM_BUMP_TRIGGER_DIFF = 10
BPM_BUMP_SMOOTH_DIFF = 3
BPM_BUMP_DUR = 2
SHORT_FAST_BPM_DUR = 4.5
MIN_DOMINANT_BPM_DUR = 13
MOST_BPM_DUR = 30

def _sec2beat(sec, bpm):
    return Beat(sec * bpm / 60)

def _fmt(decimal, fmt='.3f'):
    return format(float(decimal), fmt)

def _processStop(timing_eng, stop, dominant_bpm):
    stop_time = timing_eng.time_at(stop.beat)
    # stop_beats = _sec2beat(stop.value, timing_eng.bpm_at(stop.beat))
    stop_beats = _sec2beat(stop.value, dominant_bpm)
    return {'st': float(_fmt(stop_time)), 'dur': float(_fmt(stop.value)), 'beats': float(_fmt(stop_beats))}

def _printBPMs(bpm_times, bpm_vals) -> None:
    print('-----BPM changes-----')
    for st, ed, bpm in zip(bpm_times[:-1], bpm_times[1:], bpm_vals[:-1]):
        print(f'{_fmt(st)} -- {_fmt(ed)}: {_fmt(st-ed)} sec @ {_fmt(bpm)}')

def _printSTOPs(timing_data, timing_eng) -> None:
    print('-----STOPs-----')
    for stop in timing_data.stops:
        # timestamp
        stop_time = timing_eng.time_at(stop.beat)
        # duration in beats 
        stop_beats = _sec2beat(stop.value, timing_eng.bpm_at(stop.beat))
        print(f'{_fmt(stop_time)} -- {_fmt(stop_time + stop.value)}: {_fmt(stop_beats)}')

class SimfileParser:
    def __init__(self, simfile_path):
        self.simfile = simfile.open(simfile_path)
        self.charts = self.simfile.charts
        self.per_chart = self.isPerChart()
        
        self.measures = sum(c==',' for c in self.charts[0].notes)
        self.song_length = self.getSongLength()

        self.parseData()

    def parseData(self):
        title = self.simfile.title
        title_translit = self.simfile.titletranslit

        self.song_data = {
            'title': title,
            'titletranslit':  title_translit or title,
            'song_length': float(_fmt(self.song_length)),
            'per_chart': self.per_chart,
            }
        self.levels_data = self.parseLevels()
        self.chart_data = self.parseCharts()

    def isPerChart(self):
        # per_chart if any chart has its own BPM/stops data
        for chart in self.charts:
            if hasattr(chart, 'stops') or hasattr(chart, 'bpms'):
                return True
        return False

    def getSongLength(self):
        chart = self.charts[0]
        timing_data = TimingData(self.simfile, chart)
        timing_eng = TimingEngine(timing_data)
        song_length = timing_eng.time_at(Beat(4*self.measures))
        return song_length

    def parseLevels(self):
        sp_levels = {}
        dp_levels = {}
        for chart in self.charts:
            if chart.stepstype == 'dance-double':
                dp_levels[chart.difficulty.lower()] = int(chart.meter)
            elif chart.stepstype == 'dance-single':
                sp_levels[chart.difficulty.lower()] = int(chart.meter)
        return {'single': sp_levels, 'double': dp_levels}

    def parseCharts(self):
        data = []
        if not self.per_chart:
            return self.parseChart(self.charts[0])

        diffs = ''
        for chart in self.charts:
            if chart.difficulty[0] not in diffs:
                diffs += chart.difficulty[0]
                data += self.parseChart(chart)
        # check difficulties are in order from Beginner to Challenge
        order = 'BEMHC'
        assert(diffs in order)
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

        data['stops'] = [_processStop(timing_eng, stop, data['dominant_bpm']) for stop in timing_data.stops]

        return [data]

    def parseBpm(self, bpm_times, bpm_vals):
        bpms = [{'st': float(_fmt(st)), 'ed': float(_fmt(ed)), 'val': int(_fmt(val,'.0f'))} for st, ed, val in zip(bpm_times[:-1], bpm_times[1:], bpm_vals[:-1]) ]

        bpms = self.cleanBPM(bpms)

        d = {}
        d['dominant_bpm'], dominant_dur = self.dominantBPM(bpms)
        
        # Get actual min/max bpm, actual meaning the bpm must last a significant amount of duration
        # true_min/max is instantaneous min/max bpm
        durs = list(map(lambda x: x['ed'] - x['st'], bpms))
        vals = list(map(lambda x: x['val'], bpms))
        d['true_min'] = _max = min(vals)
        d['true_max'] = _min = max(vals)
        for dur, val in zip(durs, vals):
            if dur < SHORT_FAST_BPM_DUR and dominant_dur > MIN_DOMINANT_BPM_DUR:
                continue
            if val < _min:
                _min = val
            if val > _max:
                _max = val
    
        d['bpm_range'] = f'{_min}~{_max}' if _min != _max else f'{_min}'
        d['bpms'] = bpms
        return d

    def cleanBPM(self, bpms):
        '''
        smoothen bpm bumps & merge consecutive sections with equal bpm
        '''

        # skip 
        if self.simfile.titletranslit == 'deltaMAX':
            return bpms

        new = [bpms.pop(0)]
        while bpms:
            b2 = bpms.pop(0)
            st, ed, val = new[-1].values()
            st2, ed2, val2 = b2.values()

            # false bpm bump?
            if abs(val2 - val) <= BPM_BUMP_TRIGGER_DIFF:
                if abs(val2 - val) <= BPM_BUMP_SMOOTH_DIFF and (ed - st) < BPM_BUMP_DUR:
                    new[-1]['val'] = val2 if (ed2 - st2) > (ed - st) else val
                    new[-1]['ed'] = ed2
                    LOGGER.info(self.simfile.title + '\n\t' +
                                f'bpm bump {st}~{ed}~{ed2} @ {val}~{val2} -> {st}~{ed2} @ {new[-1]["val"]}')
                else:
                    LOGGER.debug(self.simfile.title + '\n\t' +
                                f'bpm bump {st}~{ed}~{ed2} @ {val}~{val2}')
                    new.append(b2)
                    continue

            # check for matching bpm, noting new[-1] may have changed
            st, ed, val = new[-1].values()
            if val == val2:
                new[-1]['ed'] = ed2
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
                d[val] += (ed - st) #/ self.song_length
            else:
                d[val] = (ed - st) #/ self.song_length

        dominant_bpm = max(d, key=d.get)
        dominant_dur = d[dominant_bpm]
        for k, v in d.items():
            if k > dominant_bpm and (v > MOST_BPM_DUR or dominant_dur < MIN_DOMINANT_BPM_DUR):
                dominant_bpm = k
                dominant_dur = v

        return dominant_bpm, dominant_dur

