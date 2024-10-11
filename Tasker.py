import tkinter as tk

def Focus_Next_Widget(event: tk.Event) -> str:
    event.widget.tk_focusNext().focus()  # Cambiar el foco al siguiente widget.
    return "break"  # Detener el comportamiento predeterminado de TAB.

# Función para subrayar el texto y mover el checkbox al final al seleccionarlo.
def On_Checkbox_Select(Checkbox: tk.Checkbutton, Checkbox_Frame: tk.Frame, Checkbox_Variable: tk.IntVar) -> None:
    if Checkbox_Variable.get() == 1:  # Si está seleccionado.
        Checkbox.config(font=("Calibri Light", 16, "overstrike"))  # Subrayar el texto.
    else:
        Checkbox.config(font=("Calibri Light", 16))  # Quitar subrayado.

def Check_If_All_Selected(Window: tk.Toplevel, Checkbox_Variables: list[tk.IntVar]) -> None:
    if all(Checkbox_Variable.get() == 1 for Checkbox_Variable in Checkbox_Variables):
        Window.destroy()  # Close the window.

# Function that creates a new window with checkboxes from predefined input values.
def Create_Checklist_Window() -> None:
    Checklist_Window = tk.Tk()  # Create new main window (Checklist window).
    Checklist_Window.title("Ender")
    Checklist_Window.geometry("1200x500")
    Checklist_Window.geometry("+{}+{}".format(int(Checklist_Window.winfo_screenwidth() / 2 - 600), int(Checklist_Window.winfo_screenheight() / 2 - 250)))  # Center the window.

    Checklist_Window.attributes('-topmost', True)  # Keep the window on top.
    Checklist_Window.attributes('-toolwindow', True)  # Disable minimize.
    
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

    # Frame to hold the checkboxes with padding.
    Checkbox_Frame_Container = tk.Frame(Checklist_Scrollable_Frame)
    Checkbox_Frame_Container.pack(pady=10, padx=500, anchor='center')  # Center the checkboxes.

    Checkbox_Variables = []

    # Predefined inputs (texts) for the checkboxes.
    Inputs = ["Code",
              "Doce",
              "Read",
              "Write", 
              "Burn", 
              "Chess"]  
    
    # Create the checkboxes.
    for Input_Value in Inputs:
        Checkbox_Variable = tk.IntVar()
        Checkbox_Variables.append(Checkbox_Variable)

        # Create a frame for each checkbox.
        Checkbox_Frame = tk.Frame(Checkbox_Frame_Container)
        
        # Create the checkbox inside that frame.
        Checkbox = tk.Checkbutton(Checkbox_Frame, text=Input_Value, variable=Checkbox_Variable, font=("Calibri Light", 16), height=2)
        Checkbox.pack(anchor='w', pady=0)

        # Add the checkbox frame to the main container.
        Checkbox_Frame.pack(anchor='w', pady=0)

        # Link the checkbox to the function for moving and underlining.
        Checkbox.config(command=lambda cb=Checkbox, cf=Checkbox_Frame, cv=Checkbox_Variable: On_Checkbox_Select(cb, cf, cv))

    Accept_Button = tk.Button(Checkbox_Frame_Container, text="Check", command=lambda: Check_If_All_Selected(Checklist_Window, Checkbox_Variables), width=10, height=2)
    Accept_Button.pack(pady=40, side='bottom')

    Checklist_Window.mainloop()

    # Main loop to run the window.
    Checklist_Window.mainloop()

# Run the checklist window directly with predefined tasks.
Create_Checklist_Window()
