import tkinter as tk
from tkinter import messagebox

# Function that checks if all checkboxes are selected and closes the window.
def Check_If_All_Selected(Window: tk.Tk, Checkbox_Variables: list[tk.IntVar]) -> None:
    if all(Checkbox_Variable.get() == 1 for Checkbox_Variable in Checkbox_Variables):  # If all checkboxes are selected.
        Window.destroy()  # Close the window.
        Main_Window.destroy()

def Focus_Next_Widget(event: tk.Event) -> str:
    event.widget.tk_focusNext().focus()  # Cambiar el foco al siguiente widget.
    return "break"  # Detener el comportamiento predeterminado de TAB.

# Function to add a new input field dynamically with a remove button.
def Add_New_Input_With_Remove(Main_Window: tk.Tk, Input_Entries: list[tk.Frame]) -> None:
    New_Input_Frame = tk.Frame(Main_Window)  # Create a frame for the new input and button.
    
#    New_Input_Label = tk.Label(New_Input_Frame, text = f"Task:", font=("Calibri Light", 13))
#    New_Input_Label.grid(row=0, column=0, padx=5, pady=5, sticky='e')  # Place label on the left side.

    New_Input_Text = tk.Text(New_Input_Frame, font=("Calibri Light", 12), height=1,  width=50)  # Set height and width
    New_Input_Text.bind("<Tab>", lambda e: Focus_Next_Widget(e))  # Cambiar foco con TAB.
    New_Input_Text.grid(row=0, column=1, padx=10, pady=5, sticky='w')  # Place the text box.
    
    Remove_Button = tk.Button(New_Input_Frame, text = "x", font=("Calibri Light", 12), width=3,
                              command = lambda: Remove_Input(Main_Window, New_Input_Frame, Input_Entries))
    Remove_Button.grid(row=0, column=2, padx=5, pady=5)  # Place remove button next to the entry.
    
    New_Input_Frame.pack(pady=5)  # Pack the frame containing the input and button.
    Input_Entries.append(New_Input_Frame)  # Store the new frame with entry.

# Function to remove an input field dynamically.
def Remove_Input(Main_Window: tk.Tk, Input_Frame: tk.Frame, Input_Entries: list[tk.Frame]) -> None:
    Input_Frame.destroy()  # Destroy the input frame.
    Input_Entries.remove(Input_Frame)  # Remove the frame from the list.

# Function that handles input collection and opens the checklist window.
def Collect_Inputs(Input_Entries: list[tk.Frame]) -> None:
    Inputs = []
    for Input_Frame in Input_Entries:  # Iterate through each input frame.
        for widget in Input_Frame.winfo_children():  # Iterate through each child widget.
            if isinstance(widget, tk.Text):  # Check if the widget is a Text widget.
                Inputs.append(widget.get("1.0", "end-1c"))  # Collect the input value.
                break  # Exit the loop once the Text widget is found.
    if all(Inputs):  # Proceed if all inputs are filled.
        Create_Checklist_Window(Inputs)
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

# Función para subrayar el texto y mover el checkbox al final al seleccionarlo.
def On_Checkbox_Select(Checkbox: tk.Checkbutton, Checkbox_Frame: tk.Frame, Checkbox_Variable: tk.IntVar) -> None:
    if Checkbox_Variable.get() == 1:  # Si está seleccionado.
        Checkbox.config(font=("Calibri Light", 16, "overstrike"))  # Subrayar el texto.
#        Checkbox_Frame.pack_forget()  # Remover el checkbox de su posición actual.
#        Checkbox_Frame.pack(anchor='w', pady=1, side='bottom')  # Añadirlo de nuevo al final del Frame.
    else:
        Checkbox.config(font=("Calibri Light", 16))  # Quitar subrayado.

