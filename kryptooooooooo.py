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
        self.root = tk.Tk()
        self.root.title("Virtual Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#000000')  # Set background color to black

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

        self.is_listening = False
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

        self.configure_commands()

        self.listen_thread = None

    def configure_commands(self):
        self.commands = {
            "hello": self.say_hello,
            "play": self.play_song,
            "what is your name": self.say_name,
            "time": self.get_time,
            "tell me a joke": self.tell_joke,
            "bye": self.say_goodbye,
            "send email": self.send_email,
            "make a call": self.make_call,
            "what is": self.get_wikipedia_info,
            "who is": self.get_wikipedia_info
        }

    def say_hello(self):
        self.speak("Hello! How can I assist you today?")

    def play_song(self, song):
        self.speak(f'playing {song}')
        pywhatkit.playonyt(song)

    def say_name(self):
        self.speak("I am your virtual assistant Krypto.")

    def get_time(self):
        time = datetime.datetime.now().strftime('%I:%M %p')
        self.speak('current time is ' + time)

    def tell_joke(self):
        joke = pyjokes.get_joke()
        self.speak(joke)

    def say_goodbye(self):
        self.speak("Goodbye!")
        self.root.destroy()

    def get_wikipedia_info(self, person):
        info = wikipedia.summary(person, 2)
        self.speak(info)

    def send_email(self):
        subject = 'Test'
        body = "This is a test email"
        to = "recipient@example.com"  # Replace with the actual recipient email address

        msg = MIMEMultipart()
        msg.attach(MIMEText(body, 'plain'))
        msg['subject'] = subject
        msg['to'] = to
        user = "your_email@gmail.com"  # Replace with your actual Gmail email address
        msg['from'] = user
        password = "your_email_password"  # Replace with your actual Gmail password

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(user, password)
            server.sendmail(user, to, msg.as_string())
            server.quit()
            print('Email sent successfully')
            self.speak('Email sent')
        except Exception as e:
            print(f"Error sending email: {e}")
            self.speak('Error sending email')

    def make_call(self):
        account_sid = "your_account_sid"  # Replace with your Twilio account SID
        auth_token = "your_auth_token"  # Replace with your Twilio authentication token
        client = Client(account_sid, auth_token)  # Initialize the Twilio Client

        call = client.calls.create(
            twiml='<Response><Say>Hello</Say></Response>',
            to='+1234567890',  # Replace with the recipient's phone number
            from_="+0987654321"  # Replace with your Twilio phone number
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
                print('listening')
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)

            try:
                command = self.recognizer.recognize_google(audio)
                print("You said:", command)
                self.process_command(command.lower())
            except sr.UnknownValueError:
                self.speak("Sorry, I couldn't understand your command. Thank you for having me")
                print("Sorry, I couldn't understand your command.")
            except sr.RequestError as e:
                print(f"Sorry, there was an error with the speech recognition service: {e}")

    def toggle_listen(self):
        if not self.is_listening:
            self.is_listening = True
            self.btn_listen["text"] = "Listening..."
            self.listen_thread = Thread(target=self.listen_thread)
            self.listen_thread.start()
        else:
            self.is_listening = False
            self.btn_listen["text"] = "Start Listening"

    def process_command(self, command):
        for keyword, function in self.commands.items():
            if keyword in command:
                if 'play' in keyword:
                    function(command.replace('play', '').strip())
                elif 'what is ' in keyword or 'who is ' in keyword:
                    function(command.replace(keyword, '').strip())
                else:
                    function()
                break
        else:
            self.speak("I'm not sure how to respond to that.")


if __name__ == "__main__":
    assistant_gui = VirtualAssistantGUI()
    assistant_gui.root.mainloop()