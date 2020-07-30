# zorroHelpBox.py
import maya.cmds as cmds
import maya.mel as mel
from functools import partial  
# import thomas as tk

'''
Tools for zorro sim
---------------------------------------------------


'''


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
        'belt_cn_lo_geo', 'beltSheathLong_cn_lo_geo', 'beltSheathWide_cn_lo_geo', 'furVolume_cn_mid_anim_geo' ]
    
    nmSpcAnim = cmds.textField('tfNmSpcAnim', tx=1, q=1)
    nmSpcFX = cmds.textField('tfNmSpcFX', tx=1, q=1)
    if nmSpcAnim:
        nmSpcAnim   = nmSpcAnim + ':'
        nmSpcFX     = nmSpcFX + ':'

        for clt in CLT:
            print clt
            shapes = cmds.listRelatives(nmSpcFX + clt, s=1)    
            if action == 1:
                print 'connecting... '
                cmds.select(nmSpcAnim + clt, nmSpcFX + clt)
                mel.eval('performBlendShape 0 1')
                bs = cmds.listConnections(shapes[0], s=1, d=0, type='blendShape')
                bs = cmds.rename(bs[0], 'BS_' + clt)
                print 'bs:'
                print bs
                cmds.setAttr(bs + '.' + clt, 1)
            else:
                print 'disconnecting... '
                bs = cmds.listConnections(shapes[0], s=1, d=0, type='blendShape')
                cmds.setAttr(bs[0] + '.' + clt, 0) 
                cmds.delete(bs) 




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
        nmSpc = nmSpc + ':'
        low = cmds.checkBox('cbLow', v=1, q=1)
        mid = cmds.checkBox('cbMid', v=1, q=1)
        hgh = cmds.checkBox('cbHgh', v=1, q=1)

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

    else:
        print 'no namespace!'
    

def cSelectSimELements(*args):
    nmSpcFX = cmds.textField('tfNmSpcFX', tx=1, q=1)
    CLT = ['cape_cn_cfx_mid_geo_SIM', 'shirt_cn_cfx_mid_geo_SIM']
    if nmSpcFX:
        nmSpcFX = nmSpcFX + ':'

    cmds.select(nmSpcFX + CLT, r=1)


def cClothCache(*args):
    mel.eval('doCreateNclothCache 5 { "2", "1", "10", "OneFile", "1", "","0","","0", "0", "0", "1", "1","0","1","mcx" }') 


def cDeleteCache(*args):
    mel.eval('fluidDeleteCache')




def zorroHelpBoxUI(*args):
    colFrame  = [0.3, 0.3, 0.3]
    colFrameRed  = [0.4, 0.3, 0.3]
    colDarkRed  = [0.16, 0.1, 0.08]
    colFrameGreen    = [0.3, 0.4, 0.28]
    colDarkGreen  = [0.1, 0.16, 0.08]
    colSilverDark   = [0.08, 0.08, 0.08]
    colDark    = [0.1, 0.1, 0.1]
    ver = '0.1'
    windowStartHeight = 50
    windowStartWidth = 200
    bh1 = 24

    if (cmds.window('win_zorroHelpBox', exists=1)):
        cmds.deleteUI('win_zorroHelpBox')
    myWindow = cmds.window('win_zorroHelpBox', t=('Zorro FX Helper' + ver), s=1)

    cmds.columnLayout(adj=1, bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]))
    # cmds.rowColumnLayout(nc=2, cw = [(1, 90), (2, 330)])

    cmds.rowColumnLayout(nc=4, cw = [(1, 120), (2, 95), (3, 120), (4, 95)])
    cmds.button(l='nmSpc FX Rig >>', h=bh1, c=partial(cGetNmSpc, 'tfNmSpcFX'))
    cmds.textField('tfNmSpcFX', tx='zor_01', bgc=(0,0,0), ed=0)

    cmds.button(l='nmSpc Anim >>', h=bh1, c=partial(cGetNmSpc, 'tfNmSpcAnim'))
    cmds.textField('tfNmSpcAnim', tx='zor_02', bgc=(0,0,0), ed=0)
    cmds.setParent(top=1)

    cmds.columnLayout(adj=1)
    cmds.frameLayout('flVisibility', l='Visbility', bgc=(colFrameGreen[0], colFrameGreen[1], colFrameGreen[2]), cll=1, cl=1, cc=partial(cShrinkWin, "win_zorroHelpBox"))
    cmds.rowColumnLayout(nc=5, cw = [(1, 90), (2, 70), (3, 70), (4, 70), (5, 120)])

    cmds.text('Anim Elements')
    cmds.checkBox('cbLow', l='low', v=0)
    cmds.checkBox('cbMid', l='mid', v=1)
    cmds.checkBox('cbHgh', l='high', v=0)
    cmds.button(l='Set Visibility', h=bh1, bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), c=partial(tkSetVisibilty))
    cmds.setParent(top=1)

    cmds.columnLayout(adj=1, bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]))
    cmds.frameLayout('flLinkAnim', l='Link Anim', bgc=(colFrameGreen[0], colFrameGreen[1], colFrameGreen[2]), cll=1, cl=1, cc=partial(cShrinkWin, "win_zorroHelpBox"))

    cmds.rowColumnLayout(nc=2, cw = [(1, 210), (2, 210)])
    cmds.button(l='Link Anim to Cloth Setup', h=bh1, bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), c=partial(tk_linkAnimToCloth, 1))
    cmds.button(l='Disconnect Anim', h=bh1, bgc=(colDarkRed[0], colDarkRed[1], colDarkRed[2]), c=partial(tk_linkAnimToCloth, 0))
    cmds.setParent(top=1)

    cmds.frameLayout('flCache', l='Caching', bgc=(colFrameGreen[0], colFrameGreen[1], colFrameGreen[2]), cll=1, cl=0, cc=partial(cShrinkWin, "win_zorroHelpBox"))
    cmds.rowColumnLayout(nc=3, cw = [(1, 210), (2, 105), (3, 105)])
    cmds.button(l='Select Cloth Geos', h=bh1, bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), c=partial(cSelectSimELements))
    cmds.button(l='Create Cache', h=bh1, bgc=(colDarkGreen[0], colDarkGreen[1], colDarkGreen[2]), c=partial(cClothCache))
    cmds.button(l='Delete Cache', h=bh1, bgc=(colDarkRed[0], colDarkRed[1], colDarkRed[2]), c=partial(cDeleteCache))

   


    cmds.showWindow(myWindow)
    cmds.window('win_zorroHelpBox', e=1, w=300)




zorroHelpBoxUI()
cShrinkWin('win_zorroHelpBox')
