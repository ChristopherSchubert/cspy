import bpy
import cspy
import math, mathutils

from mathutils import Matrix, Vector

EDIT_MODE_CHECK = 'EDIT_ARMATURE'
EDIT_MODE_SET = 'EDIT'
POSE_MODE_SET = 'POSE'

def enter_edit_mode():
    return bpy.context.mode != EDIT_MODE_CHECK
def exit_edit_mode(entered):
    return entered and bpy.context.mode == EDIT_MODE_CHECK

def set_bone_parenting(obj, bone_name, parent_name, use_connect):    
    entered = False
    if enter_edit_mode():
        entered = True
        active, mode = cspy.utils.enter_mode(obj, EDIT_MODE_SET)

    edit_bones = obj.data.edit_bones
    bone = edit_bones[bone_name]
    if parent_name in edit_bones:
        bone.parent = edit_bones[parent_name]
    
    bone.use_connect = use_connect
    
    if exit_edit_mode(entered):
        cspy.utils.exit_mode(active, mode)


def is_bone_in_layer(obj, bone_name, index):
    if not bone_name in obj.data.bones:
        return False
        
    bone = obj.data.bones[bone_name]
    return bone.layers[index]


def set_bone_layer(obj, bone_name, index, value):
    if not bone_name in obj.data.bones:
        return
        
    obj.data.bones[bone_name].layers[index] = value


def remove_bones_startwith(obj, prefix):
    if not bone_name in obj.data.bones:
        return
        
    entered = False
    if enter_edit_mode():
        entered = True
        active, mode = cspy.utils.enter_mode(obj, EDIT_MODE_SET)

    edit_bones = obj.data.edit_bones

    removing = []

    for edit_bone in edit_bones:
        if edit_bone.name.startswith(prefix):
            removing.append(edit_bone)
    
    for edit_bone in remove:
        edit_bones.remove(edit_bone)    
    
    if exit_edit_mode(entered):
        cspy.utils.exit_mode(active, mode)


def remove_bones(obj, bone_names):
    if not bone_name in obj.data.bones:
        return
        
    entered = False
    if enter_edit_mode():
        entered = True
        active, mode = cspy.utils.enter_mode(obj, EDIT_MODE_SET)

    edit_bones = obj.data.edit_bones

    for bone_name in bone_names:
        bone = edit_bones[bone_name]
        edit_bones.remove(bone)    
    
    if exit_edit_mode(entered):
        cspy.utils.exit_mode(active, mode)

def remove_bone(obj, bone_name):
    if not bone_name in obj.data.bones:
        return
        
    entered = False
    if enter_edit_mode():
        entered = True
        active, mode = cspy.utils.enter_mode(obj, EDIT_MODE_SET)

    edit_bones = obj.data.edit_bones
    bone = edit_bones[bone_name]
    edit_bones.remove(bone)    
    
    if exit_edit_mode(entered):
        cspy.utils.exit_mode(active, mode)


def get_pose_bone(obj, bone_name):
    if bone_name in obj.data.bones:
        return obj.pose.bones[bone_name]

    return None

def get_bone_and_pose_bone(obj, bone_name):
    if bone_name in obj.data.bones:
        return obj.data.bones[bone_name], obj.pose.bones[bone_name]

    return None, None

def create_or_get_bone(obj, bone_name):    
    if bone_name in obj.data.bones:
        return obj.data.bones[bone_name]

    entered = False
    if enter_edit_mode():
        entered = True
        active, mode = cspy.utils.enter_mode(obj, EDIT_MODE_SET)

    edit_bones = obj.data.edit_bones
    ebone = edit_bones.new(bone_name)
    ebone.tail = Vector([0.0, 0.0, 1.0])
    
    if exit_edit_mode(entered):
        cspy.utils.exit_mode(active, mode)
        return obj.data.bones[bone_name]
    
    return ebone


def shift_bones(obj, matrix):
    entered = False
    if enter_edit_mode():
        entered = True
        active, mode = cspy.utils.enter_mode(obj, EDIT_MODE_SET)

    edit_bones = obj.data.edit_bones

    for bone in edit_bones:
        if not bone.use_connect:
            bone.head = matrix @ bone.head

        bone.tail = matrix @ bone.tail
    
    if exit_edit_mode(entered):
        cspy.utils.exit_mode(active, mode)


def set_local_head_tail(obj, bone_name, head, tail): 
    entered = False
    if enter_edit_mode():
        entered = True
        active, mode = cspy.utils.enter_mode(obj, EDIT_MODE_SET)

    edit_bones = obj.data.edit_bones
    bone = edit_bones[bone_name]

    bone.head = head
    bone.tail = tail
    bone.roll = 0
    
    if exit_edit_mode(entered):
        cspy.utils.exit_mode(active, mode)

def set_local_tail(obj, bone_name, tail): 
    entered = False
    if enter_edit_mode():
        entered = True
        active, mode = cspy.utils.enter_mode(obj, EDIT_MODE_SET)

    edit_bones = obj.data.edit_bones
    bone = edit_bones[bone_name]

    bone.tail = tail
    
    if exit_edit_mode(entered):
        cspy.utils.exit_mode(active, mode)

def set_edit_bone_matrix_by_object(obj, bone_name, target_object, bone_length = 1.0): 
    entered = False
    if enter_edit_mode():
        entered = True
        active, mode = cspy.utils.enter_mode(obj, EDIT_MODE_SET)
    
    set_edit_bone_matrix(obj, bone_name, target_object.matrix_local, bone_length)

    if exit_edit_mode(entered):
        cspy.utils.exit_mode(active, mode)


