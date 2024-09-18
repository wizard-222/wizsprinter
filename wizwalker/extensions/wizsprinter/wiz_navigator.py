import os
import asyncio
import sys
import traceback
from wizwalker import XYZ, ClientHandler
from wizwalker import Keycode
from loguru import logger
from itertools import takewhile
from .text_parser import *
import math
from wizwalker.memory import Window

handleQuestCollection = True
is_tab = '\t'.__eq__

cur_path = os.path.dirname(__file__)

import os
import sys

#notfaj was here
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

@logger.catch()
async def go_through_dialog(p):
    while await p.is_in_dialog():
        await p.send_key(Keycode.SPACEBAR, 0.1)

    await asyncio.sleep(.5)


@logger.catch()
async def gateTypeDifferentiation(x, y, z, p, zoneAccessType):
    # standard zone gate, just teleport
    if zoneAccessType == 'standard':
        await p.teleport(XYZ(x,y,z))

        await p.wait_for_zone_change()

    # dungeon ENTRANCE, teleport, click x, wait for change
    elif zoneAccessType == 'dungeon':

        await p.teleport(XYZ(float(x), float(y), float(z)))

        while not await p.is_in_npc_range():
            pass

        while await p.is_in_npc_range():
            await asyncio.sleep(.8)
            await p.send_key(Keycode.X, 0.1)
            await p.send_key(Keycode.X, 0.1)
            await p.send_key(Keycode.X, 0.1)

        await p.wait_for_zone_change()

    # this is a dungeon exit, user may need to confirm to leave the dungeon.  Teleport, click confirm
    elif zoneAccessType == 'dungeonExitConfirm':

        if await p.is_in_dialog():
            await go_through_dialog(p)

        await p.teleport(XYZ(float(x), float(y), float(z)))

        await p.mouse_handler.activate_mouseless()
        await asyncio.sleep(1)

        try:
            await p.mouse_handler.click_window_with_name('centerButton')
            await p.wait_for_zone_change()
        except ValueError:
            await asyncio.sleep(8)

        await p.mouse_handler.deactivate_mouseless()

    elif zoneAccessType == 'xNoWait':

        if await p.is_in_dialog():
            await go_through_dialog(p)

        await p.teleport(XYZ(float(x), float(y), float(z)))

        while not await p.is_in_npc_range():
            pass

        while await p.is_in_npc_range():
            await asyncio.sleep(.4)
            await p.send_key(Keycode.X, 0.1)

        await p.wait_for_zone_change()

    elif zoneAccessType == 'xNoWaitMirageCaterwaulToCaravan':
        if await p.is_in_dialog():
            await go_through_dialog(p)

        await p.teleport(XYZ(float(x), float(y), float(z)))

        await asyncio.sleep(7)

        while not await p.is_in_npc_range():
            pass

        while await p.is_in_npc_range():
            await asyncio.sleep(.4)
            await p.send_key(Keycode.X, 0.1)

        await p.wait_for_zone_change()

    elif zoneAccessType == 'xNoWaitPolaris':
        await p.teleport(XYZ(float(x), float(y), float(z)))

        await asyncio.sleep(4)

        while not await p.is_in_npc_range():
            pass

        while await p.is_in_npc_range():
            await asyncio.sleep(.4)
            await p.send_key(Keycode.X, 0.1)

        await p.wait_for_zone_change()

    elif zoneAccessType == 'xSkipRideKrok1':
        await p.teleport(XYZ(4521.9609375, 3189.564208984375, 25.792266845703125))

        # there is a vendor near the boat, sleep to make sure you click the boat instead of the vendor
        await asyncio.sleep(1.5)

        while not await p.is_in_npc_range():
            pass

        while await p.is_in_npc_range():
            await asyncio.sleep(.4)
            await p.send_key(Keycode.X, 0.1)

        await p.wait_for_zone_change()

        while not await p.is_in_npc_range():
            pass

        while await p.is_in_npc_range():
            await asyncio.sleep(.4)
            await p.send_key(Keycode.X, 0.1)

        await p.wait_for_zone_change()

    elif zoneAccessType == 'xSkipRideKrok2':
        await p.teleport(XYZ(11749.1123046875, -189.94265747070312, 1219.797119140625))

        while not await p.is_in_npc_range():
            pass

        while await p.is_in_npc_range():
            await asyncio.sleep(.4)
            await p.send_key(Keycode.X, 0.1)

        await p.wait_for_zone_change()

        while not await p.is_in_npc_range():
            pass

        while await p.is_in_npc_range():
            await asyncio.sleep(.4)
            await p.send_key(Keycode.X, 0.1)

        await p.wait_for_zone_change()

    elif zoneAccessType == 'xNoWaitSkipRideMarleyboneChelsea':
        await p.teleport(XYZ(float(x), float(y), float(z)))

        await p.wait_for_zone_change()

        while not await p.is_in_npc_range():
            pass

        while await p.is_in_npc_range():
            await asyncio.sleep(.4)
            await p.send_key(Keycode.X, 0.1)

        await p.wait_for_zone_change()

    elif zoneAccessType == 'xNoWaitSkipRideMarleyboneChelseaReturn':
        await p.teleport(XYZ(float(x), float(y), float(z)))

        await p.wait_for_zone_change()

        await asyncio.sleep(.3)
        await p.send_key(Keycode.X, 0.1)

        await p.wait_for_zone_change()

    elif zoneAccessType == 'xNoWaitSkipRideMarleyboneHyde':
        await p.teleport(XYZ(float(x), float(y), float(z)))

        await p.wait_for_zone_change()

        while not await p.is_in_npc_range():
            pass

        while await p.is_in_npc_range():
            await asyncio.sleep(.4)
            await p.send_key(Keycode.X, 0.1)

        await asyncio.sleep(4)

    elif zoneAccessType == 'xSkipRideMarleyboneIronworksReturn':
        await p.teleport(XYZ(float(x), float(y), float(z)))
        await asyncio.sleep(1)

        await p.mouse_handler.activate_mouseless()

        try:
            await p.mouse_handler.click_window_with_name('centerButton')
        except ValueError:
            await asyncio.sleep(0.01)

        await p.wait_for_zone_change()

        while not await p.is_in_npc_range():
            pass

        while await p.is_in_npc_range():
            await asyncio.sleep(.4)
            await p.send_key(Keycode.X, 0.1)

        await p.wait_for_zone_change()

        await p.mouse_handler.deactivate_mouseless()

    elif zoneAccessType == 'xNoWaitSkipRideMarleyboneHydeReturn':
        await p.teleport(XYZ(float(x), float(y), float(z)))

        await p.wait_for_zone_change()

        while not await p.is_in_npc_range():
            pass

        while await p.is_in_npc_range():
            await asyncio.sleep(.4)
            await p.send_key(Keycode.X, 0.1)

        await p.wait_for_zone_change()

    elif zoneAccessType == 'dungeonSkipRideMarleyboneIronworks':
        await asyncio.sleep(1)

        await p.teleport(XYZ(float(x), float(y), float(z)))
        while not await p.is_in_npc_range():
            pass

        while await p.is_in_npc_range():
            await asyncio.sleep(.4)
            await p.send_key(Keycode.X, 0.1)

        await p.wait_for_zone_change()

        while not await p.is_in_npc_range():
            pass

        while await p.is_in_npc_range():
            await asyncio.sleep(.4)
            await p.send_key(Keycode.X, 0.1)

        await p.wait_for_zone_change()

    elif zoneAccessType == 'xSkipRideMarleyboneIronworksReturn':
        await p.send_key(Keycode.PAGE_UP, 0.1)
        await p.wait_for_zone_change()


    # special case, krokotopia obelisks
    elif zoneAccessType == 'xNoWaitKrokObelisk':
        # Obelisk 1 (to Tomb of Storms)
        await p.teleport(XYZ(-3287.2294921875, -2826.498779296875, -35.353118896484375))
        while not await p.is_in_npc_range():
            pass

        # print('sent x press for obelisk 1')
        while await p.is_in_npc_range():
            await asyncio.sleep(.4)
            await p.send_key(Keycode.X, 0.1)
            await p.send_key(Keycode.X, 0.1)
            await p.send_key(Keycode.X, 0.1)
            await p.send_key(Keycode.X, 0.1)
            await p.send_key(Keycode.X, 0.1)

        await asyncio.sleep(.5)

        # Obelisk 2 (to Tomb of Storms)
        await p.teleport(XYZ(-4532.013671875, -2590.87451171875, -35.353668212890625))
        while not await p.is_in_npc_range():
            pass

        while await p.is_in_npc_range():
            await asyncio.sleep(.4)
            await p.send_key(Keycode.X, 0.1)
            await p.send_key(Keycode.X, 0.1)
            await p.send_key(Keycode.X, 0.1)
            await p.send_key(Keycode.X, 0.1)
            await p.send_key(Keycode.X, 0.1)
        await asyncio.sleep(.5)

        # Obelisk 3 (to Tomb of Storms)
        await p.teleport(XYZ(-4274.5419921875, -1374.5045166015625, -35.353607177734375))
        while not await p.is_in_npc_range():
            pass

        await asyncio.sleep(.5)
        while await p.is_in_npc_range():
            await asyncio.sleep(.4)
            await p.send_key(Keycode.X, 0.1)
            await p.send_key(Keycode.X, 0.1)
            await p.send_key(Keycode.X, 0.1)
            await p.send_key(Keycode.X, 0.1)
            await p.send_key(Keycode.X, 0.1)
        logger.info("Waiting a long time for the mouth thing to open")
        await asyncio.sleep(20)
        logger.info("If you haven't changed zones by now, manually turn on the obelisks and walk to the zone gate.  The script should continue after you change zones")

        # Zone Change - Tomb of Storms
        # Teleport to front of mouth thing
        await p.teleport(XYZ(-3364.827392578125, -1802.46630859375, -35.354522705078125))

        await p.wait_for_zone_change()

    elif zoneAccessType == 'dungeonDragonSpireGrandChasm':
        await asyncio.sleep(1)
        await p.send_key(Keycode.PAGE_DOWN, 0.1)

        await p.teleport(XYZ(float(x), float(y), float(z)))

        await asyncio.sleep(.5)
        await p.send_key(Keycode.X, 0.1)
        await p.send_key(Keycode.X, 0.1)
        await p.send_key(Keycode.X, 0.1)
        await p.send_key(Keycode.X, 0.1)
        await p.send_key(Keycode.X, 0.1)
        await p.wait_for_zone_change()

        await asyncio.sleep(.3)

        await p.teleport(XYZ(1.292851448059082, 227.6787567138672, 24.999969482421875))
        await asyncio.sleep(1)
        await p.send_key(Keycode.X, 0.1)
        await p.send_key(Keycode.X, 0.1)
        await p.send_key(Keycode.X, 0.1)
        await p.send_key(Keycode.X, 0.1)
        await p.send_key(Keycode.X, 0.1)


        #await asyncio.sleep(10)
        #await p.teleport(XYZ(-4138.177734375, 4193.40185546875, 30.1983642578125))
        await asyncio.sleep(1)

    elif zoneAccessType == 'dungeonExitConfirmMana':
        await p.send_key(Keycode.PAGE_UP, 0.1)
        await p.send_key(Keycode.PAGE_UP, 0.1)
        await p.send_key(Keycode.PAGE_UP, 0.1)
        await p.wait_for_zone_change()


    elif zoneAccessType == 'xSkipRideDragonspireRoost':
        await p.send_key(Keycode.PAGE_DOWN)

        await p.teleport(XYZ(float(x), float(y), float(z)))

        while not await p.is_in_npc_range():
            pass

        while await p.is_in_npc_range():
            await p.send_key(Keycode.X, 0.1)
            await asyncio.sleep(.4)

        await p.wait_for_zone_change()

        await p.send_key(Keycode.SPACEBAR, 0.1)
        await p.send_key(Keycode.SPACEBAR, 0.1)
        await p.send_key(Keycode.SPACEBAR, 0.1)
        await p.send_key(Keycode.SPACEBAR, 0.1)
        await p.send_key(Keycode.SPACEBAR, 0.1)

        await asyncio.sleep(.5)

        while not await p.is_in_npc_range():
            pass

        while await p.is_in_npc_range():
            await p.send_key(Keycode.X, 0.1)
            await asyncio.sleep(.4)

        await p.wait_for_zone_change()

        await p.send_key(Keycode.SPACEBAR, 0.1)
        await p.send_key(Keycode.SPACEBAR, 0.1)
        await p.send_key(Keycode.SPACEBAR, 0.1)
        await p.send_key(Keycode.SPACEBAR, 0.1)
        await p.send_key(Keycode.SPACEBAR, 0.1)

        await asyncio.sleep(.5)

        await asyncio.sleep(1)

    elif zoneAccessType == 'xNoWaitDragonSpireReturnToAcademy':
        await p.send_key(Keycode.PAGE_UP, 0.1)

        await p.wait_for_zone_change()

    elif zoneAccessType == 'dungeonExitConfirmCelestiaTemple':

        if await p.is_in_dialog():
            await go_through_dialog(p)

        await asyncio.sleep(.3)
        await p.send_key(Keycode.SPACEBAR, 0.1)
        await p.send_key(Keycode.SPACEBAR, 0.1)
        await p.send_key(Keycode.SPACEBAR, 0.1)
        await p.send_key(Keycode.SPACEBAR, 0.1)
        await p.send_key(Keycode.SPACEBAR, 0.1)

        await asyncio.sleep(1)

        await p.teleport(XYZ(float(x), float(y), float(z)))

        await p.mouse_handler.activate_mouseless()
        await asyncio.sleep(1)

        try:
            await p.mouse_handler.click_window_with_name('centerButton')
        except ValueError:
            await asyncio.sleep(0.01)

        await p.mouse_handler.deactivate_mouseless()

        await p.wait_for_zone_change()

    elif zoneAccessType == 'khrysDungeon1':
        await p.teleport(XYZ(float(x), float(y), float(z)))

        await asyncio.sleep(2)

        while not await p.is_in_npc_range():
            pass

        while await p.is_in_npc_range():
            await p.send_key(Keycode.X, 0.1)
            await asyncio.sleep(.4)

        await p.wait_for_zone_change()
        # teleport to second zone door
        await p.teleport(XYZ(1647.79248046875, 29.44374656677246, 6.103515625e-05))
        await p.wait_for_zone_change()
        await asyncio.sleep(2)


    elif zoneAccessType == 'khrysSerpentIsland':
        await p.teleport(XYZ(float(x), float(y), float(z)))
        await p.wait_for_zone_change()
        await asyncio.sleep(2)

        await p.teleport(XYZ(1647.79248046875, 29.44374656677246, 6.103515625e-05))
        await asyncio.sleep(1)
        await p.send_key(Keycode.X, 0.1)
        await p.send_key(Keycode.X, 0.1)
        await p.send_key(Keycode.X, 0.1)
        await p.send_key(Keycode.X, 0.1)
        await p.send_key(Keycode.X, 0.1)
        await asyncio.sleep(4)

        await p.teleport(XYZ(7662.78564453125, 7625.587890625, 1265.4591064453125))
        await asyncio.sleep(.6)


