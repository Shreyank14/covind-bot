
import os
import random
import argparse
import time
import discord

from discord.ext import commands, tasks
from dotenv import load_dotenv
from cowinAPI import cowinapi

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv('DISCORD_CHANNEL')
ERROR_CHANNEL = os.getenv('DISCORD_ERROR_CHANNEL')
client = discord.Client()


final_update_messages = [
    'These are the latest updates. I will wait for sometime and check again for new slots',
    'That\'s all for now. I will be back with more updates as soon as they are available',
    'Hope this helps!',
    'These were the latest updates that I could fetch',
    'That\'s it for now. Stay safe, mask up'
]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
    This script is going to check for open vaccination slots. 
    """)

    parser.add_argument("--age", help="Min age for vaccination center")
    parser.add_argument(
        "--district", help="District ID where check needs to be done in")
    parser.add_argument(
        "--poll", help="Time interval between polling the cowin API.")

    args = parser.parse_args()
    age = args.age
    districtID = args.district
    poll = args.poll

    if age:
        age = int(args.age)
        print("Min Age: "+str(age))
    else:
        # get deafault
        age = int(os.getenv(('AGE')))
        print("Min Age: "+str(age))
    if districtID:
        print("Disctict ID: "+str(districtID))
    else:
        districtID = os.getenv('DISTRICT_ID')  # deafult
        print("Disctict ID: "+str(districtID))
    if poll:
        poll = int(args.poll)
        print("Poll timer: "+str(poll))
    else:
        poll = int(os.getenv('POLL'))  # deafult
        print("Poll timer: "+str(poll))

    def get_embed(center):
        disc = "Pincode: {}\nAvailable Capacity: {}\nDate: {}\nVaccie Name: {}\nFee Type: {}\nMin Age: {}\nBlock Name: {}\nAddress: {}".format(
            center['pincode'], center['available_capacity'], center['date'], center['vaccine'], center['fee_type'], center['age'], center['block_name'], center['address'])
        name = center['name']
        registration_url = 'https://selfregistration.cowin.gov.in/'
        embed = discord.Embed(title=name, url=registration_url,
                              description=disc, color=discord.Color.blue())
        return embed

    @tasks.loop(seconds=poll)  # task runs every 60 seconds
    async def my_background_task():
        channel = client.get_channel(int(CHANNEL))  # channel ID goes here
        cowin = cowinapi()
        vaccine_center = cowin.call_api(age, districtID)
        if vaccine_center == None:
            errorChannel = client.get_channel(int(ERROR_CHANNEL))
            await errorChannel.send("The Cowin API is currently not responding. Don't Worry I got your back, I will try again after some time.")
            time.sleep(60)
            return
        if len(vaccine_center['centers']) == 0:
            errorChannel = client.get_channel(int(ERROR_CHANNEL))
            await errorChannel.send("Currently, no centers in the requested district have vaccine available for the required age group")
            # time.sleep(300)  # wait for 5 minutes
        else:
            print(vaccine_center)
            for center in vaccine_center['centers']:
                embed = get_embed(center)
                await channel.send('NEW UPDATE!')
                await channel.send(embed=embed)
                print('Sending message to discord')
            final_update_message = random.choice(final_update_messages)
            await channel.send(final_update_message)
            time.sleep(180)

    @client.event
    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to my Discord server!'
        )

    @client.event
    async def on_ready():
        print(f'{client.user.name} has connected to Discord!')
        print('Logged in as')
        my_background_task.start()

    client.run(TOKEN)
