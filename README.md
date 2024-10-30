# imageTotext_gradio

## Features
- Upload an image to generate a descriptive caption.
- Generate new images based on the generated caption.
- Simple and intuitive user interface powered by Gradio.

## Technologies Used
- Python
- Gradio
- Hugging Face APIs
- PIL (Python Imaging Library)
- dotenv

## Installation

1. Clone the repository:
   git clone https://github.com/yourusername/describe-and-generate-game.git
   cd describe-and-generate-game

2. Install required packagee using pip
   pip install requests Pillow gradio python-dotenv

3. Create a .env file in the root directory with the following variables:
HF_API_KEY=your_hugging_face_api_key
HF_API_TTI_BASE=https://api-inference.huggingface.co/models/your_model_name_for_text_to_image
HF_API_ITT_BASE=https://api-inference.huggingface.co/models/your_model_name_for_image_to_text
PORT1=your_port_number_1
PORT2=your_port_number_2

4. Run the application
   python app.py

5. Open your web browser and go to http://localhost:<your_port_number_1>.

##Google slide presentation - https://docs.google.com/presentation/d/1byhvhQKKFjzfno1aZ71BQBTVxnsHvHxVyoOA-4QEY2s/edit?usp=sharing