# uses an interactive teleporter (such as those in empyrea and later worlds) to teleport between zones
@logger.catch()
async def interactiveTeleportToZone(p, menuButtonNumber):

    while not await p.is_in_npc_range():
        pass

    while await p.is_in_npc_range():
        await p.send_key(Keycode.X, 0.1)
        await asyncio.sleep(.4)

    await asyncio.sleep(.4)
    await p.mouse_handler.activate_mouseless()

    # 4 buttons per page - menuButtonNum / 4 rounded up to nearest whole number equals the page that the button is on
    actualButtonToClick = menuButtonNumber

    if menuButtonNumber > 4:
        pageNum = int(math.ceil(menuButtonNumber / 4)) - 1
        # click to correct page
        if pageNum > 0:
            for i in range(pageNum):
                await p.mouse_handler.click_window_with_name('rightButton')
                await asyncio.sleep(0.4)

        # the actual button number on the page, considering that there are 4 buttons per page (0 -> 3)
        actualButtonToClick = ((menuButtonNumber) - ((pageNum) * 4))

    await p.mouse_handler.click_window_with_name('opt' + str(actualButtonToClick - 1))
    await asyncio.sleep(.4)
    await p.mouse_handler.click_window_with_name('teleportButton')
    await p.wait_for_zone_change()

    await p.mouse_handler.deactivate_mouseless()


