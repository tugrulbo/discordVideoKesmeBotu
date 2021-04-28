import os
import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
from discord.utils import get
import datetime
import json
import discord
from discord.ext import commands
import youtube_dl as yt
import youtube_dl
from youtube_search import YoutubeSearch
import asyncio
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip



url =""


ytdl_format_options = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]',
        'outtmpl': 'video1.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
    }

ffmpeg_options = {
        'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource():
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)


class CommandsEvents(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    async def convertToGif(self):
        trimmed_video = VideoFileClip("test.mp4")
        trimmed_video.write_gif("test.gif",fps=10)
    


    @commands.command(name="trimVideo")
    async def trimmedVideo(self, ctx):
        if ctx.message.content.startswith('.trimVideo'):
            message = ctx.message.content
            replace_prefix = message.replace('.trimVideo',"")
            split_content = replace_prefix.split('|')
            print(split_content)
            url = split_content[0]
            url = url.strip()
            start_time = split_content[1]
            start_time = start_time.strip()
            end_time = split_content[2]
            end_time= end_time.strip()
            async with ctx.typing():
                await YTDLSource.from_url(url, stream=False)
                
            ffmpeg_extract_subclip("video1.mp4", int(start_time), int(end_time), targetname="test.mp4")
            await ctx.send(file=discord.File("test.mp4"))
            os.remove("video1.mp4")
            os.remove("test.mp4")
        
            
    
    
def setup(bot):
    bot.add_cog(CommandsEvents(bot))