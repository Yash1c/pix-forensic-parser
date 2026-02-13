import re
from typing import List, Tuple

def parse_emv(payload: str) -> List[Tuple[str, str, str]]:
    """
    Parser EMV completo com nome dos campos.
    Baseado no padrão EMV QR Code e especificações do BACEN.
    """
    i = 0
    result = []
    
    # Dicionário de tags conhecidas do PIX
    tags_conhecidas = {
        "00": "Payload Format Indicator",
        "01": "Point of Initiation Method",
        "26": "Merchant Account Information - PIX",
        "52": "Merchant Category Code",
        "53": "Transaction Currency",
        "54": "Transaction Amount",
        "58": "Country Code",
        "59": "Merchant Name",
        "60": "Merchant City",
        "61": "Postal Code",
        "62": "Additional Data Field",
        "63": "CRC"
    }
    
    while i < len(payload):
        tag = payload[i:i+2]
        length = int(payload[i+2:i+4])
        value = payload[i+4:i+4+length]
        
        nome_tag = tags_conhecidas.get(tag, "Tag Desconhecida")
        result.append((tag, nome_tag, value))
        
        # Se for a tag do PIX (26), tenta parsear internamente
        if tag == "26" and value.startswith("0014br.gov.bcb.pix"):
            print("  → PIX identificado! URL:", value[20:])
            
        i += 4 + length
    
    return result

# Seu payload:
pix_payload = ""

print("\n" + "="*60)
print("ANÁLISE FORENSE DE QR CODE PIX")
print("="*60 + "\n")

decoded = parse_emv(pix_payload)

for tag, nome, valor in decoded:
    print(f"-> {tag} - {nome}")
    print(f"   Valor: {valor}")
    
    # Extrações especiais
    if tag == "59":
        print(f"   → Comerciante: {valor}")
    elif tag == "60":
        print(f"   → Cidade: {valor}")
    elif tag == "61":
        print(f"   → CEP: {valor}")
    elif tag == "26":
        print(f"   → URL do PIX: {valor[20:] if valor.startswith('0014br.gov.bcb.pix') else 'Formato não padrão'}")
    
    print()

print("="*60)
