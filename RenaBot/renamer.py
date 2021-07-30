from RenaBot.config import client as C
from telethon import events,Button
from RenaBot.breh import download_without_progressbar
from RenaBot.breh import upload_without_progress_bar
from telethon.utils import is_image,get_input_media
import re
import os
import shutil 

Batch=False
AutoBatch=False
usage= False

@C.on(events.NewMessage(pattern="/start"))
async def st(event):
    await event.reply("What are you trying to achieve ?")
    
@C.on(events.NewMessage(pattern="/help"))
async def hel(event):
    await event.reply('''1) /setthumb - reply to an image and make it thumbnail.
2)/setthumb to replace your previous thumb.
3)/remthumb - Removes the last set thumb.
4) /rename - Renames and sets thumb for a single file. Reply to the file you wanna rename.
5) /batch- Renames and sets thumb for multiple files. Reply to the first forwarded post.
6) /autoforward -  use this followed by channel/group id and message from where u replied will be forwarded.
7) /batch(number) - it will rename as many files as specified on number. eg - /batch5 (name of file). 5 Files will be renamed.
8)/autoforward(number) -  use this followed by channel/group id and message from where u replied will be forwarded. eg- /autoforward5 will auto forward 5 next files.


Only works for batchrename- Batch rename will add default counter in the end which starts from 1 if you want to start numbering from some other number. use 
#zzz123


#zzz wherever you write this, the numbering will start so, be careful.


123 is any number.


IMPORTANT- DO NOT PROVIDE FILE EXTENSION !!! IT WILL AUTO DETECT.''')

@C.on(events.NewMessage(pattern="/setthumb"))
async def thumb(event):
    reply=await event.get_reply_message()
    if is_image(reply):
        thumb = await C.download_media(reply.photo)
        with open(thumb, "rb") as i:
            Pic = i.read()
        with open(f"Thumbs\\{event.peer_id.user_id}.png", "wb") as i:
            i.write(Pic)
        await event.reply("Image set as thumb.")
        os.remove(thumb)
    else:
        await event.reply("Image not found.")
    
@C.on(events.NewMessage(pattern="/rename"))
async def renamer(event):
    global usage
    if usage==False:
        usage=True
    else:
        await event.reply("Currently, someone else is using the bot.")
        return
        
    text=event.raw_text
    reply=await event.get_reply_message()
    if event.is_reply:
        pass
    else:
        await event.reply("Reply to something to rename it.")
        return
    try:
        text=text.split(" ",maxsplit=1)[1]
    except IndexError:
         await event.reply("Yea, I should rename it as nothing then ?")
         return
    if text=="":
        await event.reply("Yea, I should rename it as nothing then ?")
        return
    if '.' in text:
        await event.reply("Sorry, we don't rename files with '.' in the renamed text. A precaution to prevent harm to your files.We automatically detect and put extensions.")
        return
    try:
        a=get_input_media(reply)
    except TypeError:
        await event.reply("No media found to rename.")
        return  
    await event.reply("Please wait while we rename your file.")
    download=await download_without_progressbar(client=C,msg=reply,down_location=f'{event.peer_id.user_id}\\')
    download_ext='.'+download.split(".")[-1]
    await event.reply("Please wait while we upload your file.")
    if os.path.exists(f"Thumbs\\{event.peer_id.user_id}.png"):
        await upload_without_progress_bar(client=C,entity=event.chat_id,file_location=download, name=f'{text}{download_ext}',thumbnail=f"Thumbs\\{event.peer_id.user_id}.png")
    else:
        await upload_without_progress_bar(client=C,entity=event.chat_id,file_location=download, name=f'{text}{download_ext}')
    shutil.rmtree((f'{event.peer_id.user_id}\\'))
    usage=False
