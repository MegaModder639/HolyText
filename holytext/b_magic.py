import webbrowser
from pathlib import Path
import unicodedata
import random

from .l_magic import THEMES, is_cyrillic, create_particles, open_html

CAKE_SVG = """
<svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
  <!-- нижний слой -->
  <rect x="130" y="310" width="252" height="50" rx="10" fill="#d2691e" />
  <!-- средний слой -->
  <rect x="150" y="260" width="212" height="50" rx="10" fill="#f4a460" />
  <!-- верхний слой -->
  <rect x="170" y="210" width="172" height="50" rx="10" fill="#f5deb3" />
  <!-- свеча -->
  <rect x="250" y="160" width="12" height="50" fill="#ffd700" />
  <!-- пламя -->
  <ellipse cx="256" cy="150" rx="10" ry="15" fill="#ff4500" />
  <ellipse cx="256" cy="145" rx="6" ry="10" fill="#ffa500" />
  <!-- украшения -->
  <circle cx="180" cy="300" r="10" fill="#ff69b4" />
  <circle cx="220" cy="290" r="8" fill="#ff1493" />
  <circle cx="280" cy="295" r="9" fill="#ff69b4" />
  <circle cx="330" cy="300" r="10" fill="#ff1493" />
  <circle cx="190" cy="250" r="8" fill="#ff0000" />
  <circle cx="240" cy="240" r="7" fill="#ffa500" />
  <circle cx="300" cy="245" r="8" fill="#ff0000" />
  <circle cx="340" cy="250" r="7" fill="#ffa500" />
</svg>
"""

def birthday(name, theme="default", color=None, particles=True):
    name = name.strip().capitalize()

    if is_cyrillic(name):
        message = f"С днём рождения, {name}! 🎉"
    else:
        message = f"Happy birthday, {name}! 🎂"

    theme_data = THEMES.get(theme, THEMES["default"])

    heart_color = color if color else theme_data["heart_color"]
    text_color = theme_data["text_color"]
    particle_color = heart_color

    if particles:
        particles_html = create_particles(theme_data["particle_symbols"])
    else:
        particles_html = ""

    html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Birthday</title>
<style>
* {{
    margin:0;
    padding:0;
    box-sizing:border-box;
}}

body {{
    height:100vh;
    overflow:hidden;
    display:flex;
    justify-content:center;
    align-items:center;
    {theme_data["bg"]}
    font-family: Arial, sans-serif;
    position: relative;
}}

{theme_data["extra_css"]}

.container {{
    text-align:center;
    position:relative;
    z-index:2;
}}

/* Стиль для торта */
.cake {{
    width:320px;
    filter: drop-shadow(0 0 25px {heart_color});
    animation: appear 2s ease-out, bounce 1.5s infinite 2s;
}}

.cake path, .cake rect, .cake circle, .cake ellipse, .cake polygon {{
    stroke: none;
}}

/* Текст поздравления */
.text {{
    margin-top:40px;
    color: {text_color};
    font-size:40px;
    font-weight:bold;
    letter-spacing:3px;
    opacity:0;
    animation: showText 3s forwards 2s;
    text-shadow: {theme_data["text_shadow"].replace(theme_data["heart_color"], heart_color)};
}}

/* Анимация появления */
@keyframes appear {{
    from {{ transform:scale(0); opacity:0; }}
    to {{ transform:scale(1); opacity:1; }}
}}

/* Анимация подпрыгивания (вместо биения) */
@keyframes bounce {{
    0%,100% {{ transform: translateY(0) scale(1); }}
    50% {{ transform: translateY(-15px) scale(1.02); }}
}}

/* Появление текста */
@keyframes showText {{
    from {{ opacity:0; transform: translateY(30px); }}
    to {{ opacity:1; transform: translateY(0); }}
}}

/* Частицы */
.particle {{
    position:absolute;
    bottom:-50px;
    color: {particle_color};
    animation: float linear infinite;
    opacity:0;
}}

@keyframes float {{
    0% {{ transform: translateY(0) rotate(0deg); opacity:0; }}
    20% {{ opacity:1; }}
    100% {{ transform: translateY(-120vh) rotate(360deg); opacity:0; }}
}}
</style>
</head>
<body>

{theme_data["extra_html"]}
{particles_html}

<div class="container">
    <!-- Вместо сердца – торт -->
    <div class="cake">
        {CAKE_SVG}
    </div>
    <div class="text">{message}</div>
</div>

</body>
</html>
    """

    open_html(html, "birthday.html", delete_after=True)

if __name__ == "__main__":
    birthday("Вика", theme="galaxy")