import discord
from discord.ext import commands
from queue1 import queue
from question import tree
from googletrans import LANGUAGES, Translator
import json
from gtts import gTTS
from io import BytesIO
import asyncio
import io




intents = discord.Intents.all()
client = commands.Bot(command_prefix="+", intents=intents)

historique = {}
history_queue = queue("start")
translator = Translator()


# Chargement des données depuis le fichier JSON
try:
    with open("data.json", "r") as f:
        data = json.load(f)
        if "historique" in data:
            historique = data["historique"]
except FileNotFoundError:
    pass

# Enregistrement des données dans le fichier JSON à la fermeture du bot
@client.event
async def on_disconnect():
    with open("data.json", "w") as f:
        json.dump({"historique": historique}, f)

@client.command(name="history")
async def command_history(ctx):
    user_id = str(ctx.message.author.id)
    commands = historique.get(user_id, [])
    if isinstance(commands, str):
        await ctx.send(commands)
    else:
        message = "Historique des commandes : \n"
        for command in commands:
            message += command + "\n"
        await ctx.send(message)

# Annonce ready BOT
@client.event
async def on_ready():
    print(f'{client.user.name} EST LA !')

# Commmande Last
@client.command(name="last")
async def get_last_command(ctx):
    user_id = str(ctx.message.author.id)
    last_command = historique.get(user_id, [""])[-1]
    await ctx.send(last_command)
# Commmande Next
@client.command(name="next")
async def next_command(ctx):
    user_id = str(ctx.message.author.id)
    await ctx.send(history_queue.next())
# Commmande Previous
@client.command(name="previous")
async def previous_command(ctx):
    user_id = str(ctx.message.author.id)
    await ctx.send(history_queue.previous())
# Commmande Clear_history
@client.command(name="clear_history")
async def clear_history(ctx):
    user_id = str(ctx.message.author.id)
    historique[user_id] = []
    await ctx.send("Historique effacé.")
# Commmande Ping
@client.command(name="ping")
async def ping(ctx):
    user_id = str(ctx.message.author.id)
    command = "+ping"
    await ctx.send("Pong!")
    historique.setdefault(user_id, []).append(command)
    history_queue.append(command)
# Commmande car
@client.command(name="car")
async def car(ctx):
    user_id = str(ctx.message.author.id)
    command = "+car"
    await ctx.send("Vroum")
    historique.setdefault(user_id, []).append(command)
    history_queue.append(command)

# Commmande avion
@client.command(name="avion")
async def avion(ctx):
    user_id = str(ctx.message.author.id)
    command = "+avion"
    await ctx.send("Piou")
    historique.setdefault(user_id, []).append(command)
    history_queue.append(command)
# Commmande Disconnect
@client.command(name="disconnect")
async def disconnect(ctx):
    await ctx.send("Déconnexion en cours...")
    await client.close()

@client.command(name="purge")
async def purge_command(ctx, amount=5):
    await ctx.message.delete() 

    if amount <= 0:
        await ctx.send("Le nombre de messages à purger doit être supérieur à zéro.")
        return

    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f"Purged {len(deleted)} messages.", delete_after=5)

# Commmande My_help
@client.command(name="my_help")
async def help_command(ctx):
    embed = discord.Embed(title="Liste des commandes", description="Voici la liste des commandes disponibles :", color=0x00ff00)
    embed.add_field(name="+ping", value="PONG", inline=False)
    embed.add_field(name="+car", value="VROUM", inline=False)
    embed.add_field(name="+last", value="Affiche la dernière commande utilisée par l'utilisateur", inline=False)
    embed.add_field(name="+next", value="Affiche la commande suivante dans l'historique de l'utilisateur", inline=False)
    embed.add_field(name="+previous", value="Affiche la commande précédente dans l'historique de l'utilisateur", inline=False)
    embed.add_field(name="+clear_history", value="Efface l'historique de l'utilisateur", inline=False)
    embed.add_field(name="+history", value="Affiche l'historique des commandes de l'utilisateur", inline=False)
    embed.add_field(name="+sandwich", value="Questionnaire sur sandwich", inline=False)
    embed.add_field(name="+tr", value="Pour utiliser la traduction , il faut faire +tr (avec la langues) et (ce qu'on veut traduire)", inline=False)
    embed.add_field(name="+langues", value="Affiche les langues avec leur alias pour la traduction", inline=False)
    await ctx.send(embed=embed)
    user_id = str(ctx.message.author.id)
    command = "+help"
    historique.setdefault(user_id, []).append(command)

