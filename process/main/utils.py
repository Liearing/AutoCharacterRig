from maya import cmds
import maya.api.OpenMaya as om2
import maya.mel as mel

'''
Fonctions utiles pour d'autres processus 
'''


def parent_matrix_constraint(parent, child):

            parent_matrix = om2.MMatrix(cmds.getAttr(f'{parent}.worldMatrix[0]'))
            child_matrix = om2.MMatrix(cmds.getAttr(f'{child}.worldMatrix[0]'))

            cmds.setAttr(f'{child}.jointOrient', 0, 0, 0)

            offset_matrix = om2.MTransformationMatrix(child_matrix * parent_matrix.inverse()).asMatrix()
    
            mult_matrix_node = cmds.createNode("multMatrix", name = f'{parent}_to_{child}_mult')
            decompose_matrix_node = cmds.createNode("decomposeMatrix", name = f'{parent}_to_{child}_decomposeMatrix')
    
            cmds.setAttr(f'{mult_matrix_node}.matrixIn[0]', offset_matrix, type='matrix')
            cmds.connectAttr(f'{parent}.worldMatrix[0]', f'{mult_matrix_node}.matrixIn[1]')
            cmds.connectAttr(f'{child}.parentInverseMatrix[0]', f'{mult_matrix_node}.matrixIn[2]')
    
            cmds.connectAttr(f'{mult_matrix_node}.matrixSum', f'{decompose_matrix_node}.inputMatrix')
    
            cmds.connectAttr(f'{decompose_matrix_node}.outputTranslate', f'{child}.translate')
            cmds.connectAttr(f'{decompose_matrix_node}.outputRotate', f'{child}.rotate')
            cmds.connectAttr(f'{decompose_matrix_node}.outputScale', f'{child}.scale')