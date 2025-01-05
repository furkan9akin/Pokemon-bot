import discord
from discord.ext import commands
from logic import Pokemon, Warrior, Mage
import random
from config import token

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def go(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        chance = random.randint(1, 3)
        if chance == 1:
            pokemon = Pokemon(author)
        elif chance == 2:
            pokemon = Warrior(author)
        elif chance == 3:
            pokemon = Mage(author)
        await ctx.send(await pokemon.info())
        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Gagal memuat gambar Pokémon.")
    else:
        await ctx.send("Anda sudah memiliki Pokémon!")

@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None
    if target:
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]
            attacker = Pokemon.pokemons[ctx.author.name]
            result = await attacker.attack(enemy)
            await ctx.send(result)
        else:
            await ctx.send("Kedua pemain harus memiliki Pokémon untuk pertarungan!")
    else:
        await ctx.send("Tetapkan pemain yang ingin Anda serang dengan menyebutnya.")

@bot.command()
async def info(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        await ctx.send(await pokemon.info())
    else:
        await ctx.send("Anda tidak memiliki Pokémon!")

@bot.command()
async def saldir(ctx, target):
    if target in Pokemon.pokemons.values() and ctx.author.name in Pokemon.pokemons.keys():
        attacker=Pokemon.pokemons[ctx.author.name]
        await ctx.send(await attacker.saldir(target))
    else:
        await ctx.send("Kendin mi savaşacağın pokemonla?")

@bot.command()
async def bilgi(ctx):
    if ctx.author.name in Pokemon.pokemons.keys():
        pokemon=Pokemon.pokemons[ctx.author.name]
        await ctx.send(await pokemon.info())
    else:
        ctx.send("Kendine pokemon seçiniz.")


@bot.command()
async def besle(ctx):
    if not hasattr(ctx.author, 'pokemon'):  # Kullanıcının Pokémon'u yoksa
        await ctx.send(f"{ctx.author.mention}, önce bir Pokémon seçmelisin!")
        return

    pokemon = ctx.author.pokemon

    # Pokémon'u besleme işlemi
    try:
        message = await pokemon.feed()
        await ctx.send(f"{ctx.author.mention}, {message}")
    except Exception as e:
        await ctx.send(f"{ctx.author.mention}, bir hata oluştu: {e}") 


bot.run(token)

