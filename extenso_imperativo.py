import re

# Listas fixas de números por extenso
UNIDADES = ["zero", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove"]
DEZENAS = ["dez", "onze", "doze", "treze", "quatorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove"]
DEZENAS_COMPOSTAS = ["", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa"]
CENTENAS = ["", "cem", "duzentos", "trezentos", "quatrocentos", "quinhentos", "seiscentos", "setecentos", "oitocentos", "novecentos"]

def limpar_numero(numero):
    """
    Remove os pontos de milhar e troca a vírgula decimal por ponto, convertendo para float.
    :param numero: String no formato brasileiro (ex: "9.999.999,99")
    :return: Número float (ex: 9999999.99)
    """
    numero = re.sub(r'\.', '', numero)
    numero = numero.replace(',', '.')
    return float(numero)

def separar_partes(numero):
    """
    Separa a parte inteira e decimal de um número float.
    :param numero: Número float
    :return: Tupla com parte inteira e parte decimal como inteiros
    """
    parte_inteira, _, parte_decimal = f"{numero:.2f}".partition('.')
    return int(parte_inteira), int(parte_decimal)

def converter_numero(numero):
    """
    Converte um número inteiro para sua forma por extenso.
    :param numero: Inteiro entre 0 e 999999999
    :return: String com número por extenso
    """
    if numero < 10:
        return UNIDADES[numero]
    elif numero < 20:
        return DEZENAS[numero - 10]
    elif numero < 100:
        dezena = numero // 10
        unidade = numero % 10
        return DEZENAS_COMPOSTAS[dezena] + (f" e {UNIDADES[unidade]}" if unidade else "")
    elif numero < 1000:
        centena = numero // 100
        resto = numero % 100
        if centena == 1 and resto > 0:
            return "cento" + (f" e {converter_numero(resto)}" if resto else "")
        return CENTENAS[centena] + (f" e {converter_numero(resto)}" if resto else "")
    elif numero < 1000000:
        milhar = numero // 1000
        resto = numero % 1000
        if milhar == 1:
            return "mil" + (f" {converter_numero(resto)}" if resto else "")
        return f"{converter_numero(milhar)} mil" + (f" {converter_numero(resto)}" if resto else "")
    elif numero < 1000000000:
        milhao = numero // 1000000
        resto = numero % 1000000
        if milhao == 1:
            return "um milhão" + (f" {converter_numero(resto)}" if resto else "")
        return f"{converter_numero(milhao)} milhões" + (f" {converter_numero(resto)}" if resto else "")
    else:
        return "Número fora do limite"

# Bloco principal: entrada e saída do usuário (modo imperativo)
while True:
    entrada = input("Digite um número até 999.999.999,99 (use pontos e vírgula) ou 'sair' para encerrar o programa: ")
    if entrada.lower() == "sair":
        print("Encerrando o programa...")
        break
    try:
        numero = limpar_numero(entrada)  # Transforma entrada textual em float
        parte_inteira, parte_decimal = separar_partes(numero) # Separa as partes
        extenso_inteiro = converter_numero(parte_inteira) # Converte parte inteira
        if extenso_inteiro == "Número fora do limite":
            print(extenso_inteiro)
            continue # Volta ao início do loop
        extenso_decimal = converter_numero(parte_decimal) if parte_decimal > 0 else ""

        # Monta o resultado com tratamento de plural
        resultado = f"{extenso_inteiro} reais"
        if parte_decimal > 0:
            resultado += f" e {extenso_decimal} centavos"

        print(resultado.capitalize()) # Exibe com a primeira letra maiúscula
    except:
        print("Número inválido. Verifique o formato e tente novamente.")
