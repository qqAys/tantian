from datetime import datetime, timezone
from uuid import uuid4

from nicegui import ui, app, Client


APP_NAME = "谈天"
APP_AUTHOR = "me@qqays.xyz"
APP_GIT_URL = "https://github.com/qqAys/tantian"

messages_list: list[tuple[str, str, str, str]] = []
online_users_list: list[str] = []

MAX_MESSAGES_DISPLAY = 9999


@ui.refreshable
def online_users() -> None:
    if online_users_list:
        ui.label(f"{len(online_users_list)} 人在线").classes("text-bold")


@ui.refreshable
def chat_messages(own_id: str) -> None:
    if messages_list:
        recent_messages = messages_list[-MAX_MESSAGES_DISPLAY:]
        for user_id, avatar, text, stamp in recent_messages:
            with ui.chat_message(stamp=stamp, avatar=avatar, sent=own_id == user_id, name=user_id):
                ui.markdown(text)
    else:
        ui.label("无消息").classes("absolute-center w-max text-inherit")
    ui.run_javascript("window.scrollTo(0, document.body.scrollHeight)")


@ui.page("/")
async def main(client: Client):
    ui.colors(primary="#424242")
    ui.add_css(r"a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}")

    def send() -> None:
        if not text.value.strip():
            ui.notify("请输入内容。", type="warning")
            text.value = ""
            return
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %z (%Z)")
        messages_list.append((user_id, avatar, text.value, stamp))
        text.value = ""
        chat_messages.refresh()
        online_users.refresh()

    if "user_id" not in app.storage.browser:
        user_id = str(uuid4())
        app.storage.browser["user_id"] = user_id
    else:
        user_id = app.storage.browser["user_id"]

    online_users_list.append(user_id)

    avatar = f"https://robohash.org/{user_id}?bgset=bg2"

    with ui.header().classes("items-center justify-between"):
        ui.label(APP_NAME).classes("text-2xl text-bold tracking-tighter")
        online_users()

    with ui.footer().classes("bg-white"), ui.column().classes("w-full max-w-3xl mx-auto my-6"):
        with ui.row().classes("text-xs self-end text-primary h-4"):
            ui.markdown(f"不存储您的信息和消息，查看 [政策]({APP_GIT_URL}/blob/main/DISCLAIMER.md)")
            ui.markdown(f"[GitHub]({APP_GIT_URL})")

        with ui.row().classes("w-full no-wrap items-center"):
            text = ui.input(placeholder="请输入内容，支持Markdown").props("autofocus rounded outlined").classes(
                "flex-grow")
            text.on("keydown.enter", send)
            with text.add_slot("prepend"):
                with ui.avatar():
                    ui.image(avatar)
            with text.add_slot("append"):
                ui.button(icon="send", on_click=send).props("rounded flat")

    await ui.context.client.connected()
    with ui.column().classes("w-full max-w-2xl mx-auto items-stretch"):
        chat_messages(user_id)

    @client.on_connect
    def on_client_connected() -> None:
        online_users.refresh()

    @client.on_disconnect
    def on_client_disconnected() -> None:
        online_users_list.remove(user_id)


if __name__ in {"__main__", "__mp_main__"}:
    import os
    ui.run(
        host=os.getenv("APP_HOST", "127.0.0.1"),
        port=int(os.getenv("APP_PORT", "8080")),
        title=APP_NAME,
        language="zh-CN",
        storage_secret=os.getenv("STORAGE_SECRET"),
        fastapi_docs=False,
        reload=False
    )
