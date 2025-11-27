from typing import Callable

from nicegui import ui
from nicegui.testing import User


async def test_basic_startup_appearance(user: User) -> None:
    await user.open("/")
    await user.should_see("谈天")
    await user.should_see("1 人在线")
    await user.should_see("© qqAys")
    await user.should_see("无消息")


async def test_sending_messages(create_user: Callable[[], User]) -> None:
    """Test sending messages from two different screens."""
    user1 = create_user()
    user2 = create_user()

    await user1.open("/")
    user1.find(ui.input).type("Hello from screen A!").trigger("keydown.enter")
    await user1.should_see("Hello from screen A!")

    await user2.open("/")
    await user2.should_see("Hello from screen A!")
    user2.find(ui.input).type("Hello from screen B!").trigger("keydown.enter")

    await user1.should_see("Hello from screen A!")
    await user1.should_see("Hello from screen B!")