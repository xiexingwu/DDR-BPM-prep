from string import Formatter
from functools import reduce

from BPMRange import BPMRange

import simfile

from simfile import timing
from simfile import notes

from simfile.notes import NoteData, count
from simfile.notes.timed import time_notes
from simfile.timing import Beat, TimingData
from simfile.timing.engine import TimingEngine

import pdb

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
        self.sim_file = simfile.open(simfile_path)
        self.charts = self.sim_file.charts
        self.per_chart = self.isPerChart()

        self.measures = reduce(lambda x,y:x+y, (c==',' for c in self.charts[0].notes))
        self.song_length = self.getSongLength()

        t = self.sim_file.title
        tt = self.sim_file.titletranslit
        song_d = {
            'title': t,
            'titletranslit':  tt if tt else t,
            'song_length': float(_fmt(self.song_length)),
            'per_chart': self.per_chart,
            }
        self.song_data = song_d

        self.levels_data = self.parseLevels()
        self.chart_data = self.parseTiming()

    def isPerChart(self):
        # per_chart if any chart has its own BPM/stops data
        for chart in self.charts:
            if hasattr(chart, 'stops') or hasattr(chart, 'bpms'):
                return True
        return False

    def getSongLength(self):
        chart = self.charts[0]
        timing_data = TimingData(self.sim_file, chart)
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

    def parseTiming(self, chart=None):
        if chart is None and self.per_chart:
            data = []
            diffs = ''
            for chart in self.charts:
                if chart.difficulty[0] not in diffs:
                    diffs += chart.difficulty[0]
                    data += self.parseTiming(chart)
            # check difficulties are in order from Beginner to Challenge
            order = 'BEMHC'
            # diffs = reduce(lambda x, y: x+y, map(lambda s: s[0], d.keys()), '')
            assert(diffs in order)

            return data

        data = {}
        if chart is None:
            timing_data = TimingData(self.sim_file)
            displaybpm = (self.sim_file.displaybpm)
        else:
            timing_data = TimingData(self.sim_file, chart)
            displaybpm = (chart.displaybpm)

        # if displaybpm:
        #     bpm_range = BPMRange(displaybpm)
        # else:
        #     bpm_range = BPMRange.from_TimingData(timing_data)

        timing_eng = TimingEngine(timing_data)

        # note_data = NoteData(chart)
        # timed_notes = time_notes(note_data, timing_data) # generator of TimedNote() types, 

        bpm_times = [timing_eng.time_at(bpm.beat) for bpm in timing_data.bpms]
        bpm_times.append(self.song_length) 
        bpm_vals = [bpm.value for bpm in timing_data.bpms]
        bpm_vals.append(bpm_vals[-1])

        data.update(self.processBPM(bpm_times, bpm_vals))

        data['stops'] = [_processStop(timing_eng, stop, data['dominant_bpm']) for stop in timing_data.stops]

        return [data]

    def stripBPMFalseStart(self, bpms):
        '''
        Some charts have a different starting bpm (off by 1 or 2) for like 1 measure, but are otherwise constant
        '''
        if len(bpms) > 2:
            return

        bpm = bpms[0]
        if bpm['ed'] - bpm['st'] < 1:
            bpms[1]['st'] = bpms[0]['st']
            del bpms[0]
            print(f'stripped false start for {self.sim_file.title}')

    def cleanBPM(self, bpms):
        new = []
        for i in range(len(bpms)):
            if i+1 < len(bpms):
                st, _, val = bpms[i].values()
                _, _, val2 = bpms[i+1].values()
                if val2 == val:
                    bpms[i+1]['st'] = st
                    # print(f'merging {val} section at {st} in {self.sim_file.title}')
                    continue

            new.append(bpms[i])
        return new

    def processBPM(self, bpm_times, bpm_vals):
        bpms = [{'st': float(_fmt(st)), 'ed': float(_fmt(ed)), 'val': int(_fmt(val,'.0f'))} for st, ed, val in zip(bpm_times[:-1], bpm_times[1:], bpm_vals[:-1]) ]
        bpms = self.cleanBPM(bpms)
        self.stripBPMFalseStart(bpms)

        d = {}
        d['dominant_bpm'], dominant_dur = self.dominantBPM(bpms)
        
        # initialise _max as minimum, and update while looping through
        durs = list(map(lambda x: x['ed'] - x['st'], bpms))
        vals = list(map(lambda x: x['val'], bpms))
        d['true_min'] = _max = min(vals)
        d['true_max'] = _min = max(vals)
        for dur, val in zip(durs, vals):
            if dur < 4:
                continue
            if val < _min:
                _min = val
            if val > _max:
                _max = val
        for dur, val in zip(durs, vals):
            if dur < 4 and dur > 2:
                if val < _min or val > _max:
                    print(f'Ignored short {val} section in {self.sim_file.title}')
    
        d['bpm_range'] = f'{_min}~{_max}'
        d['bpms'] = bpms
        return d

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
            if k > dominant_bpm and (v > 8 or dominant_dur < 13):
                dominant_bpm = k
                dominant_dur = v
                # print(f'higher bpm: {k} section with duration {v:.1f} in {self.sim_file.title}')
        for k, v in d.items():
            if k > dominant_bpm and (v > 8 or dominant_dur < 13):
                print(f'higher bpm: {k} section with duration {v:.1f} in {self.sim_file.title}')

        return dominant_bpm, dominant_dur * self.song_length