@logger.catch()
async def createStack(p1WorldName):

    lines = await parseFile("traversalData/zoneMap.txt", p1WorldName)

    lines = iter(lines)
    stack = []
    stackPaths = []
    fullZonePaths = []

    for line in lines:
        if 'END' in line:
            break

        indent = len(list(takewhile(is_tab, line)))
        newList = []

        stack[indent:] = newList
        stack[indent:] = [line.lstrip()]
        stackPaths[indent:] = [line.lstrip().split(';')]
        fullZonePaths.append(stackPaths[:])

    return fullZonePaths


@logger.catch()
# returns true if a special interactable teleporter was found and teleported to
async def teleportToInteractiveTeleportIfAvailable(p, currentZone, destinationZone, teleporterList):

    currentTeleporter = ''
    destinationZoneButtonNumber = ''
    for i in teleporterList:
        if i.strip() == 'END':
            break

        splitTeleporter = i.strip().split(';')

        if splitTeleporter[4].strip() == currentZone and splitTeleporter[4].strip() == destinationZone:
            currentTeleporter = ''
            destinationZoneButtonNumber = ''
            break

        elif splitTeleporter[4].strip() == currentZone.strip():
            currentTeleporter = i

        elif splitTeleporter[4].strip() == destinationZone.strip():
            destinationZoneButtonNumber = splitTeleporter[0].strip().split('_', 1)[1]

    # teleporter found in both current zone and destination zone.  This is our path
    if currentTeleporter != '' and destinationZoneButtonNumber != '':
        split = currentTeleporter.strip().split(';')

        await p.teleport(XYZ(float(split[1]), float(split[2]), float(split[3])), wait_on_inuse=True)
        await asyncio.sleep(.4)

        await interactiveTeleportToZone(p, int(destinationZoneButtonNumber) + 1)
        return True
    else:
        return False


