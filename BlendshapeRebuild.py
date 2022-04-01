## Selecionar mesh e clicar no botao ##

import maya.cmds as cmds
import pymel.core as pm

selection = cmds.ls(sl=True)                         #load da seleçao para uma lista
history = cmds.listHistory( selection )              #history da selecao para uma lista
blendshapeList = pm.ls(history,type="blendShape")    #nodes de blendshape dentro da history da mesh
groupList = []                                        #lista vazia
groupname = blendshapeList[0]+"_Rebuild"              #nome para o grupo = nome do primeiro item na lista das blendshapes da mesh + _Rebuild à frente

for bs in blendshapeList:                            #para cada node blendshape na lista fazer as cenas abaixo
    
    for bsTarget in bs.w:                            #para cada target dentro da node blendshape fazer cenas abaixo
        shapeName = bsTarget.getAlias()                #ir buscar nome 
        bsTarget.set(0)                                #valor a 0
        bsTarget.set(1)                                #valor a 1
        cmds.select(selection,r=True)                            #selecionar mesh original
        duplicate = cmds.duplicate(rr=True, name=shapeName)      #duplicate e por o nome do target
        groupList.append(duplicate[0])                            #adicionar esta mesh à lista groupList
        bsTarget.set(0)                                    #valor a 0
        
cmds.group(groupList,name=str(groupname))        #criar um grupo com tudo o que está dentro da groupList e dar nome
pm.select(str(groupname),hi=True)                #selecionar grupo + children
for obj in pm.ls(sl=True):                       #para cada object no grupo
    newname = obj.nodeName().replace("1","")     #definir novo nome, nome antigo menos o 1
    cmds.rename(str(obj),str(newname))           #rename para o nome novo
