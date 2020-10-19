__doc__="This addin calculates total volume of Structural Columns/Framing/Floors/Walls which are visible in Active view"
__title__="Total\nVolume" #Title of the extension
__author__ = "Shahabaz Sha"

from pyrevit import revit, DB, UI
from pyrevit import forms
 
 # make sure active view is not a sheet
curview = revit.activeview
if isinstance(curview, DB.ViewSheet):
    forms.alert("You're on a Sheet. Activate a model view please.",
                exitscript=True)
                
 # Creating a dictionary
options = {'Structural Columns': DB.BuiltInCategory.OST_StructuralColumns,
    'Walls': DB.BuiltInCategory.OST_Walls,
    'Structural Framing': DB.BuiltInCategory.OST_StructuralFraming,
    'Floors': DB.BuiltInCategory.OST_Floors,
    'Foundation':DB.BuiltInCategory.OST_StructuralFoundation
}

try:
    selected_switch = \
        forms.CommandSwitchWindow.show(sorted(options.keys()),
                                    message='Select volume of category:')

    curview = revit.activeview
    if selected_switch:
        target = options[selected_switch]
        
        target_elements = DB.FilteredElementCollector(revit.doc, curview.Id)\
                .OfCategory(target)\
                .WhereElementIsNotElementType()\
                .ToElements()
        
        total_volume = 0.0
        for ele in target_elements:
            vol_para=ele.Parameter[DB.BuiltInParameter.HOST_VOLUME_COMPUTED]
            if vol_para:
                total_volume+=vol_para.AsDouble()

    total_volume = total_volume*0.3048*0.3048*0.3048
    print("Total Volume of {0} is {1} m3".format(selected_switch, total_volume))
except: # exception to deal with user exiting the application
    pass 