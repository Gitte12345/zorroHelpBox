# zorroHelpBox.py
import maya.cmds as cmds
import maya.mel as mel
from functools import partial  
# import thomas as tk

'''
Tools for zorro sim
---------------------------------------------------


'''
ver                 = '1.2'

colDarkGreen    = [0.1, 0.16, 0.08]
colFrame        = [0.3, 0.3, 0.3]
colFrameRed     = [0.4, 0.3, 0.3]
colDarkRed      = [0.32, 0.2, 0.14]
colFrameGreen   = [0.3, 0.4, 0.28]
colLightGreen   = [0.4, 0.5, 0.36]
colDark         = [0.1, 0.1, 0.1]
colRed         = [0.32, 0.2, 0.14]
colBrown        = [0.1, 0.16, 0.08]

defaultPath     = 'X:/zorro_zor-5069/_library/assets/characters/chr_zorroFox/cfx_groom/'
approvedxGen    = 'zor_chr_zorroFox_cfx_groom_v080_thk__body_collection'
xGenBaseGeo     = 'body_cn_hi_cfx'
dynControl       = 'dyn_GRP'

windowStartHeight   = 50
windowStartWidth    = 200
bh1                 = 24

def tkHelpSwitchInstancerInputs(*args):
    if cmds.window('win_tkSwitchInstancerINPUtsHELP', exists=1):
        cmds.deleteUI('win_tkSwitchInstancerINPUtsHELP')
    myWindow = cmds.window('win_tkSwitchInstancerINPUtsHELP', s=1, t='help', wh=[200, 200])
    helpText = 'Replace instanced references without changing order\n---------------------------------------------------\nInstancer:          Choose Instancer \nUses                   The namespace of the first connected    obj\nReplace With:   Select file you want to replace from\n                           Gets the namespace automatically'
    cmds.columnLayout(adj=1)
    cmds.text(helpText, al='left')
    cmds.showWindow(myWindow )



def cShrinkWin(windowToClose, *args):
    cmds.window(windowToClose, e=1, h=20)
    cmds.window(windowToClose, e=1, w=420)



def cLoadRef(nameSpace, *args):
    strVersion = ''
    version = cmds.intField('iFXVersion', v=1, q=1)
    if version < 100:
        strVersion = '0' + str(version)
    if version < 10:
        strVersion = '00' + str(version)
    if strVersion == '025':
        file = 'X:/zorro_zor-5069/_library/assets/characters/chr_zorroFox/cfx_cloth/_publish/zor_chr_zorroFox_cfx_cloth_v' + strVersion + '_jwo.mb'
    else:
        file = 'X:/zorro_zor-5069/_library/assets/characters/chr_zorroFox/cfx_cloth/_publish/zor_chr_zorroFox_cfx_cloth_v' + strVersion + '_thk.mb'

    cmds.file(file, r=1, type='mayaBinary', ignoreVersion=1, gl=1, mergeNamespacesOnClash=1, namespace='zor_01', options='v=0;')



def tk_linkAnimToCloth(action, *args):
    bs = []
    CLT = ['cape_cn_cfx_mid_geo_oneSided', 'shirt_cn_cfx_mid_geo_oneSided', 
        'cape_cn_cfx_hi_geo_oneSided', 'shirt_cn_cfx_hi_geo_oneSided', 
        'leatherSheath_cn_lo_geo', 'metalSheath_cn_lo_geo', 'beltBuckle_cn_lo_geo', 
        'belt_cn_lo_geo', 'beltSheathLong_cn_lo_geo', 'beltSheathWide_cn_lo_geo', 'furVolume_cn_mid_anim_geo',
        'hat_cn_lo_geo', 'visor_cn_lo_geo', 'knotTwo_cn_lo_geo', 'knotOne_cn_lo_geo', 'body_cn_hi_cfx']  
    failList = []
    fails = ''

    nmSpcAnim = cmds.textField('tfNmSpcAnim', tx=1, q=1)
    nmSpcFX = cmds.textField('tfNmSpcFX', tx=1, q=1)
    if nmSpcAnim:
        nmSpcAnim   = nmSpcAnim + ':'
        nmSpcFX     = nmSpcFX + ':'

    for i in CLT:
        if cmds.objExists(nmSpcFX + i) is False:
            failList.append(i)
        if cmds.objExists(nmSpcAnim + i) is False:
            failList.append(i)



    else:
        print '-------------------------'

        for clt in CLT:
            # print clt
            shapes = cmds.listRelatives(nmSpcFX + clt, s=1, ni=1)    
            print 'shapes:'
            print shapes
            
            # disconnect
            if action == 0: 
                if cmds.objExists('BS_' + clt):
                    print 'disconnecting ' + clt 
                    bs = cmds.listConnections(shapes[0], s=1, d=0, type='blendShape')
                    cmds.setAttr(bs[0] + '.' + clt, 0) 
                    cmds.delete(bs) 
            
            # connect
            if action == 1:
                if not cmds.objExists('BS_' + clt):
                    if cmds.objExists(nmSpcAnim + clt):
                        print 'connecting ' + clt
                        cmds.select(nmSpcAnim + clt, nmSpcFX + clt)
                        mel.eval('performBlendShape 0 1')

                        shapes = cmds.listRelatives(nmSpcFX + clt, s=1, ni=1)    

                        bs = cmds.listConnections(shapes[0], s=1, d=0, type='blendShape')

                        print '--> blendShape before:'
                        print bs
                        bs = cmds.rename(bs[0], 'BS_' + clt)
                        print '--> blendShape after:'
                        print bs
                        print '\n'
                        cmds.setAttr(bs + '.' + clt, 1)

                else:
                    print (clt + ' is already connected - disconnect first!')

        print '-------------------------'
        if action == 1 and len(failList) == 0:
            cClear('tfFeedback', 'Successfully linked anim to FX!', [0, 0.3, 0]) 

        if action == 1 and len(failList) > 0:
            print '-------------------------'
            print 'Missing objects:'
            for fail in failList:
                fails += fail + ' '
                print fail
            cClear('tfFeedback', ('Missing objects! Check ScriptEditor for details'), [.3, 0, 0])  
            print '-------------------------'

        if action == 0:
            cClear('tfFeedback', 'Successfully disconnected anim from FX!', [0, 0.3, 0]) 


