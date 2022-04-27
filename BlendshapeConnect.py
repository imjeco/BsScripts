#Selecionar mesh e clicar no botao, controlador tem de se chamar CC_BlendShapes, só precisa dos attributes das shapes base

import maya.cmds as cmds
import pymel.core as pm

selection = cmds.ls(sl=True)                         #mesh selecionado
history = cmds.listHistory( selection )             #ver history da mesh
blendshapes = pm.ls(history,type="blendShape")     #escolher node blendshape da history da mesh
targetsList = blendshapes[0].listAliases()            #Lista dos targets em tuples [(alias+attribute),(alias+attribute) ]
list_of_names = [l[0] for l in targetsList]          #Lista dos targets, só nome ['shape1', 'shape2', 'combo_shape1_x_shape2']
list_of_attributes = [l[1] for l in targetsList]      #Lista dos targets, só attribute ['blendShape1.weight[0]', 'blendShape1.weight[1]', ...]
cc = pm.PyNode('CC_BlendShapes')                 #Definir controlador
comboList = []
BSnode = blendshapes[0]

def filterString(name):                        #function para filtrar tudo o que tem combo no nome
   if 'combo' in name:
      return True
   else:
      return False

filteredList=filter(filterString,list_of_names)

for name in filteredList:                            #adicionar à lista comboList
   comboList.append(name)

for bs in blendshapes:                               #ligar por nome ao controlador
    for target in bs.w:
        shapeName = target.getAlias()
        if cc.hasAttr(shapeName):
            ccAttr = cc.attr(shapeName)
            try:
                ccAttr.connect(target, force=True)
            except:
                continue
                                                
# buscar index do nome/attribute
#shape_idx = list_of_names.index(shape_name)
#shape_attribute = list_of_attributes[shape_idx]
   
for c in comboList:  
    comboNode = pm.createNode("combinationShape", n=BSnode+"_"+c)
    y = c.split("_")                                    #Separar string por _ e por numa lista
    comboSplit = y[1::2]                                #Selecionar alternadamente itens da lista, para excluir "combo_ e _x_
    for l in comboSplit:
            shape_idx = list_of_names.index(l)
            shape_attribute = list_of_attributes[shape_idx]
            combo_Attr = comboNode.inputWeight[shape_idx]
            shape_attribute.connect(combo_Attr, force=True)
            combo_index = list_of_names.index(c)
            combo_cc = comboNode.outputWeight
            combo_cc.connect("{0}.{1}".format(BSnode,str(c)), force=True)
           
#### LIGAR IN-BETWEENS
IBList = []

def filterStringIB(name):                        #function para filtrar tudo o que tem IB no nome
   if 'IB' in name:
      return True
   else:
      return False
      
filteredListIB=filter(filterStringIB,list_of_names)

for name in filteredListIB:                            #adicionar à lista comboList
   IBList.append(name)
           
for IB in IBList:  
    y = IB.split("_")                                   
    IBSplit = y[-2:]
    FirstTerm = IBSplit[0]
    IB_Value = '.'.join(IBSplit[1][i:i + 1] for i in range(0, len(IBSplit[1]), 1))                           
    IBNode = cmds.createNode("remapValue",n=BSnode+"_"+IB)
    cmds.setAttr(IBNode + ".value[1].value_FloatValue", 0)
    cmds.setAttr(IBNode + ".value[3].value_FloatValue", 1)
    cmds.setAttr(IBNode + ".value[3].value_Position", float(IB_Value))
    cmds.setAttr(IBNode + ".value[3].value_Interp", 1)
    ccAttrIB = cc.attr(IBSplit[0])
    pm.connectAttr( '{0}'.format(ccAttrIB), '{0}.{1}'.format(IBNode,"inputValue"))
    shape_idx = list_of_names.index(IB)
    shape_attribute = list_of_attributes[shape_idx]
    pm.connectAttr( '{0}.{1}'.format(IBNode,"outValue"), '{0}'.format(shape_attribute))

        
cmds.listAttr("BS_Cara_IB_eyeBlinkLeft_05")
            
       