# Commmande Sandwich
@client.command()
async def sandwich(ctx):
    q = tree("Bienvenue chez MCDO ! Quel menu souhaitez-vous ? (Végétarien ou Classique)")

    q.append("Végétarien, souhaitez-vous une formule ou un sandwich à l'unité ?", ["végétarien"], "Bienvenue chez MCDO ! Quel menu souhaitez-vous ? (Végétarien ou Classique)")
    q.append("Classique, souhaitez-vous une formule ou un sandwich à l'unité ?", ["classique"], "Bienvenue chez MCDO ! Quel menu souhaitez-vous ? (Végétarien ou Classique)")
    
    q.append("Formule, Quel type de pain souhaitez-vous ? (Complet,Baguette,Ciabatta)", ["formule"], "Végétarien, souhaitez-vous une formule ou un sandwich à l'unité ?")
    q.append("Unité, Quel type de pain souhaitez-vous ? (Complet,Baguette,Ciabatta)", ["unité"], "Végétarien, souhaitez-vous une formule ou un sandwich à l'unité ?")
    q.append("Formule, Quel type de pain souhaitez-vous ? (Complet,Baguette,Ciabatta)", ["formule"], "Classique, souhaitez-vous une formule ou un sandwich à l'unité ?")
    q.append("Unité, Quel type de pain souhaitez-vous ? (Complet,Baguette,Ciabatta)", ["unité"], "Classique, souhaitez-vous une formule ou un sandwich à l'unité ?")  

    q.append("Complet, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)", ["complet"], "Formule, Quel type de pain souhaitez-vous ? (Complet,Baguette,Ciabatta)")
    q.append("Baguette, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)", ["baguette"], "Formule, Quel type de pain souhaitez-vous ? (Complet,Baguette,Ciabatta)")
    q.append("Ciabatta, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)", ["ciabatta"], "Formule, Quel type de pain souhaitez-vous ? (Complet,Baguette,Ciabatta)")
    q.append("Complet, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)", ["complet"], "Unité, Quel type de pain souhaitez-vous ? (Complet,Baguette,Ciabatta)")
    q.append("Baguette, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)", ["baguette"], "Unité, Quel type de pain souhaitez-vous ? (Complet,Baguette,Ciabatta)")
    q.append("Ciabatta, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)", ["ciabatta"], "Unité, Quel type de pain souhaitez-vous ? (Complet,Baguette,Ciabatta)")



    q.append("Fromage, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)", ["fromage"], "Complet, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)")
    q.append("Jambon, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)", ["jambon"], "Complet, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)")
    q.append("Poulet grillé, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)", ["poulet grillé"], "Complet, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)")
    q.append("Thon, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)", ["thon"], "Complet, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)")
    q.append("Saumon fumé, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)", ["Saumon fumé"], "Complet, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)")
    q.append("Fromage, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)", ["fromage"], "Baguette, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)")
    q.append("Jambon, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)", ["jambon"], "Baguette, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)")
    q.append("Poulet grillé, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)", ["poulet grillé"], "Baguette, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)")
    q.append("Thon, Quel type de salade souhaitez-vous ? (salade verte,fromage,carottes râpées)", ["thon"], "Baguette, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)")
    q.append("Saumon fumé, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)", ["Saumon fumé"], "Baguette, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)")
    q.append("Fromage, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)", ["fromage"], "Ciabatta, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)")
    q.append("Jambon, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)", ["jambon"], "Ciabatta, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)")
    q.append("Poulet grillé, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)", ["poulet grillé"], "Ciabatta, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)")
    q.append("Thon, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)", ["thon"], "Ciabatta, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)")
    q.append("Saumon fumé, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)", ["Saumon fumé"], "Ciabatta, Quel type de garniture souhaitez-vous ? (Fromage,jambon,poulet grillé,thon,saumon fumé)")
    


    q.append("Salade verte, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)", ["salade verte"], "Fromage, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)")
    q.append("Tomates, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)", ["tomates"], "Fromage, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)")
    q.append("Concombre, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)", ["concombre"], "Fromage, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)")
    q.append("Carottes râpées, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)", ["carottes râpées"], "Fromage, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)")

    q.append("Salade verte, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)", ["salade verte"], "Jambon, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)")
    q.append("Tomates, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)", ["tomates"], "Jambon, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)")
    q.append("Concombre, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)", ["concombre"], "Jambon, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)")
    q.append("Carottes râpées, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)", ["carottes râpées"], "Jambon, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)")

    q.append("Salade verte, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)", ["salade verte"], "Poulet grillé, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)")
    q.append("Tomates, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)", ["tomates"], "Poulet grillé, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)")
    q.append("Concombre, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)", ["concombre"], "Poulet grillé, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)")
    q.append("Carottes râpées, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)", ["carottes râpées"], "Poulet grillé, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)")

    q.append("Salade verte, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)", ["salade verte"], "Thon, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)")
    q.append("Tomates, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)", ["tomates"], "Thon, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)")
    q.append("Concombre, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)", ["concombre"], "Thon, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)")
    q.append("Carottes râpées, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)", ["carottes râpées"], "Thon, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)")

    q.append("Salade verte, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)", ["salade verte"], "Saumon fumé, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)")
    q.append("Tomates, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)", ["tomates"], "Saumon fumé, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)")
    q.append("Concombre, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)", ["concombre"], "Saumon fumé, Quel type de salade souhaitez-vous  (salade verte,concombre,carottes râpées)?")
    q.append("Carottes râpées, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)", ["carottes râpées"], "Saumon fumé, Quel type de salade souhaitez-vous ? (salade verte,concombre,carottes râpées)")


    q.append("Mayonnaise, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)", ["mayonnaise"], "Salade verte, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)")
    q.append("Ketchup, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)", ["ketchup"], "Salade verte, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)")
    q.append("Barbecue, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)", ["barbecue"], "Salade verte, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)")

    q.append("Mayonnaise, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)", ["mayonnaise"], "Tomates, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)")
    q.append("Ketchup, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)", ["ketchup"], "Tomates, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)")
    q.append("Barbecue, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)", ["barbecue"], "Tomates, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)")

    q.append("Mayonnaise, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)", ["mayonnaise"], "Concombre, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)")
    q.append("Ketchup, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)", ["ketchup"], "Concombre, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)")
    q.append("Barbecue, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)", ["barbecue"], "Concombre, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)")

    q.append("Mayonnaise, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)", ["mayonnaise"], "Carottes râpées, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)")
    q.append("Ketchup, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)", ["ketchup"], "Carottes râpées, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)")
    q.append("Barbecue, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)", ["barbecue"], "Carottes râpées, Quelle sauce souhaitez-vous ? (barbecue,ketchup,mayonnaise)")




    q.append("Plate, Quel type de dessert souhaitez-vous ? (fruit,gâteau,yaourt)", ["plate"], "Mayonnaise, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)")
    q.append("Gazeuse, Quel type de dessert souhaitez-vous ? (fruit,gâteau,yaourt)", ["gazeuse"], "Mayonnaise, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)")
    q.append("Soda, Quel type de dessert souhaitez-vous ? (fruit,gâteau,yaourt)", ["soda"], "Mayonnaise, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)")

    q.append("Plate, Quel type de dessert souhaitez-vous ? (fruit,gâteau,yaourt)", ["plate"], "Ketchup, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)")
    q.append("Gazeuse, Quel type de dessert souhaitez-vous ? (fruit,gâteau,yaourt)", ["gazeuse"], "Ketchup, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)")
    q.append("Soda, Quel type de dessert souhaitez-vous ? (fruit,gâteau,yaourt)", ["soda"], "Ketchup, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)")

    q.append("Plate, Quel type de dessert souhaitez-vous ? (fruit,gâteau,yaourt)", ["plate"], "Barbecue, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)")
    q.append("Gazeuse, Quel type de dessert souhaitez-vous ? (fruit,gâteau,yaourt)", ["gazeuse"], "Barbecue, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)")
    q.append("Soda, Quel type de dessert souhaitez-vous ? (fruit,gâteau,yaourt)", ["soda"], "Barbecue, Quel type de boisson souhaitez-vous ? (plate,gazeuse,soda)")



    q.append("Fruit, Merci de votre commande", ["fruit"], "Plate, Quel type de dessert souhaitez-vous ? (fruit,gâteau,yaourt)")
    q.append("Gâteau, Merci de votre commande", ["gâteau"], "Plate, Quel type de dessert souhaitez-vous ? (fruit,gâteau,yaourt)")
    q.append("Yaourt, Merci de votre commande", ["yaourt"], "Plate, Quel type de dessert souhaitez-vous ? (fruit,gâteau,yaourt)")

    q.append("Fruit, Merci de votre commande", ["fruit"], "Gazeuse, Quel type de dessert souhaitez-vous ? (fruit,gâteau,yaourt)")
    q.append("Gâteau, Merci de votre commande", ["gâteau"], "Gazeuse, Quel type de dessert souhaitez-vous ? (fruit,gâteau,yaourt)")
    q.append("Yaourt, Merci de votre commande", ["yaourt"], "Gazeuse, Quel type de dessert souhaitez-vous ? (fruit,gâteau,yaourt)")
    
    q.append("Fruit, Merci de votre commande", ["fruit"], "Soda, Quel type de dessert souhaitez-vous ? (fruit,gâteau,yaourt)")
    q.append("Gâteau, Merci de votre commande", ["gâteau"], "Soda, Quel type de dessert souhaitez-vous ? (fruit,gâteau,yaourt)")
    q.append("Yaourt, Merci de votre commande", ["yaourt"], "Soda, Quel type de dessert souhaitez-vous ? (fruit,gâteau,yaourt)")


    await ctx.send(q.get_question())

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    current_question = q.get_question()
    while current_question:
        try:
            msg = await client.wait_for('message', check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.send("Temps écoulé, votre commande a été annulée.")
            await client.close()
            return

        reponse = msg.content.lower().strip()  
        question_suivante = q.choice(reponse)
        if not question_suivante:
            await ctx.send("Merci d'avoir passé commande !")
            await client.close()
            return
        else:
            current_question = question_suivante
            await ctx.send(current_question)

@client.command()
async def informatique(ctx):

    q = tree("Bonjour, quel langage informatique voulez-vous utiliser ? (Java, PHP, Python, Go, Ruby, C++)")


    q.append("Voici un document Java : https://fr.wikipedia.org/wiki/Java_(langage)", ["java"], "Bonjour, quel langage informatique voulez-vous utiliser ? (Java, PHP, Python, Go, Ruby, C++)")
    q.append("Voici un document PHP : https://fr.wikipedia.org/wiki/PHP", ["php"], "Bonjour, quel langage informatique voulez-vous utiliser ? (Java, PHP, Python, Go, Ruby, C++)")
    q.append("Voici un document Python : https://fr.wikipedia.org/wiki/Python_(langage)", ["python"], "Bonjour, quel langage informatique voulez-vous utiliser ? (Java, PHP, Python, Go, Ruby, C++)")
    q.append("Voici un document Go : https://fr.wikipedia.org/wiki/Go_(langage)", ["go"], "Bonjour, quel langage informatique voulez-vous utiliser ? (Java, PHP, Python, Go, Ruby, C++)")
    q.append("Voici un document Ruby : https://fr.wikipedia.org/wiki/Ruby_(langage)", ["ruby"], "Bonjour, quel langage informatique voulez-vous utiliser ? (Java, PHP, Python, Go, Ruby, C++)")
    q.append("Voici un document C++ : https://fr.wikipedia.org/wiki/C++", ["c++"], "Bonjour, quel langage informatique voulez-vous utiliser ? (Java, PHP, Python, Go, Ruby, C++)")


    question = q.get_question()
    await ctx.send(question)


    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    while True:
        try:
            response = await client.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send("Temps écoulé. Veuillez réessayer.")
            break


        if response.content.lower() == "aide":
            await ctx.send("Entrez le nom du langage informatique pour recevoir un document à ce sujet. Entrez 'reset' pour recommencer la conversation. Entrez 'liste' pour voir tous les langages disponibles.")
        elif response.content.lower() == "reset":
            q.reset()
            question = q.get_question()
            await ctx.send("Conversation réinitialisée.")
            await ctx.send(question)
        elif response.content.lower() == "liste":
            languages = ", ".join([node.answer_to_go_here[0] for node in q.current_node.next_nodes])
            await ctx.send("Voici une liste des langages disponibles: " + languages)
            await ctx.send(q.get_question())
        else:
            question = q.choice(response.content.lower())
            if question.startswith("Voici un document"):
                await ctx.send(question)
                break
            else:
                await ctx.send(question)
                await ctx.send(q.get_question())

    # Envoyer un message de fin de conversation
    await ctx.send("Merci d'avoir utilisé ce service ! N'hésitez pas à revenir si vous avez d'autres questions sur les langages informatiques.") 





# Commmande Traduction
@client.command(name='traduire', aliases=['tr'])
async def translate_text(ctx, lang: str, *, text: str):
    """
    Traduire un texte dans une langue spécifique.
    Syntaxe: +traduire [code de langue cible] [texte à traduire]
    Exemple: +traduire es Hello, world!
    """
    if lang not in LANGUAGES:
        lang_list = "\n".join([f"{key}: {value}" for key, value in LANGUAGES.items()])
        await ctx.send(f"La langue '{lang}' n'est pas prise en charge. Voici la liste des langues supportées :\n{lang_list}")
        return
    
    try:
        translated = translator.translate(text, dest=lang)
        await ctx.send(f"**Texte original:**\n{text}\n\n**Texte traduit ({LANGUAGES[lang].capitalize()}):**\n{translated.text}")
        await read_translation(ctx, text=translated.text)
    except Exception as e:
        await ctx.send("Une erreur s'est produite lors de la traduction.")

# Commmande Affiche les langues 
@client.command(name='langues')
async def display_languages(ctx):
    """
    Afficher la liste des langues prises en charge avec leurs alias.
    """
    languages = []
    for code, name in LANGUAGES.items():
        languages.append(f"{code}: {name.capitalize()}")
    await ctx.send("**Langues prises en charge avec leurs alias :**\n" + "\n".join(languages))



@client.command(name='lire')
async def read_translation(ctx, *, text: str):
    """
    Lire une traduction à haute voix.
    Syntaxe: +lire [texte à lire]
    """
    try:
        lang = translator.detect(text).lang
        translated = translator.translate(text, dest=lang)
        
        with BytesIO() as file:
            tts = gTTS(translated.text, lang=lang)
            tts.write_to_fp(file)
            file.seek(0)
            await ctx.send(f"**Texte à lire ({LANGUAGES[lang].capitalize()}):**", file=discord.File(file, filename=f"{translated.text}.mp3"))
    except Exception as e:
        await ctx.send("Une erreur s'est produite lors de la lecture du texte.")

@client.command()
@commands.has_permissions(ban_members=True)  
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} a été banni. Raison : {reason}")

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} a été expulsé du serveur pour la raison suivante : {reason}")





client.run("MTA5MTMzNDI4NjE5NzY3MDAwOA.G8Nevc.Yv-37WbvHEM5De4SwgW7Hl2O5C9FkYxil41k4A")
