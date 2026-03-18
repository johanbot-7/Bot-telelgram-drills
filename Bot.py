import json
import os
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler,
)
from datetime import datetime

TOKEN = "8613703715:AAHHzducDO0j46k5xS0jyJ27QsAddFvsb7I"os.environ.get("TELEGRAM_TOKEN", "")
ADMIN_ID = 7957443258

USUARIOS_FILE = "usuarios.json"
INTENTOS_FILE = "intentos.json"
FUNCION17_FILE = "funcion17.json"
PEDIDOS_FILE = "pedidos.json"
MANTENIMIENTO_FILE = "mantenimiento.json"


# ------------------------
# JSON
# ------------------------

def cargar_json(file, default):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return default


def guardar_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)


usuarios = set(cargar_json(USUARIOS_FILE, []))
intentos = cargar_json(INTENTOS_FILE, {})
funcion17 = cargar_json(FUNCION17_FILE, {})
pedidos = cargar_json(PEDIDOS_FILE, [])
mantenimiento = cargar_json(MANTENIMIENTO_FILE, {"activo": False})


# ------------------------
# BASICO
# ------------------------

def es_admin(uid):
    return uid == ADMIN_ID


def esta_autorizado(uid):
    return str(uid) in usuarios or es_admin(uid)


def esta_bloqueado(uid):
    return intentos.get(str(uid), 0) >= 3


# ------------------------
# MENU
# ------------------------

menu_text = """━━━━━━━━━━━━━
OPCIONES DISPONIBLES🎮

1. Cromar calipers.
2. Cromar luces.
3. Ventanas GG.
4. Modificar 1 HP.
5. Cromar rines.
6. Cromar aleron.
7. Traspasar auto.
8. Modificar shiftime.
9. Quitar parachoques.
10. Auto 6 segundos.
11. Modificar ID.
12. 30k / 50M.
13. Comprar casas.
14. Cuenta full.
15. Auto Full GG.
16. FULL GG PREMIUM
17. Cuentas/Diseños.
18. 🔒Comandos (👑Admin.)
19. 🔒Comandos (👑Admin.)



━━━━━━━━━━━━━"""

menu_admin = """━━━━━━━━━━━━━
👑 PANEL ADMIN

1. Cromar calipers
2. Cromar luces
3. Ventanas GG
4. Modificar 1 HP
5. Cromar rines
6. Cromar aleron
7. Traspasar auto
8. Modificar shiftime
9. Quitar parachoques
10. Auto 6 segundos
11. Modificar ID
12. 30k / 50M
13. Comprar casas
14. Cuenta full
15. Auto Full GG
16. FULL GG PREMIUM
17. Cuentas/Diseños

━━━━━━━━━━━━━
⚙ ADMIN

18. Panel Admin
19. Ver Pedidos
━━━━━━━━━━━━━
"""

FORMULARIOS = {
    "1": ["📧 Correo electrónico", "🔐 Contraseña de la cuenta", "🚗 Modelo del vehículo"],
    "2": ["📧 Correo electrónico", "🔐 Contraseña de la cuenta", "🚗 Modelo del vehículo"],
    "3": ["📧 Correo electrónico", "🔐 Contraseña de la cuenta", "🚗 Modelo del vehículo"],
    "4": ["📧 Correo electrónico", "🔐 Contraseña de la cuenta"],
    "5": ["📧 Correo electrónico", "🔐 Contraseña de la cuenta", "🚗 Modelo del vehículo"],
    "6": ["📧 Correo electrónico", "🔐 Contraseña de la cuenta", "🚗 Modelo del vehículo"],
    "7": ["📧 Correo electrónico", "🔐 Contraseña de la cuenta"],
    "8": ["📧 Correo electrónico", "🔐 Contraseña de la cuenta"],
    "9": ["📧 Correo electrónico", "🔐 Contraseña de la cuenta"],
    "10": ["📧 Correo electrónico", "🔐 Contraseña de la cuenta"],
    "11": ["📧 Correo electrónico", "🔐 Contraseña de la cuenta", "Nuevo ID:"],
    "12": ["📧 Correo electrónico", "🔐 Contraseña de la cuenta"],
    "13": ["📧 Correo electrónico", "🔐 Contraseña de la cuenta"],
    "14": ["📧 Correo electrónico", "🔐 Contraseña de la cuenta"],
    "15": ["📧 Correo electrónico", "🔐 Contraseña de la cuenta", "🚗 ID DEL AUTO"],
    "16": [
        "📧 Correo electrónico",
        "🔐 Contraseña de la cuenta",
        "🚗 Modelo del vehículo"
    ],
    "17": [],
}

