# -----------------------------
# Configuración del bot
# -----------------------------

import discord
from discord.ext import commands
import random
import os
import json

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

INVENTARIO_FILE = "inventario.json"

# -----------------------------
# Cargar inventario
# -----------------------------
if os.path.exists(INVENTARIO_FILE):
    with open(INVENTARIO_FILE, "r") as f:
        inventario = json.load(f)
else:
    inventario = {}

# -----------------------------
# Guardar inventario
# -----------------------------
def guardar_inventario():
    with open(INVENTARIO_FILE, "w") as f:
        json.dump(inventario, f, indent=4)

# -----------------------------
# Normalizar inventario completo
# -----------------------------
def actualizar_todo_inventario():
    categorias = ["Clase Social", "Familia", "Talento", "Grimorio", "Reino"]
    for user_id in inventario:
        inventario[user_id].setdefault("rr", {})
        inventario[user_id].setdefault("objetos", {})
        for cat in categorias:
            inventario[user_id]["rr"].setdefault(cat, 3 if cat != "Talento" else 1)
            inventario[user_id]["objetos"].setdefault(cat, [])
    guardar_inventario()

actualizar_todo_inventario()

# -----------------------------
# Función general spin
# -----------------------------
async def tirar_spin(ctx, categoria, items_dict, color=discord.Color.blue()):
    user_id = str(ctx.author.id)

    if user_id not in inventario:
        inventario[user_id] = {
            "rr": {
                "Clase Social": 3,
                "Familia": 3,
                "Talento": 1,
                "Grimorio": 3,
                "Reino": 3
            },
            "objetos": {
                "Clase Social": [],
                "Familia": [],
                "Talento": [],
                "Grimorio": [],
                "Reino": []
            }
        }

    if inventario[user_id]["rr"].get(categoria, 0) <= 0:
        await ctx.send(f"❌ {ctx.author.mention}, no te quedan RR para {categoria}!")
        return

    inventario[user_id]["rr"][categoria] -= 1

    if categoria == "Clase Social":
        ponderados = ["No tienes"] * 6 + ["Clase Plebeyo", "Clase Media", "Clase Noble"]
        elegido = random.choice(ponderados)
    else:
        elegido = random.choice(list(items_dict.keys()))

    imagen = items_dict.get(elegido)

    inventario[user_id]["objetos"][categoria] = [elegido]
    guardar_inventario()

    embed = discord.Embed(
        title=f"🎲 {ctx.author.display_name} ha sacado **{elegido}** en {categoria}!",
        color=color
    )

    if imagen:
        embed.set_image(url=imagen)

    embed.set_footer(text=f"Te quedan {inventario[user_id]['rr'][categoria]} RR en {categoria}")
    await ctx.send(embed=embed)

# -----------------------------
# ITEMS
# -----------------------------
ClaseSocial = {
    "Clase Plebeyo": "https://i.pinimg.com/736x/79/e0/1f/79e01fd9da05a2f2aabd49fde829ec77.jpg",
    "Clase Media": "https://i.pinimg.com/1200x/3b/df/81/3bdf81a2953900bc411141704a7a4488.jpg",
    "Clase Noble": "https://i.pinimg.com/1200x/b9/c0/2c/b9c02c0c9f1c2278e8f625b83cd737d2.jpg"
}

FamiliaPlebeyo = {
    "Staria": "https://i.pinimg.com/736x/d6/90/46/d6904644ee33d8c9e5503b1f402cf43f.jpg",
    "Sukehiro": "https://i.pinimg.com/control1/736x/b3/d0/71/b3d071b0d252608ad5c5e5220cb72c73.jpg",
    "Voltia": "https://i.pinimg.com/1200x/56/d7/44/56d744dcd0e27acbf6c008350a07f6ad.jpg",
    "Agrippa": "https://i.pinimg.com/1200x/3f/31/1d/3f311d447d518cb57bc982b99d006188.jpg",
    "Swing": "https://i.pinimg.com/736x/ca/ae/25/caae2584970789666061360408ebb044.jpg",
}

FamiliaClaseMedia = {
    "Faust": "https://i.pinimg.com/736x/d8/16/41/d8164177101f6263e72f1ecc941c85a6.jpg",
    "Granvorka": "https://i.pinimg.com/1200x/1f/85/1f/1f851f68bf2f13796bd6a733ac76a1f3.jpg",
    "Unsworth": "https://i.pinimg.com/736x/46/1b/a4/461ba4bd3e6118b88112bcfb2f56dcf7.jpg",
    "Enoteca": "https://i.pinimg.com/736x/b5/59/34/b5593449d194af29c5adf98fc77b83d2.jpg",
}

