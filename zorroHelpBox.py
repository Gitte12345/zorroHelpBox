# zorroHelpBox.py
import maya.cmds as cmds
import maya.mel as mel
from functools import partial  
# import thomas as tk

'''
Tools for zorro sim
---------------------------------------------------


'''
colDarkGreen        = [0.1, 0.16, 0.08]
colFrame            = [0.3, 0.3, 0.3]
colFrameRed         = [0.4, 0.3, 0.3]
colDarkRed          = [0.32, 0.2, 0.14]
colFrameGreen       = [0.3, 0.4, 0.28]
colLightGreen       = [0.4, 0.5, 0.36]
colDark             = [0.1, 0.1, 0.1]

defaultPath     = 'X:/zorro_zor-5069/_library/assets/characters/chr_zorroFox/cfx_groom/'
approvedxGen    = 'zor_chr_zorroFox_cfx_groom_v080_thk__body_collection'
xGenBaseGeo     = 'body_cn_hi_cfx'

def tkHelpSwitchInstancerInputs(*args):
    if cmds.window('win_tkSwitchInstancerINPUtsHELP', exists=1):
        cmds.deleteUI('win_tkSwitchInstancerINPUtsHELP')
    myWindow = cmds.window('win_tkSwitchInstancerINPUtsHELP', s=1, t='help', wh=[200, 200])
    helpText = 'Replace instanced references without changing order\n---------------------------------------------------\nInstancer:          Choose Instancer \nUses                   The namespace of the first connected obj\nReplace With:   Select file you want to replace from\n                           Gets the namespace automatically'
    cmds.columnLayout(adj=1)
    cmds.text(helpText, al='left')
    cmds.showWindow(myWindow )



def cShrinkWin(windowToClose, *args):
    cmds.window(windowToClose, e=1, h=20)
    cmds.window(windowToClose, e=1, w=420)



def tk_linkAnimToCloth(action, *args):
    CLT = ['cape_cn_cfx_mid_geo_oneSided', 'shirt_cn_cfx_mid_geo_oneSided', 
        'leatherSheath_cn_lo_geo', 'metalSheath_cn_lo_geo', 'beltBuckle_cn_lo_geo', 
        'belt_cn_lo_geo', 'beltSheathLong_cn_lo_geo', 'beltSheathWide_cn_lo_geo', 'furVolume_cn_mid_anim_geo', 
        'body_cn_hi_cfx']        
    
    nmSpcAnim = cmds.textField('tfNmSpcAnim', tx=1, q=1)
    nmSpcFX = cmds.textField('tfNmSpcFX', tx=1, q=1)
    if nmSpcAnim:
        nmSpcAnim   = nmSpcAnim + ':'
        nmSpcFX     = nmSpcFX + ':'

        print '-------------------------'

        for clt in CLT:
            # print clt
            shapes = cmds.listRelatives(nmSpcFX + clt, s=1)    
            
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
                    print 'connecting ' + clt
                    cmds.select(nmSpcAnim + clt, nmSpcFX + clt)
                    mel.eval('performBlendShape 0 1')
                    bs = cmds.listConnections(shapes[0], s=1, d=0, type='blendShape')
                    bs = cmds.rename(bs[0], 'BS_' + clt)
                    # print 'bs:'
                    # print bs
                    cmds.setAttr(bs + '.' + clt, 1)
                else:
                    print (clt + ' is already connected - disconnect first!')

        print '-------------------------'



def cGetNmSpc(field, *args):
    curSel = cmds.ls(sl=1)
    if curSel:
        if ':' in curSel[0]:
            cmds.textField(field, tx=curSel[0].split(':')[0], e=1)
        else:
            cmds.textField(field, tx='', e=1)
    else:
        cmds.textField(field, tx='', e=1)



def tkSetVisibilty(*args):
    nmSpc = cmds.textField('tfNmSpcAnim', tx=1, q=1)
    if nmSpc:
        nmSpc   = nmSpc + ':'
        low     = cmds.checkBox('cbLow', v=1, q=1)
        mid     = cmds.checkBox('cbMid', v=1, q=1)
        hgh     = cmds.checkBox('cbHgh', v=1, q=1)
        but     = cmds.checkBox('cbButtons', v=1, q=1)

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

    else:
        print 'no namespace!'
    


