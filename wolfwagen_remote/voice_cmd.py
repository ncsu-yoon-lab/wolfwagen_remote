import speech_recognition as sr
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

commands = ["start", "stop", "left", "right"]

def pre_process(cmd):
    for c in commands:
        if cmd.find(c) != -1:
            return c    
    return "none"

def main():
    print('Hi from wolfwagen_remote.')

    rclpy.init()
    node = Node("voice_command")
    pub_voice_cmd = node.create_publisher(String, "voice_cmd", 1)

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
                msg = String()
                msg.data = pre_process(ret)
                pub_voice_cmd.publish(msg)
                print("input: %s --> cmd: %s" % (ret, msg.data))
            except Exception as e:
                # print(e)
                print("-- try again --")


if __name__ == '__main__':
    main()