def cGetNmSpc(field, *args):
    curSel = cmds.ls(sl=1)
    if curSel:
        if ':' in curSel[0]:
            cmds.textField(field, tx=curSel[0].split(':')[0], e=1)
        else:
            cmds.textField(field, tx='', e=1)
    else:
        cmds.textField(field, tx='', e=1)



def tkSetVisibility(object, *args):
    animGrp      = 'ANIM_GRP'
    animGrpHi    = 'ANIM_hi_GRP'
    wrapGrp      = 'wrap_GRP'
    collGrp      = 'passive_GRP'
    exClothGrp   = 'export_cloth_GRP'
    xGenBaseGrp  = 'xGenBase_GRP'
    nmSpc        = cmds.textField('tfNmSpcAnim', tx=1, q=1)
    nmSpcFX      = cmds.textField('tfNmSpcFX', tx=1, q=1)

    if nmSpc:
        nmSpc = nmSpc + ':'   
    if nmSpcFX:
        nmSpcFX = nmSpcFX + ':'

    if object is 'Anim':
        low     = cmds.checkBox('cbLow', v=1, q=1)
        mid     = cmds.checkBox('cbMid', v=1, q=1)
        hgh     = cmds.checkBox('cbHgh', v=1, q=1)
        but     = cmds.checkBox('cbButtons', v=1, q=1)  

        if cmds.objExists(nmSpc + 'furVolume_cn_mid_anim_geo') is False:
            cClear('tfFeedback', 'Objects not found! Check the namespace!', [.3, 0, 0])  

        else:
            dagList = cmds.ls(nmSpc + '*_lo_*', type='transform')
            for i in dagList:
                print i
                cmds.setAttr(i + '.v', low)

            dagList = cmds.ls(nmSpc + '*_mid_*', type='transform')
            for i in dagList:
                print i
                cmds.setAttr(i + '.v', mid)

            dagList = cmds.ls(nmSpc + '*_hi_*', type='transform')
            for i in dagList:
                print i
                cmds.setAttr(i + '.v', hgh)
            
            dagList = cmds.ls(nmSpc + '*button_*', type='transform')
            for i in dagList:
                print i
                cmds.setAttr(i + '.v', but)

    if object is 'FX':
        anim     = cmds.checkBox('cbAnimGRP', v=1, q=1)
        animHi   = cmds.checkBox('cbAnimHiGRP', v=1, q=1)
        coll     = cmds.checkBox('cbColliderGRP', v=1, q=1)
        wrap     = cmds.checkBox('cbWrapGRP', v=1, q=1)
        cape     = cmds.checkBox('cbCape', v=1, q=1)
        shirt    = cmds.checkBox('cbShirt', v=1, q=1)
        exCloth  = cmds.checkBox('cbExportClothGRP', v=1, q=1)
        xGenBase = cmds.checkBox('cbxGenBase', v=1, q=1)

        if cmds.objExists(nmSpcFX + collGrp) is False:
                    cClear('tfFeedback', 'Objects not found! Check the namespace!', [.3, 0, 0])  

        else:
            cmds.setAttr(nmSpcFX + collGrp + '.v', coll)
            children = cmds.listRelatives(nmSpcFX + collGrp, c=1, type = 'transform')
            for child in children:
                cmds.setAttr(child + '.v', coll)

            cmds.setAttr(nmSpcFX + animGrp + '.v', anim)
            children = cmds.listRelatives(nmSpcFX + animGrp, c=1, type = 'transform')
            for child in children:
                cmds.setAttr(child + '.v', anim)

            cmds.setAttr(nmSpcFX + animGrpHi + '.v', animHi)
            children = cmds.listRelatives(nmSpcFX + animGrpHi, c=1, type = 'transform')
            for child in children:
                cmds.setAttr(child + '.v', animHi)

            cmds.setAttr(nmSpcFX + wrapGrp + '.v', wrap)
            children = cmds.listRelatives(nmSpcFX + wrapGrp, c=1, type = 'transform')
            for child in children:
                cmds.setAttr(child + '.v', wrap)

            cmds.setAttr(nmSpcFX + exClothGrp + '.v', exCloth)
            children = cmds.listRelatives(nmSpcFX + exClothGrp, c=1, type = 'transform')
            for child in children:
                cmds.setAttr(child + '.v', exCloth)

            cmds.setAttr(nmSpcFX + xGenBaseGrp + '.v', xGenBase)
            children = cmds.listRelatives(nmSpcFX + xGenBaseGrp, c=1, type = 'transform')
            for child in children:
                cmds.setAttr(child + '.v', xGenBase)

            cmds.setAttr(nmSpcFX + dynControl + '.cape', cape)
            cmds.setAttr(nmSpcFX + dynControl + '.shirt', shirt)
            






