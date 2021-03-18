#!/usr/bin/python

from pydub import AudioSegment
from random import randint
from pathlib import Path
import os
from glob import glob


def prepare_project_dir(wav_in):
    base_dir = os.path.dirname(wav_in)
    stem = Path(wav_in).stem
    if os.path.isfile(wav_in) and os.path.exists(wav_in):
        project_dir = base_dir + os.sep + stem + os.sep
        if not os.path.exists(project_dir):
            Path(project_dir).mkdir()
        return project_dir
    return False


class MucksChopper:
    num_samples: 100

    audio: AudioSegment

    frame_cnt: int

    len_span: dict = {'min': 110, 'max': 350}

    max_end: int

    project_dir: str

    def __init__(self, wav_in, project_dir=None, num_samples=400):
        self.num_samples = num_samples
        self.audio = AudioSegment.from_wav(wav_in)
        self.frame_cnt = self.audio.frame_count()
        self.max_end = len(self.audio) - self.len_span['max']
        self.project_dir = project_dir

    def chop(self):
        cur_idx = 0
        while cur_idx < self.num_samples:
            self._write_sample(cur_idx)
            cur_idx += 1

    def _write_sample(self, cur_idx, prefix="mucks_"):
        start = self._random_start()
        end = start + self._random_len()
        sample = self.audio[start:end]
        prefix = self.project_dir + prefix if self.project_dir else prefix
        sample.export(prefix + str(cur_idx) + '.wav', format="wav")

    def _random_start(self):
        return randint(0, self.max_end)

    def _random_len(self):
        return randint(self.len_span['min'], self.len_span['max'])


class MucksFranken:
    samples_cnt: int

    project_dir: str

    def __init__(self, project_dir: str, samples_cnt=500):
        self.samples_cnt = samples_cnt
        self.project_dir = project_dir

    def stein(self):
        samples = [AudioSegment.from_wav(wav) for wav in glob(self.project_dir + os.sep + '*.wav')]
        max_len = len(samples) - 1
        combined = None
        sample_idx = 0
        while sample_idx < self.samples_cnt:
            sample = samples[randint(0, max_len)]
            if combined is None:
                combined = sample
            else:
                combined = combined.append(sample, randint(20, 50))
            sample_idx += 1
        combined.export(self.project_dir + 'mucks_exported.wav', format="wav")


# Example - will create a catatonic dir in your home dir.
#if __name__ == '__main__':
#    fname = "/home/roho/catatonic.wav"
#    output = prepare_project_dir(fname)
#    chopper = MucksChopper(fname, project_dir=output, num_samples=500)
#    chopper.chop()
#    frank = MucksFranken(output)
#    frank.stein()