ClaseNoble = {
    "Roselei": "https://i.pinimg.com/736x/0d/74/be/0d74be5e8e1b9f45b45d5be34ed0df73.jpg",
    "Silva": "https://i.pinimg.com/1200x/da/91/21/da9121f77189b84f26fc65d437a96f4f.jpg",
    "Lunettes": "https://i.pinimg.com/736x/2b/a5/21/2ba5213d21cac1c1c532c89c99a7ea4d.jpg",
    "Vaude": "https://i.pinimg.com/1200x/71/a7/43/71a74308aa7d15ed1f7f26abbf0517f1.jpg",
    "Caseus": "https://i.pinimg.com/736x/7c/ca/db/7ccadb8848891ffb7652ec02df84a24b.jpg",
    "Boismortier": "https://i.pinimg.com/1200x/94/36/59/94365990aaa0e40063704b467e8394b3.jpg",
    "Novachrono": "https://i.pinimg.com/736x/34/a7/a1/34a7a1ccc3dbddea0daf2629c9d38944.jpg",
    "Vangeance": "https://i.pinimg.com/1200x/51/52/b9/5152b92de4dd72e030e44054efe2b097.jpg",
    "Grinberryal": "https://i.pinimg.com/736x/50/95/b8/5095b8f2eddb0c4960807c852825395b.jpg",
    "Vermillion": "https://i.pinimg.com/736x/2f/3b/7c/2f3b7c65da6b70c431bdc7dba6578488.jpg",
    "Kira": "https://i.pinimg.com/1200x/96/ff/9d/96ff9d3204f7b349bf4e1ee21abdadba.jpg",
}

Grimorio = {
    "3 hojas": "https://i.pinimg.com/1200x/7a/fe/09/7afe09ff61c8b311f05d2217638f6262.jpg",
    "4 hojas": "https://i.pinimg.com/736x/8d/02/5e/8d025e6a0b46a3f0095849c3edbd5299.jpg",
    "5 hojas": "https://i.pinimg.com/1200x/95/98/18/959818b45a30c4f19a851cc372bf4486.jpg"
}

Reino = {
    "Reino del Diamante": "https://i.pinimg.com/736x/1b/c7/23/1bc723b2957850f93020d9023a737dcd.jpg",
    "Reino del Corazón": "https://i.pinimg.com/736x/c7/2d/9a/c72d9a3366cd540ae87f6195ffcd40de.jpg",
    "Reino de la Pica": "https://i.pinimg.com/1200x/f3/3e/c2/f33ec2ec51db6d09532d8445a878a92f.jpg",
    "Reino del Trébol": "https://i.pinimg.com/1200x/b6/c7/55/b6c755d9a59acdda182acb0d2dbef4c2.jpg",
}

TALENTOS = {
    "Prodigio": "https://i.pinimg.com/736x/da/1e/90/da1e90524557ee189825504242c5753a.jpg",
    "Genio": "https://i.pinimg.com/736x/da/1e/90/da1e90524557ee189825504242c5753a.jpg",
    "Reencarnado": "https://i.pinimg.com/736x/da/1e/90/da1e90524557ee189825504242c5753a.jpg"
}

# -----------------------------
# COMANDOS SPIN
# -----------------------------
@bot.command(name="plebeyo")
async def cmd_plebeyo(ctx):
    await tirar_spin(ctx, "Familia", FamiliaPlebeyo, color=discord.Color.blurple())

@bot.command(name="media")
async def cmd_media(ctx):
    await tirar_spin(ctx, "Familia", FamiliaClaseMedia, color=discord.Color.green())

@bot.command(name="noble")
async def cmd_noble(ctx):
    await tirar_spin(ctx, "Familia", ClaseNoble, color=discord.Color.gold())

@bot.command(name="talento")
async def cmd_talento(ctx):
    await tirar_spin(ctx, "Talento", TALENTOS, color=discord.Color.orange())

@bot.command(name="grimorio")
async def cmd_grimorio(ctx):
    await tirar_spin(ctx, "Grimorio", Grimorio, color=discord.Color.gold())

@bot.command(name="clasesocial")
async def cmd_clasesocial(ctx):
    await tirar_spin(ctx, "Clase Social", ClaseSocial, color=discord.Color.gold())

# -----------------------------
# Comando de inventario
# -----------------------------
@bot.command(name="inventario")
async def inventario_cmd(ctx, miembro: discord.Member = None):
    if miembro is None:
        miembro = ctx.author
    user_id = str(miembro.id)

    # 🔥 ACTUALIZACIÓN AUTOMÁTICA POR USUARIO
    categorias = ["Clase Social", "Familia", "Talento", "Grimorio", "Reino"]
    if user_id not in inventario:
        inventario[user_id] = {"rr": {}, "objetos": {}}
    for cat in categorias:
        inventario[user_id]["rr"].setdefault(cat, 3 if cat != "Talento" else 1)
        inventario[user_id]["objetos"].setdefault(cat, [])
    guardar_inventario()

    embed = discord.Embed(
        title=f"🎒 Inventario de {miembro.display_name}",
        color=discord.Color.dark_teal()
    )

    for cat, items in inventario[user_id]["objetos"].items():
        lista = ", ".join(items) if items else "Vacío"
        embed.add_field(name=cat, value=lista, inline=False)

    rr_text = ", ".join(f"{cat}: {cantidad}" for cat, cantidad in inventario[user_id]["rr"].items())
    embed.set_footer(text=f"RR disponibles → {rr_text}")
    await ctx.send(embed=embed)