async def read_control_checkbox_text(checkbox: Window) -> str:
    return await checkbox.read_wide_string_from_offset(616)


@logger.catch()
# trace back to the nearest spiral door and teleport to destinationWorld
async def goToNewWorld(p, destinationWorld):
    while not await p.is_in_npc_range():
        pass

    while await p.is_in_npc_range():
        await p.send_key(Keycode.X, 0.1)
        await asyncio.sleep(.4)

    await p.mouse_handler.activate_mouseless()

    # each worldList item (in-file name for a world) correlates to a zoneDoorOptions (in-file name for the buttons in the spiral door)
    worldList = ["WizardCity", "Krokotopia", "Marleybone", "MooShu", "DragonSpire", "Grizzleheim", "Celestia", "Wysteria", "Zafaria", "Avalon", "Azteca", "Khrysalis", "Polaris", "Arcanum", "Mirage", "Empyrea", "Karamelle", "Lemuria"]
    zoneDoorOptions = ["wbtnWizardCity", "wbtnKrokotopia", "wbtnMarleybone", "wbtnMooShu", "wbtnDragonSpire", "wbtnGrizzleheim", "wbtnCelestia", "wbtnWysteria", "wbtnZafaria", "wbtnAvalon", "wbtnAzteca", "wbtnKhrysalis", "wbtnPolaris", "wbtnArcanum", "wbtnMirage", "wbtnEmpyrea", "wbtnKaramelle", "wbtnLemuria"]
    zoneDoorNameList = ["Wizard City", "Krokotopia", "Marleybone", "MooShu", "Dragonspyre", "Grizzleheim", "Celestia", "Wysteria", "Zafaria", "Avalon", "Azteca", "Khrysalis", "Polaris", "Arcanum", "Mirage", "Empyrea", "Karamelle", "Lemuria"]

    option_window = await p.root_window.get_windows_with_name("optionWindow")

    assert len(option_window) == 1, str(option_window)

    # Get page count, current selected page number, and max page number
    for child in await option_window[0].children():
        if await child.name() == 'pageCount':
            pageCount = await child.maybe_text()
            pageCount = pageCount[8:-9]
            currentPage = pageCount.split('/', 1)[0]
            maxPage = pageCount.split('/', 1)[1]
            break

    # user could be on any of the three pages when opening the world door depending on what their active quest is
    # switch all the way to the first page to standardize it
    # in case wizwalker misclicked / didn't click enough originally when resetting to page 1, ensure we are on page 1 (and if not click over again)
    while str(currentPage) != '1':
        await p.mouse_handler.click_window_with_name('leftButton')
        await asyncio.sleep(0.2)
        for child in await option_window[0].children():
            if await child.name() == 'pageCount':
                pageCount = await child.maybe_text()
                pageCount = pageCount[8:-9]
                currentPage = pageCount.split('/', 1)[0]
    worldIndex = -1
    for i in range(len(worldList)):
        if worldList[i] in destinationWorld:
            worldIndex = i
            break
    if worldIndex == -1:
        logger.error("destination not found!")
        return
    spiralGateName = zoneDoorNameList[worldIndex]

    isChildFound = False

    for i in range(int(maxPage)):
        for child in await option_window[0].children():
            if await child.name() in ['opt0', 'opt1', 'opt2', 'opt3']:
                name = await read_control_checkbox_text(child)
                if name == spiralGateName:
                    await p.mouse_handler.click_window_with_name(zoneDoorOptions[worldIndex])
                    await asyncio.sleep(.4)
                    await p.mouse_handler.click_window_with_name('teleportButton')
                    await p.wait_for_zone_change()

                    await p.mouse_handler.deactivate_mouseless()

                    # move away from the spiral door so we dont accidentally click on it again after teleporting later
                    await p.send_key(Keycode.W, 1.5)

                    isChildFound = True
                    break

        # correct world was not found - check the next page
        if not isChildFound:
            previousPage = currentPage
            loopCount = 0
            while currentPage == previousPage and loopCount < 30:
                loopCount += 1
                await p.mouse_handler.click_window_with_name('rightButton')

                # ensure that wizwalker didn't misclick and that we actually changed pages
                for child in await option_window[0].children():
                    if await child.name() == 'pageCount':
                        pageCount = await child.maybe_text()
                        pageCount = pageCount[8:-9]
                        currentPage = pageCount.split('/', 1)[0]
    return