def cSelectSimELements(object, *args):
    CLT = []
    nmSpcFX = cmds.textField('tfNmSpcFX', tx=1, q=1)
    if (object == 'shirt'):
        CLT = ['shirt_cn_cfx_mid_geo_SIM']
    if (object == 'cape'):
        CLT = ['cape_cn_cfx_mid_geo_SIM']
    if (object == 'both'):
        CLT = ['cape_cn_cfx_mid_geo_SIM', 'shirt_cn_cfx_mid_geo_SIM']



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
    if nmSpcFX:
        nmSpcFX = nmSpcFX + ':'

    cmds.select(nmSpcFX + grp, r=1)
    cmds.select(nmSpcFX + 'xGenBase_GRP', add=1)


def cExportAsABC(*args):
    mel.eval('AlembicExportSelectionOptions')



def cReferenceAnimABC(*args):
    mel.eval(' projectViewer AlembicReference')
   


def cClothCache(*args):
    mel.eval('doCreateNclothCache 5 { "2", "1", "10", "OneFile", "1", "","0","","0", "0", "0", "1", "1","0","1","mcx" }') 



def cDeleteCache(*args):
    mel.eval('fluidDeleteCache')



def cWrapStatus(action, *args):
    nmSpcFX = cmds.textField('tfNmSpcFX', tx=1, q=1)
    if nmSpcFX:
        nmSpcFX = nmSpcFX + ':'

    if action == 'select':
        cmds.select(nmSpcFX + 'wrap_cape', r=1)
        cmds.select(nmSpcFX + 'wrap_shirt.envelope', add=1)

    elif action == 'read':
        cape        = cmds.getAttr(nmSpcFX + 'wrap_cape.envelope')  
        shirt       = cmds.getAttr(nmSpcFX + 'wrap_cape.envelope')
        cmds.checkBox('cbCape', v=cape, e=1)
        cmds.checkBox('cbShirt', v=shirt, e=1)
    
    elif action == 'set':
        cape        = cmds.checkBox('cbCape', v=1, q=1)
        shirt       = cmds.checkBox('cbShirt', v=1, q=1)
        cmds.setAttr(nmSpcFX + 'wrap_cape.envelope', cape)
        cmds.setAttr(nmSpcFX + 'wrap_shirt.envelope', shirt)



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







