import openai, os, json
from flask import Flask, render_template, request

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__,
            template_folder="templates"
            )


def get_colors(msg):
    prompt = f"""
    You are a color palette generating assistant that responds to text prompts for color palettes
    Your should generate color palettes that fit the theme, mood, or instructions in the prompt.
    The palettes should be between 2 and 8 colors.

    Q: Convert the following verbal description of a color palette into a list of colors: The Mediterranean Sea
    A: ["#006699", "#66CCCC", "#F0E68C", "#008000", "#F08080"]

    Q: Convert the following verbal description of a color palette into a list of colors: sage, nature, earth
    A: ["#EDF1D6", "#9DC08B", "#609966", "#40513B"]


    Desired Format: a JSON array of hexadecimal color codes

    Q: Convert the following verbal description of a color palette into a list of colors: {msg} 
    A:
    """

    response = openai.Completion.create(
        prompt = prompt,
        model = "text-davinci-003",
        max_tokens = 200
    )
    # Converting to a list
    colors = json.loads(response["choices"][0]["text"])
    return colors


@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    # app.logger.info("HIT THE POST REQUEST ROUTE!!!")
    query = request.form.get("query")
    colors = get_colors(query)
    # app.logger.info(colors)
    return {"colors":colors}
    # OPEN AI COMPLETION CALL
    
    # RETURN LIST OF COLORS


@app.route("/")
def index():
    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt="Give me a funny word: "
    )
    return response["choices"][0]["text"]
    # return render_template("index.html")

# @app.route("/dog")
# def dog():
#     return "WOOF WOOF WOOF!!!"

# @app.route("/cat")
# def cat():
#     return "MEOW MEOW MEOW!!!"

if __name__ == "__main__":
    app.run(debug=True)