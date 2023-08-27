import tkinter as tk
from tkinter import ttk
import a  # Importe o módulo a

class WeekdayAgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Semanal")
        
        self.weekdays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        self.notes = {weekday: {'note': '', 'done': False, 'food': '', 'quantity': ''} for weekday in self.weekdays}
        
        self.note_entries = {}
        self.done_buttons = {}
        self.note_outputs = {}
        
        self.create_ui()
        
    def create_ui(self):
        self.root.configure(background='#F0F0F0')
        
        header_label = tk.Label(self.root, text="Agenda Semanal", font=("Helvetica", 16), padx=10, pady=10, background='#F0F0F0')
        header_label.grid(row=0, columnspan=len(self.weekdays)+1)
        
        for idx, weekday in enumerate(self.weekdays):
            label = tk.Label(self.root, text=weekday, font=("Helvetica", 12, "bold"), padx=10, pady=5, background='#F0F0F0')
            label.grid(row=1, column=idx+1)
            
            name_entry = tk.Entry(self.root, width=30, font=("Helvetica", 10))
            name_entry.grid(row=2, column=idx+1, padx=10, pady=5)
            self.note_entries[weekday] = name_entry
            
            quantity_entry = tk.Entry(self.root, width=10, font=("Helvetica", 10))
            quantity_entry.grid(row=3, column=idx+1, padx=10, pady=5)
            self.notes[weekday]['quantity'] = quantity_entry
            
            # Configurar validação para aceitar apenas números
            vcmd = self.root.register(self.validate_numeric_input)
            quantity_entry.config(validate="key", validatecommand=(vcmd, "%P"))
            
            done_button = ttk.Button(self.root, text="Concluído", style="RoundedButton.TButton", command=lambda day=weekday: self.toggle_done(day))
            done_button.grid(row=4, column=idx+1, padx=10, pady=5)
            self.done_buttons[weekday] = done_button
            
            output_label = tk.Label(self.root, text="", wraplength=200, justify="left", font=("Helvetica", 10), background='#F0F0F0')
            output_label.grid(row=5, column=idx+1, padx=10, pady=5)
            self.note_outputs[weekday] = output_label
        
        style = ttk.Style()
        style.configure("RoundedButton.TButton", relief="flat", background="#A9A9A9", borderwidth=0, bordercolor="#A9A9A9", font=("Helvetica", 10))
        
    def toggle_done(self, weekday):
        self.notes[weekday]['done'] = not self.notes[weekday]['done']
        
        # Chame a função 'req' do módulo 'a' para obter informações de calorias
        name = self.note_entries[weekday].get()
        quantity = self.notes[weekday]['quantity'].get()
        
        if name and quantity:
            note_text = f"{name} (✔️)\nQuantidade: {quantity}"
            calorias_info = a.req(name)
            
            # Atualize o texto de saída das notas com informações de calorias
            if calorias_info:
                calorias_text = f"Calorias: {calorias_info['calorias']}\nQuantidade: {calorias_info['quantidade']}"
                note_text += f"\n{calorias_text}"
            
        else:
            note_text = "(✔️)"
            
        self.note_outputs[weekday].config(text=note_text)
    
    def validate_numeric_input(self, new_value):
        return new_value == "" or new_value.isnumeric()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeekdayAgendaApp(root)
    root.mainloop()
