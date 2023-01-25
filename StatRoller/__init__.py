from .statroller import StatRoller


def setup(bot):
    bot.add_cog(StatRoller(bot))