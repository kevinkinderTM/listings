from hugchat import hugchat
from hugchat.login import Login
import os
from utils import stringProcessing

# Variables
EMAIL = os.getenv('HF_EMAIL')
PASSWD = os.getenv('HF_PASSWD')
cookie_path_dir = os.getenv('HF_cookie_path_dir')

# Init chatbot globally
sign = Login(EMAIL, PASSWD)
cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

def generate_content_for_keyword(keyword: str):
    keyword = stringProcessing.text_to_keyword(keyword)
    prompt = f"""- Eres un copywriter que va a escribir contenido para un producto "{keyword}" que no tienes que nombrar en el texto solo con sinonimos.
    - Organiza el contenido con etiquetas h2 y h3 de acuerdo a la jerarquía del tema. Asegúrate de que cada sección tenga al menos 250 palabras para una descripción detallada que se acerque a las 1000 palabras en total.
    - La Meta Description debe ser una frase atractiva para vender el producto, incluyendo la keyword y una invitación a la compra. Utiliza un tono cálido y motivador.
    - Incluye "meta-description" y "description" en la estructura JSON.
    - Comienza el contenido con un listado de 5 puntos fundamentales que el usuario debe saber antes de comprar este dispositivo. Utiliza viñetas para presentar estos puntos clave.
    - El estilo de escritura debe ser profundo, cálido, motivador y rico en juegos de palabras, reflejando una voz única y atractiva para el lector.
    - Asegúrate de que la descripción sea detallada y extensa, manteniendo la palabra clave principal mencionada solo tres veces en todo el texto.
    - No utilices la palabra "conclusión" al final del texto.
    - Utiliza un lenguaje claro y conciso, evitando jerga técnica excesiva.
    - Incluye anécdotas o referencias culturales relevantes para hacer la descripción más atractiva.
    - Asegúrate de que el contenido sea original, único y no esté copiado de otras fuentes.
    - Haz que el texto sea coherente y fluido, manteniendo un tono consistente en toda la descripción."""
    return chatbot.chat(prompt, True)


