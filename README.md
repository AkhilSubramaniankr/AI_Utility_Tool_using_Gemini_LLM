# AI_Utility_Tool_using_Gemini_LLM

# AI Text Summarizer

A Python-based tool for summarizing text or web articles using Google's Gemini-2.0-Flash model, with a Gradio interface for customizable summary length and tone.

## Approach
- **LLM Integration**: Utilizes Gemini-2.0-Flash for abstractive text summarization, supporting up to 1,048,576 tokens (~700,000 words).
- **Input Processing**: Accepts raw text or URLs, extracting content using BeautifulSoup for web pages.
- **Customization**: Offers five tones (neutral, formal, casual, technical, engaging) and adjustable summary lengths (200–700,000 words).
- **User Interface**: Built with Gradio for interactive input, real-time word count, progress tracking, and stop functionality.
- **Logging**: Captures LLM inputs, prompts, and outputs in `logs/llm_interactions.log` for debugging and analysis.
- **Evaluation**: Uses ROUGE-L metric to assess summary quality (see `evaluation/evaluation.md`).

## Setup
1. **Install Dependencies**:
   ```bash
   pip install gradio google-generativeai requests beautifulsoup4 rouge-score
   ```
2. **Set Up Gemini API**:
   - Obtain an API key from [Google’s API portal](https://makersuite.google.com/app/apikey).
   - Replace `"YOUR_API_KEY_HERE"` in `src/text_summarizer.py` with your key.
3. **Create Log Directory**:
   ```bash
   mkdir logs
   ```
4. **Run the Application**:
   ```bash
   python src/text_summarizer.py
   ```
   - Opens a Gradio UI at `http://localhost:7860`.

## Usage
1. **Launch the UI**:
   - Run the script and access the interface in your browser.
2. **Select Input Type**:
   - Choose **Text** to paste text or **URL** to summarize a webpage.
3. **Configure Options**:
   - Set **Max Input Characters** (default: min: 200, max: 700,000).
   - Choose **Summary Word Count** (200–700,000).
   - Select **Tone** (neutral, formal, casual, technical, engaging).
4. **Generate Summary**:
   - Click **Generate Summary** to process the input.
   - Monitor progress via the progress bar.
   - Click **Stop** to halt and reset.
5. **View Logs**:
   - Check `logs/llm_interactions.log` for LLM interactions.
6. **Evaluate Summaries**:
   - Follow `evaluation/evaluation.md` to compute ROUGE-L scores.

## Example
- **Input Text**: "The rapid advancement of AI technologies, such as large language models, has transformed industries like healthcare, finance, and education..."
- **Settings**: 100 words, neutral tone.
- **Output**: "Large language models have revolutionized industries like healthcare, finance, and education by generating human-like text and assisting with complex tasks..."

## Evaluation
- **Method**: ROUGE-L F1 score comparing generated summaries to reference summaries.
- **Example**: A sample summary achieved a ROUGE-L F1 score of ~0.95 (see `evaluation/evaluation.py` or `evaluation/evaluation.ipynb).
- **Limitations**: ROUGE-L measures word overlap, not semantic accuracy. Consider human evaluation for tone and coherence.
