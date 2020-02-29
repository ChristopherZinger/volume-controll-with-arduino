"""
https://github.com/AndreMiras/pycaw/blob/develop/examples/audio_endpoint_volume_example.py
"""
from __future__ import print_function
from pycaw.pycaw import AudioUtilities
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class AudioController(object):
    def __init__(self, process_name):
        self.process_name = process_name
        self.volume = .5
        self.master_volume = VOLUME.GetMasterVolumeLevel()
        self.master_range = VOLUME.GetVolumeRange()

    def mute(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process :
                interface.SetMute(1, None)
                # print(self.process_name, 'has been muted.')  # debug

    def unmute(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process :
                interface.SetMute(0, None)
                # print(self.process_name, 'has been unmuted.')  # debug

    def process_volume(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # print('Volume:', interface.GetMasterVolume())  # debug
                return interface.GetMasterVolume()

    def set_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # only set volume in the range 0.0 to 1.0
                self.volume = min(1.0, max(0.0, decibels))
                interface.SetMasterVolume(self.volume, None)
                # print('Volume set to', self.volume)  # debug

    def decrease_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            # 0.0 is the min value, reduce by decibels
            if session.Process:
                interface = session.SimpleAudioVolume
                # print('volume: ', self.volume)
                # print('decibels: ', decibels)
                self.volume = max(0.0, self.volume-decibels)
                interface.SetMasterVolume(self.volume, None)
                # print('Volume reduced to', self.volume)  # debug

    def increase_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process:
                interface = session.SimpleAudioVolume
                # 1.0 is the max value, raise by decibels
                self.volume = min(1.0, self.volume+decibels)
                interface.SetMasterVolume(self.volume, None)
                # print('Volume raised to', self.volume)  # debug

    def decrease_master_volume(self, decibels):
        self.master_volume = max(self.master_range[0], self.master_volume-decibels)
        VOLUME.SetMasterVolumeLevel(
            self.master_volume,
            None
        )
        # print('Master Volume reduced to', self.master_volume)  # debug

    def increase_master_volume(self, decibels):
        self.master_volume = min(self.master_range[1], self.master_volume+decibels)
        VOLUME.SetMasterVolumeLevel(
            self.master_volume,
            None
        )
        # print('Master Volume reduced to', self.master_volume)  # debug


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
VOLUME = cast(interface, POINTER(IAudioEndpointVolume))
# print("volume.GetMute(): %s" % VOLUME.GetMute())
# print("volume.GetMasterVolumeLevel(): %s" % VOLUME.GetMasterVolumeLevel())
# print("volume.GetVolumeRange(): (%s, %s, %s)" % VOLUME.GetVolumeRange())
# print("volume.SetMasterVolumeLevel()")
# VOLUME.SetMasterVolumeLevel(-20.0, None)
# print("volume.GetMasterVolumeLevel(): %s" % VOLUME.GetMasterVolumeLevel())
audio_controller = AudioController('chrome.exe') # proccess name is irrelevant
