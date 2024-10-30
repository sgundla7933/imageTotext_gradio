import os
import io
import base64
import requests
import json
from PIL import Image
import gradio as gr
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) 

hf_api_key = os.environ['HF_API_KEY']
TTI_ENDPOINT = os.environ['HF_API_TTI_BASE']
ITT_ENDPOINT = os.environ['HF_API_ITT_BASE']

# Helper functions
def get_completion(inputs, parameters=None, ENDPOINT_URL=""):
    headers = {
        "Authorization": f"Bearer {hf_api_key}",
        "Content-Type": "application/json"
    }
    data = {"inputs": inputs}
    if parameters is not None:
        data.update({"parameters": parameters})
    
    response = requests.post(ENDPOINT_URL, headers=headers, json=data)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
    # Check if the response is JSON or binary
    if "application/json" in response.headers.get("Content-Type", ""):
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Failed to decode JSON. Response was:", response.content)
            return None
    else:
        # For binary data, return the raw content
        return response.content

def image_to_base64_str(pil_image):
    pil_image = pil_image.resize((512, 512))  # Resize to reduce payload size
    byte_arr = io.BytesIO()
    pil_image.save(byte_arr, format='PNG')
    byte_arr = byte_arr.getvalue()
    return str(base64.b64encode(byte_arr).decode('utf-8'))

def base64_to_pil(img_base64):
    base64_decoded = base64.b64decode(img_base64)
    byte_stream = io.BytesIO(base64_decoded)
    return Image.open(byte_stream)

# Main functions
def captioner(image):
    base64_image = image_to_base64_str(image)
    result = get_completion(base64_image, None, ITT_ENDPOINT)
    if result and isinstance(result, list) and 'generated_text' in result[0]:
        return result[0]['generated_text']
    else:
        return "Error: Unable to generate caption."

def generate(prompt):
    output = get_completion(prompt, None, TTI_ENDPOINT)
    
    # Check if we received binary data or JSON
    if isinstance(output, bytes):
        # Convert binary data to an image
        byte_stream = io.BytesIO(output)
        image = Image.open(byte_stream)
        return image
    elif output:
        # If output is JSON, look for potential keys that might contain the image data
        base64_image = output.get('generated_images') or output.get('image') or output.get('data')
        
        # Check if base64_image is a list or a single string, and decode if possible
        if base64_image:
            if isinstance(base64_image, list):
                base64_image = base64_image[0]  # Take the first image if it's in a list
            
            # Decode base64 image and return as PIL image
            return base64_to_pil(base64_image)
        else:
            return "Error: Image data not found in API response. Check response format."
    else:
        return "Error: No output from API."

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# Describe-and-Generate game 🖍️")
    image_upload = gr.Image(label="Your first image", type="pil")
    btn_caption = gr.Button("Generate caption")
    caption = gr.Textbox(label="Generated caption")
    btn_image = gr.Button("Generate image")
    image_output = gr.Image(label="Generated Image")
    
    btn_caption.click(fn=captioner, inputs=[image_upload], outputs=[caption])
    btn_image.click(fn=generate, inputs=[caption], outputs=[image_output])

demo.launch(share=True, server_port=int(os.environ['PORT1']))

def caption_and_generate(image):
    # Generate caption
    base64_image = image_to_base64_str(image)
    caption_result = get_completion(base64_image, None, ITT_ENDPOINT)
    
    # Verify if caption generation succeeded
    if caption_result and isinstance(caption_result, list) and 'generated_text' in caption_result[0]:
        caption = caption_result[0]['generated_text']
    else:
        return "Error: Unable to generate caption.", None
    
    # Generate image based on caption
    image_result = get_completion(caption, None, TTI_ENDPOINT)
    
    # Check if the image generation returned binary data or JSON with base64
    if isinstance(image_result, bytes):
        byte_stream = io.BytesIO(image_result)
        generated_image = Image.open(byte_stream)
    elif image_result:
        base64_image = image_result.get('generated_images') or image_result.get('image') or image_result.get('data')
        if base64_image:
            if isinstance(base64_image, list):
                base64_image = base64_image[0]
            generated_image = base64_to_pil(base64_image)
        else:
            return caption, "Error: Image data not found in API response."
    else:
        return caption, "Error: No output from API."

    return caption, generated_image

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# Describe-and-Generate game 🖍️")
    image_upload = gr.Image(label="Your first image", type="pil")
    btn_all = gr.Button("Caption and generate")
    caption = gr.Textbox(label="Generated caption")
    image_output = gr.Image(label="Generated Image")

    btn_all.click(fn=caption_and_generate, inputs=[image_upload], outputs=[caption, image_output])

gr.close_all()
demo.launch(share=True, server_port=int(os.environ['PORT2']))