def set_edit_bone_matrix(obj, bone_name, matrix, bone_length = 1.0): 
    entered = False
    if enter_edit_mode():
        entered = True
        active, mode = cspy.utils.enter_mode(obj, EDIT_MODE_SET)

    edit_bones = obj.data.edit_bones
    bone = edit_bones[bone_name]
    bone.matrix = matrix
    bone.length = bone_length
    
    if exit_edit_mode(entered):
        cspy.utils.exit_mode(active, mode)

def set_edit_bone_matrix_world(obj, bone_name, matrix): 
    entered = False
    if enter_edit_mode():
        entered = True
        active, mode = cspy.utils.enter_mode(obj, EDIT_MODE_SET)

    edit_bones = obj.data.edit_bones
    bone = edit_bones[bone_name]
    bone.matrix = obj.matrix_world.inverted() @ matrix
    
    if exit_edit_mode(entered):
        cspy.utils.exit_mode(active, mode)

def set_world_tail(obj, bone_name, tail): 
    entered = False
    if enter_edit_mode():
        entered = True
        active, mode = cspy.utils.enter_mode(obj, EDIT_MODE_SET)

    edit_bones = obj.data.edit_bones
    bone = edit_bones[bone_name]
    matrix = obj.matrix_world

    bone.tail = matrix.inverted() @ tail
    
    if exit_edit_mode(entered):
        cspy.utils.exit_mode(active, mode)

def set_world_head_tail(obj, bone_name, head, tail): 
    entered = False
    if enter_edit_mode():
        entered = True
        active, mode = cspy.utils.enter_mode(obj, EDIT_MODE_SET)

    edit_bones = obj.data.edit_bones
    bone = edit_bones[bone_name]
    matrix = obj.matrix_world

    bone.head = matrix.inverted() @ head
    bone.tail = matrix.inverted() @ tail
    bone.roll = 0
    
    if exit_edit_mode(entered):
        cspy.utils.exit_mode(active, mode)

def set_world_head_tail_xaxis(obj, bone_name, head, tail, x_axis):
    
    entered = False
    if enter_edit_mode():
        entered = True
        active, mode = cspy.utils.enter_mode(obj, EDIT_MODE_SET)

    edit_bones = obj.data.edit_bones
    bone = edit_bones[bone_name]
    matrix = obj.matrix_world

    bone.head = matrix.inverted() @ head
    bone.tail = matrix.inverted() @ tail
    cspy.bones.align_bone_x_axis(bone, x_axis)
    
    if exit_edit_mode(entered):
        cspy.utils.exit_mode(active, mode)


def get_world_head_tail(obj, bone_name):
    
    entered = False
    if enter_edit_mode():
        entered = True
        active, mode = cspy.utils.enter_mode(obj, EDIT_MODE_SET)

    edit_bones = obj.data.edit_bones
    bone = edit_bones[bone_name]

    matrix = obj.matrix_world
    head = matrix @ bone.head
    tail = matrix @ bone.tail
    x_axis = matrix @ bone.x_axis
    
    if exit_edit_mode(entered):
        cspy.utils.exit_mode(active, mode)

    return matrix, head, tail, x_axis

def are_bones_same_values(obj, bone, obj2, bone2):
    
    h = obj.matrix_world @ bone.bone.matrix_local @ bone.bone.head
    t = obj.matrix_world @ bone.bone.matrix_local @ bone.bone.tail
    x = bone.x_axis
    y = bone.y_axis
    z = bone.z_axis

    h2 = obj2.matrix_world @ bone2.bone.matrix_local @ bone.head
    t2 = obj2.matrix_world @ bone2.bone.matrix_local @ bone2.bone.tail
    x2 = bone2.x_axis
    y2 = bone2.y_axis
    z2 = bone2.z_axis

    #print(h, t, x)
    #print(h2, t2, x2)

    return (h == h2 and t == t2 and x == x2 and y == y2 and z == z2)


def get_edit_bone_data_dict(obj):
    entered = False
    if enter_edit_mode():
        entered = True
        active, mode = cspy.utils.enter_mode(obj, EDIT_MODE_SET)

    edit_bones = obj.data.edit_bones
    edit_bone_dict = {}

    for bone in edit_bones:
        edit_bone_dict[bone.name] = (bone.head.copy(), bone.tail.copy(), bone.roll, bone.use_connect)
    
    if exit_edit_mode(entered):
        cspy.utils.exit_mode(active, mode)

    return edit_bone_dict

def get_edit_bone_matrices(obj):   

    active, mode = cspy.utils.enter_mode(obj, EDIT_MODE_SET) 
        
    bone_matrices = {}

    for bone in obj.data.edit_bones:
        bone_matrices[bone.name] = bone.matrix.copy()

    cspy.utils.exit_mode(active, mode)

    return bone_matrices

def get_pose_bone_matrices(obj):   

    active, mode = cspy.utils.enter_mode(obj, POSE_MODE_SET) 
        
    bone_matrices = {}

    for bone in obj.pose.bones:
        bone_matrices[bone.name] = bone.matrix.copy()

    cspy.utils.exit_mode(active, mode)

    return bone_matrices

def align_bone_x_axis(edit_bone, new_x_axis):
    """ new_x_axis is a 3D Vector the edit_bone's x-axis will point towards.
    """
    new_x_axis = new_x_axis.cross(edit_bone.y_axis)
    new_x_axis.normalize()
    dot = max(-1.0, min(1.0, edit_bone.z_axis.dot(new_x_axis)))
    angle = math.acos(dot)
    edit_bone.roll += angle
    dot1 = edit_bone.z_axis.dot(new_x_axis)
    edit_bone.roll -= angle * 2.0
    dot2 = edit_bone.z_axis.dot(new_x_axis)
    if dot1 > dot2:
        edit_bone.roll += angle * 2.0


 