from sgpt.config import cfg
from sgpt.role import DefaultRoles, SystemRole        
from sgpt.handlers.default_handler import DefaultHandler
import speech_recognition as sr
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        print(f"You said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""

def ask_assistant(question):
		role_class = SystemRole.get("sysadmin")
		md = False
		model = cfg.get("DEFAULT_MODEL")
		temperature = 0.0
		top_p = 1.0
		cache = True
		function_schemas = None
		full_completion = DefaultHandler(role_class, md).handle(
		    prompt=question,
		    model=model,
		    temperature=temperature,
		    top_p=top_p,
		    caching=cache,
		    functions=function_schemas,
		)
		return full_completion    

def main():
    speak("Hello! How can I assist you today?")
    while True:
        command = listen()
        if "exit" in command or "quit" in command:
            speak("Goodbye!")
            break
        elif command:
            # Use OpenAI for response
            response = ask_assistant(command)
            print(f"Assistant: {response}")
            speak(response)
            
if __name__ == "__main__":
    main()                            