# -----------------------------
# Comandos admin: dar/quitar RR
# -----------------------------
@bot.command(name="dar_rr")
@commands.has_permissions(administrator=True)
async def dar_rr(ctx, miembro: discord.Member, categoria: str, cantidad: int):
    categoria = categoria.capitalize()
    if categoria not in ["Clase Social", "Familia", "Talento", "Grimorio", "Reino"]:
        await ctx.send("❌ Categoría inválida.")
        return
    user_id = str(miembro.id)
    # Normalizar inventario del usuario
    categorias = ["Clase Social", "Familia", "Talento", "Grimorio", "Reino"]
    if user_id not in inventario:
        inventario[user_id] = {"rr": {}, "objetos": {}}
    for cat in categorias:
        inventario[user_id]["rr"].setdefault(cat, 3 if cat != "Talento" else 1)
        inventario[user_id]["objetos"].setdefault(cat, [])
    inventario[user_id]["rr"][categoria] += cantidad
    guardar_inventario()
    await ctx.send(f"✅ Se han añadido {cantidad} RR de {categoria} a {miembro.display_name}.")

@bot.command(name="quitar_rr")
@commands.has_permissions(administrator=True)
async def quitar_rr(ctx, miembro: discord.Member, categoria: str, cantidad: int):
    categoria = categoria.capitalize()
    if categoria not in ["Clase Social", "Familia", "Talento", "Grimorio", "Reino"]:
        await ctx.send("❌ Categoría inválida.")
        return
    user_id = str(miembro.id)
    categorias = ["Clase Social", "Familia", "Talento", "Grimorio", "Reino"]
    if user_id not in inventario:
        inventario[user_id] = {"rr": {}, "objetos": {}}
    for cat in categorias:
        inventario[user_id]["rr"].setdefault(cat, 3 if cat != "Talento" else 1)
        inventario[user_id]["objetos"].setdefault(cat, [])
    inventario[user_id]["rr"][categoria] = max(0, inventario[user_id]["rr"][categoria] - cantidad)
    guardar_inventario()
    await ctx.send(f"✅ Se han quitado {cantidad} RR de {categoria} a {miembro.display_name}.")

# -----------------------------
# Comandos admin: dar/quitar objetos
# -----------------------------
@bot.command(name="dar_objeto")
@commands.has_permissions(administrator=True)
async def dar_objeto(ctx, miembro: discord.Member, categoria: str, *, nombre: str):
    categoria = categoria.capitalize()
    if categoria not in ["Clase Social", "Familia", "Talento", "Grimorio", "Reino"]:
        embed_error = discord.Embed(
            title="❌ Error",
            description="La categoría no es válida.\nCategorías válidas: Clase Social, Familia, Talento, Grimorio, Reino",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed_error)
        return
    user_id = str(miembro.id)
    categorias = ["Clase Social", "Familia", "Talento", "Grimorio", "Reino"]
    if user_id not in inventario:
        inventario[user_id] = {"rr": {}, "objetos": {}}
    for cat in categorias:
        inventario[user_id]["rr"].setdefault(cat, 3 if cat != "Talento" else 1)
        inventario[user_id]["objetos"].setdefault(cat, [])
    inventario[user_id]["objetos"][categoria].append(nombre)
    guardar_inventario()
    embed_confirm = discord.Embed(
        title="✅ Objeto añadido",
        description=f"{miembro.mention} ha recibido **{nombre}** en **{categoria}**",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed_confirm)

@bot.command(name="quitar_objeto")
@commands.has_permissions(administrator=True)
async def quitar_objeto(ctx, miembro: discord.Member, categoria: str, *, nombre: str):
    categoria = categoria.capitalize()
    if categoria not in ["Clase Social", "Familia", "Talento", "Grimorio", "Reino"]:
        embed_error = discord.Embed(
            title="❌ Error",
            description="La categoría no es válida.\nCategorías válidas: Clase Social, Familia, Talento, Grimorio, Reino",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed_error)
        return
    user_id = str(miembro.id)
    categorias = ["Clase Social", "Familia", "Talento", "Grimorio", "Reino"]
    if user_id not in inventario:
        inventario[user_id] = {"rr": {}, "objetos": {}}
    for cat in categorias:
        inventario[user_id]["rr"].setdefault(cat, 3 if cat != "Talento" else 1)
        inventario[user_id]["objetos"].setdefault(cat, [])
    if nombre not in inventario[user_id]["objetos"][categoria]:
        embed_error = discord.Embed(
            title="❌ Error",
            description=f"{miembro.mention} no tiene **{nombre}** en **{categoria}**",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed_error)
        return
    inventario[user_id]["objetos"][categoria].remove(nombre)
    guardar_inventario()
    embed_confirm = discord.Embed(
        title="✅ Objeto retirado",
        description=f"Se ha quitado **{nombre}** de **{categoria}** a {miembro.mention}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed_confirm)

@bot.command(name="reino")
async def cmd_reino(ctx):
    await tirar_spin(ctx, "Reino", Reino, color=discord.Color.gold())

import os

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)



