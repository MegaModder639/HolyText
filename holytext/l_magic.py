import webbrowser
from pathlib import Path
import unicodedata
import random
import os
import time

def is_cyrillic(text):
    for char in text:
        if char.isalpha():
            try:
                return "CYRILLIC" in unicodedata.name(char)
            except ValueError:
                pass
    return False

def create_particles(symbols, count=25):
    """Генерирует HTML для частиц с заданным набором символов."""
    particles = ""
    for _ in range(count):
        left = random.randint(0, 100)
        delay = random.uniform(0, 5)
        duration = random.uniform(5, 12)
        size = random.randint(15, 35)
        particles += f"""
        <div class="particle"
        style="
        left:{left}%;
        animation-delay:{delay}s;
        animation-duration:{duration}s;
        font-size:{size}px;
        ">
        {random.choice(symbols)}
        </div>
        """
    return particles

THEMES = {
    "default": {
        "bg": """
            background:
            radial-gradient(circle at center, #5a0033, #100010);
        """,
        "heart_path": "M256 464 L48 256 C-30 170 20 40 130 40 C190 40 235 75 256 135 C277 75 322 40 382 40 C492 40 542 170 464 256 Z",
        "heart_color": "#ff1744",
        "text_color": "white",
        "text_shadow": "0 0 10px #ff1744, 0 0 30px #ff1744",
        "particle_symbols": ["♥", "✦", "✧", "♡", "*"],
        "particle_color": "#ff7aa2",
        "extra_css": "",
        "extra_html": "",
    },
    "galaxy": {
        "bg": """
            background: radial-gradient(ellipse at bottom, #1b2735 0%, #090a0f 100%);
        """,
        "heart_path": "M256 464 C256 464 100 300 50 200 C0 100 80 20 160 80 C200 110 230 150 256 180 C282 150 312 110 352 80 C432 20 512 100 462 200 C412 300 256 464 256 464 Z",
        "heart_color": "#bb86fc",
        "text_color": "#e0e0ff",
        "text_shadow": "0 0 20px #bb86fc, 0 0 60px #6200ea",
        "particle_symbols": ["✦", "✧", "★", "☆", "•"],
        "particle_color": "#bb86fc",
        "extra_css": """
            /* Звёзды на фоне */
            body::before, body::after {
                content: '';
                position: absolute;
                top: 0; left: 0; right: 0; bottom: 0;
                background-image:
                    radial-gradient(2px 2px at 20px 30px, #eee, transparent),
                    radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.8), transparent),
                    radial-gradient(1px 1px at 90px 40px, #fff, transparent),
                    radial-gradient(1px 1px at 160px 120px, #ddd, transparent),
                    radial-gradient(2px 2px at 200px 50px, rgba(255,255,255,0.6), transparent);
                background-size: 200px 200px;
                background-repeat: repeat;
                opacity: 0.5;
                pointer-events: none;
                z-index: 0;
            }
            .container { z-index: 1; }
        """,
        "extra_html": "",
    },
    "sunset": {
        "bg": """
            background: linear-gradient(to bottom, #ff6b6b, #f06595, #cc5de8, #845ef7);
        """,
        "heart_path": "M256 464 C256 464 50 300 50 200 C50 100 150 50 200 120 C220 150 240 190 256 220 C272 190 292 150 312 120 C362 50 462 100 462 200 C462 300 256 464 256 464 Z",
        "heart_color": "#ffd93d",
        "text_color": "#fff5e6",
        "text_shadow": "0 0 20px #ffd93d, 0 0 60px #f0932b",
        "particle_symbols": ["☀", "✦", "✧", "•", "◦"],
        "particle_color": "#ffd93d",
        "extra_css": """
            /* Облака (простые) */
            .cloud {
                position: absolute;
                background: rgba(255,255,255,0.15);
                border-radius: 50%;
                width: 200px; height: 60px;
                filter: blur(5px);
                animation: drift 20s linear infinite;
                z-index: 0;
            }
            .cloud:nth-child(2) { width: 300px; height: 80px; top: 20%; left: -100px; animation-duration: 25s; }
            .cloud:nth-child(3) { width: 150px; height: 50px; top: 60%; left: -50px; animation-duration: 18s; }
            @keyframes drift {
                0% { transform: translateX(-200px); }
                100% { transform: translateX(calc(100vw + 200px)); }
            }
            .container { z-index: 1; }
        """,
        "extra_html": """
            <div class="cloud" style="top:10%; left:-150px;"></div>
            <div class="cloud" style="top:30%; left:-200px;"></div>
            <div class="cloud" style="top:70%; left:-100px;"></div>
        """,
    },
    "forest": {
        "bg": """
            background: radial-gradient(circle at center, #1e3c2c, #0a1f0a);
        """,
        "heart_path": "M256 464 C256 464 120 340 70 250 C20 160 80 80 150 100 C180 108 210 130 240 170 C260 145 280 120 310 100 C380 80 440 160 390 250 C340 340 256 464 256 464 Z",
        "heart_color": "#4caf50",
        "text_color": "#c8e6c9",
        "text_shadow": "0 0 15px #2e7d32, 0 0 40px #1b5e20",
        "particle_symbols": ["🌿", "🍃", "🌱", "✦", "•"],
        "particle_color": "#66bb6a",
        "extra_css": """
            /* Листья падают */
            .leaf {
                position: absolute;
                font-size: 30px;
                color: #4caf50;
                opacity: 0.3;
                animation: fall linear infinite;
                z-index: 0;
                pointer-events: none;
            }
            @keyframes fall {
                0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; }
                10% { opacity: 0.5; }
                100% { transform: translateY(110vh) rotate(720deg); opacity: 0; }
            }
            .container { z-index: 1; }
        """,
        "extra_html": """
            <div class="leaf" style="left:10%; animation-duration:8s; animation-delay:0s;">🍃</div>
            <div class="leaf" style="left:30%; animation-duration:10s; animation-delay:2s;">🌿</div>
            <div class="leaf" style="left:50%; animation-duration:7s; animation-delay:4s;">🍃</div>
            <div class="leaf" style="left:70%; animation-duration:12s; animation-delay:1s;">🌱</div>
            <div class="leaf" style="left:90%; animation-duration:9s; animation-delay:3s;">🍃</div>
        """,
    },
    "ocean": {
        "bg": """
            background: linear-gradient(to bottom, #0c2340, #1a5276, #2e86c1);
        """,
        "heart_path": "M256 464 C256 464 80 340 40 240 C0 140 70 60 150 80 C190 90 230 130 256 170 C282 130 322 90 362 80 C442 60 512 140 472 240 C432 340 256 464 256 464 Z",
        "heart_color": "#5dade2",
        "text_color": "#d6eaf8",
        "text_shadow": "0 0 20px #2e86c1, 0 0 60px #1a5276",
        "particle_symbols": ["○", "◯", "•", "◦", "⁕"],
        "particle_color": "#85c1e9",
        "extra_css": """
            /* Волны */
            .wave {
                position: absolute;
                bottom: 0;
                left: 0;
                width: 200%;
                height: 100px;
                background: repeating-linear-gradient(90deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.1) 50%, transparent 100%);
                border-radius: 50%;
                animation: waveMove 8s linear infinite;
                z-index: 0;
            }
            .wave:nth-child(2) {
                bottom: 30px;
                animation-duration: 12s;
                opacity: 0.5;
                height: 70px;
            }
            @keyframes waveMove {
                0% { transform: translateX(0) scaleY(1); }
                50% { transform: translateX(-25%) scaleY(1.2); }
                100% { transform: translateX(-50%) scaleY(1); }
            }
            .container { z-index: 1; }
        """,
        "extra_html": """
            <div class="wave"></div>
            <div class="wave"></div>
        """,
    },
    "matrix": {
        "bg": """
            background: radial-gradient(circle at center, #0a0a0a, #000000);
            /* Добавим лёгкое зелёное свечение */
            box-shadow: inset 0 0 100px rgba(0, 255, 65, 0.05);
        """,
        "heart_path": "M256 464 L48 256 C-30 170 20 40 130 40 C190 40 235 75 256 135 C277 75 322 40 382 40 C492 40 542 170 464 256 Z",
        "heart_color": "#00ff41",
        "text_color": "#00ff41",
        "text_shadow": "0 0 10px #00ff41, 0 0 30px #00ff41, 0 0 60px #008f11",
        "particle_symbols": ["0", "1", "10", "01", "#", "$", "&", "%"],
        "particle_color": "#00ff41",
        "extra_css": """
            /* Стили для падающих строк кода */
            .code-line {
                position: absolute;
                top: -100px;
                color: #00ff41;
                font-family: 'Courier New', monospace;
                font-size: 20px;
                opacity: 0.4;
                white-space: nowrap;
                z-index: 0;
                animation: fall linear infinite;
                pointer-events: none;
                text-shadow: 0 0 5px #00ff41;
            }
            @keyframes fall {
                0% { transform: translateY(-100px); opacity: 0.2; }
                10% { opacity: 0.6; }
                100% { transform: translateY(calc(100vh + 200px)); opacity: 0.1; }
            }
            /* Сделаем несколько столбцов с разными задержками */
            .code-line:nth-child(1) { left: 5%; animation-duration: 12s; animation-delay: 0s; font-size: 22px; }
            .code-line:nth-child(2) { left: 20%; animation-duration: 15s; animation-delay: 3s; font-size: 18px; }
            .code-line:nth-child(3) { left: 35%; animation-duration: 10s; animation-delay: 5s; font-size: 24px; }
            .code-line:nth-child(4) { left: 50%; animation-duration: 18s; animation-delay: 1s; font-size: 20px; }
            .code-line:nth-child(5) { left: 65%; animation-duration: 13s; animation-delay: 7s; font-size: 16px; }
            .code-line:nth-child(6) { left: 80%; animation-duration: 16s; animation-delay: 2s; font-size: 22px; }
            .code-line:nth-child(7) { left: 92%; animation-duration: 11s; animation-delay: 4s; font-size: 19px; }

            /* Эффект глюка для текста */
            .glitch {
                animation: glitch 3s infinite;
            }
            @keyframes glitch {
                0%, 100% { opacity: 1; transform: translate(0); }
                20% { opacity: 0.8; transform: translate(-2px, 2px); }
                40% { opacity: 1; transform: translate(2px, -2px); }
                60% { opacity: 0.9; transform: translate(-1px, 1px); }
                80% { opacity: 1; transform: translate(1px, -1px); }
            }

            .container { z-index: 1; }
            .text {
                animation: showText 3s forwards 2s, glitch 3s 3s infinite;
            }
            .heart {
                animation: appear 2s ease-out, beat 1.3s infinite 2s, glitch 3s 3s infinite;
            }
        """,
        "extra_html": """
            <!-- Падающие строки кода -->
            <div class="code-line">01001011 01101001 01101100 01101100</div>
            <div class="code-line">01101000 01100001 01100011 01101011</div>
            <div class="code-line">01101101 01100001 01110100 01110010</div>
            <div class="code-line">01101001 01111000 00100000 01110011</div>
            <div class="code-line">01111001 01110011 01110100 01100101</div>
            <div class="code-line">01101101 00100000 01101001 01110011</div>
            <div class="code-line">01101100 01101001 01110110 01100101</div>
        """,
    },
    "glitch": {
        "bg": """
            background: #0a0a0a;
        """,
        "heart_path": "M256 464 L48 256 C-30 170 20 40 130 40 C190 40 235 75 256 135 C277 75 322 40 382 40 C492 40 542 170 464 256 Z",
        "heart_color": "#ff00cc",
        "text_color": "#ff00cc",
        "text_shadow": "0 0 10px #ff00cc, 0 0 30px #ff00cc, 0 0 60px #cc0066",
        "particle_symbols": ["✖", "⚡", "💥", "❌", "⨯", "✕"],
        "particle_color": "#ff00cc",
        "extra_css": """
            /* Шум на фоне */
            body::before {
                content: '';
                position: fixed;
                top: 0; left: 0; right: 0; bottom: 0;
                background: repeating-linear-gradient(45deg, transparent, transparent 2px, rgba(255,0,204,0.03) 2px, rgba(255,0,204,0.03) 4px);
                pointer-events: none;
                z-index: 0;
            }
            /* Глюк для текста */
            .text {
                animation: showText 3s forwards 2s, glitchText 2s infinite 3s;
            }
            @keyframes glitchText {
                0%, 100% { transform: translate(0, 0) skewX(0deg); text-shadow: 0 0 10px #ff00cc, 0 0 30px #ff00cc; }
                20% { transform: translate(-3px, 2px) skewX(2deg); text-shadow: 0 0 15px #00ffff, 0 0 40px #00ffff; }
                40% { transform: translate(3px, -2px) skewX(-2deg); text-shadow: 0 0 20px #ff00ff, 0 0 50px #ff00ff; }
                60% { transform: translate(-5px, 1px) skewX(1deg); text-shadow: 0 0 10px #ff00cc, 0 0 30px #ff00cc; }
                80% { transform: translate(4px, -3px) skewX(-1deg); text-shadow: 0 0 25px #00ff00, 0 0 60px #00ff00; }
            }
            /* Глюк для сердца */
            .heart {
                animation: appear 2s ease-out, beat 1.3s infinite 2s, glitchHeart 2s infinite 3s;
            }
            @keyframes glitchHeart {
                0%, 100% { transform: scale(1) translate(0, 0); filter: drop-shadow(0 0 25px #ff00cc); }
                25% { transform: scale(1.05) translate(-5px, 3px); filter: drop-shadow(0 0 35px #00ffff) drop-shadow(0 0 20px #ff00ff); }
                50% { transform: scale(0.95) translate(5px, -3px); filter: drop-shadow(0 0 45px #ff00ff) drop-shadow(0 0 15px #00ffff); }
                75% { transform: scale(1.02) translate(-3px, -2px); filter: drop-shadow(0 0 30px #ff00cc); }
            }
            /* Горизонтальные линии глюка */
            .glitch-line {
                position: absolute;
                background: rgba(255,0,204,0.1);
                height: 2px;
                width: 100%;
                top: 50%;
                left: 0;
                animation: glitchLine 4s infinite;
                z-index: 0;
                pointer-events: none;
            }
            .glitch-line:nth-child(2) {
                top: 30%;
                animation-delay: 1s;
                height: 4px;
                background: rgba(0,255,255,0.08);
            }
            .glitch-line:nth-child(3) {
                top: 70%;
                animation-delay: 2s;
                height: 1px;
                background: rgba(255,0,255,0.12);
            }
            @keyframes glitchLine {
                0% { transform: translateX(-100%); opacity: 0; }
                10% { opacity: 1; }
                90% { opacity: 1; }
                100% { transform: translateX(100%); opacity: 0; }
            }
            /* Вертикальные линии */
            .glitch-line-v {
                position: absolute;
                background: rgba(0,255,255,0.08);
                width: 2px;
                height: 100%;
                left: 50%;
                top: 0;
                animation: glitchLineV 5s infinite;
                z-index: 0;
                pointer-events: none;
            }
            .glitch-line-v:nth-child(5) {
                left: 25%;
                animation-delay: 0.5s;
                width: 1px;
                background: rgba(255,0,204,0.06);
            }
            .glitch-line-v:nth-child(6) {
                left: 75%;
                animation-delay: 1.5s;
                width: 3px;
                background: rgba(255,0,255,0.05);
            }
            @keyframes glitchLineV {
                0% { transform: translateY(-100%); opacity: 0; }
                10% { opacity: 1; }
                90% { opacity: 1; }
                100% { transform: translateY(100%); opacity: 0; }
            }
            /* Дополнительный шумовой слой (поверх всего) */
            .noise {
                position: fixed;
                top: 0; left: 0; right: 0; bottom: 0;
                background: repeating-linear-gradient(45deg, transparent, transparent 3px, rgba(255,0,204,0.02) 3px, rgba(255,0,204,0.02) 6px);
                pointer-events: none;
                z-index: 0;
            }
            .container { z-index: 1; }
        """,
        "extra_html": """
            <div class="noise"></div>
            <div class="glitch-line"></div>
            <div class="glitch-line"></div>
            <div class="glitch-line"></div>
            <div class="glitch-line-v"></div>
            <div class="glitch-line-v"></div>
            <div class="glitch-line-v"></div>
        """
    }
}