###TOO MUCH SHIT TO TAMPER WITH#####  END GAME
@C.on(events.NewMessage(pattern="/batch"))
async def batchrenamer(event):
    global usage
    if usage==False:
        usage=True
    else:
        await event.reply("Currently, someone else is using the bot.")
        return
    if event.is_reply:
        pass
    else:
        await event.reply("Reply to something to rename it.")
        return
    reply=await event.get_reply_message()
    text=event.raw_text
    if '.' in text:
        await event.reply("Sorry, we don't rename files with '.' in the renamed text. A precaution to prevent harm to your files.We automatically detect and put extensions.")
        return
    text=text.split(" ",1)
    try:
        _=text[1]
    except:
        await event.reply("Can't rename the files without any input.")  
        return
    Amount_Fetcher=int(*re.findall(r'\d+', text[0]))
    if Amount_Fetcher==0:
        Batch=False
    else:
        Batch=True
    temp=text[1]
    if '#zzz' in temp:
        number=temp.split("#zzz",1)
        file_name=number[0]
        file_name=file_name.strip()
        try:
            number=int(number[1])
        except:
            await event.reply("Enter a number after zzz not text.")
            return
    else:
        number=1
        file_name=temp.strip()
        
    if Batch==True:
        start=reply.id
        end=start+Amount_Fetcher
    elif Batch==False:
        start=reply.id
        end=event.id
    
    for i in range(start,end):
        message=await C.get_messages(event.chat_id,ids=i)
        try:
            a=get_input_media(message)
        except:
            continue
        if i==start:
            await event.reply("Please sit back and relax. This might take a while...")
        else:
            pass
        download=await download_without_progressbar(client=C,msg=message,down_location=f"{event.peer_id.user_id}\\")
        download_ext='.'+download.split(".")[-1]
        if os.path.exists(f"Thumbs\\{event.peer_id.user_id}.png"):
            await upload_without_progress_bar(client=C,entity=event.chat_id,file_location=download, name=f"{file_name} {number}{download_ext}",thumbnail=f"Thumbs\\{event.peer_id.user_id}.png")
        else:
            await upload_without_progress_bar(client=C,entity=event.chat_id,file_location=download, name=f"{file_name} {number}{download_ext}")
        number=number+1
    await event.reply("Process Finished.")
    usage=False
    shutil.rmtree((f'{event.peer_id.user_id}\\'))   
        
@C.on(events.NewMessage(pattern="/autoforward"))
async def auto(event):
    if event.is_reply:
        pass
    else:
        await event.reply("Reply to a message, you can't make use of command like this.")
        return
    reply=await event.get_reply_message()
    text=event.raw_text
    try:
        _=text[1]
    except:
        await event.reply("Can't forward to nothingness")  
        return
    Amount_Fetcher=int(*re.findall(r'\d+', text[0]))
    if Amount_Fetcher==0:
        AutoBatch=False
    else:
        AutoBatch=True
    await event.reply(text[1])
    if text[1].isdigit():
        text[1]='-100'+text[1]
        try:
            a=await C.get_entity(int(text[1]))
        except Exception as e:
            await event.reply(e)
            await event.reply("Chat not found, Add me to the chat, so i can do something about it.")
        chat=a
    else:
        try:
            a=await C.get_permission(int(f"t.me/{text[1]}"))
        except:
            await event.reply("Chat not found, Add me to the chat, so i can do something about it.")
            return
        chat=a
    if AutoBatch==True:
        start=reply.id
        end=start+Amount_Fetcher
    elif AutoBatch==False:
        start=reply.id
        end=event.id
    for i in range(start,end):
        message=await C.get_messages(event.chat_id,ids=i)
        await C.send_message(chat,message)   
            
        
@C.on(events.NewMessage(pattern="/remthumb"))
async def rem(event):
    if os.path.exists(f"Thumbs\\{event.peer_id.user_id}.png"):
        os.remove(f"Thumbs\\{event.peer_id.user_id}.png")
        await event.reply("Thumb Deleted.")
        return               
    else:
        await event.reply("You haven't set a thumb.")
    