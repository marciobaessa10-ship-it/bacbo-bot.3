import asyncio
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors import UserAlreadyParticipantError

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

API_ID           = 31922041
API_HASH         = "3f1efb25a51933118b55a0669c593365"
SESSION_STRING   = "1ApWapzMBuzJDA1QeuteePvKYxu8m5vRzb4v5RqRhey46V-RywtGTdoO6aVWWD34klG0P5JvCIMkb1VJE5MbXI1IRS_CBHBDnNP_66xFeKdjYEKzP0r7OUgMP_W-9c7TEyWGH42mLLQBCCf8r7BSGGRjMCa7o13WCC_m5ukZAJFhX53L_VVzDGZHoB81f365oEqPeNESOaqCSaRifvje64FkRJBEsV7JhLE-qsW9EvJTvu7pVujpEzRZEgpmmYs_1XJg9ObgDcREIG-UdXUbjdSFdvMZ7FZ0kfT571vblCl7q3FyPAHSg3CmNltkOARp-3dmm85KxzDWynYCOGQx7Hb9vu50iZ3g="
INVITE_ORIGEM    = "-A5qwQIaM-8zYjc0"
INVITE_DESTINO   = "hv0RZl113chhMGEy"
LINK_PLATAFORMA  = "https://bantubet.co.ao/affiliates/?btag=2442098"
RODAPE           = f"\n\n🎰 Joga aqui → {LINK_PLATAFORMA}"

async def entrar_grupo(client, invite_hash, nome):
    try:
        result = await client(ImportChatInviteRequest(invite_hash))
        grupo = result.chats[0]
        logger.info(f"✅ Entrou em '{grupo.title}'")
        return grupo
    except UserAlreadyParticipantError:
        logger.info(f"✅ Já está em '{nome}'!")
        async for dialog in client.iter_dialogs():
            if dialog.is_group or dialog.is_channel:
                try:
                    invite = await client.get_entity(f"t.me/joinchat/{invite_hash}")
                    if dialog.id == invite.id:
                        return dialog.entity
                except:
                    pass
        # fallback — procura pelo hash
        async for dialog in client.iter_dialogs():
            logger.info(f"   {dialog.name} | ID: {dialog.id}")
        return None
    except Exception as e:
        logger.error(f"❌ Erro ao entrar em '{nome}': {e}")
        return None

async def main():
    logger.info("🚀 Bot 2 — Cópia de Sinais — A FUNCIONAR!")
    logger.info(f"📡 Origem : t.me/+-{INVITE_ORIGEM}")
    logger.info(f"📤 Destino: t.me/+{INVITE_DESTINO}")
    logger.info("━" * 50)

    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    logger.info("✅ Userbot conectado!")

    # Entrar nos dois grupos
    canal = await entrar_grupo(client, INVITE_ORIGEM, "canal origem")
    grupo = await entrar_grupo(client, INVITE_DESTINO, "grupo destino")

    if not canal or not grupo:
        logger.error("❌ Não foi possível aceder a um dos grupos! A listar diálogos...")
        async for dialog in client.iter_dialogs():
            logger.info(f"   {dialog.name} | ID: {dialog.id}")
        return

    logger.info(f"✅ Canal origem : {canal.title}")
    logger.info(f"✅ Grupo destino: {grupo.title}")
    logger.info("👀 A monitorizar... aguardando sinais!")

    @client.on(events.NewMessage(chats=canal))
    async def handler(event):
        msg = event.message
        text = msg.text or ""
        texto_final = text + RODAPE

        logger.info("📨 Sinal recebido! A enviar...")
        try:
            if msg.photo:
                await client.send_file(grupo, msg.media, caption=texto_final, link_preview=False)
            elif msg.video:
                await client.send_file(grupo, msg.media, caption=texto_final, link_preview=False)
            elif msg.text:
                await client.send_message(grupo, texto_final, link_preview=False)
            else:
                await client.forward_messages(grupo, msg)
            logger.info("✅ Enviado com sucesso!")
        except Exception as e:
            logger.error(f"❌ Erro ao enviar: {e}")

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
