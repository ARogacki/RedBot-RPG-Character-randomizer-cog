from redbot.core.bot import Red
from .statroller import StatRoller


async def setup(bot: Red) -> None:
    await bot.add_cog(StatRoller(bot))