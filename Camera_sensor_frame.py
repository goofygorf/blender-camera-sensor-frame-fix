# Camera_sensor_frame - David Spencer - 3/14/21
# Creates an Image Plane Empty on the selected camera
# to function as a temporary Sensor Frame, since Blender v2.90+ is broken
# Empty frame is locked to camera and driven by focal length and sensor w/h
 
# Usage == Select camera first, then run script
# To display a background image in the Sensor Frame, the image MUST be the same
# aspect ratio as the camera's chosen Sensor Size.  Set the Sensor Frame scale X,Y
# to 1.0 . This will break the driver that resizes the Sensor Frame, so do it only 
# after you have set the correct camera sensor size.
# Then set the Sensor Frame Size to the Sensor width/100. 
# Then import your background image.


import bpy
  # provide a generic name for the new sensor_frame empty
sensor_name = "Sensor Frame"
  # camera must be manually selected to begin construction, must be first or only selected object
selected = bpy.context.selected_objects
try:
    cam = selected[0]
    
except IndexError:
    print("no valid camera selection")
    raise Exception()
# need to perform a selection check for empty selection, and for proper camera selection

  # create a new Empty Image type
snsr_frm = bpy.data.objects.new(name=sensor_name, object_data=None)
snsr_frm.empty_display_type ='IMAGE'
  # add the empty to the current active view layer
view_layer = bpy.context.view_layer
view_layer.active_layer_collection.collection.objects.link(snsr_frm)
  # parent the empty to the selected camera
snsr_frm.parent = cam

# -----------

 # Sensor Frame location.z (depth) Driver setup - 
driver = bpy.data.objects[snsr_frm.name].driver_add("location", 2).driver
driver.expression = "-focal_length/100" 

  # Sensor Frame distance from camera variable
var = driver.variables.new()
var.name = "focal_length"  
var.type = 'SINGLE_PROP'
var.targets[0].id_type = 'CAMERA'
var.targets[0].id = bpy.data.cameras[cam.name]
var.targets[0].data_path = "lens"


 # Sensor Frame Scale.x (width) Driver setup - 
driver = bpy.data.objects[snsr_frm.name].driver_add("scale", 0).driver
driver.expression = "sw/100" 

  # Sensor Frame distance from camera variable
var = driver.variables.new()
var.name = "sw"  
var.type = 'SINGLE_PROP'
var.targets[0].id_type = 'CAMERA'
var.targets[0].id = bpy.data.cameras[cam.name]
var.targets[0].data_path = "sensor_width"


 # Sensor Frame Scale.y (height) Driver setup - 
driver = bpy.data.objects[snsr_frm.name].driver_add("scale", 1).driver
driver.expression = "sh/100" 

  # Sensor Frame distance from camera variable
var = driver.variables.new()
var.name = "sh"  
var.type = 'SINGLE_PROP'
var.targets[0].id_type = 'CAMERA'
var.targets[0].id = bpy.data.cameras[cam.name]
var.targets[0].data_path = "sensor_height"

########################

# Lock all unused channels, and constrain channels to useable range
  # lock sensor frame trans x,y , rot x,y , scale x,y,z
snsr_frm.lock_location = (True, True, False)
snsr_frm.lock_rotation = (True, True, True)
snsr_frm.lock_scale = (False, False, True)
  # apply location constraints to sensor frame
snsr_frm.constraints.new(type='LIMIT_LOCATION')
snsr_frm.constraints["Limit Location"].use_min_x = True
snsr_frm.constraints["Limit Location"].use_max_x = True
snsr_frm.constraints["Limit Location"].use_min_y = True
snsr_frm.constraints["Limit Location"].use_max_y = True
snsr_frm.constraints["Limit Location"].use_max_z = True
snsr_frm.constraints["Limit Location"].max_z = -0.01
snsr_frm.constraints["Limit Location"].use_transform_limit = True
snsr_frm.constraints["Limit Location"].owner_space = 'LOCAL'
  # apply rotation constraints to sensor frame
snsr_frm.constraints.new(type='LIMIT_ROTATION')
snsr_frm.constraints["Limit Rotation"].use_limit_x = True
snsr_frm.constraints["Limit Rotation"].use_limit_y = True
snsr_frm.constraints["Limit Rotation"].use_limit_z = True
snsr_frm.constraints["Limit Rotation"].use_transform_limit = True
snsr_frm.constraints["Limit Rotation"].owner_space = 'LOCAL'
  # apply scale constraints to sensor frame
snsr_frm.constraints.new(type='LIMIT_SCALE')
snsr_frm.constraints["Limit Scale"].min_x = 0.0
snsr_frm.constraints["Limit Scale"].max_x = 10.0
snsr_frm.constraints["Limit Scale"].use_min_x = True
snsr_frm.constraints["Limit Scale"].use_max_x = True
snsr_frm.constraints["Limit Scale"].min_y = 0.0
snsr_frm.constraints["Limit Scale"].max_y = 10.0
snsr_frm.constraints["Limit Scale"].use_min_y = True
snsr_frm.constraints["Limit Scale"].use_max_y = True
snsr_frm.constraints["Limit Scale"].min_z = 1.0
snsr_frm.constraints["Limit Scale"].max_z = 1.0
snsr_frm.constraints["Limit Scale"].use_min_z = True
snsr_frm.constraints["Limit Scale"].use_max_z = True
snsr_frm.constraints["Limit Scale"].use_transform_limit = True
snsr_frm.constraints["Limit Scale"].owner_space = 'LOCAL'

  # deselect the camera and make the new Sensor Frame the active object
bpy.ops.object.select_all(action='DESELECT')
snsr_frm.select_set(state = True)
