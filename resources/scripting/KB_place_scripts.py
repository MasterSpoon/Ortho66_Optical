#exec(open('C:/<path>/Ortho66_Optical/resources/scripting/KB_place_scripts.py').read())

#Based on scripts by Alan Samet https://github.com/AlanSamet/KiCadExtensions/blob/master/Scripts/PlaceComponents.py
#
#This is a handful of useful scripts that I wrote for placing components in pcbnew. It is important to note that the Edit >> Undo menu command doesn't
#seem to add these steps to the undo buffer, so you'll probably want to save your PCB before experimenting with this. 

import pcbnew
import re
pcb = pcbnew.GetBoard()

def mm_to_nm(v):
    return int(v * 1000000)

def get_component(name):
    return pcb.FindFootprintByReference(name)

def place_component_relative_mm(reference_component_name, component_to_move, relative_x, relative_y, suppress_refresh = False):
    a = get_component(reference_component_name)
    b = get_component(component_to_move)

    pos_a = a.GetPosition()
    b.SetPosition(pcbnew.wxPoint(pos_a[0] + mm_to_nm(relative_x), pos_a[1] + mm_to_nm(relative_y)))
    if not suppress_refresh:
        pcbnew.Refresh()

def place_component_orientation(component_to_move, orientation, suppress_refresh = False):
    a = get_component(component_to_move)

    a.SetOrientation(orientation)
    if not suppress_refresh:
        pcbnew.Refresh()

#place_components_relative_mm('SW1 SW2 SW3'.split(), 19.05, 0)
def place_components_relative_mm(components_list, relative_x, relative_y, suppress_refresh = False):
    for i in range(len(components_list) - 1):
        place_component_relative_mm(components_list[i], components_list[i+1], relative_x, relative_y, True)
    if not suppress_refresh:
        pcbnew.Refresh()

def place_switches(reference_switch, last_switch, suppress_refresh = False):
    for i in range(reference_switch, last_switch):
        place_component_relative_mm( f"SW{i}", f"SW{i+1}", 19.05, 0, True)
    if not suppress_refresh:
        pcbnew.Refresh()
		
def place_comp_list(comp_to_move, first, last, x_off, y_off, suppress_refresh = False):
    for i in range(first, last):
        place_component_relative_mm( f"{comp_to_move}{i}", f"{comp_to_move}{i+1}", x_off, y_off, True)
    if not suppress_refresh:
        pcbnew.Refresh()

def place_comp_orient(comp_to_move, first, last, orientation, suppress_refresh = False):
    for i in range(first, last+1):
        place_component_orientation( f"{comp_to_move}{i}", orientation, True)
    if not suppress_refresh:
        pcbnew.Refresh()

def place_aux_comp(ref_comp, comp_to_move, first, last, x_off, y_off, orientation, suppress_refresh = False):
    for i in range(first, last+1):
        place_component_relative_mm( f"{ref_comp}{i}", f"{comp_to_move}{i}", x_off, y_off, True)
        place_component_orientation( f"{comp_to_move}{i}", orientation, True)
    if not suppress_refresh:
        pcbnew.Refresh()

#For placing RGB, PT & IR for Keychron LP Optical keyboard switches
def place_kclp(first_switch, last_switch, suppress_refresh = False):
    for i in range(first_switch, last_switch+1):
        place_aux_comp("SW", "RGB", first_switch, last_switch, 0, -4.8, 1800, True)
        place_aux_comp("SW", "IR", first_switch, last_switch, -2.9, 3.75, -900, True)
        place_aux_comp("SW", "PT", first_switch, last_switch, 1.7, 3.75, 900, True)
    if not suppress_refresh:
        pcbnew.Refresh()