async def parseFile(fileName, worldName):
    file = open(resource_path(f"{cur_path}/{fileName}"), "r")

    lines = file.readlines()
    start = 'WORLD - ' + worldName + '\n'

    try:
        indexStart = lines.index(start)
        removeIndex = indexStart + 1
        lines = lines[removeIndex:]
    except ValueError:
        await asyncio.sleep(.01)

    return lines


@logger.catch()
# from any zone in any world (excluding certain ones, such as aquila), travel to a destination zone
async def goToDestination(p, destinationZone, p1WorldName):
    currentZone = await p.zone_name()
    pathToZone = getPath(currentZone.lower(), destinationZone)
    for path in pathToZone.items():
        if currentZone == destinationZone:
           break
        zone_name = path[0]
        path_details = path[1]
        if zone_name == "zonedoor":
            await p.teleport(XYZ(path_details['x'], path_details['y'], path_details['z']))
            await asyncio.sleep(2)
            await goToNewWorld(p, destinationZone)
            logger.info(f'User in wrong world - heading to {destinationZone}')
        else:
            path_details = path[1]
            await gateTypeDifferentiation(path_details['x'], path_details['y'], path_details['z'],  p, path_details['type'])
        currentZone = await p.zone_name()


@logger.catch()
async def toZoneDisplayName(clients, destinationZoneDisplay):
    worldAbbreviations = ['WC', 'KT', 'MB', 'MS', 'DS', 'GH', 'CL', 'WT', 'ZF', 'AV', 'AZ', 'KR', 'PL', 'AC', 'MI', 'EM', 'KM', 'LM']
    worldList = ["WizardCity", "Krokotopia", "Marleybone", "MooShu", "DragonSpire", "Grizzleheim", "Celestia",
                 "Wysteria", "Zafaria", "Avalon", "Azteca", "Khrysalis", "Polaris", "Arcanum", "Mirage", "Empyrea",
                 "Karamelle", "Lemuria"]

    file = open(resource_path(f"{cur_path}/{'traversalData/displayZones.txt'}"), "r")
    lines = file.readlines()
    lines = iter(lines)
    destinationZone = ''

    # if specific world command was used, create a new list of zones only within the specified world
    for abbreviation in worldAbbreviations:
        if destinationZoneDisplay.startswith(abbreviation + ' '):
            abbrIndex = worldAbbreviations.index(abbreviation)
            worldLines = []
            world = worldList[abbrIndex]

            for q, s in enumerate(lines):
                split = s.split(';')
                if split[0] == world:
                    worldLines.append(s)

                lines = iter(worldLines)

            # for some reason this code runs even with the if statement evaluates to false... unless there is a print statement here
            # blame python idk what to tell you
            destinationZoneDisplay = destinationZoneDisplay.split(abbreviation + ' ')[1]

    # if any(destinationZoneDisplay.startswith(abbreviation + ' ') for abbreviation in worldAbbreviations):


    for q, s in enumerate(lines):
        s = s.split(';')

        # substring match instead of equality - it is acceptable for users to guess a partial zone name
        if destinationZoneDisplay.lower() in s[2].lower().strip():
            destinationZone = s[1]
            break

    if destinationZone != '':
        zoneChange = await toZone(clients, destinationZone)
        return zoneChange
    else:
        logger.error('Given zone either does not exist, is not valid, or was spelled incorrectly.')
        return 1


