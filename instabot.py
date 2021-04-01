import discord
import instagram
from environs import Env

env = Env()
env.read_env()  # read .env file, if it exists

client = discord.Client()

hashtag_search = instagram.HashtagSearch(
    env("INSTAGRAM_USERNAME"),
    env("INSTAGRAM_PASSWORD")
)


def create_embed_from_instapost(post):
    embed = discord.Embed(
        url=post.get_url(),
        description=post.get_description(),
        timestamp=post.get_timestamp()
    )

    embed.set_image(url=post.get_image_url())
    # embed.set_thumbnail(url=post.get_thumbnail_url())
    embed.set_author(
        name=post.get_profile_name(),
        url=post.get_profile_url(),
        icon_url=post.get_profile_picture_url()
    )
    return embed


@client.event
async def on_ready() -> None:
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('#'):
        message.content = message.content + ' hack'
        hashtag, _ = message.content.split(maxsplit=2)
        try:
            post = hashtag_search.get_random_post_for_hashtag(hashtag.lstrip('#'))
            await message.channel.send(embed=create_embed_from_instapost(post))
        except Exception as e:
            await message.channel.send(str(e))


client.run(env("DISCORD_TOKEN"))
