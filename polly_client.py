#!/usr/bin/env python3
# File:        polly_client.py
# Created:     27/03/2019 by Daniel Burr <dburr@dburr.net>
# Description: Python client for communicating with speech-dispatcher
# License:     GNU Public License, version 3
#
# Uses boto3 to communicate with Amazon Polly

import getopt, sys, signal, os
import subprocess
import boto3


running = True

def signal_handler(signal, frame):
    global running
    running = False
    sys.exit(1)


class Client:
    def __init__(self, verbose):
        self.verbose = verbose

        self.polly = boto3.client('polly')

    def speak(self, text, lang, voice):
        resp = self.polly.synthesize_speech(OutputFormat='mp3', Text=text, LanguageCode=lang, VoiceId=voice)
        audio_stream = resp['AudioStream']
        audio_data = audio_stream.read()
        audio_stream.close()
        subprocess.run(['mpg123', '-q', '-'], input=audio_data, stderr=subprocess.DEVNULL)

        print("FINISHED_UTTERANCE")

    def list_voices(self, lang):
        print(self.polly.describe_voices(LanguageCode=lang))


def help(name):
    print("%s: python wrapper for communicating with Amazon Polly\n" % name)
    print("Usage:")
    print("\t--lang=<lang>:     Use the specified language (default: en-AU)")
    print("\t--voice=<voice>:   Use the specified voice (default: Nicole)")
    print("\t--debug:           Increase verbosity")
    print("\t--help:            This message\n")
    sys.exit(2)


def main():
    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "l:v:dh", ["lang=", "voice=", "debug", "help"])
    except getopt.GetoptError as err:
        print(str(err))
        help(sys.argv[0])
    lang = 'en-AU'
    voice = 'Nicole'
    debug = False
    for opt, arg in opts:
        if opt in ("-l", "--lang"):
            lang = arg
        elif opt in ("-v", "--voice"):
            voice = arg
        elif opt in ("-d", "--debug"):
            debug = True
        else:
            help(sys.argv[0])
            sys.exit()

    client = Client(debug)

    if(debug):
        client.list_voices(lang)

    while running == True:
        try:
            text = input()
        except EOFError:
            signal_handler(0, 0)
        client.speak(text, lang, voice)


if __name__ == "__main__":
    main()
