import pyperclip
import keyboard
import sys
from plyer import notification
import time 
import re 
import customtkinter
import pyautogui
from library.CallAI import CallAI

class GUI:
    """Class to handle the graphical user interface for the Code Assistant."""

    def __init__(self) -> None:
        """Initializes the GUI class, setting up the main window and its elements."""
        customtkinter.set_appearance_mode("dark")
        
        self.program_running = False
        self.prompt = ""
        self.lang = "English"

        self.call_ai = CallAI()
        
        self.root = customtkinter.CTk()
        self.root.title("Code Assistant Control")
        self.root.iconbitmap('./icon/favicon.ico')

        self.frame = customtkinter.CTkFrame(self.root)
        self.frame.pack(pady=20)

        self.switch = customtkinter.CTkSwitch(self.frame,text="Turn On", command=self.toggle_program)
        self.switch.pack(pady=10)

        self.combobox = customtkinter.CTkComboBox(self.frame,values=["English", "Portuguese"], command=self.change_language)
        self.combobox.pack(pady=30)

        customtkinter.CTkLabel(self.frame,text="Click 'Turn On' to activate the Code Assistant").pack()
    
    def trigger_notification(self, message: str, timeout: float) -> None:
        """Triggers a desktop notification.

        Args:
            message (str): The message to be displayed in the notification.
            timeout (float): Duration the notification will be displayed.
        """
        notification.notify(
            title='Convergint - Code Assistant',
            message=message,
            app_icon="./icon/favicon.ico",
            timeout=timeout,
        )

    def change_language(self,value: str) -> None:
        """This function changes the language of the documentation output 

        Args:
            value (str): The value chosen in the checkbox 
        """
        self.call_ai.change_language(value) 
        return None 
    
    def add_clipboard(self, mode: str) -> None:
        """Processes clipboard content and generates code using the AI.
        
        Args:
            mode (str): The mode of generation , can be code or documentation
        """
        time.sleep(2)
        prompt = pyperclip.paste()
        self.prompt = prompt
        if self.prompt:
            self.trigger_notification('Processing code...', 3)
            if mode == "code":
                code = self.call_ai.generate_code(prompt)
            pyperclip.copy(code)
            self.trigger_notification('Code ready and copied to the clipboard', 3)
    
    def new_code(self):
        """Generate the code and then add to the clipboard"""
        self.add_clipboard("code")
        return 
    
    def select_word(self) -> str:
        """Goes the cursor to the left until the method is found"""
        pyautogui.doubleClick()  
        pyautogui.hotkey('ctrl', 'c')  
        content = pyperclip.paste().strip()  
        return content

    def move_cursor(self,content: str =""):
        """Find the word with the end part in the . because methods are easier to be predicted"""
        content = self.select_word()   
        generated = self.call_ai.complete_code(content)
        pyperclip.copy(generated)
    
    
    def toggle_program(self) -> None:
        """Toggles the program state between running and stopped."""
        if self.program_running:
            self.program_running = False
            self.switch.configure(text="Turn On")
            keyboard.unhook_all_hotkeys()
        else:
            self.program_running = True
            self.switch.configure(text="Turn Off")
            keyboard.add_hotkey('esc+c', self.stop)            
            keyboard.add_hotkey('ctrl+q',self.move_cursor)
            keyboard.add_hotkey("ctrl+c", self.new_code)
    
    def stop(self) -> None:
        """Stops the program."""
        sys.exit()

    def run(self) -> None:
        """Runs the main GUI loop."""
        self.root.mainloop()

if __name__ == "__main__":
    g = GUI() 
    g.run()

# eof