def open_html(html_content, filename, delete_after=False, delay=0.8):
    """
    Сохраняет HTML, открывает в браузере, и если delete_after=True,
    удаляет файл через заданную задержку.
    """
    file = Path(filename)
    file.write_text(html_content, encoding="utf-8")
    webbrowser.open(file.resolve().as_uri())

    if delete_after:
        time.sleep(delay)
        if file.exists():
            file.unlink()

def love(name, theme="default", color=None, particles=True):
    name = name.strip().capitalize()

    if is_cyrillic(name):
        message = f"{name}, я люблю тебя"
    else:
        message = f"I love {name}"

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
<title>Love</title>
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

.heart {{
    width:320px;
    filter: drop-shadow(0 0 25px {heart_color});
    animation: appear 2s ease-out, beat 1.3s infinite 2s;
}}

.heart path {{
    fill: {heart_color};
}}

.text {{
    margin-top:40px;
    color: {text_color};
    font-size:40px;
    font-weight:bold;
    letter-spacing:3px;
    opacity:0;
    animation: showText 3s forwards 2s;
    text-shadow: {theme_data["text_shadow"].replace(theme_data["heart_color"], heart_color)};
    /* заменяем цвет в тени на актуальный */
}}

@keyframes appear {{
    from {{ transform:scale(0); opacity:0; }}
    to {{ transform:scale(1); opacity:1; }}
}}

@keyframes beat {{
    0%,100% {{ transform:scale(1); }}
    50% {{ transform:scale(1.12); }}
}}

@keyframes showText {{
    from {{ opacity:0; transform: translateY(30px); }}
    to {{ opacity:1; transform: translateY(0); }}
}}

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
    <svg class="heart" viewBox="0 0 512 512">
        <path d="{theme_data["heart_path"]}" />
    </svg>
    <div class="text">{message}</div>
</div>

</body>
</html>
    """

    open_html(html, "love.html", delete_after=True)

if __name__ == "__main__":
    love("Вика", theme="galaxy", color="pink")