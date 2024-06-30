import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image
import os

load_dotenv()

if __name__ == "__main__":

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    img = PIL.Image.open(
        r'runs\detect\predict4\358131089_1598284357678845_8367029803511623159_n.jpg')

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(
        ["This is the result of a image from object detection algorithm, base on this, please discribe the context of the image", img])

    print(response.text)
