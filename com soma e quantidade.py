import tkinter as tk
from tkinter import ttk
import requests

class WeekdayAgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Semanal")
        
        self.weekdays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        self.notes = {weekday: {'foods': [], 'quantities': []} for weekday in self.weekdays}
        
        self.note_entries = {}
        self.add_buttons = {}
        self.note_outputs = {}
        
        self.create_ui()
        
    def create_ui(self):
        self.configure_root()
        self.create_header()
        self.create_weekday_elements()
        self.create_calories_elements()
        self.configure_styles()
        
    def configure_root(self):
        self.root.configure(background='#F0F0F0')
        self.root.minsize(800, 800)
        
    def create_header(self):
        header_label = tk.Label(self.root, text="Agenda Semanal", font=("Helvetica", 16), padx=10, pady=10, background='#F0F0F0')
        header_label.pack(fill="x")
        
    def create_weekday_elements(self):
        for weekday in self.weekdays:
            frame = self.create_frame(self.root)
            self.create_weekday_label(weekday, frame)
            self.create_note_entry(weekday, frame)
            self.create_add_button(weekday, frame)
            self.create_output_label(weekday, frame)
        
    def create_frame(self, parent):
        frame = tk.Frame(parent, background="#F0F0F0")
        frame.pack(fill="x", padx=10, pady=5)
        return frame
        
    def create_weekday_label(self, weekday, frame):
        label = tk.Label(frame, text=weekday, font=("Helvetica", 12, "bold"), padx=10, pady=5, background='#F0F0F0')
        label.pack(side="left")
            
    def create_note_entry(self, weekday, frame):
        name_entry = tk.Entry(frame, width=30, font=("Helvetica", 10))
        name_entry.pack(side="left", padx=10, pady=5)
        self.note_entries[weekday] = name_entry
        
    def create_add_button(self, weekday, frame):
        add_button = self.create_button(frame, "+", lambda day=weekday: self.add_foods(day))
        self.add_buttons[weekday] = add_button
        
    def create_button(self, parent, text, command):
        button = ttk.Button(parent, text=text, style="RoundedButton.TButton", command=command)
        button.pack(side="left", padx=5, pady=5)
        return button
        
    def create_output_label(self, weekday, frame):
        output_label = tk.Listbox(frame, selectmode=tk.SINGLE, width=30, height=3)
        output_label.pack(side="left", padx=10, pady=5)
        self.note_outputs[weekday] = output_label
    
    def create_calories_elements(self):
        sum_calories_button = self.create_button(self.root, "Calcular Soma de Calorias", self.calculate_total_calories)
        self.total_calories_label = self.create_label(self.root, "Total de Calorias: 0.00", ("Helvetica", 12, "bold"))
        
    def create_label(self, parent, text, font):
        label = tk.Label(parent, text=text, font=font, background='#F0F0F0')
        label.pack(fill="x", padx=10, pady=10)
        return label
        
    def configure_styles(self):
        style = ttk.Style()
        style.configure("RoundedButton.TButton", relief="flat", background="#A9A9A9", borderwidth=0, bordercolor="#A9A9A9", font=("Helvetica", 10))
        
    def add_foods(self, weekday):
        foods_entry = self.note_entries[weekday].get()
        foods = foods_entry.split(',')
        
        for food in foods:
            food = food.strip()
            if food:
                self.notes[weekday]['foods'].append(food)
                self.notes[weekday]['quantities'].append("1")
        self.update_output_text(weekday)
    
    def update_output_text(self, weekday):
        self.note_outputs[weekday].delete(0, tk.END)
        
        foods = self.notes[weekday]['foods']
        quantities = self.notes[weekday]['quantities']
        
        for food, quantity in zip(foods, quantities):
            calorias_info = self.get_calories_info(food)
            if calorias_info and 'calorias' in calorias_info:
                calorias_value = calorias_info['calorias'].split()[0]
                self.note_outputs[weekday].insert(tk.END, f"{food} ({quantity}) - {calorias_value} cal")

    def calculate_total_calories(self):
        total_calories = 0
        for weekday in self.weekdays:
            foods = self.notes[weekday]['foods']
            quantities = self.notes[weekday]['quantities']
            
            for food, quantity in zip(foods, quantities):
                calorias_info = self.get_calories_info(food)
                if calorias_info and 'calorias' in calorias_info:
                    calorias_value = calorias_info['calorias'].split()[0]
                    total_calories += float(calorias_value) * float(quantity.replace(',', '.'))
        self.total_calories_label.config(text=f"Total de Calorias: {total_calories:.2f}")

    def get_calories_info(self, food):
        url = f'https://caloriasporalimentoapi.herokuapp.com/api/calorias/?descricao={food}'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = WeekdayAgendaApp(root)
    root.columnconfigure(0, weight=1)
    root.mainloop()
