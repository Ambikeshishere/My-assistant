import os
import speech_recognition as sr
import signal
import psutil
import threading
import tkinter as tk

class VoiceControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Command App")
        self.root.geometry("400x300")
        
        self.command_label = tk.Label(self.root, text="Say a command", font=("Helvetica", 14))
        self.command_label.pack(pady=20)
        
        self.status_label = tk.Label(self.root, text="Status: Idle", font=("Helvetica", 10))
        self.status_label.pack(pady=10)

        self.listen_thread = threading.Thread(target=self.continuous_listening, daemon=True)
        self.listen_thread.start()

    def continuous_listening(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            self.update_status("Listening...")
            while True:
                try:
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio).lower()
                    self.command_label.config(text=f"You said: {command}")
                    self.execute_command(command)
                except sr.UnknownValueError:
                    self.command_label.config(text="Sorry, I didn't catch that.")
                    self.update_status("Status: Error - Couldn't understand.")
                except sr.RequestError:
                    self.command_label.config(text="Could not request results.")
                    self.update_status("Status: Error - Request failed.")

    def close_vs_code(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == "Code.exe" or proc.info['name'] == "code":
                os.kill(proc.info['pid'], signal.SIGTERM)
                self.update_status("VS Code closed.")
                return
        self.update_status("VS Code is not running.")

    def execute_command(self, command):
        if "hello baby" in command:
            self.command_label.config(text="Opening VS Code...")
            self.update_status("VS Code opening...")
            os.system("code")
        elif "bye baby" in command:
            self.command_label.config(text="Closing VS Code...")
            self.update_status("Closing VS Code...")
            self.close_vs_code()
        else:
            self.command_label.config(text="Command not recognized.")
            self.update_status("Status: Command not recognized.")

    def update_status(self, status_text):
        self.status_label.config(text=f"Status: {status_text}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceControlApp(root)
    root.mainloop()
