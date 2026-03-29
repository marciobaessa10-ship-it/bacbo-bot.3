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

async def main():
    logger.info("🚀 Bot 2 — Cópia de Sinais — A FUNCIONAR!")
    logger.info("━" * 50)

    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    logger.info("✅ Userbot conectado!")

    # Entrar no canal origem
    canal = None
    try:
        result = await client(ImportChatInviteRequest(INVITE_ORIGEM))
        canal = result.chats[0]
        logger.info(f"✅ Entrou no canal: {canal.title}")
    except UserAlreadyParticipantError:
        logger.info("✅ Já está no canal origem!")
        async for dialog in client.iter_dialogs():
            if dialog.id == -1002468260611 or "BAC BO" in (dialog.name or "").upper():
                canal = dialog.entity
                logger.info(f"✅ Canal encontrado: {dialog.name}")
                break
    except Exception as e:
        logger.error(f"❌ Erro no canal: {e}")

    # Entrar no grupo destino
    grupo = None
    try:
        result = await client(ImportChatInviteRequest(INVITE_DESTINO))
        grupo = result.chats[0]
        logger.info(f"✅ Entrou no grupo: {grupo.title}")
    except UserAlreadyParticipantError:
        logger.info("✅ Já está no grupo destino!")
        async for dialog in client.iter_dialogs():
            if dialog.id == -1003637982143 or "BacBo Bilionário VIP" in (dialog.name or ""):
                grupo = dialog.entity
                logger.info(f"✅ Grupo encontrado: {dialog.name}")
                break
    except Exception as e:
        logger.error(f"❌ Erro no grupo: {e}")

    if not canal or not grupo:
        logger.error("❌ Não foi possível aceder a um dos grupos!")
        async for dialog in client.iter_dialogs():
            logger.info(f"   {dialog.name} | ID: {dialog.id}")
        return

    logger.info(f"✅ Canal : {canal.title}")
    logger.info(f"✅ Grupo : {grupo.title}")
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
