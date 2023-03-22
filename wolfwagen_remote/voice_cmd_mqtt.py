#!/usr/bin/env python
import speech_recognition as sr
import time
import paho.mqtt.client as paho
broker_ip="eb2-3254-ub01.csc.ncsu.edu"
broker_port=12345

commands = ["start", "stop", "left", "right"]

def pre_process(cmd):
    for c in commands:
        if cmd.find(c) != -1:
            return c    
    return "none"

def main():
    print('Hi from wolfwagen_remote -- voice commander')
    client= paho.Client("client-laptop")
    client.connect(broker_ip, broker_port)
    client.loop_start()

    r = sr.Recognizer()
    mic = sr.Microphone(device_index=0)

    with mic as source:
        while True:
            # print("[adjusting for noise]")
            r.adjust_for_ambient_noise(source)
            print("[Say something]")
            audio = r.listen(source, phrase_time_limit=1.5)
            try:
                ret = r.recognize_google(audio)
                cmd = pre_process(ret)
                client.publish("voice_cmd_mqtt", cmd)
                print("input: %s" % (ret))
            except Exception as e:
                # print(e)
                print("-- try again --")


if __name__ == '__main__':
    main()
