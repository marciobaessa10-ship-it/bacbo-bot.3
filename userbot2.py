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

API_ID          = 31922041
API_HASH        = "3f1efb25a51933118b55a0669c593365"
SESSION_STRING  = "1ApWapzMBu11mySx-BZCOCyY8Yta-WPE9B6j8xKt-wesWEgWt6euRvrE9xllQB5J4bhfTv4GFFK6il7dC0WuOA46QoyFAkfr12a5iVdC8ABxm5XDocUlua_VzjhjTCTD6C5MW1X4xb456Rg6MxLTlxl3aXpTaqtvIYVjeFN9xcsb-I4sWStt_d2K39Q1EQMv1rjndn2KYsd60OXJHJXgrY1k4IQRxwSAStgxrHk1kprru2t0BXhE1x1MxvZDkkZo_c3A4_GFFtNIV2YMNaefKYdwBdXjLojGQ6J4Wpy5AF9HFsnh_agC4JaOhIc7_g0HOjZKVpMM3hunq9dmXObOA1EMAPaPDYqM="
INVITE_ORIGEM   = "-A5qwQIaM-8zYjc0"
INVITE_DESTINO  = "hv0RZl113chhMGEy"
LINK_PLATAFORMA = "https://bantubet.co.ao/affiliates/?btag=2442098"
RODAPE          = f"\n\n🎰 Joga aqui → {LINK_PLATAFORMA}"

async def entrar_grupo(client, invite_hash):
    try:
        result = await client(ImportChatInviteRequest(invite_hash))
        grupo = result.chats[0]
        logger.info(f"✅ Entrou em: {grupo.title}")
        return grupo
    except UserAlreadyParticipantError:
        logger.info("✅ Já está no grupo!")
        async for dialog in client.iter_dialogs():
            try:
                entity = await client.get_entity(f"t.me/joinchat/{invite_hash}")
                if abs(dialog.id) == abs(entity.id):
                    return dialog.entity
            except:
                continue
        return None
    except Exception as e:
        logger.error(f"❌ Erro ao entrar: {e}")
        return None

async def main():
    logger.info("🚀 Bot 2 — Cópia de Sinais — A FUNCIONAR!")
    logger.info("━" * 50)

    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    logger.info("✅ Userbot conectado!")

    canal = await entrar_grupo(client, INVITE_ORIGEM)
    grupo = await entrar_grupo(client, INVITE_DESTINO)

    if not canal or not grupo:
        logger.error("❌ Não foi possível aceder a um dos grupos!")
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
