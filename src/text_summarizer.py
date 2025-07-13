import gradio as gr
import google.generativeai as genai
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import validators
import logging

# Configure logging
logging.basicConfig(filename='logs/llm_interactions.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")
genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

def count_words(text):
    """Count words in the input text."""
    return len(text.split()) if text.strip() else 0

def fetch_url_content(url, max_chars=700000):
    """Fetch text content from a URL with character limit."""
    if not validators.url(url):
        return "Invalid URL format."
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        if response.status_code == 429:
            return "Rate limit exceeded. Please try again later."
        soup = BeautifulSoup(response.text, "html.parser")
        text_elements = soup.find_all(["p", "h1", "h2", "h3", "article"])
        content = " ".join(element.get_text(strip=True) for element in text_elements)
        return content[:max_chars]
    except requests.exceptions.RequestException as e:
        return f"Error - We couldn't access the website: {str(e)}"

def summarize_text(input_text, word_count=100, tone="neutral"):
    """Summarize text using Gemini LLM."""
    tone_instructions = {
        "neutral": "Use clear, concise, and objective language with a neutral tone.",
        "formal": "Use precise, professional language suitable for formal reports or academic writing.",
        "casual": "Use relaxed, conversational language suitable for informal contexts.",
        "technical": "Use precise, domain-specific terminology suitable for technical audiences.",
        "engaging": "Use lively, attention-grabbing language to make the summary compelling."
    }
    tone_prompt = tone_instructions.get(tone, tone_instructions["neutral"])

    prompt = f"""
    Summarize the following text in approximately {word_count} words. 
    Focus on retaining the main ideas, key facts, and structure of the original text. 
    {tone_prompt}
    Ensure the summary closely matches the style and level of detail of a high-quality reference summary.
    Avoid omitting critical information or introducing extraneous details.
    Text: {input_text}
    """
    
    try:
        logging.info(f"Input text: {input_text[:1000]}...")
        logging.info(f"Prompt: {prompt}")
        logging.info(f"Tone used: {tone}")
        response = model.generate_content(prompt)
        logging.info(f"Summary: {response.text.strip()}")
        return response.text.strip()
    except genai.exceptions.ApiException as e:
        logging.error(f"API error: {str(e)}")
        if "rate limit" in str(e).lower():
            return "API rate limit exceeded. Please try again later."
        return f"Error generating summary: {str(e)}"
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return f"Error generating summary: {str(e)}"

def summarize_interface(input_type, text_input, url_input, word_count, tone):
    """Handle text or URL input for summarization with fixed max_input_chars."""
    max_input_chars = 700000  # Fixed maximum character limit
    min_input_chars = 200     # Fixed minimum character limit
    
    if input_type == "Text":
        if not text_input.strip():
            return "Please provide text to summarize."
        if len(text_input) < min_input_chars:
            return f"Input text must be at least {min_input_chars} characters."
        input_text = text_input[:max_input_chars]
        return summarize_text(input_text, word_count, tone)
    elif input_type == "URL":
        if not url_input.strip():
            return "Please provide a valid URL."
        content = fetch_url_content(url_input, max_chars=max_input_chars)
        if content.startswith("Error") or content.startswith("Invalid"):
            return content
        if len(content) < min_input_chars:
            return f"URL content must be at least {min_input_chars} characters."
        return summarize_text(content, word_count, tone)
    return "Invalid input type."

# Create Gradio interface
with gr.Blocks(title="AI Text Summarizer") as iface:
    gr.Markdown("""
    # AI Text Summarizer
    Summarize articles or text using Gemini LLM. Paste text or provide a URL, then customize summary length and tone.
    """)
    
    input_type = gr.Radio(choices=["Text", "URL"], label="Input Type", value="Text")
    
    gr.Markdown("**Input must be between 200 and 700,000 words.**")
    
    text_input = gr.Textbox(lines=10, placeholder="Paste your article or text here...", label="Text Input")
    word_count_display = gr.Textbox(label="Input Word Count", interactive=False)
    
    text_input.change(
        fn=count_words,
        inputs=text_input,
        outputs=word_count_display
    )
    
    url_input = gr.Textbox(placeholder="Enter a URL (e.g., https://example.com)", label="URL Input")
    
    with gr.Row():
        word_count = gr.Slider(minimum=100, maximum=100000, value=100, step=50, label="Summary Word Count")
        tone = gr.Dropdown(choices=["neutral", "formal", "casual", "technical", "engaging"], label="Tone", value="neutral")
    
    submit_btn = gr.Button("Generate Summary")
    
    output = gr.Textbox(label="Summary")
    
    submit_btn.click(
        fn=summarize_interface,
        inputs=[input_type, text_input, url_input, word_count, tone],
        outputs=output
    )
    
    gr.Examples(
        examples=[
            ["Text", "Onam is the most important and popular festival celebrated in the Indian state of Kerala. It is a vibrant harvest festival that usually falls in the Malayalam month of Chingam (August–September) and lasts for ten days. Onam is deeply rooted in Kerala’s culture and heritage and is celebrated by people of all religions and communities, making it a symbol of unity, tradition, and joy. The festival is marked by elaborate feasts, traditional dances like Thiruvathira, intricate floral designs called Pookalam, and the famous Vallamkali boat races. Onam also commemorates the legendary King Mahabali, whose reign is believed to have been a golden era of prosperity and happiness.", "", 100, "neutral"],
            ["URL", "https://en.wikipedia.org/wiki/Artificial_intelligence", "", 100, "technical"]
        ],
        inputs=[input_type, text_input, url_input, word_count, tone],
        outputs=output
    )

# Launch the interface
if __name__ == "__main__":
    iface.launch()