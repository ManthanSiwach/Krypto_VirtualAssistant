import tkinter as tk
from tkinter import ttk, scrolledtext
from threading import Thread
import speech_recognition as sr
import pyttsx3
import pyjokes
import wikipedia
import pywhatkit
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client

class VirtualAssistantGUI:
    def __init__(self):
        self.wakeup_word = "crypto"
        self.is_listening = False
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.root = tk.Tk()
        self.root.title("Virtual Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#000000')

        style = ttk.Style()
        style.theme_use("clam")

        self.text_area = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, width=60, height=15, font=("Helvetica", 14), fg='#00ff00', bg='#000000'
        )
        self.text_area.pack(pady=10, padx=10)

        self.btn_listen = ttk.Button(
            self.root, text="Start Listening", command=self.toggle_listen, style="TButton"
        )
        self.btn_listen.pack(pady=10)

        self.btn_stop = ttk.Button(
            self.root, text="Stop Listening", command=self.stop_listen, style="TButton"
        )
        self.btn_stop.pack(pady=10)
        self.btn_stop["state"] = "disabled"

        self.configure_commands()

    def configure_commands(self):
        self.commands = {
            "hello": self.say_hello,
            "play": self.play_song,
            "what is your name": self.say_name,
            "time": self.get_time,
            "tell me a joke": self.tell_joke,
            "goodbye": self.say_goodbye,
            "send email": self.send_email,
            "make a call": self.make_call,
            "what is": self.get_wikipedia_info,
            "who is": self.get_wikipedia_info
        }

    def say_hello(self):
        self.speak("Hello! How can I assist you today?")

    def play_song(self, song):
        self.speak(f'Playing {song}')
        pywhatkit.playonyt(song)

    def say_name(self):
        self.speak("I am your virtual assistant Krypto.")

    def get_time(self):
        time = datetime.datetime.now().strftime('%I:%M %p')
        self.speak(f'The current time is {time}')

    def tell_joke(self):
        joke = pyjokes.get_joke()
        self.speak(joke)

    def say_goodbye(self):
        self.speak("Goodbye!")
        self.root.destroy()

    def get_wikipedia_info(self, topic):
        print(f"Fetching Wikipedia info for topic: {topic}")  # Debug statement
        try:
            info = wikipedia.summary(topic, sentences=2)
            self.speak(info)
        except wikipedia.DisambiguationError as e:
            self.speak("Multiple results found. Please be more specific.")
            print(f"DisambiguationError: {e}")
        except wikipedia.PageError as e:
            self.speak(f"Sorry, no information found on {topic}.")
            print(f"PageError: {e}")
        except Exception as e:
            self.speak(f"An error occurred: {e}")
            print(f"Exception: {e}")

    def send_email(self):
        subject = 'Test'
        body = "This is a test email"
        to = "rs20020717@gmail.com"

        msg = MIMEMultipart()
        msg.attach(MIMEText(body, 'plain'))
        msg['subject'] = subject
        msg['to'] = to
        user = "kryp17to@gmail.com"
        msg['from'] = user
        password = "zobeigzsgmzdxskl"

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(user, password)
            server.sendmail(user, to, msg.as_string())
            server.quit()
            self.speak('Email sent')
        except Exception as e:
            print(f"Error sending email: {e}")
            self.speak('Error sending email')

    def make_call(self):
        account_sid = "AC30a442e846481e2e9dcdf5cb1f75cdc8"
        auth_token = "1406e1c7df1068680511699f7aaacf39"
        client = Client(account_sid, auth_token)

        call = client.calls.create(
            twiml='<Response><Say>Hello</Say></Response>',
            to='+918586883992',
            from_="+18065573779"
        )

        self.speak('Making a call')

    def speak(self, text):
        self.text_area.insert(tk.END, f"Assistant: {text}\n")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_thread(self):
        while self.is_listening:
            with sr.Microphone() as source:
                self.speak("Listening for commands...")
                print('Listening')
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)

            try:
                command = self.recognizer.recognize_google(audio).lower()
                print("You said:", command)

                if command.startswith(self.wakeup_word):
                    self.process_command(command[len(self.wakeup_word):].strip())
                else:
                    self.speak("Sorry, I didn't hear the wakeup word.")
                    print("Sorry, I didn't hear the wakeup word.")
                    
            except sr.UnknownValueError:
                self.speak("Sorry, I couldn't understand your command.")
                print("Sorry, I couldn't understand your command.")
            except sr.RequestError as e:
                print(f"Sorry, there was an error with the speech recognition service: {e}")

    def toggle_listen(self):
        if not self.is_listening:
            self.is_listening = True
            self.btn_listen["state"] = "disabled"
            self.btn_stop["state"] = "normal"
            self.listen_thread = Thread(target=self.listen_thread)
            self.listen_thread.start()
        else:
            self.stop_listen()

    def stop_listen(self):
        self.is_listening = False
        self.btn_listen["state"] = "normal"
        self.btn_stop["state"] = "disabled"

    def process_command(self, command):
        print(f"Processing command: {command}")  # Debug statement
        for keyword, function in self.commands.items():
            if command.startswith(keyword):
                argument = command[len(keyword):].strip()
                if keyword in ['send email', 'goodbye', 'make a call', 'tell me a joke', 'what is your name', 'time', 'hello']:
                    # Call functions that do not require arguments
                    function()
                elif argument:
                    # Call functions that require arguments
                    function(argument)
                else:
                    self.speak("I need more information to process this command.")
                return
        self.speak("I'm not sure how to respond to that.")

if __name__ == "__main__":
    assistant_gui = VirtualAssistantGUI()
    assistant_gui.root.mainloop()
