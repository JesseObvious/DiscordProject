from PIL import Image, ImageFilter, ImageDraw, ImageFont
import math
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import base64
import os
from dotenv import load_dotenv

dotenv_path = '../../.env'
load_dotenv(dotenv_path)

userName = os.environ.get("userName")
userName = str(userName)

#Relative Path
#Image on which we want to paste
def dropShadow( image, offset=(5,5), background=(255, 255, 255), shadow=(255, 255, 255), border=10, iterations=3):

  # Create the backdrop image -- a box in the background colour with a 
  # shadow on it.
  totalWidth = image.size[0] + abs(offset[0]) + 2*border
  totalHeight = image.size[1] + abs(offset[1]) + 2*border
  back = Image.new(image.mode, (totalWidth, totalHeight), background)
  
  # Place the shadow, taking into account the offset from the image
  shadowLeft = border + max(offset[0], 0)
  shadowTop = border + max(offset[1], 0)
  back.paste(shadow, [shadowLeft, shadowTop, shadowLeft + image.size[0], shadowTop + image.size[1]] )
  
  # Apply the filter to blur the edges of the shadow.  Since a small kernel
  # is used, the filter must be applied repeatedly to get a decent blur.
  n = 0
  while n < iterations:
    back = back.filter(ImageFilter.BLUR)
    n += 1
    
  # Paste the input image onto the shadow backdrop  
  imageLeft = border - min(offset[0], 0)
  imageTop = border - min(offset[1], 0)
  back.paste(image, (imageLeft, imageTop))
  
  return back
  
if __name__ == "__main__":
    import sys

    #Building search string to find the movie art
    with open ('/home/' + userName +'/DiscordProject/PythonPlex/TxtFiles/FullDownloadname.txt') as f:
        Input = f.read()
        Input = Input.split(')')
        UserInput = Input[0].replace('(', '')
        UserInput = Input[0].replace('(', ' ')
        MovieTitle = str(UserInput)
        UserInput = UserInput.replace(' ', '+')

    PictureScrape = 'https://www.google.com/search?q='+UserInput+'+movie&sxsrf=AOaemvI2Y253PrzgCOE6rQqzPm9uBtfdiQ:1638907971264&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjO0sj7v9L0AhXBGc0KHQD5AY0Q_AUoAnoECAMQBA&biw=2560&bih=955&dpr=1'
   
    #rendering the Java on the page 
    session = HTMLSession() 
    session = session.get(PictureScrape)
    session.html.render()

    #finding name and description link
    soup = BeautifulSoup(session.html.html, 'lxml')
    Link = soup.find(id = "islrg")
    Link = Link.find(class_ = "wXeWr islib nfEiy")
    Link = str(Link)
    
    #cleaning
    Link = Link.split('src="')
    Link = Link[1].split('" width')
    Link = Link[0]
    Link = Link[23:]
    Link = Link.encode('utf-8')
  
    #decoding the file from base64 and saving it
    with open("/home/" + userName + "/DiscordProject/PythonPlex/Art/art.jpeg", "wb") as fh:
      fh.write(base64.decodebytes(Link))

    #opening seed file
    with open ('/home/' + userName +'/DiscordProject/PythonPlex/TxtFiles/seeds.txt') as f:
        seeds = f.read()
        seeds = str(seeds)

    with open('/home/' + userName +'/DiscordProject/PythonPlex/TxtFiles/FileSize.txt') as d:
        fileSize = d.read()
        fileSize = str(fileSize)

    #Opening needed files to create the picture
    img = Image.open("/home/" + userName + "/DiscordProject/PythonPlex/Art/gradient.jpeg") 
    img2 = Image.open("/home/" + userName + "/DiscordProject/PythonPlex/Art/art.jpeg") 

    #setting the font and movetitle
    title_font = ImageFont.truetype('/home/' + userName + '/DiscordProject/PythonPlex/Fonts/static/OpenSans/OpenSans-SemiBold.ttf', 30)
    title = MovieTitle.upper()

    #Generating the file, drop shadow, and text. outputting it.
    image_editable = ImageDraw.Draw(img)
    image_editable.text((75, 40), title, (255, 255, 255), font=title_font)
    image_editable.text((170, 608), seeds, (255, 255, 255), font=title_font)
    image_editable.text((765, 608), fileSize, (255, 255, 255), font = title_font) 
    img2 = img2.resize((300, 425))
    img2 = dropShadow(img2)
    img.paste(img2, (60, 113))
    img.save('/home/' + userName + '/DiscordProject/PythonPlex/Art/pic.jpg', format = 'JPEG', subsampling = 0, quality = 100)

