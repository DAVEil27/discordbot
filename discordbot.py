import discord
from discord.ext import commands
import datetime
import requests
from PIL import Image, ImageFont, ImageDraw
import io
from math import *



PREFIX = '.'
client = commands.Bot( command_prefix = PREFIX)
client.remove_command( 'help' )

@client.event
async def on_ready():
    print('conected')

    await client.change_presence( status = discord.Status.online, activity = discord.Game( '.help' ) )

@client.event
async def on_member_join(member):
    channel = client.get_channel( 810903228383363113 )

    role = discord.utils.get( member.guild.roles, id = 811253715570524221 )

    await member.add_roles( role )
    await channel.send( embed = discord.Embed( description = f'user { member.name} joind our server. Have fun!'))

@client.command( pass_context=True )
@commands.has_permissions( administrator=True )

async def clearall( ctx, amount=99999 ):
    await ctx.channel.purge(limit = amount)


@client.command( pass_context=True )

async def clear( ctx ):
    await ctx.channel.purge(limit = 2)



@client.command( pass_context = True )
@commands.has_permissions( administrator = True)

async def kick( ctx, member: discord.Member, *, reason = None ):
     await ctx.channel.purge(limit = 1)

     await member.kick( reason = reason )
     await ctx.send(f'kick user {member.mention}')

@client.command( pass_context = True )
@commands.has_permissions( administrator = True)

async def ban( ctx, member: discord.Member, *, reason = None ):
    emb = discord.Embed( title = 'BAN!', colour = discord.Colour.dark_magenta())
    await ctx.channel.purge(limit = 1)

    await member.ban( reason = reason )
    await ctx.send(f'ban user {member.mention}')

    emb.set_author(name = member.name, icon_url = member.avatar_url)
    emb.add_field( name = 'Ban User', value = 'Banned user : {}'.format( member.mention ))
    emb.set_footer( text = 'Was banned by {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url)

    await ctx.send( embed = emb)

@client.command( pass_context = True )
@commands.has_permissions( administrator = True)

async def unban( ctx, *, member ):
    await ctx.channel.purge(limit = 1)

    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:
        user = ban_entry.user

        await ctx.guild.unban( user )
        await ctx.send(f'unband { user.mention }')

        return

@client.command( pass_context = True )
async def help(ctx):
    emb = discord.Embed(title = 'command info ')
    emb.add_field( name= '{}clear 2'.format( PREFIX ), value='clear last message (permision-everyone)')
    emb.add_field( name= '{}clearall'.format( PREFIX ), value='how many messages you want (permision-admin)')
    emb.add_field( name= '{}kick'.format( PREFIX ), value='kick particapent from server (permision-admin)')
    emb.add_field( name= '{}ban'.format( PREFIX ), value='ban particapent (permision-admin)')
    emb.add_field( name= '{}unban'.format( PREFIX ), value='unban particapent (permision-admin)')
    emb.add_field( name= '{}time'.format( PREFIX ), value='show current time (permision-everyone)')
    emb.add_field( name= '{}mute'.format( PREFIX ), value='mute particapent (permision-admin)')
    emb.add_field( name= '{}math'.format( PREFIX ), value='do simple math (permision-everyone)')
    emb.add_field( name= '{}card'.format( PREFIX ), value='show your discord card (permision-everyone),(you can also type ` me or i)')
    emb.add_field( name= '{}root'.format( PREFIX ), value='square root of your number (permision-everyone)')

    await ctx.send(embed = emb)

@client.command( pass_context = True )

async def time( ctx ):
    emb = discord.Embed( title = 'Open TimeServer', description = ' you can find out the current time ', colour = discord.Colour.dark_magenta(), url = 'https://www.timeserver.ru/')

    emb.set_author( name = client.user.name, icon_url = client.user.avatar_url )
    emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url )
    #emb.set_image(url = 'https://ctl.s6img.com/society6/img/jz5_vpJDdNvyk-OZb1ok6tUvHUk/w_1500/wall-clocks/front/natural-frame/black-hands/~artwork,fw_3500,fh_3500,iw_3500,ih_3500/s6-0036/a/16969701_5681453/~~/math-clock-clock-only-wall-clocks.jpg')
    emb.set_thumbnail(url = 'https://ctl.s6img.com/society6/img/jz5_vpJDdNvyk-OZb1ok6tUvHUk/w_1500/wall-clocks/front/natural-frame/black-hands/~artwork,fw_3500,fh_3500,iw_3500,ih_3500/s6-0036/a/16969701_5681453/~~/math-clock-clock-only-wall-clocks.jpg')

    now_date = datetime.datetime.now()

    emb.add_field( name = 'Time', value = 'Time : {}'.format(now_date) )

    await ctx.send( embed = emb)

@client.command()
@commands.has_permissions( administrator = True)

async def user_mute( ctx, member: discord.Member ):
    await ctx.channel.purge(limit = 1)

    mute_role = discord.utils.get( ctx.message.guild.roles, name = 'mute' )

    await member.add_roles( mute_role )
    await ctx.send(f'{ member.mention} is in mute')

@client.command()
async def math( ctx, a : float, arg, b : float ):
    if arg == '+':
        await ctx.send( f'Result: {a + b}')

    if arg == '-':
        await ctx.send( f'Result: {a - b}')

    if arg == '*':
        await ctx.send( f'Result: {a * b}')

    if arg == '/':
        await ctx.send( f'Result: {a / b}')

    if arg == '**':
        await ctx.send( f'Result: {a ** b}')


@client.command()
async def root( ctx, c : float):
    rt = sqrt(c)

    await ctx.send(f' Result: {rt}')

@client.command()
async def dis( ctx, a : float, b : float, c : float):
    d = sqrt(b**2 - 4*a*c)

    x1 = round((-b - d)/(2*a), 2)
    x2 = round((-b + d)/(2*a), 2)

    await ctx.send(f' first result is {x1} second result is {x2}')


@client.command()
async def sibo( ctx ):
    await ctx.send('@Человек Alex#5046 GO FUCK YOURSELF!')

@client.command(aliases = ['i', 'me', 'card'])
async def card_user(ctx):
    img = Image.new('RGBA', (400, 200), '#776B69')
    url = str(ctx.author.avatar_url)[:-10]
    resp = requests.get(url, stream = True)
    resp = Image.open(io.BytesIO(resp.content))
    resp = resp.convert('RGBA')
    resp = resp.resize((100, 100), Image.ANTIALIAS)

    img.paste(resp, (15, 15, 115, 115))

    idraw = ImageDraw.Draw(img)

    name = ctx.author.name
    teg = ctx.author.discriminator 

    headline = ImageFont.truetype('arial.ttf', size = 20)
    undertext = ImageFont.truetype('arial.ttf', size = 12)

    idraw.text((145, 15), f'{name}#{teg}', font = headline)
    idraw.text((145, 50), f'ID: {ctx.author.id}', font = undertext)

    img.save('user_card.png')

    await ctx.send(file = discord.File(fp = 'user_card.png'))

#connecting
client.run('ODEwOTIyMjcxNjM1MTQ0NzA0.YCqsNw.0N2U8LA2iu0Qua1-7q_yfQOz4vU')
