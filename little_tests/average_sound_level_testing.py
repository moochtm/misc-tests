import pyaudio
import audioop
from collections import deque
import numpy
from array import array
import struct
import time
import wave

class Mic:
    def __init__(self):
        self._CHUNK_SIZE = 1024
        self._FORMAT = pyaudio.paInt16
        self._RATE = 16000
        self._audio = pyaudio.PyAudio()
        self._stream = self._audio.open(format=self._FORMAT, channels=1, rate=self._RATE,
                                          input=True, output=True,
                                          frames_per_buffer=self._CHUNK_SIZE)
        self._signal_started = False
        self._signal_stop_level = 0
        self._threshold = None
        self._threshold_time = 1
        self._threshold_start_multiplier = 3
        self._threshold_stop_multiplier = 1.5
        self._max_active_listen_time = 10

    def __del__(self):
        self._stream.stop_stream()
        self._stream.close()
        self._audio.terminate()

    def _get_sound_level(self, data):
        rms = audioop.rms(data, 2)
        sound_level = rms
        return sound_level

    def _set_threshold(self):

        data = deque(maxlen=int(self._RATE/self._CHUNK_SIZE*self._threshold_time))

        while 1:
            chunk = self._stream.read(self._CHUNK_SIZE)
            data.append(self._get_sound_level(chunk))

            if len(data) == data.maxlen:
                break

        self._threshold = numpy.mean(data)
        print("Threshold taken over %d seconds as %d" % (self._threshold_time, self._threshold))

    def _is_signal_present(self, rms_data):

        sound_level = numpy.mean(rms_data)
        print "Sound level: %s" % sound_level

        if sound_level > self._threshold * self._threshold_start_multiplier:
            if not self._signal_started:
                self._signal_stop_level = self._threshold + ((sound_level - self._threshold) / 3)
            self._signal_started = True
            return True
        else:
            if not self._signal_started:
                return False
            elif sound_level < self._signal_stop_level:
                #self._signal_started = False
                return False
        return True

    # Returns as many (up to returnNum) blocks as it can.
    def _return_up_to(self, iterator, values, return_num):
        if iterator + return_num < len(values):
            return (iterator + return_num,
                    "".join(values[iterator:iterator + return_num]))

        else:
            temp = len(values) - iterator
            return iterator + temp + 1, "".join(values[iterator:iterator + temp])

    def _signal_gen(self):
        """
        SIGNAL GENERATOR
        :return:
        """
        if self._threshold == None:
            self._set_threshold()

        self._signal_started = False

        maxlen = int(self._RATE / self._CHUNK_SIZE * self._threshold_time / 2)
        iterable = (self._threshold for i in range(maxlen))
        level_data = deque(iterable=iterable, maxlen=maxlen)

        num_silent = 0
        counter = 0
        counter_limit = self._max_active_listen_time * (self._RATE / self._CHUNK_SIZE)

        i = 0
        data = []

        start_time = time.time()

        # TODO: add jasper high beep

        while 1:
            chunk = self._stream.read(self._CHUNK_SIZE)
            snd_data = array('i', chunk)
            for d in snd_data:
                data.append(struct.pack('<i', d))
            level_data.append(self._get_sound_level(chunk))

            # signal not started
            if not self._signal_started:
                # signal not started, but there is signal
                if self._is_signal_present(level_data):
                    i = len(data) - self._CHUNK_SIZE * 2  # Set the counter back a few seconds
                    if i < 0:  # so we can hear the start of speech.
                        i = 0
            # signal is started, and there's still signal
            elif self._is_signal_present(level_data) and not i >= len(data):
                i, temp = self._return_up_to(i, data, 1024)
                yield temp
                num_silent = 0
            # signal is started, but there's no signal right now
            else:
                num_silent += 1
                print "NUM_SILENT: %s" % str(num_silent)

            if self._signal_started and num_silent > 2:
                print "quiet for too long - stopping the stream"
                break

            if counter > counter_limit:
                print "signal lasting too long - stopping the stream"
                break

            if self._signal_started:
                counter += 1

        # TODO: add jasper low beep

        print("--- %s seconds ---" % (time.time() - start_time))
        # Yield the rest of the data.
        print "Pre-streamed " + str(i) + " of " + str(len(data)) + "."
        while i < len(data):
            i, temp = self._return_up_to(i, data, 512)
            yield temp

    def signal_to_file(self, f):
        if not self._threshold:
            self._set_threshold()

        frames = []

        for data in self._signal_gen():
            frames.append(data)

        waveFile = wave.open(f, 'wb')
        waveFile.setnchannels(1)
        waveFile.setsampwidth(self._audio.get_sample_size(self._FORMAT))
        waveFile.setframerate(self._RATE)
        waveFile.writeframes(''.join(frames))
        waveFile.close()

    def signal_to_stream(self):
        if not self._threshold:
            self._set_threshold()

        for data in self._signal_gen():
            yield data

    def start_passivelisten(self):
        pass

    def start_activelisten(self):
        pass

    def test(self):

        self.signal_to_file('test.wav')

def test():

    test = Mic()
    test.test()

def main():

    test = Mic()
    while 1:
        print('Starting Passive Listening')
        test.start_passivelisten()
        print('Starting Active Listening')
        test.start_activelisten()

if __name__ == '__main__':
    test()