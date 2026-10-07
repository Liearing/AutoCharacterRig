from maya import cmds 
import maya.api.OpenMaya as om2
import maya.mel as mel

from .utils import parent_matrix_constraint



# Encapsule les fonctions affectant le rig en fonction des inputs utilisateurs

class fk_build_rig():

    def __init__(self):
        '''
        Initialize a list for futher uses
        '''
        self.joint_list = []
        
    def retrieve_joint_list(self):
        '''
        Retrieve a joint list from selection
        '''
        self.joint_list = cmds.ls(selection = True ) or []
        return self.joint_list
    
    def create_fk_rig(self, *args):
        '''
        Create a FK rig using bone position and rotation, creating too a clean an proper hierarchy of controlers
        '''
        joints = self.joint_list

        for rig_joint in joints:

            current_ctrl = cmds.circle(normal=(1, 0, 0), center=(0, 0, 0), constructionHistory = False, name=f'{rig_joint}_ctrl')[0]
            delimiter = ""
            current_ctrl = delimiter.join(current_ctrl)

            current_grp = cmds.group(current_ctrl, name = f'{rig_joint}_ctrl_grp')

            joint_world = cmds.xform(rig_joint, query=True, matrix=True, worldSpace=True)
            cmds.xform(current_grp, matrix=joint_world, worldSpace=True)

            parent_matrix_constraint(current_ctrl, rig_joint)

           
        for current_joint in joints:
            print(f'Current joint is : {current_joint}')
            hierachy_child = cmds.listRelatives(current_joint, type = 'joint')

            if not hierachy_child:
                print(f'Current bone is end bone')
                previous_bone = cmds.listRelatives(current_joint, type = 'joint', parent = True)
                cmds.parent(f'{current_joint}_ctrl_grp' , f'{previous_bone[0]}_ctrl')

            else:
            
                for found_child in hierachy_child:
                    print(f'hierachy_child is : {hierachy_child}')
                    cmds.parent(f'{found_child}_ctrl_grp', f'{current_joint}_ctrl')


class ik_build_rig():

    def __init__(self):
        self.ik_list = {}


    def add_ik(self):
            
            ik_sel = cmds.ls(selection = True) # Selection des joints actuels
            index = len(self.ik_list) # Longueur du dictionnaire
            self.ik_list[f'ik_{index}'] = ik_sel # Crée une entrée dans le dictionnaire 
            print(self.ik_list)
            return self.ik_list

        
    def build_ik(self):

        print(self.ik_list)
        for key_ik, object_ik in self.ik_list.items():

            print(f'{key_ik}_{object_ik}')
            cmds.ikHandle( n=f'Ik_arm_{key_ik}', sj=object_ik[0], ee=object_ik[-1])

