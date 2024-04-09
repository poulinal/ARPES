import dearpygui.dearpygui as dpg

def send_rixs_command(sender, app_data):
    print("START RIXS command sent")

with dpg.texture_registry():
    texture = dpg.load_texture("../static/dearpygui_icon.png")

with dpg.window(label="DeLTA Lab RIXS GUI", width=800, height=600):
    dpg.add_image(texture.id, width=100, height=100)
    dpg.add_text("Parameters")
    
    with dpg.child(width=380, height=200):
        dpg.add_input_text(label="Valence Orbitals", width=150)
        dpg.add_input_text(label="Active Core", width=150)
        dpg.add_input_int(label="Valence Occupancy", width=150)
        dpg.add_input_float(label="Hund's", width=150)
        dpg.add_input_float(label="Jh", width=150)
        dpg.add_input_float(label="Spin-Orbit-Coupling", width=150)
        
    dpg.add_text("X-Ray Transition")
    
    with dpg.child(width=380, height=100):
        atom_dropdown = dpg.add_combo(label="Atom", items=["Option 1", "Option 2", "Option 3"], width=150)
        shell_dropdown = dpg.add_combo(label="Shell", items=["Option 1", "Option 2", "Option 3"], width=150)
        
    dpg.add_button(label="START RIXS", callback=send_rixs_command, width=150)
    
    dpg.add_text("RIXS Output")
    
    with dpg.child(width=380, height=200):
        dpg.add_text("Summary of Slater integrals:")
        
    with dpg.child(width=380, height=200):
        dpg.add_plot(label="Plots")
        dpg.add_checkbox(label="Export Chart", default_value=True)
        
dpg.create_context()
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
