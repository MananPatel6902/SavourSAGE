### Health Management APP
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai  
from PIL import Image
import io

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("Google API Key not found! Please check your .env file.")

## Function to load Google Gemini Pro Vision API and get response
# def get_gemini_response(input_prompt, image_data, input_text):
#     try:
#         # Use correct function to generate text (adjust to your library’s method)
#         response = genai.generate_content(
#             model='text-bison-001',  # Adjust the model as needed
#             prompt=f"{input_prompt}\n{input_text}"
#         )
#         # Check for valid response structure
#         if 'generations' in response and len(response['generations']) > 0:
#             return response['generations'][0]['text']
#         else:
#             return "No valid response from the API."
#     except Exception as e:
#         return f"Error during API call: {str(e)}"


# def get_gemini_response(input_prompt, image_data=None, input_text=""):
    # try:
    #     # Combine prompt and input text
    #     full_prompt = f"{input_prompt}\n{input_text}" if input_text else input_prompt
        
    #     # Initialize the model
    #     model = genai.GenerativeModel('gemini-pro')
        
    #     # Generate content
    #     if image_data:
    #         # For multimodal requests (text + image)
    #         response = model.generate_content([full_prompt, image_data])
    #     else:
    #         # For text-only requests
    #         response = model.generate_content(full_prompt)
        
    #     # Check if response is valid
    #     if response and hasattr(response, 'text'):
    #         return response.text
    #     else:
    #         return "No valid response generated."
            
    # except Exception as e:
    #     return f"Error during API call: {str(e)}"

def get_gemini_response(input_prompt, image_data=None, input_text=""):
    try:
        # Combine prompt and input text
        full_prompt = f"{input_prompt}\n{input_text}" if input_text else input_prompt
        
        # Initialize the model
        model = genai.GenerativeModel('gemini-1.5-flash-002')
        
        # Handle image data conversion
        if image_data:
            # Check if image_data is in the format you provided
            if isinstance(image_data, list) and len(image_data) > 0 and 'data' in image_data[0]:
                # Convert bytes to PIL Image
                image_bytes = image_data[0]['data']
                image = Image.open(io.BytesIO(image_bytes))
                generation_response = model.generate_content([full_prompt, image])
            elif isinstance(image_data, (Image.Image, bytes)):
                # Handle direct PIL Image or bytes input
                if isinstance(image_data, bytes):
                    image = Image.open(io.BytesIO(image_data))
                else:
                    image = image_data
                generation_response = model.generate_content([full_prompt, image])
            else:
                raise ValueError("Unsupported image format")
        else:
            # Text-only request
            generation_response = model.generate_content(full_prompt)
        
        # Get the response
        if generation_response and hasattr(generation_response, 'text'):
            return generation_response.text
        else:
            return "No valid response generated."
            
    except Exception as e:
        return f"Error during API call: {str(e)}"

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file as a PIL image
        image = Image.open(uploaded_file)
        return image
    else:
        raise FileNotFoundError("No file uploaded")


## Initialize Streamlit app
st.set_page_config(page_title="SavourSAGE")

st.header("SavourSAGE")
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me the total calories")

input_prompt = """
You are an expert nutritionist where you need to see the food items from the image
and calculate the total calories, also provide the details of every food item with calorie intake in the format:

1. Item 1 - number of calories
2. Item 2 - number of calories
----
----
"""

## If submit button is clicked
if submit:
    if uploaded_file is not None:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.error("Please upload an image to proceed.")

# from dotenv import load_dotenv
# import streamlit as st
# import os
# import google.generativeai as genai
# from PIL import Image

# # Load environment variables
# load_dotenv()

# # Configure the generative AI model with your API key
# api_key = os.getenv("GOOGLE_API_KEY")

# if api_key:
#     genai.configure(api_key=api_key)
# else:
#     st.error("Google API Key not found! Please check your .env file.")

# # Function to generate content using the Google Generative AI
# def get_gemini_response(input_prompt, input_text="", image_data=None):
#     try:
#         # Combine prompt and input text
#         full_prompt = f"{input_prompt}\n{input_text}" if input_text else input_prompt

#         # Generate content, assuming images can be passed (adjust if the API does not support this)
#         if image_data:
#             response = genai.generate_content(
#                 model='text-bison-001',  # Adjust the model as needed
#                 prompt=full_prompt,
#                 images=[image_data]  # Replace with the correct parameter if necessary
#             )
#         else:
#             response = genai.generate_content(
#                 model='text-bison-001',  # Adjust the model as needed
#                 prompt=full_prompt
#             )
        
#         # Check if the response contains valid data
#         if 'generations' in response and len(response['generations']) > 0:
#             return response['generations'][0]['text']
#         else:
#             return "No valid response from the API."
#     except Exception as e:
#         return f"Error during API call: {str(e)}"

# def input_image_setup(uploaded_file):
#     if uploaded_file is not None:
#         # Read the file into bytes
#         bytes_data = uploaded_file.getvalue()

#         # Adjust the image format to match what the API expects (if needed)
#         image_parts = {
#             "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
#             "data": bytes_data
#         }
#         return image_parts
#     else:
#         raise FileNotFoundError("No file uploaded")

# # Initialize Streamlit app
# st.set_page_config(page_title="Gemini Health App")

# st.header("Gemini Health App")
# input_text = st.text_input("Input Prompt: ", key="input")
# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# if uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Image.", use_column_width=True)

# submit = st.button("Tell me the total calories")

# input_prompt = """
# You are an expert nutritionist where you need to see the food items from the image
# and calculate the total calories, also provide the details of every food item with calorie intake in the format:

# 1. Item 1 - number of calories
# 2. Item 2 - number of calories
# ----
# ----
# """

# # If submit button is clicked
# if submit:
#     if uploaded_file is not None:
#         try:
#             image_data = input_image_setup(uploaded_file)
#             response = get_gemini_response(input_prompt, input_text, image_data)
#             st.subheader("The Response is")
#             st.write(response)
#         except Exception as e:
#             st.error(f"Error processing the request: {str(e)}")
#     else:
#         st.error("Please upload an image to proceed.")