OPCIONES_CON_COLOR = {"1", "2", "3", "5", "6", "15"}
OPCION_FULL_GG = "16"

user_states = {}


# ------------------------
# START
# ------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    uid = user.id
    uid_str = str(uid)

    if esta_bloqueado(uid):
        return

    if mantenimiento["activo"] and not es_admin(uid):
        await update.message.reply_text(
            "━━━━━━━━━━━━━\n"
            "🔧 MANTENIMIENTO 🔧\n"
            "━━━━━━━━━━━━━\n\n"
            "El bot se encuentra en mantenimiento temporal.\n\n"
            "⏳ Por favor intenta más tarde.\n\n"
            "Disculpa las molestias 🙏\n"
            "━━━━━━━━━━━━━"
        )
        return

    if esta_autorizado(uid):

        if es_admin(uid):
            await update.message.reply_text(menu_admin)
        else:
            await update.message.reply_text(menu_text)

        await update.message.reply_text(
            "Elige una función respondiendo con el número correspondiente:"
        )
        return

    intentos[uid_str] = intentos.get(uid_str, 0) + 1
    guardar_json(INTENTOS_FILE, intentos)

    if intentos[uid_str] >= 3:

        await update.message.reply_text(
            "🚫 Has sido bloqueado permanentemente por intentar explotar el bot. Si crees que es un error, contacta al administrador."
        )

        fecha = datetime.now().strftime("%d/%m/%Y")
        hora = datetime.now().strftime("%H:%M:%S")

        texto = f"""🚫═════════════════🚫
      🚫  USUARIO BLOQUEADO  🚫
🚫═════════════════🚫

👤  NOMBRE
└➤ {user.first_name}

🔗  USUARIO
└➤ @{user.username}

🆔  ID DEL USUARIO
└➤ {user.id}

📅  FECHA
└➤ {fecha}

⏰  HORA
└➤ {hora}

⚠️ ACCESO DENEGADO
Este usuario se encuentra en la
lista de usuarios bloqueados.
"""

        fotos = await context.bot.get_user_profile_photos(uid)

        if fotos.total_count > 0:
            file = fotos.photos[0][-1].file_id
            await context.bot.send_photo(ADMIN_ID, file, caption=texto)
        else:
            await context.bot.send_message(ADMIN_ID, texto)

        return

    await update.message.reply_text(
        "🚫 No tienes acceso a este bot. Contacta al administrador @drillscars para solicitar acceso."
    )


# ------------------------
# MANEJO FORMULARIOS
# ------------------------

