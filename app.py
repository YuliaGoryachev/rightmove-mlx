from PIL import Image
import pytesseract
from fastapi import FastAPI, HTTPException
import scraper
from scraper import get_floorplan
from openai_parsing import get_floor_area
import requests

app = FastAPI()

# Local file path to save the image
async def download(url):
        url = await get_floorplan([url])
        print('url of floorplan', url)
        local_file_path = "downloaded_image.jpeg"
        try:
                # Download the image
                response = requests.get(url[0])
                if response.status_code == 200:
                        with open(local_file_path, 'wb') as file:
                                file.write(response.content)
                                print(f"Image successfully downloaded and saved to {local_file_path}")
                else:
                        print(f"Failed to download the image. Status code: {response.status_code}")
        except Exception as e:
                print(f"An error occurred: {e}")


@app.post("/download-image/")
async def download_image(url):
        print(url)
        try:
                #Download the image
                await download(url)
                image_path = "downloaded_image.jpeg"
                print('downloaded')
                # Perform OCR
                image = Image.open(image_path)
                # Extract text using Tesseract
                extracted_text = pytesseract.image_to_string(image)

                # Print the extracted text
                print("Extracted Text:\n")
                print('url: ', url)
                print(extracted_text[:1000])
                ans = get_floor_area(extracted_text[:1000])
                print('openai reply: \n', ans)
                return {"message": f"house info is: {ans}"}
        except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
