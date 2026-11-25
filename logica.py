import xml.etree.ElementTree as ET
import requests

URL_BCE = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"


def descargar_xml(url=URL_BCE):
    """Realiza una petición HTTP GET al BCE y devuelve el contenido XML."""
    respuesta = requests.get(url, timeout=10)
    if respuesta.status_code != 200:
        raise ConnectionError(
            f"Error al conectar con el servidor (código {respuesta.status_code})."
        )
    return respuesta.content


def parsear_xml(contenido_xml):
    """
    Recorre el árbol XML del BCE con ElementTree y extrae:
    - La fecha de actualización (atributo 'time').
    - Un diccionario con las monedas y sus tasas respecto al Euro.
    """
    raiz = ET.fromstring(contenido_xml)
    fecha = "Desconocida"
    # Añadimos EUR manualmente como moneda base (1 EUR = 1.0 EUR)
    tasas = {"EUR": 1.0}

    for elemento in raiz.iter():
        if "time" in elemento.attrib:
            fecha = elemento.attrib["time"]
        elif "currency" in elemento.attrib and "rate" in elemento.attrib:
            moneda = elemento.attrib["currency"]
            tasa = float(elemento.attrib["rate"])
            tasas[moneda] = tasa

    return fecha, tasas


def obtener_datos_bce():
    """Descarga y parsea el XML del BCE en un solo paso."""
    contenido_xml = descargar_xml()
    return parsear_xml(contenido_xml)


def convertir_divisa(importe, moneda_origen, moneda_destino, tasas):
    """
    Realiza la conversión cruzada usando el Euro (EUR) como moneda puente:
    CantidadFinal = (Importe / TasaOrigen) * TasaDestino
    """
    tasa_origen = tasas[moneda_origen]
    tasa_destino = tasas[moneda_destino]
    importe_en_euros = importe / tasa_origen
    return importe_en_euros * tasa_destino
