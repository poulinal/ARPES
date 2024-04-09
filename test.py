import tkinter as tk
import customtkinter

'''
class CustomDropdown(tk.Frame):
    def __init__(self, master, options):
        super().__init__(master)

        self.options = options

        self.selected_option = tk.StringVar()
        self.selected_option.set("Select an Option")

        self.label = tk.Label(self, textvariable=self.selected_option, bg="white", fg="blue", bd=1, relief="solid", padx=10, pady=5)
        self.label.pack(side="left", fill="both", expand=True)

        self.dropdown_frame = tk.Frame(self, bd=1, relief="solid")
        self.listbox = tk.Listbox(self.dropdown_frame, bg="white", fg="blue", selectbackground="lightblue", exportselection=False)
        for option in self.options:
            self.listbox.insert("end", option)
        self.listbox.bind("<Button-1>", self.on_listbox_click)
        self.listbox.pack(fill="both", expand=True)

        self.dropdown_frame.pack_forget()

        self.label.bind("<Button-1>", self.toggle_dropdown)

    def toggle_dropdown(self, event):
        if self.dropdown_frame.winfo_ismapped():
            self.dropdown_frame.pack_forget()
        else:
            self.dropdown_frame.pack(in_=self, side="left", fill="both", expand=True)

    def on_listbox_click(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.selected_option.set(self.options[selected_index[0]])
        self.dropdown_frame.pack_forget()

'''

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x240")

def button_function():
    print("button pressed")


# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


app.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Custom Dropdown Menu")

    options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]
    dropdown = CustomDropdown(root, options)
    dropdown.pack(padx=10, pady=10)

    root.mainloop()
