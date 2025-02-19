import tkinter as tk
from tkinter import font
import time
import os

class StoryGame:
    def __init__(self, root, story_file):
        self.root = root
        self.root.title("Sztori Mesélő Játék")
        self.root.geometry("800x600") 
        self.root.configure(bg="black")

        
        if not os.path.exists(story_file):
            raise FileNotFoundError(f"A '{story_file}' fájl nem található!")

        self.story_file = story_file
        self.story_data = self.load_story_data()
        self.current_step = 0

        
        self.root.tk.call("font", "create", "PressStart2P", "-family", "Press Start 2P", "-size", 16)

        
        self.pixel_font = font.Font(family="PressStart2P", size=16)

        
        self.label = tk.Label(
            root,
            text="",
            font=self.pixel_font,
            wraplength=700,
            anchor="w",  # Balra igazítás
            justify="left",  # Balra igazított szöveg
            bg="black",  # Háttérszín
            fg="green",  # Szövegszín
            borderwidth=10,  # Szegély vastagsága
            padx=20,  # Vízszintes kitöltés
            pady=20,  # Függőleges kitöltés
        )
        self.label.pack(pady=20)

        # Gombok
        self.button_a = tk.Button(
            root,
            text="",
            font=self.pixel_font,
            bg="black",  # Háttérszín
            fg="green",  # Szövegszín
            command=self.choose_a,
        )
        self.button_a.pack(pady=10)
        self.button_a.pack_forget()  # Elrejtjük a gombot kezdetben

        self.button_b = tk.Button(
            root,
            text="",
            font=self.pixel_font,
            bg="black",  # Háttérszín
            fg="green",  # Szövegszín
            command=self.choose_b,
        )
        self.button_b.pack(pady=10)
        self.button_b.pack_forget()  # Elrejtjük a gombot kezdetben

        self.update_story()

    def load_story_data(self):
        with open(self.story_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        story_data = []
        for line in lines:
            parts = line.strip().split(' | ')
            story_data.append({
                'text': parts[0],
                'option_a': parts[1],
                'option_b': parts[2],
                'target_a': int(parts[3]),
                'target_b': int(parts[4])
            })
        return story_data

    def animate_text(self, text):
        for i in range(len(text) + 1):
            self.label.config(text=text[:i])
            self.root.update()
            time.sleep(0.025)  # Szöveg megjelenítésének sebessége

        # A szöveg betöltése után megjelenítjük a gombokat
        self.button_a.pack(pady=10)
        self.button_b.pack(pady=10)

    def update_story(self):
        step = self.story_data[self.current_step]
        self.animate_text(step['text'])
        self.button_a.config(text=step['option_a'])
        self.button_b.config(text=step['option_b'])

    def choose_a(self):
        self.current_step = self.story_data[self.current_step]['target_a']
        if self.current_step == -1:
            self.end_game()
        else:
            self.button_a.pack_forget()  # Elrejtjük a gombot
            self.button_b.pack_forget()  # Elrejtjük a gombot
            self.update_story()

    def choose_b(self):
        self.current_step = self.story_data[self.current_step]['target_b']
        if self.current_step == -1:
            self.end_game()
        else:
            self.button_a.pack_forget()  # Elrejtjük a gombot
            self.button_b.pack_forget()  # Elrejtjük a gombot
            self.update_story()

    def end_game(self):
        self.label.config(text="A történet véget ért!")
        self.button_a.config(state=tk.DISABLED)
        self.button_b.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()

    # A szkript mappájának meghatározása
    script_dir = os.path.dirname(os.path.abspath(__file__))
    story_file = os.path.join(script_dir, "story.txt")
    
    # Ellenőrizd, hogy a fájl létezik-e
    if not os.path.exists(story_file):
        print(f"Hiba: A '{story_file}' fájl nem található!")
    else:
        game = StoryGame(root, story_file)
        root.mainloop()