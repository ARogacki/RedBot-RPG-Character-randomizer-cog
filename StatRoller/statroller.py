from redbot.core import commands
import random
import math
import json

class StatRoller(commands.Cog):
    tries_amount = 4
    pf2_json = {}
    dnd_json = {}
    directory = r'C:\Users\adria\OneDrive\Dokumenty\RedBot Custom Cogs\StatRoller\\'

    def __init__(self, bot):
        self.bot = bot
        self.pf2_json = json.load(open(self.directory + 'pf2e.json'))
        self.generic = json.load(open(self.directory + 'generic.json'))
        self.dnd_json = json.load(open(self.directory + 'dnd5e.json'))

    @commands.command()
    async def rollhelp(self, ctx):
        """Displays available rolling commands."""
        await ctx.send("""**Available commands:**
        
        :game_die:Basic rolls:
            ```
            >rollstats
            >rollstat <stat name>```
        :pencil:Custom rolls:
            ```
            >rollcustomstats <dice_type> <dice_amount>
            >rollcustomstats <dice_type> <dice_amount> <dice_threshold>
            >rollcustomstat <stat name> <dice_type> <dice_amount>
            >rollcustomstat <stat name> <dice_type> <dice_amount> <dice_threshold>```
        :railway_track:Pf2 specific:
            ```
            >rollclasspf2
            >rollracepf2```
        :dragon_face:Dnd specific:
            ```
            >rollclassdnd
            >rollclassdnd <class name>
            >rollracednd
            >rollracednd <race tier>```
        """)

    @commands.command()
    async def rollalignment(self, ctx):
        """Roll for alignment.
        """
        alignments = self.generic["alignment"]
        author = ctx.author
        rolled_alignment = self.RollForCustomList(alignments)
        await ctx.send(f"You are {rolled_alignment}!\n Congratulations {author.mention}! :partying_face:")


    @commands.command()
    async def rollstats(self, ctx):
        """Roll for all starting statistics.
        """
        stats = self.pf2_json["stats"]
        await self.StatRolls(ctx, stats)

    @commands.command()
    async def rollstat(self, ctx, stat_name):
        """Roll for a single statistic.
        Usage: rollstat <stat name>
        """
        stats = {stat_name}
        await self.StatRolls(ctx, stats)

    @commands.command()
    async def rollcustomstats(self, ctx, dice_type, dice_amount, dice_threshold = "3"):
        """Roll for all starting statistics with a custom amount of dice per roll and a custom dice.
        Usage: rollcustomstats <dice_type> <dice_amount>
        Alt Usage: rollcustomstats <dice_type> <dice_amount> <dice_threshold>
        """
        stats = self.pf2_json["stats"]
        await self.StatRolls(ctx, stats, dice_amount, dice_type, dice_threshold)

    @commands.command()
    async def rollcustomstat(self, ctx, stat_name, dice_type, dice_amount, dice_threshold = "3"):
        """Roll for a single statistic with a custom amount of dice and a custom die.
        Usage: rollcustomstat <stat name> <dice_type> <dice_amount>
        Alt Usage: rollcustomstat <stat name> <dice_type> <dice_amount> <dice_threshold>
        """
        stats = {stat_name}
        await self.StatRolls(ctx, stats, dice_amount, dice_type, dice_threshold)

    @commands.command()
    async def rollclasspf2(self, ctx):
        """Roll for a single pf2 class.
        """
        class_dictionary = self.pf2_json["class"]
        author = ctx.author
        rolled_class = self.RollForCustomList(list(class_dictionary.keys()))
        result_message = f"You get to play as the {rolled_class}!\n"
        if rolled_class == "Psychic":
            psychic = class_dictionary[rolled_class]
            conscious = self.RollForCustomList(psychic["Conscious Mind"])
            subconscious = self.RollForCustomList(psychic["Subconscious Mind"])
            result_message += f"Consider taking the following:" \
                              f"\nConscious mind - {conscious}" \
                              f"\nSubconscious mind - {subconscious}\n"
        elif rolled_class == "Wizard":
            wizard = class_dictionary[rolled_class]
            school = self.RollForCustomList(wizard["Arcane School"])
            thesis = self.RollForCustomList(wizard["Arcane Thesis"])
            result_message += f"Consider taking the following:" \
                              f"\nArcane School - {school}" \
                              f"\nArcane Thesis - {thesis}\n"
        else:
            if len(class_dictionary[rolled_class]) > 0:
                rolled_subclass = self.RollForCustomList(class_dictionary[rolled_class])
                result_message += f"Consider taking the {rolled_subclass} subclass.\n"
        await ctx.send(result_message + f"Congratulations {author.mention}! :partying_face:")

    @commands.command()
    async def rollracepf2(self, ctx):
        """Roll for a single pf2 race.
        """
        races = self.pf2_json["race"]
        author = ctx.author
        rolled_race = self.RollForCustomList(races)
        await ctx.send(f"You are the one and only {rolled_race}!\n Congratulations {author.mention}! :partying_face:")

    @commands.command()
    async def rollarchetypepf2(self, ctx):
        """Roll for a single pf2 archetype.
        """
        archetypes = self.pf2_json["archetype"]
        author = ctx.author
        rolled_archetype = self.RollForCustomList(archetypes)
        await ctx.send(f"Becoming a {rolled_archetype} would suit you nicely!\n Congratulations {author.mention}! :partying_face:")

    @commands.command()
    async def rolldeitypf2(self, ctx):
        """Roll for a single pf2 deity.
        """
        deities = self.pf2_json["deity"]
        author = ctx.author
        rolled_deity = self.RollForCustomList(deities)
        await ctx.send(f"You are a devout follower of  {rolled_deity}!\n Congratulations {author.mention}! :partying_face:")

    @commands.command()
    async def rollbackgroundpf2(self, ctx):
        """Roll for a single pf2 background.
        """
        backgrounds = self.pf2_json["background"]
        author = ctx.author
        rolled_background = self.RollForCustomList(backgrounds)
        await ctx.send(f"Who you are today is only thanks to your past - {rolled_background}!\n Congratulations {author.mention}! :partying_face:")

    @commands.command()
    async def createcharacterpf2(self, ctx):
        """Randomize one entire character.
        """
        author = ctx.author
        result_message = f"Enjoy your new character, {author.mention}! :partying_face:\n"
        result_message += f"Race: {self.RollForPropertyPf2('race')}\n"
        class_dictionary = self.pf2_json["class"]
        rolled_class = self.RollForCustomList(list(class_dictionary.keys()))
        result_message += f"Class: {rolled_class}\n"
        if rolled_class == "Psychic":
            psychic = class_dictionary[rolled_class]
            conscious = self.RollForCustomList(psychic["Conscious Mind"])
            subconscious = self.RollForCustomList(psychic["Subconscious Mind"])
            result_message += f"    Conscious mind - {conscious}\n" \
                              f"    Subconscious mind - {subconscious}\n"
        elif rolled_class == "Wizard":
            wizard = class_dictionary[rolled_class]
            school = self.RollForCustomList(wizard["Arcane School"])
            thesis = self.RollForCustomList(wizard["Arcane Thesis"])
            result_message += f"    Arcane School - {school}\n" \
                              f"    Arcane Thesis - {thesis}\n"
        else:
            if len(class_dictionary[rolled_class]) > 0:
                rolled_subclass = self.RollForCustomList(class_dictionary[rolled_class])
                result_message += f"    Subclass: {rolled_subclass}\n"
        result_message += f"Archetype: {self.RollForPropertyPf2('archetype')}\n"
        result_message += f"Background: {self.RollForPropertyPf2('background')}\n"
        result_message += f"Deity: {self.RollForPropertyPf2('deity')}\n"
        result_message += f"Alignment: {self.RollForPropertyGeneric('alignment')}\n"
        stats = self.pf2_json["stats"]
        stat_dictionary = {}
        for stat in stats:
            stat_dictionary[stat] = self.rollForStatistic()
        result_message += f"Stats: \n"
        result_message = self.CreateRollMessage(result_message, stat_dictionary)
        await ctx.send(result_message)





    @commands.command()
    async def rollclassdnd(self, ctx, class_name = ""):
        """Roll for a single dnd class.
        """
        class_dictionary = self.dnd_json["class"]
        rolled_class = self.RollForCustomList(list(class_dictionary.keys()))
        if len(class_name) > 0:
            if class_name in class_dictionary:
                rolled_class = class_name
            else:
                await ctx.send(f"{class_name}? That's a class now? :face_with_monocle:\nCase sensitive btw.")
                return
        rolled_subclass = self.RollForCustomList(class_dictionary[rolled_class])
        author = ctx.author
        await ctx.send(f"You get to play as the {rolled_class}!"
                       f"\n You should consider the {rolled_subclass} subclass."
                       f"\n Congratulations {author.mention}! :partying_face:")

    @commands.command()
    async def rollracednd(self, ctx, race_tier = "monstrous"):
        """Roll for a single dnd race.
        Usage: rollracednd common/exotic/monstrous
        """
        race_dictionary = self.dnd_json["race"]
        races = []
        if race_tier.upper() == "COMMON":
            races += race_dictionary["common"]
        if race_tier.upper() == "EXOTIC":
            races += race_dictionary["exotic"]
        if race_tier.upper() == "MONSTROUS":
            races += race_dictionary["monstrous"]
        if len(races) > 0:
            author = ctx.author
            rolled_race = self.RollForCustomList(races)
            await ctx.send(f"You are the one and only {rolled_race}!\n Congratulations {author.mention}! :partying_face:")
        else:
            await ctx.send(f"Not sure what you mean by {race_tier}")

    async def StatRolls(self, ctx, stats, dice_amount = "4", dice_type = "D6", dice_threshold = "3"):
        if dice_amount.isnumeric() is False or dice_threshold.isnumeric() is False:
            await ctx.send("Stop trying to cheat the system :wink:")
            return
        dice_amount = math.floor(float(dice_amount))
        dice_threshold = math.floor(float(dice_threshold))
        if dice_amount < dice_threshold:
            dice_threshold = dice_amount
        if dice_amount < 1 or dice_threshold < 1:
            await ctx.send("Stop trying to cheat the system :wink:")
        elif dice_amount > 100 or dice_threshold > 100:
            await ctx.send("That's a bit excessive :fearful:")
        else:
            dice_sizes = {"D4": 4,
                          "D6": 6,
                          "D8": 8,
                          "D10": 10,
                          "D12": 12,
                          "D20": 20,
                          "D100": 100}
            if dice_type.upper() in dice_sizes:
                stat_dictionary = {}
                for stat in stats:
                    stat_dictionary[stat] = self.rollForStatistic(dice_amount, dice_sizes[dice_type.upper()], dice_threshold)
                author = ctx.author
                result_message = f"{author.mention} new stats:game_die::\n"
                max_roll = dice_sizes[dice_type.upper()] * dice_threshold
                min_roll = dice_threshold
                if dice_amount < dice_threshold:
                    min_roll = dice_amount
                await ctx.send(self.CreateCustomRollMessage(result_message, stat_dictionary, max_roll, min_roll))
            else:
                await ctx.send(f"What kind of a dice size is {dice_type} :thinking:")

    def RollForCustomList(self, list):
        return random.choice(list)

    def rollForStatistic(self, dice_amount = 4, dice_size = 6, dice_threshold = 3):
        roll_list = []
        for i in range(dice_amount):
            roll_list.append(random.randrange(1, dice_size+1))
        roll_list.sort(reverse=True)
        if dice_amount < dice_threshold:
            return sum(roll_list[:dice_amount])
        return sum(roll_list[:dice_threshold])

    def CreateCustomRollMessage(self, result_message, stat_dictionary, max_roll, min_roll):
        for key in stat_dictionary:
            if stat_dictionary[key] == max_roll:
                result_message += f"    {key}: {stat_dictionary[key]} :crown:\n"
            elif stat_dictionary[key] == min_roll:
                result_message += f"    {key}: {stat_dictionary[key]} :cry:\n"
            elif stat_dictionary[key] >= max_roll * 0.8:
                result_message += f"    {key}: {stat_dictionary[key]} :crossed_swords:\n"
            elif stat_dictionary[key] >= max_roll * 0.4:
                result_message += f"    {key}: {stat_dictionary[key]}\n"
            else:
                result_message += f"    {key}: {stat_dictionary[key]} :poop:\n"
        return result_message

    def CreateRollMessage(self, result_message, stat_dictionary):
        for key in stat_dictionary:
            if stat_dictionary[key] == 18:
                result_message += f"    {key}: {stat_dictionary[key]} :crown:\n"
            elif stat_dictionary[key] == 3:
                result_message += f"    {key}: {stat_dictionary[key]} :cry:\n"
            elif stat_dictionary[key] >= 16:
                result_message += f"    {key}: {stat_dictionary[key]} :crossed_swords:\n"
            elif stat_dictionary[key] >= 8:
                result_message += f"    {key}: {stat_dictionary[key]}\n"
            else:
                result_message += f"    {key}: {stat_dictionary[key]} :poop:\n"
        return result_message

    def RollForPropertyPf2(self, property):
        properties = self.pf2_json[property]
        return self.RollForCustomList(properties)

    def RollForPropertyGeneric(self, property):
        properties = self.generic[property]
        return self.RollForCustomList(properties)