def zorroHelpBoxUI(*args):
    ver                 = '0.1'
    windowStartHeight   = 50
    windowStartWidth    = 200
    bh1                 = 24

    if (cmds.window('win_zorroHelpBox', exists=1)):
        cmds.deleteUI('win_zorroHelpBox')
    myWindow = cmds.window('win_zorroHelpBox', t=('Zorro FX Helper' + ver), s=1)


    cmds.columnLayout(adj=1, bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]))
    # cmds.frameLayout('flZoorHelpBox', l='zorroHelpBox', bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), cll=1, cl=0, cc=partial(cShrinkWin, "win_zorroHelpBox"))
    
    # name space

    cmds.rowColumnLayout(nc=4, cw = [(1, 120), (2, 90), (3, 120), (4, 90)])
    cmds.button(l='nmSpc FX Rig >>', h=bh1, c=partial(cGetNmSpc, 'tfNmSpcFX'))
    cmds.textField('tfNmSpcFX', tx='zor_01', bgc=(0,0,0), ed=0)

    cmds.button(l='nmSpc Anim >>', h=bh1, c=partial(cGetNmSpc, 'tfNmSpcAnim'))
    cmds.textField('tfNmSpcAnim', tx='zor_02', bgc=(0,0,0), ed=0)
    cmds.setParent(top=1)



    # visibility
    cmds.frameLayout('flVisibility', l='Visbility Anim Elements', bgc=(colFrameGreen[0], colFrameGreen[1], colFrameGreen[2]), cll=1, cl=1, cc=partial(cShrinkWin, "win_zorroHelpBox"))
    cmds.rowColumnLayout(nc=5, cw = [(1, 120), (2, 70), (3, 70), (4, 70), (5, 90)])

    cmds.button(l='Set Visibility', h=bh1, bgc=(colLightGreen[0], colLightGreen[1], colLightGreen[2]), c=partial(tkSetVisibilty))
    cmds.checkBox('cbLow', l='low', v=0)
    cmds.checkBox('cbMid', l='mid', v=1)
    cmds.checkBox('cbHgh', l='high', v=0)
    cmds.checkBox('cbButtons', l='Buttons', v=0)

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
    cmds.button(l='Import FX Abc', h=bh1, bgc=(colDarkRed[0], colDarkRed[1], colDarkRed[2]), c=partial(cReferenceAnimABC))
    cmds.setParent(top=1)

    

    # caching
    cmds.frameLayout('flCache', l='Select Cloth And Cache', bgc=(colFrameGreen[0], colFrameGreen[1], colFrameGreen[2]), cll=1, cl=1, cc=partial(cShrinkWin, "win_zorroHelpBox"))
    # cmds.rowColumnLayout(nc=3, cw = [(1, 210), (2, 105), (3, 105)])
    cmds.rowColumnLayout(nc=5, cw = [(1, 70), (2, 70), (3, 70), (4, 105), (5, 105)])
    cmds.button(l='Shirt', h=bh1, bgc=(colLightGreen[0], colLightGreen[1], colLightGreen[2]), c=partial(cSelectSimELements, 'shirt'))
    cmds.button(l='Cape', h=bh1, bgc=(colLightGreen[0], colLightGreen[1], colLightGreen[2]), c=partial(cSelectSimELements, 'cape'))
    cmds.button(l='Both', h=bh1, bgc=(colLightGreen[0], colLightGreen[1], colLightGreen[2]), c=partial(cSelectSimELements, 'both'))
    cmds.button(l='Create Cache', h=bh1, bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), c=partial(cClothCache))
    cmds.button(l='Delete Cache', h=bh1, bgc=(colDarkRed[0], colDarkRed[1], colDarkRed[2]), c=partial(cDeleteCache))
    cmds.setParent(top=1)



    # Bring To Highres
    cmds.frameLayout('flBring To Highres', l='Bring To Highres', bgc=(colFrameGreen[0], colFrameGreen[1], colFrameGreen[2]), cll=1, cl=1, cc=partial(cShrinkWin, "win_zorroHelpBox"))
    cmds.rowColumnLayout(nc=5, cw = [(1, 120), (2, 70), (3, 70), (4, 80), (5, 80)])
    # cmds.text('Enable Wrap')
    cmds.button(l='Cloth Wraps', h=bh1, bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), c=partial(cWrapStatus, 'select'))
    cmds.checkBox('cbCape', l='Cape', v=0)
    cmds.checkBox('cbShirt', l='Shirt', v=0)
    cmds.button(l='Read', h=bh1, bgc=(colLightGreen[0], colLightGreen[1], colLightGreen[2]), c=partial(cWrapStatus, 'read'))
    cmds.button(l='Set', h=bh1, bgc=(colDarkRed[0], colDarkRed[1], colDarkRed[2]), c=partial(cWrapStatus, 'set'))
    cmds.setParent(top=1)

   

    # Attach xGen
    cmds.frameLayout('flImportxGen', l='Import xGen Description', bgc=(colFrameGreen[0], colFrameGreen[1], colFrameGreen[2]), cll=1, cl=0, cc=partial(cShrinkWin, "win_zorroHelpBox"))

    cmds.rowColumnLayout(nc=3, cw = [(1, 100), (2, 260), (3, 60)])
    cmds.button(l='xGen Path >>', bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), h=bh1, c=partial(cGetPath, 'choose'))
    cmds.textField('tfPathxGen', tx=defaultPath, bgc=(0,0,0), ed=1)
    cmds.button(l='Default', bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), h=bh1, c=partial(cGetPath, 'default'))

    cmds.button(l='Select Version', h=bh1, bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), c=partial(cSelectxGenVersion))
    cmds.textField('xGenVersion', tx=approvedxGen, bgc=(0,0,0), ed=0)
    cmds.button(l='Import', h=bh1, bgc=(colLightGreen[0], colLightGreen[1], colLightGreen[2]), c=partial(cImportxGen, 'remove'))


    cmds.showWindow(myWindow)
    cmds.window('win_zorroHelpBox', e=1, w=300)




zorroHelpBoxUI()
cShrinkWin('win_zorroHelpBox')

