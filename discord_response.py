from enum import Enum

import discord

import xur_inventory

DESTINY_TRACKER = "https://destinytracker.com/destiny-2/db/items/"

embedded: bool = False


class Emoji(Enum):
    NONE = ''
    KINETIC = '<:kinetic:773719907371450379>'
    RAID = ''
    TITAN = '<:titan:773329359384608768>'
    HUNTER = '<:hunter:773329886244110346>'
    WARLOCK = '<:warlock:773329357627195402>'
    VOID = '<:void:773391417879298058>'
    SOLAR = '<:solar:773391417446891521>'
    ARC = '<:arc:773391417438765057>'


def hyperlink(item: dict) -> str:
    """Creates hyperlink to the item's light.gg page

    :param item:
        The item you are trying to hyperlink in the form of inventory['Class']

    :return: str
    """
    link = "[" + item['name'] + "]"
    link = link + "(" + DESTINY_TRACKER + str(item['hash']) + ")"
    return link


def message():
    """Creates an Embed that contains Xur's inventory, or a generic response if Xur is not available

    :return: string or Embed
    """
    global embedded
    try:
        embed = discord.Embed(
            title="Xûr, Agent of the Nine",
            description="A peddler of strange curios, Xûr's motives are not his own. He bows to his distant masters, the Nine.",
            color=discord.Color.blue()
        )
        embed.clear_fields()
        inventory = xur_inventory.items()
        embed.set_thumbnail(url='https://warmind.io/static/img/xur_icon.png')
        embed.add_field(name="**Location**", value=xur_inventory.location(), inline=False)
        embed.add_field(name=Emoji[inventory['Weapon']['damageType']].value + " **Weapon**",
                        value=hyperlink(inventory['Weapon']), inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="\u200b", value=inventory['Weapon']['type'], inline=True)
        embed.add_field(name=Emoji.TITAN.value + " **Titan**", value=hyperlink(inventory['Titan']), inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="\u200b", value=inventory['Titan']['type'], inline=True)
        embed.add_field(name=Emoji.HUNTER.value + " **Hunter**", value=hyperlink(inventory['Hunter']), inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="\u200b", value=inventory['Hunter']['type'], inline=True)
        embed.add_field(name=Emoji.WARLOCK.value + " **Warlock**", value=hyperlink(inventory['Warlock']), inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="\u200b", value=inventory['Warlock']['type'], inline=True)
        embed.set_footer(text='I will be leaving in ' + xur_inventory.leaving_datetime())
        embedded = True
        return embed
    except:
        embedded = False
        return "*I will return on Friday guardian*"
