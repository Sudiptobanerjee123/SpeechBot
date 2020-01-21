from chatterbot import ChatBot  #ChatBot library v1.04
from chatterbot.trainers import ListTrainer
from tkinter import * # GUI
import pyttsx3 as pp # Text to Audio
import speech_recognition as s #Speech to Speech
import threading

# Train the BOT
bot = ChatBot("Warrior")
conversation = open('mydata.txt').read()
conversation = conversation.strip().split('\n')
trainer = ListTrainer(bot)
trainer.train(conversation)

#Tkinter GUI
main = Tk()
main.geometry("500x500")
main.title("Smart Bot")
main.config(bg="ivory")
frame = Frame(main)
sc = Scrollbar(frame)
msgs = Listbox(frame, width=80, height=20, yscrollcommand = sc.set)
sc.pack(side=RIGHT, fill=Y)
msgs.pack(side=LEFT, fill=BOTH, pady=10)
frame.pack()

#BOT Function
def ask_from_bot():
    query = text_field.get()
    answer_from_bot = bot.get_response(query)
    msgs.insert(END, "You : " + query)
    msgs.insert(END, "Bot : " + str(answer_from_bot))
    speak(answer_from_bot)
    text_field.delete(0, END)
    msgs.yview(END)

# Creating text field
text_field = Entry(main, font=("Times New Roman", 20), bg="powder blue")
text_field.pack(fill=X, pady=10)
btn = Button(main, text="ASK", font=("Arial", 15), command=ask_from_bot)
btn.pack()


engine = pp.init() #Initialise the audio module

voices = engine.getProperty("voices")
print(voices)

engine.setProperty('voice', voices[0].id) # Male Voice
#engine.setProperty('voice',voices[1].id)#Female

def speak(word):
    engine.say(word)
    engine.runAndWait()

def TakeQuery():
    sr = s.Recognizer()
    sr.pause_threshold =1
    print("Your Bot is Listening! Try to Speak..................")
    with s.Microphone() as m:
        try:
            audio = sr.listen(m)
            query = sr.recognize_google(audio, language='eng-in')
            print(query)
            text_field.delete(0, END)
            text_field.insert(0, query)
            ask_from_bot()
        except Exception as e:
            print(e)
            print("Not Recognised")

def enter_function(ev):
    btn.invoke()

def repeat_Listen():
    while True:
        TakeQuery()
main.bind('<Return>', enter_function)

t=threading.Thread(target=repeat_Listen)
t.start()

main.mainloop()