async def manejar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    uid = update.effective_user.id
    texto = update.message.text.strip()

    if mantenimiento["activo"] and not es_admin(uid):
        await update.message.reply_text(
            "━━━━━━━━━━━━━\n"
            "🔧 MANTENIMIENTO 🔧\n"
            "━━━━━━━━━━━━━\n\n"
            "El bot se encuentra en mantenimiento temporal.\n\n"
            "⏳ Por favor intenta más tarde.\n\n"
            "Disculpa las molestias 🙏\n"
            "━━━━━━━━━━━━━"
        )
        return

    opciones_validas = list(FORMULARIOS.keys()) + ["17", "18", "19"]

    if texto not in opciones_validas and uid not in user_states:
        await update.message.reply_text("❌ Ese comando no existe")
        return

    # 🔹 OPCION 18
    if texto == "18":

        tiempo = funcion17.get(str(uid))

        if not tiempo or tiempo < time.time():
            await update.message.reply_text("❌ No tienes acceso a función 17")
            return

        await update.message.reply_text("👑¡Bienvenido Admin!")

        botones = [[
            InlineKeyboardButton("📢 Canal", url="https://t.me/bot_multifunciones_cpm_drill_bot"),
            InlineKeyboardButton("👑¡Comandos Admin!", callback_data="comando"),
            InlineKeyboardButton("respuestas", callback_data="respuestas")
        ]]

        teclado = InlineKeyboardMarkup(botones)

        await update.message.reply_text(
            "⚙️ Panel de la función 17",
            reply_markup=teclado
        )
        return

    # 🔹 OPCION 19
    if texto == "19":

        if not es_admin(uid):
            await update.message.reply_text("❌ Solo admin puede usar esto")
            return

        if not pedidos:
            await update.message.reply_text("📦 No hay pedidos pendientes")
            return

        for i, p in enumerate(pedidos):

            mensaje = f"""📦 PEDIDO #{i+1}

👤 Usuario: @{p['usuario']}
🆔 ID: {p['id']}

📌 Opción: {p['opcion']}
📧 Correo: {p['correo']}
🎨 Color: {p['color']}

📅 {p['fecha']}  ⏰ {p['hora']}

━━━━━━━━━━━━━━━━━━
{p['datos']}
"""

            botones = [[
                InlineKeyboardButton("✅ Completar", callback_data=f"completar_{i}")
            ]]

            await update.message.reply_text(
                mensaje,
                reply_markup=InlineKeyboardMarkup(botones)
            )

        return

    # 🔹 OPCION 17
    if texto == "17":

        await update.message.reply_text("¡Selecciona Un Bot!")

        botones = [[
            InlineKeyboardButton("Bot Cuentas", url="https://t.me/bot_acuunts_drills_bot"),
            InlineKeyboardButton("Bot Diseños", url="https://t.me/personalizados_drills_bot")
        ]]

        teclado = InlineKeyboardMarkup(botones)

        await update.message.reply_text(
            "Bots Disponibles:",
            reply_markup=teclado
        )
        return

    # 🔹 FORMULARIOS
    if texto in FORMULARIOS:

        user_states[uid] = {
            "opcion": texto,
            "preguntas": FORMULARIOS[texto],
            "respuestas": [],
            "paso": 0
        }

        await update.message.reply_text(FORMULARIOS[texto][0] + ":")
        return

    # 🔹 PROCESO DE RESPUESTAS
    if uid in user_states:

        estado = user_states[uid]

        # VALIDAR CORREO
        if estado["paso"] == 0:
            if "@" not in texto or "." not in texto:
                await update.message.reply_text(
                    "❌ Correo inválido.\n\nDebe contener @ y .\nEjemplo: correo@gmail.com"
                )
                return

        # VALIDAR CONTRASEÑA
        if estado["paso"] == 1:
            if len(texto) < 6:
                await update.message.reply_text(
                    "❌ Contraseña inválida.\n\nDebe tener mínimo 6 caracteres."
                )
                return

        # VALIDAR MODELO DEL AUTO (SOLO NÚMEROS)
        if estado["paso"] == 2:
            if not texto.isdigit():
                await update.message.reply_text(
                    "❌ Modelo inválido.\n\nSolo se permiten números."
                )
                return

        estado["respuestas"].append(texto)
        estado["paso"] += 1

        if estado["paso"] < len(estado["preguntas"]):
            await update.message.reply_text(
                estado["preguntas"][estado["paso"]] + ":"
            )
            return

        opcion = estado["opcion"]

        # ⭐ OPCION 16 FULL GG PREMIUM
        if opcion == "16":

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🔴 Rojo", callback_data="aleron_rojo"),
                    InlineKeyboardButton("🔵 Azul", callback_data="aleron_azul")
                ],
                [
                    InlineKeyboardButton("🟢 Verde", callback_data="aleron_verde"),
                    InlineKeyboardButton("⚪ Blanco", callback_data="aleron_blanco")
                ]
            ])

            estado["paso_color"] = "aleron"

            await update.message.reply_text(
                "🎨 Selecciona color del alerón",
                reply_markup=keyboard
            )
            return

        # 🔹 OPCIONES NORMALES CON COLOR
        if opcion in OPCIONES_CON_COLOR:

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🔴 Rojo", callback_data="color_rojo"),
                    InlineKeyboardButton("🔵 Azul", callback_data="color_azul")
                ],
                [
                    InlineKeyboardButton("🟢 Verde", callback_data="color_verde"),
                    InlineKeyboardButton("🔵Azul Claro", callback_data="color_azul_claro")
                ],
                [
                    InlineKeyboardButton("🟠Naranja", callback_data="color_naranja"),
                    InlineKeyboardButton("🩷rosa", callback_data="color_rosa")
                ],
                [
                    InlineKeyboardButton("🟣Purpura", callback_data="color_purpura"),
                    InlineKeyboardButton("⚪Blanco", callback_data="color_blanco")
                ],
                [
                    InlineKeyboardButton("🟡Amarillo", callback_data="color_amarillo"),
                    InlineKeyboardButton("🟣Violeta Obscuro", callback_data="color_violeta__obscuro")
                ],
                [
                    InlineKeyboardButton("🔵Turqueza", callback_data="color_turqueza"),
                    InlineKeyboardButton("🟦Azul Marino", callback_data="color_azul-marino")
                ]
            ])

            estado["esperando_color"] = True

            await update.message.reply_text(
                "🎨 Selecciona color",
                reply_markup=keyboard
            )
            return

        await enviar_admin(update, context, estado, "N/A")

        del user_states[uid]


