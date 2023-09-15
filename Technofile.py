import tkinter as tk
import os
import boto3
import pywhatkit
from tkinter import simpledialog
import speech_recognition as sr
import datetime as dt
import cv2
import time
from instabot import Bot


myec2 = boto3.client("ec2")
voice_assistance_button = None

def create_basic_window():
    global voice_assistance_button
    root = tk.Tk()
    root.title("Basic GUI")
    root.geometry("400x650")
    #date
    date = dt.datetime.now()
    
    
    label = tk.Label(root,text="%s"%(date)).pack()

    # Add widgets and functionality here
    label = tk.Label(root, text="Hello jarvis here by Team Tech :")
    label.pack()

    voice_assistance_button = tk.Button(root, text="Voice Assistance", command=enable_voice_assistance)
    voice_assistance_button.pack(pady=20)

    button = tk.Button(root, text="Email", command=on_button_email)
    button.pack(pady=10)

    button = tk.Button(root, text="EC2", command=on_button_ec2)
    button.pack(pady=10)
    
    button = tk.Button(root, text="Add S3 Bucket", command=s3_bucket_create)
    button.pack(pady=10)

    button = tk.Button(root, text="Notepad", command=on_button_click)
    button.pack(pady=10)

    button = tk.Button(root, text="Chrome", command=on_click)
    button.pack(pady=10)

    button = tk.Button(root, text="Paint", command=on_click_paint)
    button.pack(pady=10)

    button = tk.Button(root, text="Word", command=on_click_word)
    button.pack(pady=10)
    
    button = tk.Button(root, text="Play on youtube", command=youtube_music)
    button.pack(pady=10)
    
    button = tk.Button(root,text="Click Photo", command=take_photo)
    button.pack(pady=10)
    
    
    button = tk.Button(root,text="Exit",width=10,fg="#fff",bg="#f00",command=root.destroy)
    button.pack(pady=10)
    
    

    
    root.mainloop()

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        user_input = recognizer.recognize_google(audio)
        print(f"User said: {user_input}")
        return user_input
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return None
    except sr.RequestError:
        print("There was a problem with the speech recognition service.")
        return None

def enable_voice_assistance():
    global voice_assistance_button

    voice_assistance_button.config(state=tk.DISABLED)
    user_input = get_voice_input()
    if user_input:
        process_voice_command(user_input)
    voice_assistance_button.config(state=tk.ACTIVE)

def process_voice_command(command):

    if "email" in command:
        on_button_email()
    elif "EC2" in command:
        on_button_ec2()
    elif "notepad" in command:
        on_button_click()
    elif "chrome" in command:
        on_click()
    elif "paint" in command:
        on_click_paint()
    elif "word" in command:
        on_click_word()
    else:
        print("Command not recognized.")

def on_button_ec2():
    response = myec2.run_instances(
        ImageId='ami-0ded8326293d3201b',
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1
    )

def on_button_email():
    msg = "Hello from python"
    recipient_email = get_voice_input()
    if not recipient_email:  # If voice input fails, use text-based input dialog
        recipient_email = simpledialog.askstring("Input", "Enter recipient's email address:")
    if recipient_email:
        pywhatkit.send_mail("testprect@gmail.com", "aljeobaueiacqtko", "test code",msg, recipient_email)

def on_button_click():
    os.system("notepad")

def on_click():
    os.system("start chrome")
    
def on_click_paint():
    os.system("start mspaint")

def on_click_word():
    os.system("start write")
    
def s3_bucket_create():
    ec2_client = boto3.client('ec2')
    response_ec2 = ec2_client.describe_instances()

    # Create an S3 Instance
    s3_client = boto3.client('s3')

    # Call create_bucket to create an S3 bucket
    response_s3 = s3_client.create_bucket(
        ACL='private',  # Use 'private' instead of 'enabled' for private ACL
        Bucket='shajafi',
        CreateBucketConfiguration={
            'LocationConstraint': 'ap-south-1'  # Use the region code, not the region name
        }
    )

def youtube_music():
    
    final_music = "dil meri na sune"
    print(f"playing {final_music} on youtube")
    pywhatkit.playonyt(final_music)

def take_photo():
    cap = cv2.VideoCapture(0)
    time.sleep(1)
    ret, frame = cap.read()
    if ret:
        cv2.imshow('photo.jpg', frame)
        cv2.imwrite('photo.jpg',frame)
        cap.release()
        cv2.destroyAllWindows()
    
    
create_basic_window()