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

    def speak(self, text, lang, voice, rate, pitch, volume, player):
        text = text.replace('<', '&lt;').replace('>', '&gt;')
        text = '<speak><prosody rate="%d%%" pitch="%+d%%" volume="%+ddB">%s</prosody></speak>' % (rate, pitch, volume, text)
        resp = self.polly.synthesize_speech(OutputFormat='mp3',
                Text=text,
                TextType='ssml',
                LanguageCode=lang,
                VoiceId=voice)
        audio_stream = resp['AudioStream']
        audio_data = audio_stream.read()
        audio_stream.close()
        subprocess.run([player, '-'], input=audio_data, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        print("FINISHED_UTTERANCE")

    def list_voices(self, lang):
        print(self.polly.describe_voices(LanguageCode=lang))


def help(name):
    print("%s: python wrapper for communicating with Amazon Polly\n" % name)
    print("Usage:")
    print("\t-l|--lang=<lang>:    Use the specified language (default: en-AU)")
    print("\t-v|--voice=<voice>:  Use the specified voice (default: Nicole)")
    print("\t-r|--rate=<rate>:    Modify the rate of speech, percentage: [20-200] (default: 100)")
    print("\t-p|--pitch=<pitch>:  Raise or lower the pitch (tone) of the speech, percentage: [-33-50] (default: 0)")
    print("\t-m|--volume=<vol>:   Change the volume for the speech, decibels (default: 0)")
    print("\t-y|--player=<vol>:   Sound playing program (default mpg123)")
    print("\t-d|--debug:          Increase verbosity")
    print("\t-h|--help:           Show usage information\n")
    sys.exit(2)


def main():
    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "l:v:r:p:m:y:dh", ["lang=", "voice=", "rate=", "pitch=", "volume=", "player=", "debug", "help"])
    except getopt.GetoptError as err:
        print(str(err))
        help(sys.argv[0])
    lang = 'en-AU'
    voice = 'Nicole'
    rate = 100 # percent
    pitch = 0 # percent (+/-)
    volume = 0 # decibels (+/-)
    player = "mpg321"
    debug = False
    for opt, arg in opts:
        if opt in ("-l", "--lang"):
            lang = arg
        elif opt in ("-v", "--voice"):
            voice = arg
        elif opt in ("-r", "--rate"):
            try:
                rate = int(arg)
            except ValueError:
                print("Error: rate should be an integer\n")
                help(sys.argv[0])
        elif opt in ("-p", "--pitch"):
            try:
                pitch = int(arg)
            except ValueError:
                print("Error: pitch should be an integer\n")
                help(sys.argv[0])
        elif opt in ("-m", "--volume"):
            try:
                volume = int(arg)
            except ValueError:
                print("Error: volume should be an integer\n")
                help(sys.argv[0])
        elif opt in ("-y", "--player"):
            player = arg
        elif opt in ("-d", "--debug"):
            debug = True
        else:
            help(sys.argv[0])

    client = Client(debug)

    if(debug):
        client.list_voices(lang)

    while running == True:
        try:
            text = input()
        except EOFError:
            signal_handler(0, 0)
        client.speak(text, lang, voice, rate, pitch, volume, player)


if __name__ == "__main__":
    main()