# ------------------------
# COLOR
# ------------------------

async def color(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    uid = query.from_user.id
    data = query.data

    await query.answer()

    if uid not in user_states:
        await query.answer("⚠️ La sesión expiró. Usa el menú otra vez.", show_alert=True)
        return

    estado = user_states[uid]

    # -------------------------
    # ALERON
    # -------------------------
    if data.startswith("aleron_"):

        color_val = data.replace("aleron_", "")
        estado["color_aleron"] = color_val

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔴 Rojo", callback_data="luces_rojo"),
                InlineKeyboardButton("🔵 Azul", callback_data="luces_azul")
            ],
            [
                InlineKeyboardButton("🟢 Verde", callback_data="luces_verde"),
                InlineKeyboardButton("⚪ Blanco", callback_data="luces_blanco")
            ]
        ])

        await query.edit_message_text(f"Alerón seleccionado: {color_val}")

        await context.bot.send_message(
            chat_id=uid,
            text="💡 Selecciona color de luces",
            reply_markup=keyboard
        )
        return

    # -------------------------
    # LUCES
    # -------------------------
    if data.startswith("luces_"):

        color_val = data.replace("luces_", "")
        estado["color_luces"] = color_val

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔴 Rojo", callback_data="calipers_rojo"),
                InlineKeyboardButton("🔵 Azul", callback_data="calipers_azul")
            ],
            [
                InlineKeyboardButton("🟢 Verde", callback_data="calipers_verde"),
                InlineKeyboardButton("⚪ Blanco", callback_data="calipers_blanco")
            ]
        ])

        await query.edit_message_text(f"Luces seleccionadas: {color_val}")

        await context.bot.send_message(
            chat_id=uid,
            text="🛑 Selecciona color de calipers",
            reply_markup=keyboard
        )
        return

    # -------------------------
    # CALIPERS
    # -------------------------
    if data.startswith("calipers_"):

        color_val = data.replace("calipers_", "")
        estado["color_calipers"] = color_val

        await query.edit_message_text(f"Calipers seleccionados: {color_val}")

        colores = f"""
Alerón: {estado['color_aleron']}
Luces: {estado['color_luces']}
Calipers: {estado['color_calipers']}
"""

        await enviar_admin(query, context, estado, colores)

        del user_states[uid]
        return

    # -------------------------
    # OPCIONES NORMALES color_
    # -------------------------
    if data.startswith("color_"):

        color_val = data.replace("color_", "")

        await query.edit_message_text(f"Color seleccionado: {color_val}")

        await enviar_admin(query, context, estado, color_val)

        del user_states[uid]
        return


# ------------------------
# ENVIAR ADMIN
# ------------------------

