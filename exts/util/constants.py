#
# This file is part of Orbyt. (https://github.com/nxmrqlly/orbyt)
# Copyright (c) 2023-present Ritam Das
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from typing import Dict

from discord import Color


EMOJIS: Dict[str, str] = {
    "join": "<:join:994585439631589467>",
    "leave": "<:leave:994585508502065182>",
    "owner_icon": "<:owner_icon:995606433527779370>",
    "channel_rules": "<:channel_rules:995606482240405514>",
    "channel_announcements": "<:channel_announcements:995606523201990656>",
    "channel_text": "<:channel_text:995606584782770197>",
    "roles_icon": "<:roles_icon:995606689036390415>",
    "members_icon": "<:members_icon:995607179220496465>",
    "channel_vc": "<:channel_vc:995607246501314601>",
    "online": "<:online:995607290780586014>",
    "dnd": "<:dnd:995607316516835428>",
    "idle": "<:idle:995607331570208792>",
    "booster_shine": "<:booster_shine:995611491778711552>",
    "music_disk": "<a:music_disk:995764773637586974>",
    "no": "<:no:996055053628612699>",
    "yes": "<:yes:996055071433437184>",
    "typing": "<a:typing:996070776602116237>",
    "helloooo": "<a:helloooo:1002388645220724756>",
    "dictionary": "<:dictionary:1022525467095482518>",
    "network": "<:network:1080529982520037446>",
    "arrow_left": "<:arrow_left:1181986837485600808>",
    "arrow_right": "<:arrow_right:1181986841851867176>",
    "white_x": "<:white_x:1182286157883650079>",
    "white_tick": "<:white_tick:1182286160278597632>",
    "double_arrow_left": "<:double_arrow_left:1182917820997185536>",
    "double_arrow_right": "<:double_arrow_right:1182917823887061103>",
    "fall": "<a:fall:1192827407191773266>",
    "white_minus": "<:white_minus:1193218998079324200>",
    "white_plus": "<:white_plus:1193219000570761308>",
    "white_pencil": "<:white_pencil:1193231256939397193>",
    "white_json": "<:white_json:1193937212736294992>",
}

SECONDARY_COLOR = Color.from_str("#1f87a7")
BG_COLOR = Color.from_str("#081927")
ACCENT_COLOR = Color.from_str("#d3d3d3")
CONTRAST_COLOR = Color.from_str("#F0B232")

ASCII_TITLE = """
  .oooooo.             .o8                       .   
 d8P'  `Y8b           "888                     .o8   
888      888 oooo d8b  888oooo.  oooo    ooo .o888oo      By Nxrmqlly
888      888 `888""8P  d88' `88b  `88.  .8'    888        https://github.com/nxrmqlly/Orbyt
888      888  888      888   888   `88..8'     888
`88b    d88'  888      888   888    `888'      888 .      Copyright (C) 2023-present Ritam Das | AGPL v3
 `Y8bood8P'  d888b     `Y8bod8P'     .8'       "888" 
                                 .o..P'              
                                 `Y8P'               
"""

HTTP_URL_REGEX = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
