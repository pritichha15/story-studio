import os
import gradio as gr
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=API_KEY)


def generate_story(genre, tone, audience, length, language, idea):
    try:
        model = genai.GenerativeModel("models/gemini-flash-latest")

        prompt = f"""
You are an award-winning creative storyteller.

Write a completely original, engaging and immersive story.

Genre: {genre}
Tone: {tone}
Target Audience: {audience}
Story Length: {length}
Language: {language}
Story Idea: {idea}

Requirements:

- Give the story an interesting title.
- Begin with a powerful opening hook.
- Divide the story into well-structured scenes.
- Include realistic and engaging dialogue.
- Use vivid descriptions.
- Build suspense and emotional depth.
- Maintain smooth pacing.
- Create memorable characters.
- End with a strong cliffhanger.
- Ensure the story feels cinematic and immersive.
"""

        response = model.generate_content(prompt)

        if response.text:
            return response.text
        else:
            return "No story generated."

    except Exception as e:
        return str(e)


css = """
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

*{
    font-family:'Manrope',sans-serif !important;
}

body{
    background:linear-gradient(135deg,#F7F8FF,#EEF3FF);
}

.gradio-container{
    background:linear-gradient(135deg,#F7F8FF,#EEF3FF);
}

h1{
    color:#5B4BFF !important;
    text-align:center;
    font-size:42px !important;
    font-weight:800 !important;
}

h3{
    text-align:center;
    color:#555;
}

label{
    color:#4C43CD !important;
    font-weight:700 !important;
}

textarea{
    border-radius:18px !important;
    border:2px solid #D8DAFF !important;
}

input{
    border-radius:14px !important;
}

button{
    background:linear-gradient(90deg,#6C63FF,#9D4EDD)!important;
    color:white!important;
    border:none!important;
    border-radius:15px!important;
    font-weight:700!important;
    transition:0.25s!important;
}

button:hover{
    transform:translateY(-2px);
}

footer{
    display:none!important;
}
"""


with gr.Blocks(
    title="Story Studio",
    theme=gr.themes.Soft(
        primary_hue="violet",
        secondary_hue="blue",
        neutral_hue="slate"
    ),
    css=css
) as demo:

    gr.Markdown("""
#  Story Studio

### Turn your imagination into cinematic stories powered by Gemini AI
""")

    with gr.Row():

        genre = gr.Dropdown(
            choices=[
                "Fantasy",
                "Mystery",
                "Thriller",
                "Horror",
                "Sci-Fi",
                "Adventure",
                "Romance",
                "Drama",
                "Crime",
                "Historical"
            ],
            value="Fantasy",
            label="Genre"
        )

        tone = gr.Dropdown(
            choices=[
                "Suspenseful",
                "Dark",
                "Emotional",
                "Funny",
                "Inspirational",
                "Psychological",
                "Heartwarming",
                "Action-Packed"
            ],
            value="Suspenseful",
            label="Tone"
        )

    with gr.Row():

        audience = gr.Dropdown(
            choices=[
                "Children",
                "Teenagers",
                "Adults"
            ],
            value="Adults",
            label="Target Audience"
        )

        length = gr.Dropdown(
            choices=[
                "Short",
                "Medium",
                "Long"
            ],
            value="Medium",
            label="Story Length"
        )

        language = gr.Dropdown(
            choices=[
                "English",
                "Hindi"
            ],
            value="English",
            label="Language"
        )

    idea = gr.Textbox(
        label="Story Idea",
        placeholder="Describe your story idea here...",
        lines=6
    )

    generate_btn = gr.Button(
        " Generate Story",
        variant="primary",
        size="lg"
    )

    output = gr.Textbox(
        label="Generated Story",
        lines=24,
        placeholder="Your AI-generated story will appear here..."
    )

    generate_btn.click(
        fn=generate_story,
        inputs=[
            genre,
            tone,
            audience,
            length,
            language,
            idea
        ],
        outputs=output
    )

demo.launch(inbrowser=True)