def tkTglAll(object, *args):
    listFX    = ['cbAnimGRP', 'cbAnimHiGRP', 'cbColliderGRP', 'cbShirt', 'cbCape', 'cbWrapGRP', 'cbExportClothGRP', 'cbxGenBase']
    listAnim  = ['cbLow', 'cbMid', 'cbHgh', 'cbButtons']
    
    if object is 'FX':
        state = cmds.checkBox(listFX[0], v=1, q=1) -1
        for i in listFX:
            cmds.checkBox(i, v=state, e=1)

    if object is 'Anim':
        state = cmds.checkBox(listAnim[0], v=1, q=1) -1
        for i in listAnim:
            cmds.checkBox(i, v=state, e=1)



def cSelect(object, *args):
    nmSpcFX = cmds.textField('tfNmSpcFX', tx=1, q=1)
    if nmSpcFX:
        nmSpcFX = nmSpcFX + ':'

    if cmds.objExists(nmSpcFX + object) is False:
        cClear('tfFeedback', 'Objects not found! Check the namespace!', [.3, 0, 0])   
    
    else:
        cmds.select(nmSpcFX + object, r=1)




def cSelectForPlayblast(set, *args):
    startFrame = cmds.playbackOptions(min=1, q=1) 
    nmSpcFX = cmds.textField('tfNmSpcFX', tx=1, q=1)
    if nmSpcFX:
        nmSpcFX = nmSpcFX + ':'

    clothSetMid = ['passive_GRP', 'wrap_GRP', 'cape_cn_hi_geo_WRP', 'shirt_cn_hi_geo_WRP']

    clothxGenSetMid = [
        'leatherSheath_cn_lo_geo_SIM ', 'metalSheath_cn_lo_geo_SIM ', 'beltBuckle_cn_lo_geo_SIM ', 
        'belt_cn_lo_geo_SIM ', 'beltSheathLong_cn_lo_geo_SIM ', 'beltSheathWide_cn_lo_geo_SIM', 
        'export_cloth_GRP', 'cape_cn_hi_geo_EXP', 'shirt_cn_hi_geo_EXP']

    zorroMask = ['hat_cn_lo_geo', 'visor_cn_lo_geo', 'knotTwo_cn_lo_geo', 'knotOne_cn_lo_geo']

    collections = cmds.ls(type='xgmPalette')


    cmds.setAttr(nmSpcFX + 'nucleus1.startFrame', startFrame)

    if set == 'clothSetMid':
        cmds.select(clear=1)
        for obj in clothSetMid:
            cmds.setAttr(nmSpcFX + obj + '.v', 1)
            cmds.select(nmSpcFX + obj, add=1)

    if set == 'clothxGenSetMid':
        cmds.select(clear=1)
        for obj in clothxGenSetMid:
            cmds.setAttr(nmSpcFX + obj + '.v', 1)
            cmds.select(nmSpcFX + obj, add=1)
            if cmds.objExists('body_cn_hi_cfx'):
                cmds.select('body_cn_hi_cfx', add=1)
            if cmds.objExists('body_collection'):
                cmds.select('body_collection', add=1)

    if set == 'zorroMask':
        for obj in zorroMask:
            cmds.setAttr(nmSpcFX + obj + '.v', 1)
            cmds.select(nmSpcFX + obj, add=1)

        cmds.select(collections, add=1)