# Function that creates a new window with checkboxes from input values.
def Create_Checklist_Window(Inputs: list[str]) -> None:
    Checklist_Window = tk.Toplevel()  # Create new window.
    Checklist_Window.title("Checklist Window")
    Checklist_Window.geometry("1200x500")
    Checklist_Window.geometry("+{}+{}".format(int(Checklist_Window.winfo_screenwidth() / 2 - 600), int(Checklist_Window.winfo_screenheight() / 2 - 250)))  # Center the window.

    # Checklist_Window.attributes('-topmost', True)  # Keep the window on top.
    #Checklist_Window.attributes('-toolwindow', True)  # Disable minimize.
    Checklist_Window.attributes('-toolwindow', False)  # Enable maximize.
    # Checklist_Window.overrideredirect(True)  # Remove window decorations (title bar).

    #Checklist_Window.focus_force()  # Force focus on the window.
    #Checklist_Window.grab_set()  # Prevent clicking outside the window.

    # Close Main_Window when Checklist_Window is closed.
    Checklist_Window.protocol("WM_DELETE_WINDOW", lambda: Close_Main_Window(Checklist_Window))

    # Create a canvas for the checkboxes and a scrollbar.
    Checklist_Canvas = tk.Canvas(Checklist_Window, highlightthickness=0)
    Checklist_Scrollbar = tk.Scrollbar(Checklist_Window, orient="vertical", command=Checklist_Canvas.yview)
    Checklist_Canvas.configure(yscrollcommand=Checklist_Scrollbar.set)  # Link scrollbar and canvas.

    # Frame to hold all dynamically added checkboxes
    Checklist_Scrollable_Frame = tk.Frame(Checklist_Canvas)

    # Configure the scrollbar.
    Checklist_Scrollable_Frame.bind("<Configure>", lambda e: Checklist_Canvas.configure(scrollregion=Checklist_Canvas.bbox("all")))  # Update scroll region.
    Checklist_Canvas.create_window((0, 0), window=Checklist_Scrollable_Frame, anchor='nw')  # Place the frame in the canvas.
    Checklist_Canvas.bind_all("<MouseWheel>", lambda event: Checklist_Canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))  # Desplazamiento con rueda del mouse.

    # Pack the canvas and scrollbar.
    Checklist_Canvas.pack(side='left', fill='both', expand=True, padx=10, pady=5)  # Pack canvas.
    Checklist_Scrollbar.pack(side='right', fill='y')  # Pack scrollbar.

    # Ajustar la ventana de los checkboxes para centrarlos.
    Checkbox_Frame_Container = tk.Frame(Checklist_Scrollable_Frame)
    Checkbox_Frame_Container.pack(pady=40, padx=500, anchor='center')  # Pack the frame containing the checkboxes and center.

    Checkbox_Variables = []

    # Cambia el bucle que crea los checkboxes para agregar esta funcionalidad.
    for Row_Index, Input_Value in enumerate(Inputs):
        Checkbox_Variable = tk.IntVar()
        Checkbox_Variables.append(Checkbox_Variable)

        # Crear un Frame por cada checkbox (para poder reordenar el grupo completo).
        Checkbox_Frame = tk.Frame(Checkbox_Frame_Container)
        
        # Crear el checkbox dentro de ese frame.
        Checkbox = tk.Checkbutton(Checkbox_Frame, text=Input_Value, variable=Checkbox_Variable, font=("Calibri Light", 16), height=2)
        Checkbox.pack(anchor='w', pady=1)

        # Añadir el frame del checkbox al contenedor principal.
        Checkbox_Frame.pack(anchor='w', pady=1)

        # Vincular la función de mover y subrayar al evento de la checkbox.
        Checkbox.config(command=lambda cb=Checkbox, cf=Checkbox_Frame, cv=Checkbox_Variable: On_Checkbox_Select(cb, cf, cv))
    
    # Button that checks if all checkboxes are selected.
    Accept_Button = tk.Button(Checklist_Scrollable_Frame, text="Check", command=lambda: Check_If_All_Selected(Checklist_Window, Checkbox_Variables),
                              width=10, height=2)
    Accept_Button.pack(padx=5, pady=5)

    Edit_Frame = tk.Frame(Checklist_Window)
    Edit_Frame.pack(side='top', padx=35, pady=25) 

    # Button that checks if all checkboxes are selected.
    Edit_Button = tk.Button(Edit_Frame, text="Edit", command=lambda: [Checklist_Window.destroy(), Main_Window.deiconify()],
                              width=10, height=2)
    Edit_Button.pack(padx=5, pady=5)

    # Hide Main_Window
    Main_Window.withdraw()  # Hide the main window.

