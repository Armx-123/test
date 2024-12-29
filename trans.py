import os
import requests
import urllib
from urllib.parse import quote
from PIL import Image


class ImageDownloader:
  def __init__(self):
    pass

  @staticmethod
  def _download_page(url):
    try:
      headers = {}
      headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                              "Chrome/77.0.3865.90 Safari/537.36"
      req = urllib.request.Request(url, headers=headers)
      resp = urllib.request.urlopen(req)
      respData = str(resp.read())
      return respData

    except Exception as e:
      print(e)
      exit(0)

  def download(self, keyword, directory='images', extensions={'.jpg', '.png', '.jpeg'}):
    if not os.path.exists(directory):
      os.makedirs(directory)

    url = 'https://www.google.com/search?q=' + quote(
        keyword.encode('utf-8')) + '&biw=1536&bih=674&tbm=isch&sxsrf=ACYBGNSXXpS6YmAKUiLKKBs6xWb4uUY5gA:1581168823770&source=lnms&sa=X&ved=0ahUKEwioj8jwiMLnAhW9AhAIHbXTBMMQ_AUI3QUoAQ'
    raw_html = self._download_page(url)

    end_object = -1
    skipped = 0  # Counter for skipped images
    download_success = False 

    while True:
      try:
        new_line = raw_html.find('"https://', end_object + 1)
        end_object = raw_html.find('"', new_line + 1)

        if new_line == -1 or end_object == -1:
          break

        object_raw = raw_html[new_line + 1:end_object]

        # Check if the URL has a valid image extension
        if any(extension in object_raw for extension in extensions):
          skipped += 1
          if skipped > 3:  # Skip the first 3 valid images
            break

        # Download the image
        r = requests.get(object_raw, allow_redirects=True, timeout=1)
        if 'html' not in str(r.content):
          # Extract file extension from URL (assuming it's valid)
          file_extension = os.path.splitext(object_raw)[1].lower()

          if file_extension not in extensions:
            continue  # Skip to the next URL if format is unsupported

          file_name = f"{keyword.replace(' ', '_')}{file_extension}"
          file_path = os.path.join(directory, file_name)

          with open(file_path, 'wb') as file:
            file.write(r.content)
          print(f"Image saved as {file_path}")
          download_success = True 
          break 

      except Exception as e:
        print(f"Error downloading image: {e}")
        continue  # Continue to the next URL on any error

      if download_success:
        break

    if not download_success:
      print("No valid image found.")

  @staticmethod
  def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
      return img.size


# Usage example
if __name__ == "__main__":
  downloader = ImageDownloader()
  downloader.download("beautiful park sunny day")