def cSelectSimELements(object, *args):
    CLT = []

    nmSpcFX = cmds.textField('tfNmSpcFX', tx=1, q=1)
    if nmSpcFX:
        nmSpcFX = nmSpcFX + ':'

    if cmds.objExists(nmSpcFX + 'shirt_cn_cfx_mid_geo_SIM') is False:            
                cClear('tfFeedback', 'Objects not found! Check the namespace!', [.3, 0, 0])  

    else:
        if (object == 'shirtMid'):
            CLT = ['shirt_cn_cfx_mid_geo_SIM']
            cmds.setAttr(nmSpcFX + dynControl + '.shirt', 1)

        if (object == 'capeMid'):
            CLT = ['cape_cn_cfx_mid_geo_SIM']
            cmds.setAttr(nmSpcFX + dynControl + '.cape', 1)
            cmds.checkBox('cbCape', v=1, e=1)

        if (object == 'bothMid'):
            CLT = ['cape_cn_cfx_mid_geo_SIM', 'shirt_cn_cfx_mid_geo_SIM']
            cmds.setAttr(nmSpcFX + dynControl + '.shirt', 1)
            cmds.setAttr(nmSpcFX + dynControl + '.cape', 1)
            cmds.checkBox('cbCape', v=1, e=1)
            cmds.checkBox('cbShirt', v=1, e=1)

        if (object == 'shirtHi'):
            CLT = ['shirt_cn_cfx_hi_geo_SIM']
            cmds.setAttr(nmSpcFX + dynControl + '.shirt', 2)
            cmds.checkBox('cbShirt', v=1, e=1)

        if (object == 'capeHi'):
            CLT = ['cape_cn_cfx_hi_geo_SIM']
            cmds.setAttr(nmSpcFX + dynControl + '.cape', 2)
            cmds.checkBox('cbCape', v=1, e=1)

        if (object == 'bothHi'):
            CLT = ['cape_cn_cfx_hi_geo_SIM', 'shirt_cn_cfx_hi_geo_SIM']
            cmds.setAttr(nmSpcFX + dynControl + '.shirt', 2)
            cmds.setAttr(nmSpcFX + dynControl + '.cape', 2)
            cmds.checkBox('cbCape', v=1, e=1)
            cmds.checkBox('cbShirt', v=1, e=1)

        if (object == 'none'):
            CLT = []
            cmds.setAttr(nmSpcFX + dynControl + '.shirt', 0)
            cmds.setAttr(nmSpcFX + dynControl + '.cape', 0)
            cmds.checkBox('cbCape', v=0, e=1)
            cmds.checkBox('cbShirt', v=0, e=1)





        cmds.select(clear=1)
        if nmSpcFX:
            nmSpcFX = nmSpcFX + ':'
            for clt in CLT:
                cmds.select(nmSpcFX + clt, add=1)

        else:
            cmds.select(CLT, r=1)



def cSelectFXAnimELements(*args):
    nmSpcFX = cmds.textField('tfNmSpcFX', tx=1, q=1)
    grp = 'ANIM_GRP'
    grpHi = 'ANIM_hi_GRP'
    if nmSpcFX:
        nmSpcFX = nmSpcFX + ':'

    if cmds.objExists(nmSpcFX + grp) is False:
                cClear('tfFeedback', 'Objects not found! Check the namespace!', [.3, 0, 0])  

    else:
        cmds.select(nmSpcFX + grp, r=1)
        cmds.select(nmSpcFX + grpHi, add=1)
        cmds.select(nmSpcFX + 'xGenBase_GRP', add=1)


def cExportAsABC(*args):
    mel.eval('AlembicExportSelectionOptions')



def cReferenceAnimABC(*args):
    mel.eval('projectViewer AlembicReference')
   


def cClothCache(*args):
    mel.eval('doCreateNclothCache 5 { "2", "1", "10", "OneFile", "1", "","0","","0", "0", "0", "1", "1","0","1","mcx" }') 



def cDeleteCache(*args):
    mel.eval('fluidDeleteCache')



def cWrapStatus(action, field, attribute, *args):
    nmSpcFX = cmds.textField('tfNmSpcFX', tx=1, q=1)
    if nmSpcFX:
        nmSpcFX = nmSpcFX + ':'

    if action == 'read':
        sl = cmds.getAttr(nmSpcFX + dynControl + '.' + attribute) +1
        # print sl
        cmds.radioButtonGrp(field, sl=sl, e=1)

    if action is 'set':
        sl = cmds.radioButtonGrp(field, sl=1, q=1) -1
        # print sl
        cmds.setAttr(nmSpcFX + dynControl + '.' + attribute, sl)
        
    # print '--------------'




def cGetPath(action, *args):
    defaultPath = "X:/zorro_zor-5069/_library/assets/characters/chr_zorroFox/cfx_groom/"

    if action == 'default':
        cmds.textField('tfPathxGen', tx=defaultPath, e=1)
        cmds.textField('xGenVersion', tx=approvedxGen, e=1)


    if action == 'choose':
        xGenPath = cmds.fileDialog2(fm=2, ds=1, dir=defaultPath, cap='Select Directory')
        cmds.textField('tfPathxGen', tx=xGenPath[0] + '/', e=1)
        files = cmds.getFileList(filespec = '*.xgen', fld=xGenPath[0])

        if files:
            if approvedxGen not in files:
               cmds.textField('xGenVersion', tx='Choose a xGen Collection!', e=1)

        else:
            cmds.textField('xGenVersion', tx='No xGen descriptions in that Folder!', e=1)