@logger.catch()
async def toZone(clients, destinationZone):
    currentZone = await clients[0].zone_name()
    worldName = currentZone.split('/', 1)[0]

    try:
        await asyncio.gather(*[goToDestination(p, destinationZone, worldName) for p in clients])
        logger.info(f'reached destination zone: {destinationZone}.')
        return 0
    except:
        print(traceback.print_exc())
        return 1



potion_ui_buy = [
    "fillallpotions",
    "buyAction",
    "btnShopPotions",
    "centerButton",
    "fillonepotion",
    "buyAction",
    "exit"
]



# Credit to Notfaj and Slackaduts for the majority of this function from UniversalBotSF
@logger.catch()
async def refillPotions(clients):
    await toZone(clients, 'WizardCity/WC_Ravenwood_Teleporter')

    # Walk to potion vendor
    for client in clients:

        try:
            await client.mouse_handler.activate_mouseless()
        except:
            logger.error('MOUSELESS ERROR')

        await client.goto(-0.5264079570770264, -3021.25244140625)
        await client.send_key(Keycode.W, 0.5)
        await client.wait_for_zone_change()
        await client.goto(11.836355209350586, -1816.455078125)
        await client.send_key(Keycode.W, 0.5)
        await client.wait_for_zone_change()
        await client.goto(-587.87927246093752, 404.43939208984375)
        await asyncio.sleep(1)
        await client.goto(-3965.254638671875, 1535.5472412109375)
        await asyncio.sleep(1)
        await client.goto(-4442.06005859375, 1001.5532836914062)
        await asyncio.sleep(1)
        while not await client.is_in_npc_range():
            await client.goto(-4442.06005859375, 1001.5532836914062)
        await client.send_key(Keycode.X, 0.1)
        await asyncio.sleep(1)
        # Buy potions
        while True:
            try:
                for i in "fillallpotions", "buyAction", "btnShopPotions", "centerButton", "fillonepotion", "buyAction", "exit":
                    await client.mouse_handler.click_window_with_name(i)
                    await asyncio.sleep(0.4)
            except ValueError:
                continue
            break

        try:
            await client.mouse_handler.deactivate_mouseless()
        except:
            logger.error('MOUSELESS ERROR')

        # Return
        await client.send_key(Keycode.PAGE_UP, 0.1)
        await client.wait_for_zone_change()


@logger.catch()
async def main(clientHandler):
    clientHandler.get_new_clients()
    clients = clientHandler.get_ordered_clients()
    p1, p2, p3, p4 = [*clients, None, None, None, None][:4]
    for i, p in enumerate(clients, 1):
        p.title = "p" + str(i)

    # Hook activation
    for p in clients:
        logger.info(f"[{p.title}] Activating Hooks")
        await p.activate_hooks()

    logger.info('Hooks activated!')
    try:
        await toZoneDisplayName(clients, 'golem court')
    finally:
        logger.info('Script complete')


async def run():
  clientHandler = ClientHandler()

  try:
    await main(clientHandler)
  except:
    import traceback

    traceback.print_exc()

  await clientHandler.close()


if __name__ == "__main__":
    asyncio.run(run())
