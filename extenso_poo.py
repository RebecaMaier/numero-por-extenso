import re

class NumeroPorExtenso:
    """
    Classe para converter um número decimal em sua representação por extenso 
    no formato de moeda brasileira, considerando valores até 999.999.999,99.
    """
    UNIDADES = ["zero", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove"]
    DEZENAS = ["dez", "onze", "doze", "treze", "quatorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove"]
    DEZENAS_COMPOSTAS = ["", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa"]
    CENTENAS = ["", "cem", "duzentos", "trezentos", "quatrocentos", "quinhentos", "seiscentos", "setecentos", "oitocentos", "novecentos"]

    def __init__(self, numero):
        """
        Inicializa a classe com o número fornecido.
        :param numero: Número decimal até 999.999.999,99
        """
        self.numero = self.limpar_numero(numero)
        self.parte_inteira, self.parte_decimal = self.separar_partes()

    def limpar_numero(self, numero):
        """
        Remove pontos de milhar e substitui vírgula por ponto para conversão correta.
        :param numero: string com o número
        :return: número como float
        """
        numero = re.sub(r'\.', '', numero)  # Remove os pontos dos milhares
        numero = numero.replace(',', '.')  # Troca vírgula decimal por ponto
        return float(numero)

    def separar_partes(self):
        """
        Separa a parte inteira e a decimal do número.
        :return: Tupla contendo a parte inteira e a parte decimal como inteiros.
        """
        parte_inteira, _, parte_decimal = f"{self.numero:.2f}".partition('.')
        return int(parte_inteira), int(parte_decimal)

    def converter_numero(self, numero):
        """
        Converte um número inteiro para sua forma por extenso.
        :param numero: inteiro até 9999999
        :return: string por extenso
        """
        if numero < 10:
            return self.UNIDADES[numero]
        elif numero < 20:
            return self.DEZENAS[numero - 10]
        elif numero < 100:
            dezena = numero // 10
            unidade = numero % 10
            return self.DEZENAS_COMPOSTAS[dezena] + (f" e {self.UNIDADES[unidade]}" if unidade else "")
        elif numero < 1000:
            centena = numero // 100
            resto = numero % 100
            if centena == 1 and resto > 0:
                return "cento" + (f" e {self.converter_numero(resto)}" if resto else "")
            return self.CENTENAS[centena] + (f" e {self.converter_numero(resto)}" if resto else "")
        elif numero < 1000000:
            milhar = numero // 1000
            resto = numero % 1000
            if milhar == 1:
                return "mil" + (f" {self.converter_numero(resto)}" if resto else "")
            return f"{self.converter_numero(milhar)} mil" + (f" {self.converter_numero(resto)}" if resto else "")
        elif numero < 1000000000:
            milhao = numero // 1000000
            resto = numero % 1000000
            if milhao == 1:
                return "um milhão" + (f" {self.converter_numero(resto)}" if resto else "")
            return f"{self.converter_numero(milhao)} milhões" + (f" {self.converter_numero(resto)}" if resto else "")
        else:
            return "Número fora do limite"

    def converter_para_extenso(self):
        """
        Converte o número completo para sua forma por extenso em reais e centavos.
        :return: String  formatada representando o número por extenso.
        """
        extenso_inteiro = self.converter_numero(self.parte_inteira)
        if extenso_inteiro == "Número fora do limite":
            return extenso_inteiro
        
        extenso_decimal = self.converter_numero(self.parte_decimal)

        resultado = f"{extenso_inteiro} real" if self.parte_inteira == 1 else f"{extenso_inteiro} reais"
        if self.parte_decimal > 0:
            resultado += " e "
            resultado += f"{extenso_decimal} centavo" if self.parte_decimal == 1 else f"{extenso_decimal} centavos"

        return resultado.capitalize()

# Programa principal com entrada do usuário
while True:
    numero = input("Digite um número até 999.999.999,99 (use pontos e vírgula) ou 'sair' para encerrar o programa: ")
    if numero.lower() == "sair":
        print("Encerrando o programa...")
        break
    try:
        obj = NumeroPorExtenso(numero)
        print(obj.converter_para_extenso())
    except ValueError:
        print("Número inválido. Certifique-se de usar o formato correto.")