def cSelectxGenVersion(action, *args):
    xGenPath    = cmds.textField('tfPathxGen', tx=1, q=1)
    cmdAppend   = '['
    if xGenPath:
        files = cmds.getFileList(filespec = '*.xgen', fld=xGenPath)
        files = sorted(files)

        if (cmds.window('win_xGenList', exists=1)):
            cmds.deleteUI('win_xGenList')
        myVersionWindow = cmds.window('win_xGenList', t=('Fox xGen Versions'), s=1)

        cmds.columnLayout(adj=1)

        amount = len(files)
        if amount > 0:
            for i in range(0, amount-1, 1):
                name = files[i].split('.')[0]
                if i != amount-2:
                    cmdAppend += '"'
                    cmdAppend += name   
                    cmdAppend += '",'
                else:
                    cmdAppend += '"'
                    cmdAppend += name
                    cmdAppend += '"]'

            cmd1 = 'cmds.textScrollList("txGenVersion", numberOfRows=8, append= '
            cmd2 = ')'
            cmd = cmd1 + cmdAppend + cmd2

            cmds.paneLayout()
            exec(cmd)
            cmds.setParent('..')
            cmds.button(l='Pick Version', bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), c=partial(tfSelectxGenVersion))

            cmds.showWindow(myVersionWindow)
            cmds.window(myVersionWindow, e=1,h=120)

        else:
            cmds.textField('xGenVersion', tx='No xGen descriptions in that Folder!', e=1)



def tfSelectxGenVersion(*args):
    chosenVersion = cmds.textScrollList('txGenVersion', si=1, q=1)
    cmds.deleteUI('win_xGenList')
    cmds.textField('xGenVersion', tx=chosenVersion[0], e=1)



def cImportxGen(action, *args):
    path    = cmds.textField('tfPathxGen', tx=1, q=1)
    file    = cmds.textField('xGenVersion', tx=1, q=1)
    nmSpcFX = cmds.textField('tfNmSpcFX', tx=1, q=1) 
    
    if nmSpcFX:
        nmSpcFX = nmSpcFX + ':'

    if cmds.objExists(nmSpcFX + xGenBaseGeo):
        pass



def cFixNaming(baseGeo, *args):
    nmSpcFX = cmds.textField('tfNmSpcFX', tx=1, q=1)
    if nmSpcFX:
        nmSpcFX = nmSpcFX + ':'    

    # cmds.rename(nmSpc + 'body_cn_hi_cfxShape', 'body_cn_hi_cfxShapeStatic')
    cmds.rename('body_cn_hi_cfxShapeDeformed', 'body_cn_hi_cfxShape')






def cClear(field, text, color, *args):
    cmds.textField(field, tx=text, bgc=color, e=1)