# Function to close Main_Window when Checklist_Window is closed.
def Close_Main_Window(Checklist_Window: tk.Toplevel) -> None:
    Checklist_Window.destroy()  # Destroy Checklist_Window
    Main_Window.destroy()  # Destroy Main_Window

# Main window setup.
Main_Window = tk.Tk()
Main_Window.title("Checklister")
Main_Window.geometry("1200x500")
Main_Window.geometry("+{}+{}".format(int(Main_Window.winfo_screenwidth() / 2 - 600), int(Main_Window.winfo_screenheight() / 2 - 250)))  # Center the window.

#Main_Window.attributes('-topmost', True)  # Keep the window on top.
#Main_Window.attributes('-toolwindow', True)  # Disable minimize.
Main_Window.attributes('-toolwindow', False)  # Enable maximize.

#Main_Window.focus_force()  # Force focus on the window.
#Main_Window.grab_set()  # Prevent clicking outside the window.

# Create a canvas for the entries and a scrollbar.
Entries_Canvas = tk.Canvas(Main_Window, highlightthickness=0)
Entries_Canvas.bind_all("<MouseWheel>", lambda event: Entries_Canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))  # Desplazamiento con rueda del mouse.
Entries_Scrollbar = tk.Scrollbar(Main_Window, orient="vertical", command=Entries_Canvas.yview)
Entries_Canvas.configure(yscrollcommand=Entries_Scrollbar.set)  # Link scrollbar and canvas.

# Frame to hold all dynamically added input fields with padding
Entries_Scrollable_Frame = tk.Frame(Entries_Canvas)

# Configure the scrollbar.
Entries_Scrollable_Frame.bind("<Configure>", lambda e: Entries_Canvas.configure(scrollregion=Entries_Canvas.bbox("all")))  # Update scroll region.
Entries_Canvas.create_window((0, 0), window=Entries_Scrollable_Frame, anchor='nw')  # Place the frame in the canvas.

# Pack the canvas and scrollbar.
Entries_Canvas.pack(side='left', fill='both', expand=True, padx=10, pady=5)  # Pack canvas.
Entries_Scrollbar.pack(side='right', fill='y')  # Pack scrollbar.

# Frame to hold all dynamically added input fields with padding.
Input_Frame = tk.Frame(Entries_Scrollable_Frame, padx=300)  # Use the scrollable frame for input entries and add padx.
Input_Frame.pack(fill='x')  # Pack the input frame with fill='x' to expand horizontally.

Input_Entries = []  # List to store dynamically added input fields.

# Initial input fields.
Add_New_Input_With_Remove(Input_Frame, Input_Entries)  # Add initial input fields.

# Frame to hold the buttons at the bottom.
Add_Frame = tk.Frame(Main_Window)
Add_Frame.pack(side='top', pady=10)  # Pack the button frame at the bottom.

# Button to add new input fields dynamically.
Add_Input_Button = tk.Button(Main_Window, text = "+", command = lambda: Add_New_Input_With_Remove(Input_Frame, Input_Entries), width=10, height=2)
Add_Input_Button.pack(in_=Add_Frame, side='left', padx=35, pady=10)  # Place the add input button inside the button frame.

# Frame to hold the buttons at the bottom.
Accept_Frame = tk.Frame(Entries_Scrollable_Frame)
Accept_Frame.pack(side='bottom', padx=50, pady=10)  # Pack the button frame at the bottom.

# Button to accept inputs and create the checklist window.
Accept_Button = tk.Button(Main_Window, text = "Accept", command = lambda: Collect_Inputs(Input_Entries), width=10, height=2)
Accept_Button.pack(in_=Accept_Frame, side='left', padx=50, pady=5)  # Place the accept button inside the button frame.

Main_Window.mainloop()