async def enviar_admin(update_or_query, context, estado, color):

    if hasattr(update_or_query, "effective_user"):
        user = update_or_query.effective_user
    else:
        user = update_or_query.from_user

    fecha = datetime.now().strftime("%d/%m/%Y")
    hora = datetime.now().strftime("%H:%M:%S")

    datos = ""

    for p, r in zip(estado["preguntas"], estado["respuestas"]):
        datos += f"{p}: {r}\n"

    pedido = {
        "usuario": user.username,
        "id": user.id,
        "opcion": estado["opcion"],
        "correo": estado["respuestas"][0] if estado["respuestas"] else "N/A",
        "color": color,
        "fecha": fecha,
        "hora": hora,
        "datos": datos
    }

    pedidos.append(pedido)
    guardar_json(PEDIDOS_FILE, pedidos)

    await context.bot.send_message(
        ADMIN_ID,
        f"""📦 ━━━━【 NUEVO PEDIDO 】━━━━ 📦

👤 Usuario: @{user.username}
🆔 ID: {user.id}

📌 Opción: {estado['opcion']}
🎨 Color: {color}

📅 Fecha: {fecha}
⏰ Hora: {hora}

━━━━━━━━━━━━━━━━━━
{datos}
"""
    )

    await context.bot.send_message(user.id, "✅ Pedido enviado")
    await context.bot.send_message(user.id, menu_text)


# ------------------------
# PUBLICACIONES
# ------------------------

async def publicar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Responde al mensaje que quieres publicar")
        return

    try:
        with open("usuarios.json", "r") as f:
            usuarios_list = json.load(f)
    except:
        await update.message.reply_text("❌ No hay usuarios guardados")
        return

    enviados = 0
    mensaje = update.message.reply_to_message

    for uid in usuarios_list:
        try:
            await context.bot.copy_message(
                chat_id=uid,
                from_chat_id=update.message.chat_id,
                message_id=mensaje.message_id
            )
            enviados += 1
        except:
            pass

    await update.message.reply_text(f"✅ Publicado a {enviados} usuarios")


# ------------------------
# COMPLETAR PEDIDO
# ------------------------

async def completar_pedido(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    i = int(query.data.split("_")[1])

    if i >= len(pedidos):
        await query.edit_message_text("❌ Pedido no encontrado")
        return

    pedido = pedidos[i]

    await context.bot.send_message(
        pedido["id"],
        f"""✅ TU PEDIDO HA SIDO COMPLETADO

📌 Función: {pedido['opcion']}
📧 Correo: {pedido['correo']}

Gracias por usar el bot."""
    )

    pedidos.pop(i)
    guardar_json(PEDIDOS_FILE, pedidos)

    await query.edit_message_text("✅ Pedido completado y eliminado")


# ------------------------
# FUNCION 17
# ------------------------

async def opcion_comando_17(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not es_admin(update.effective_user.id):
        return

    uid = context.args[0]

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("5 min", callback_data=f"f17_{uid}_300")],
        [InlineKeyboardButton("10 min", callback_data=f"f17_{uid}_600")],
        [InlineKeyboardButton("1 día", callback_data=f"f17_{uid}_86400")],
        [InlineKeyboardButton("1 semana", callback_data=f"f17_{uid}_604800")],
        [InlineKeyboardButton("1 mes", callback_data=f"f17_{uid}_2592000")],
        [InlineKeyboardButton("1 año", callback_data=f"f17_{uid}_31536000")]
    ])

    await update.message.reply_text(
        "Selecciona tiempo",
        reply_markup=keyboard
    )