def zorroHelpBoxUI(*args):
    if (cmds.window('win_zorroHelpBox', exists=1)):
        cmds.deleteUI('win_zorroHelpBox')
    myWindow = cmds.window('win_zorroHelpBox', t=('Zorro FX Helper' + ver), s=1)


    cmds.columnLayout(adj=1, bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]))


    # name space
    cmds.rowColumnLayout(nc=4, cw = [(1, 120), (2, 90), (3, 120), (4, 90)])
    cmds.button(l='nmSpc FX Rig >>', h=bh1, c=partial(cGetNmSpc, 'tfNmSpcFX'), bgc=(colBrown[0], colBrown[1], colBrown[2]))
    cmds.textField('tfNmSpcFX', tx='zor_01', bgc=(0,0,0), ed=0)

    cmds.button(l='nmSpc Anim >>', h=bh1, c=partial(cGetNmSpc, 'tfNmSpcAnim'), bgc=(colRed[0], colRed[1], colRed[2]))
    cmds.textField('tfNmSpcAnim', tx='anim', bgc=(0,0,0), ed=0)
    cmds.setParent(top=1)



    # load cloth rig
    cmds.frameLayout('flLoadRef', l='Load FX Cloth Rig', bgc=(colFrameGreen[0], colFrameGreen[1], colFrameGreen[2]), cll=1, cl=0, cc=partial(cShrinkWin, "win_zorroHelpBox"))
    cmds.rowColumnLayout(nc=3, cw = [(1, 120), (2, 90), (3, 210)])

    cmds.text('FX Cloth Rig Version', bgc = (colBrown[0], colBrown[1], colBrown[2]))
    cmds.intField('iFXVersion', v=25)
    cmds.button(l='Load', h=bh1, c=partial(cLoadRef, 'zor_01'), bgc=(colLightGreen[0], colLightGreen[1], colLightGreen[2]))

    cmds.setParent(top=1)


    # visibility
    cmds.frameLayout('flVisibility', l='Visbility', bgc=(colFrameGreen[0], colFrameGreen[1], colFrameGreen[2]), cll=1, cl=1, cc=partial(cShrinkWin, "win_zorroHelpBox"))
    cmds.rowColumnLayout(nc=6, cw = [(1, 10), (2, 100), (3, 100), (4, 10), (5, 100), (6, 100)])

    cmds.text(' ', bgc = (colBrown[0], colBrown[1], colBrown[2]))
    cmds.checkBox('cbAnimGRP', l='Anim_GRP', v=0, bgc=(colBrown[0], colBrown[1], colBrown[2]))
    cmds.checkBox('cbAnimHiGRP', l='Anim Hi GRP', v=0, bgc=(colBrown[0], colBrown[1], colBrown[2]))
    cmds.text(' ', bgc = (colRed[0], colRed[1], colRed[2]))
    cmds.checkBox('cbLow', l='Low', v=0, bgc=(colRed[0], colRed[1], colRed[2]))
    cmds.checkBox('cbMid', l='Mid', v=1, bgc=(colRed[0], colRed[1], colRed[2]))

    cmds.text(' ', bgc = (colBrown[0], colBrown[1], colBrown[2]))
    cmds.checkBox('cbCape', l='Cape', v=0, bgc=(colBrown[0], colBrown[1], colBrown[2]))
    cmds.checkBox('cbShirt', l='Shirt', v=0, bgc=(colBrown[0], colBrown[1], colBrown[2]))
    cmds.text(' ', bgc = (colRed[0], colRed[1], colRed[2]))
    cmds.checkBox('cbHgh', l='High', v=0, bgc=(colRed[0], colRed[1], colRed[2]))
    cmds.checkBox('cbButtons', l='Buttons', v=0, bgc=(colRed[0], colRed[1], colRed[2]))

    cmds.text(' ', bgc = (colBrown[0], colBrown[1], colBrown[2]))
    cmds.checkBox('cbWrapGRP', l='Wrap_GRP', v=0, bgc=(colBrown[0], colBrown[1], colBrown[2]))
    cmds.checkBox('cbExportClothGRP', l='Export Cloth', v=0, bgc=(colBrown[0], colBrown[1], colBrown[2]))
    cmds.text(' ', bgc = (colRed[0], colRed[1], colRed[2]))
    cmds.text(' ', bgc=(colRed[0], colRed[1], colRed[2]))
    cmds.text(' ', bgc=(colRed[0], colRed[1], colRed[2]))

    cmds.text(' ', bgc = (colBrown[0], colBrown[1], colBrown[2]))
    cmds.checkBox('cbxGenBase', l='xGenBase', v=0, bgc=(colBrown[0], colBrown[1], colBrown[2]))
    cmds.checkBox('cbColliderGRP', l='Collider', v=0, bgc=(colBrown[0], colBrown[1], colBrown[2]))
    cmds.text(' ', bgc=(colRed[0], colRed[1], colRed[2]))
    cmds.text(' ', bgc=(colRed[0], colRed[1], colRed[2]))
    cmds.text(' ', bgc=(colRed[0], colRed[1], colRed[2]))
    cmds.setParent('..')

    cmds.rowColumnLayout(nc=4, cw = [(1, 105), (2, 105), (3, 105), (4, 105)])
    cmds.button(l='Tgl All', h=bh1, bgc=(colBrown[0], colBrown[1], colBrown[2]), c=partial(tkTglAll, 'FX'))
    cmds.button(l='Set FX Visibility', h=bh1, bgc=(colBrown[0], colBrown[1], colBrown[2]), c=partial(tkSetVisibility, 'FX'))
    cmds.button(l='Tgl All', h=bh1, bgc=(colRed[0], colRed[1], colRed[2]), c=partial(tkTglAll, 'Anim'))
    cmds.button(l='Set Anim Visibility', h=bh1, bgc=(colRed[0], colRed[1], colRed[2]), c=partial(tkSetVisibility, 'Anim'))

    cmds.setParent(top=1)



    # link anim elements
    cmds.frameLayout('flLinkAnim', l='Link Anim', bgc=(colFrameGreen[0], colFrameGreen[1], colFrameGreen[2]), cll=1, cl=1, cc=partial(cShrinkWin, "win_zorroHelpBox"))

    cmds.rowColumnLayout(nc=2, cw = [(1, 210), (2, 210)])
    cmds.button(l='Connect Anim to Cloth Setup', h=bh1, bgc=(colLightGreen[0], colLightGreen[1], colLightGreen[2]), c=partial(tk_linkAnimToCloth, 1))
    cmds.button(l='Disconnect Anim', h=bh1, bgc=(colDarkRed[0], colDarkRed[1], colDarkRed[2]), c=partial(tk_linkAnimToCloth, 0))
    cmds.setParent(top=1)


    # Make it faster
    cmds.frameLayout('flFaster', l='Make It Faster', bgc=(colFrameGreen[0], colFrameGreen[1], colFrameGreen[2]), cll=1, cl=1, cc=partial(cShrinkWin, "win_zorroHelpBox"))

    cmds.rowColumnLayout(nc=3, cw = [(1, 210), (2, 105), (3, 105)])
    cmds.button(l='Select FX Anim Geos', h=bh1, bgc=(colLightGreen[0], colLightGreen[1], colLightGreen[2]), c=partial(cSelectFXAnimELements))
    cmds.button(l='Export As Abc', h=bh1, bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), c=partial(cExportAsABC))
    cmds.button(l='Reference FX Abc', h=bh1, bgc=(colDarkRed[0], colDarkRed[1], colDarkRed[2]), c=partial(cReferenceAnimABC))
    cmds.setParent(top=1)

    
    
    # Caching
    cmds.frameLayout('flCaching', l='Caching', bgc=(colFrameGreen[0], colFrameGreen[1], colFrameGreen[2]), cll=1, cl=1, cc=partial(cShrinkWin, "win_zorroHelpBox"))
    cmds.columnLayout(adj=1, bgc=([0,0,0]))
    # cmds.rowColumnLayout(nc=4, cw = [(1, 120), (2, 90), (3, 120), (4, 90)])
    cmds.button(l='Select Nucleus', c=partial(cSelect, 'nucleus1'), bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]))
    # cmds.setParent('..')


    cmds.rowColumnLayout(nc=7, cw = [(1, 45), (2, 45), (3, 45), (4, 45), (5, 45), (6, 100), (7, 95)])
    cmds.text(' ', h=30, bgc=[0,0,0])
    cmds.text('None', bgc=[0,0,0])
    cmds.text('Shirt', bgc=[0,0,0])
    cmds.text('Cape', bgc=[0,0,0])
    cmds.text('Both', bgc=[0,0,0])
    cmds.text('Cache', bgc=[0,0,0])
    cmds.text('Cache ', bgc=[0,0,0])

    # caching Mid
    cmds.text('MID', bgc=[0,0,0])
    cmds.button(l='None', h=bh1, bgc=(colDarkRed[0], colDarkRed[1], colDarkRed[2]), c=partial(cSelectSimELements, 'none'))
    cmds.button(l='Mid', h=bh1, bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), c=partial(cSelectSimELements, 'shirtMid'))
    cmds.button(l='Mid', h=bh1, bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), c=partial(cSelectSimELements, 'capeMid'))
    cmds.button(l='Mid', h=bh1, bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), c=partial(cSelectSimELements, 'bothMid'))
    cmds.button(l='Create', h=bh1, bgc=(colLightGreen[0], colLightGreen[1], colLightGreen[2]), c=partial(cClothCache))
    cmds.button(l='Delete', h=bh1, bgc=(colDarkRed[0], colDarkRed[1], colDarkRed[2]), c=partial(cDeleteCache))

    # caching Highres
    cmds.text('HIGH', bgc=[0,0,0])
    cmds.button(l='None', h=bh1, bgc=(colDarkRed[0], colDarkRed[1], colDarkRed[2]), c=partial(cSelectSimELements, 'none'))
    cmds.button(l='High', h=bh1, bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), c=partial(cSelectSimELements, 'shirtHi'))
    cmds.button(l='High', h=bh1, bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), c=partial(cSelectSimELements, 'capeHi'))
    cmds.button(l='High', h=bh1, bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), c=partial(cSelectSimELements, 'bothHi'))
    cmds.button(l='Create', h=bh1, bgc=(colLightGreen[0], colLightGreen[1], colLightGreen[2]), c=partial(cClothCache))
    cmds.button(l='Delete', h=bh1, bgc=(colDarkRed[0], colDarkRed[1], colDarkRed[2]), c=partial(cDeleteCache))
    cmds.setParent(top=1)



    # Bring To Highres
    cmds.frameLayout('flBring To Highres', l='Bring To Highres', bgc=(colFrameGreen[0], colFrameGreen[1], colFrameGreen[2]), cll=1, cl=1, cc=partial(cShrinkWin, "win_zorroHelpBox"))
    # cmds.rowColumnLayout(nc=3, cw = [(1, 120), (2, 210), (3, 90)])
    cmds.rowColumnLayout(nc=3, cw = [(1, 90), (2, 240), (3, 90)])

    cmds.button(l='Read Wraps', h=bh1, bgc=(colLightGreen[0], colLightGreen[1], colLightGreen[2]), c=partial(cWrapStatus, 'read', 'rbCapeWraps', 'capeWrap'))
    # cmds.radioButtonGrp('rbCapeWraps', label=' ', labelArray3=['Off', 'Mid', 'High'], numberOfRadioButtons=3, cal=[9, 'left'],cw4=[10, 67, 67, 67], sl=1)
    cmds.radioButtonGrp('rbCapeWraps', label='Cape', labelArray3=['Off', 'Mid', 'High'], numberOfRadioButtons=3, cal=[1, 'center'] ,cw4=[55, 55, 55, 55], sl=1)
    cmds.button(l='Set', h=bh1, bgc=(colDarkRed[0], colDarkRed[1], colDarkRed[2]), c=partial(cWrapStatus, 'set', 'rbCapeWraps', 'capeWrap'))
    
    cmds.button(l='Read Wraps', h=bh1, bgc=(colLightGreen[0], colLightGreen[1], colLightGreen[2]), c=partial(cWrapStatus, 'read', 'rbShirtWraps', 'shirtWrap'))
    # cmds.radioButtonGrp('rbShirtWraps', label='  ', labelArray3=['Off', 'Mid', 'High'], numberOfRadioButtons=3, cal=[9, 'left'],cw4=[10, 67, 67, 67], sl=1)
    cmds.radioButtonGrp('rbShirtWraps', label='Shirt', labelArray3=['Off', 'Mid', 'High'], numberOfRadioButtons=3, cal=[1, 'center'] ,cw4=[55, 55, 55, 55], sl=1)
    cmds.button(l='Set', h=bh1, bgc=(colDarkRed[0], colDarkRed[1], colDarkRed[2]), c=partial(cWrapStatus, 'set', 'rbShirtWraps', 'shirtWrap'))
    cmds.setParent(top=1)



    # Attach xGen
    cmds.frameLayout('flImportxGen', l='Import xGen Description', bgc=(colFrameGreen[0], colFrameGreen[1], colFrameGreen[2]), cll=1, cl=1, cc=partial(cShrinkWin, "win_zorroHelpBox"))
    # cmds.button(l='Select xGenBase Geo', h=bh1, en=1, bgc=(colLightGreen[0], colLightGreen[1], colLightGreen[2]), c=partial(cSelect, 'body_cn_hi_cfx'))

    cmds.rowColumnLayout(nc=3, cw = [(1, 100), (2, 260), (3, 60)])
    cmds.button(l='xGen Path >>', bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), h=bh1, c=partial(cGetPath, 'choose'))
    cmds.textField('tfPathxGen', tx=defaultPath, bgc=(0,0,0), ed=1)
    cmds.button(l='Default', bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), h=bh1, c=partial(cGetPath, 'default'))

    cmds.button(l='Select Version', h=bh1, bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), c=partial(cSelectxGenVersion))
    cmds.textField('xGenVersion', tx=approvedxGen, bgc=(0,0,0), ed=0)
    cmds.button(l='Import', h=bh1, en=0, bgc=(colLightGreen[0], colLightGreen[1], colLightGreen[2]), c=partial(cImportxGen, 'remove'))
    # cmds.setParent('..')
    # cmds.button(l='Fix Naming', h=bh1, en=1, bgc=(colRed[0], colRed[1], colRed[2]), c=partial(cFixNaming, 'body_cn_hi_cfx'))
    cmds.setParent(top=1)



    
     # Select Geos For Playblast
    cmds.frameLayout('flPlayblast', l='Select Geos For Playblast', bgc=(colFrameGreen[0], colFrameGreen[1], colFrameGreen[2]), cll=1, cl=1, cc=partial(cShrinkWin, "win_zorroHelpBox"))
    cmds.rowColumnLayout(nc=4, cw = [(1, 105), (2, 105), (3, 105), (4, 105)])

    cmds.button(l='Cloth Mid', h=bh1, bgc=(colLightGreen[0], colLightGreen[1], colLightGreen[2]), c=partial(cSelectForPlayblast, 'clothSetMid'))
    cmds.button(l='Cloth Mid xGen', h=bh1, bgc=(colLightGreen[0], colLightGreen[1], colLightGreen[2]), c=partial(cSelectForPlayblast, 'clothxGenSetMid'))
    cmds.button(l='Add Mask', h=bh1, bgc=(colLightGreen[0], colLightGreen[1], colLightGreen[2]), c=partial(cSelectForPlayblast, 'zorroMask'))
    cmds.setParent(top=1)


   
    # flFeedback
    cmds.frameLayout('flFeedback', l='       FEEDBACK', fn='obliqueLabelFont', bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), cll=0, cl=0)
    cmds.rowColumnLayout(nc=2, cw = [(1, 360), (2, 60)])
    cmds.textField('tfFeedback', ed=0, bgc=[0,0,0])
    cmds.button(l='Clear', bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), c=partial(cClear, 'tfFeedback', '', [0, 0, 0]))

    


    cmds.showWindow(myWindow)
    cmds.window('win_zorroHelpBox', e=1, w=300)




zorroHelpBoxUI()
cShrinkWin('win_zorroHelpBox')

