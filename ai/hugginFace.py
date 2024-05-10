from hugchat import hugchat
from hugchat.login import Login
from dotenv import load_dotenv
import os
from utils import stringProcessing

# # Variables
load_dotenv()
EMAIL = os.getenv('HF_EMAIL')
PASSWD = os.getenv('HF_PASSWD')
cookie_path_dir = './cookies/'

# Init chatbot globally
sign = Login(EMAIL, PASSWD)
cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

def generate_content_for_keyword(keyword: str):
    try:
        keyword = stringProcessing.text_to_keyword(keyword)
        print(keyword)

        prompt = f"""- Eres un copywriter que va a escribir contenido para un producto "{keyword}" que no tienes que nombrar en el texto solo con sinonimos.
            - Organiza el contenido con etiquetas h2 y h3 de acuerdo a la jerarquía del tema. Asegúrate de que cada sección tenga al menos 250 palabras para una descripción detallada que se acerque a las 1000 palabras en total.
            - La Meta Description debe ser una frase atractiva para vender el producto, incluyendo la keyword y una invitación a la compra. Utiliza un tono cálido y motivador.
            - IMPORTANTE! Organiza el contenido de "description" con varios subtítulos (utilizando solamente <h3> y <p> html elements, NO UTILICES <h1>)
            - Comienza el contenido con un listado de 5 puntos fundamentales que el usuario debe saber antes de comprar este dispositivo. Utiliza viñetas para presentar estos puntos clave.
            - El estilo de escritura debe ser profundo, cálido, motivador y rico en juegos de palabras, reflejando una voz única y atractiva para el lector.
            - Asegúrate de que la descripción sea detallada y extensa, manteniendo la palabra clave principal mencionada solo tres veces en todo el texto.
            - No utilices la palabra "conclusión" al final del texto.
            - Utiliza un lenguaje claro y conciso, evitando jerga técnica excesiva.
            - Incluye anécdotas o referencias culturales relevantes para hacer la descripción más atractiva.
            - Asegúrate de que el contenido sea original, único y no esté copiado de otras fuentes.
            - Haz que el texto sea coherente y fluido, manteniendo un tono consistente en toda la descripción.
            IMPORTANTE: Utiliza solamente h3 y p element tags para "description".
            Sigue la estructura JSON requerida para la respuesta. No respondas con otro texto que no sea el JSON, incluyendo las keys 'meta_description', y 'description'. La descripción debe ser rica en contenido y detallada, aproximándose a las 1000 palabras para cumplir con las expectativas de contenido extenso.
            - Cuando hayan dobles DENTRO del texto, has un escape de las dobles comillas con el caracter escape \. Solamente escapa dobles comillas DENTRO del texto, NO de las comillas que delimitan la string.
            - IMPORTANT! Output must be in valid JSON like the following example {{"description": "{{GENERATED_DESCRIPTION}}", "meta_description": "{{GENERATED_META_DESCRIPTION}}"}}. Output must include only JSON. """
        query_result = chatbot.chat(prompt).wait_until_done()
        text_no_breaks = ''.join(char for char in query_result if char.isprintable())
        return text_no_breaks

    except Exception as e:
        print(f"Error generating content for keyword: {e}")
    