async def activar17(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    _, uid, seg = query.data.split("_")

    funcion17[uid] = time.time() + int(seg)

    guardar_json(FUNCION17_FILE, funcion17)

    await query.edit_message_text("Función 17 activada")


async def quitar_funcion17(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not es_admin(update.effective_user.id):
        return

    uid = context.args[0]

    if uid in funcion17:
        del funcion17[uid]

    guardar_json(FUNCION17_FILE, funcion17)

    await update.message.reply_text("Función 17 eliminada")


# ------------------------
# ADMIN USUARIOS
# ------------------------

async def agregar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not es_admin(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text("⚠ Usa: /agregar ID")
        return

    uid = context.args[0]

    usuarios.add(str(uid))
    guardar_json(USUARIOS_FILE, list(usuarios))

    await update.message.reply_text("✅ Usuario agregado")

    try:
        await context.bot.send_message(
            chat_id=int(uid),
            text="🎉 Has sido agregado al bot.\n\nUsa /start para comenzar."
        )
    except:
        await update.message.reply_text(
            "⚠ No se pudo enviar mensaje al usuario.\nEl usuario debe iniciar el bot con /start primero."
        )


async def eliminar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not es_admin(update.effective_user.id):
        return

    uid = context.args[0]

    if str(uid) in usuarios:
        usuarios.remove(str(uid))

    guardar_json(USUARIOS_FILE, list(usuarios))

    await update.message.reply_text("Usuario eliminado")


async def ver_usuarios(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not es_admin(update.effective_user.id):
        return

    lista = "\n".join(usuarios)

    await update.message.reply_text(f"Usuarios:\n{lista}")


async def ver_bloqueados(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not es_admin(update.effective_user.id):
        return

    bloqueados = [u for u, n in intentos.items() if n >= 3]

    await update.message.reply_text("\n".join(bloqueados))


async def desbloquear(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not es_admin(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text("⚠️ Usa el comando así:\n/desbloquear ID")
        return

    uid = context.args[0]

    intentos[uid] = 0

    guardar_json(INTENTOS_FILE, intentos)

    await update.message.reply_text("✅ Usuario desbloqueado")


async def comando_desconocido(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id == ADMIN_ID:
        return

    await update.message.reply_text("❌ Ese comando no existe")


# ------------------------
# RARO
# ------------------------

async def raro(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    msg = update.message

    tipo = "archivo"

    if msg.sticker:
        tipo = "sticker"
    elif msg.voice:
        tipo = "audio de voz"
    elif msg.video:
        tipo = "video"
    elif msg.audio:
        tipo = "audio"
    elif msg.document:
        tipo = "documento"

    fecha = datetime.now().strftime("%d/%m/%Y")
    hora = datetime.now().strftime("%H:%M:%S")

    texto = f"""
🚨 𝗔𝗟𝗘𝗥𝗧𝗔 𝗗𝗘 𝗠𝗢𝗩𝗜𝗠𝗜𝗘𝗡𝗧𝗢 𝗦𝗢𝗦𝗣𝗘𝗖𝗛𝗢𝗦𝗢

👤 𝗨𝘀𝘂𝗮𝗿𝗶𝗼: {user.first_name}
🔗 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: @{user.username}
🆔 𝗜𝗗: {user.id}

📦 Tipo: {tipo}

📅 𝗙𝗲𝗰𝗵𝗮: {fecha}
⏰ 𝗛𝗼𝗿𝗮: {hora}

⚠️ Verifica esta actividad inmediatamente.
"""

    if update.message.sticker:
        file = update.message.sticker.file_id
        await context.bot.send_sticker(ADMIN_ID, file)
        await context.bot.send_message(ADMIN_ID, texto)

    elif update.message.photo:
        file = update.message.photo[-1].file_id
        await context.bot.send_photo(ADMIN_ID, file, caption=texto)

    elif update.message.voice:
        file = update.message.voice.file_id
        await context.bot.send_voice(ADMIN_ID, file, caption=texto)

    elif update.message.audio:
        file = update.message.audio.file_id
        await context.bot.send_audio(ADMIN_ID, file, caption=texto)

    elif update.message.video:
        file = update.message.video.file_id
        await context.bot.send_video(ADMIN_ID, file, caption=texto)

    elif update.message.document:
        file = update.message.document.file_id
        await context.bot.send_document(ADMIN_ID, file, caption=texto)

    await update.message.reply_text(
        "⚠ Accion identificada como extraña (Notificada al administrador @drillscars), por favor utiliza el bot correctamente."
    )


# ------------------------
# MANTENIMIENTO
# ------------------------

async def toggle_mantenimiento(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not es_admin(update.effective_user.id):
        return

    mantenimiento["activo"] = not mantenimiento["activo"]
    guardar_json(MANTENIMIENTO_FILE, mantenimiento)

    estado_txt = "🔧 ACTIVADO" if mantenimiento["activo"] else "✅ DESACTIVADO"

    await update.message.reply_text(
        f"Modo mantenimiento: {estado_txt}"
    )


# ------------------------
# BOTONES ADMIN
# ------------------------

async def boton_comandos_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "comando":
        await query.message.reply_text(
            "╔══════════════════════════════╗\n"
            "        👑 PANEL DE ADMIN 👑\n"
            "╚══════════════════════════════╝\n\n"
            "⚙️ CONTROL DEL BOT\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🚀 COMANDOS PRINCIPALES\n\n"
            "▶️ /start\nIniciar el bot\n\n"
            "👤 /agregar\nAgregar usuario autorizado\n\n"
            "❌ /eliminar\nEliminar usuario del sistema\n\n"
            "📋 /ver_usuarios\nVer usuarios registrados\n\n"
            "🔓 /desbloquear\nDesbloquear usuario bloqueado\n\n"
            "🔓 /ver_bloqueados\nVer usuarios bloqueados\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📢 PUBLICACIONES\n\n"
            "📡 /publicar\nEnviar mensaje a todos los usuarios\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🧩 FUNCIÓN 17\n\n"
            "🟢 /opcion_comando_17\nDar acceso a función 17\n\n"
            "🔴 /quitar_funcion17\nQuitar acceso a función 17\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🛡 Solo para administrador"
        )


async def boton_respuestas(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "respuestas":
        await query.message.reply_text(
            "╔══════════════════════════════╗\n"
            "📌 Respuestas\n"
            "───────────────────\n"
            "✅ Proceso Finalizado\n"
            "𝗧𝘂 𝗽𝗿𝗼𝗰𝗲𝘀𝗼 𝗱𝗲 𝗹𝗮 𝗰𝘂𝗲𝗻𝘁𝗮 () 𝗵𝗮 𝘀𝗶𝗱𝗼 𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗮𝗱𝗼.\n"
            "────────────────────\n"
            "➕ Agregar usuario\n"
            "𝗧𝘂 𝗰𝘂𝗲𝗻𝘁𝗮 𝗵𝗮 𝘀𝗶𝗱𝗼 𝗰𝗿𝗲𝗮𝗱𝗮 🏁🎉! 𝗣𝘂𝗲𝗱𝗲𝘀 𝘂𝘀𝗮𝗿 𝗹𝗮𝘀 𝗳𝘂𝗻𝗰𝗶𝗼𝗻𝗲𝘀 𝗰𝗼𝗻 𝗲𝗹 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 /start.\n"
            "────────────────────\n"
            "🔓 Desbloquear usuario\n"
            "𝗛𝗮𝘀 𝘀𝗶𝗱𝗼 𝗱𝗲𝘀𝗯𝗹𝗼𝗾𝘂𝗲𝗮𝗱𝗼! 𝗛𝗮𝗯𝗹𝗮 𝗰𝗼𝗻 𝗲𝗹 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿 @drillscars 𝗽𝗮𝗿𝗮 𝗾𝘂𝗲 𝘁𝗲 𝗮𝗴𝗿𝗲𝗴𝘂𝗲.\n"
            "────────────────────\n"
        )


# ------------------------
# MAIN
# ------------------------

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("agregar", agregar))
app.add_handler(CommandHandler("eliminar", eliminar))
app.add_handler(CommandHandler("ver_usuarios", ver_usuarios))
app.add_handler(CommandHandler("ver_bloqueados", ver_bloqueados))
app.add_handler(CommandHandler("desbloquear", desbloquear))
app.add_handler(CommandHandler("publicar", publicar))
app.add_handler(CommandHandler("opcion_comando_17", opcion_comando_17))
app.add_handler(CommandHandler("quitar_funcion17", quitar_funcion17))
app.add_handler(CommandHandler("mantenimiento", toggle_mantenimiento))

app.add_handler(
    MessageHandler(
        filters.Sticker.ALL | filters.VOICE | filters.AUDIO | filters.VIDEO | filters.Document.ALL,
        raro
    )
)

app.add_handler(MessageHandler(filters.COMMAND, comando_desconocido))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar))

app.add_handler(CallbackQueryHandler(color, pattern="^(color_|aleron_|luces_|calipers_)"))
app.add_handler(CallbackQueryHandler(activar17, pattern="^f17_"))
app.add_handler(CallbackQueryHandler(completar_pedido, pattern="^completar_"))
app.add_handler(CallbackQueryHandler(boton_comandos_admin, pattern="^comando$"))
app.add_handler(CallbackQueryHandler(boton_respuestas, pattern="^respuestas$"))

print("✅ BOT DE DRILLS ACTIVO")
app.run_polling()
