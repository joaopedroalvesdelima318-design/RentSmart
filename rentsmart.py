import csv
from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP

CENTAVO = Decimal("0.01")


def arredondar(valor):
    return Decimal(valor).quantize(CENTAVO, rounding=ROUND_HALF_UP)


def dinheiro(valor):
    return f"R$ {arredondar(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class Imovel(ABC):
    def __init__(self, quartos, aluguel_base):
        self.quartos = quartos
        self.aluguel_base = Decimal(str(aluguel_base))
        self.adicional_quartos = Decimal("0.00")
        self.adicional_estacionamento = Decimal("0.00")
        self.desconto = Decimal("0.00")

    @abstractmethod
    def calcular_adicionais(self):
        pass

    def calcular_desconto(self, valor):
        return Decimal("0.00")

    def calcular_aluguel(self):
        self.calcular_adicionais()
        subtotal = self.aluguel_base + self.adicional_quartos + self.adicional_estacionamento
        self.desconto = self.calcular_desconto(subtotal)
        return arredondar(subtotal - self.desconto)


class Apartamento(Imovel):
    def __init__(self, quartos, possui_criancas, possui_vaga):
        super().__init__(quartos, "700.00")
        self.possui_criancas = possui_criancas
        self.possui_vaga = possui_vaga

    def calcular_adicionais(self):
        self.adicional_quartos = Decimal("200.00") if self.quartos == 2 else Decimal("0.00")
        self.adicional_estacionamento = Decimal("300.00") if self.possui_vaga else Decimal("0.00")

    def calcular_desconto(self, valor):
        return arredondar(valor * Decimal("0.05")) if not self.possui_criancas else Decimal("0.00")


class Casa(Imovel):
    def __init__(self, quartos, possui_vaga):
        super().__init__(quartos, "900.00")
        self.possui_vaga = possui_vaga

    def calcular_adicionais(self):
        self.adicional_quartos = Decimal("250.00") if self.quartos == 2 else Decimal("0.00")
        self.adicional_estacionamento = Decimal("300.00") if self.possui_vaga else Decimal("0.00")


class Estudio(Imovel):
    def __init__(self, quantidade_vagas):
        super().__init__(0, "1200.00")
        self.quantidade_vagas = quantidade_vagas

    def calcular_adicionais(self):
        if self.quantidade_vagas == 0:
            self.adicional_estacionamento = Decimal("0.00")
        else:
            extras = max(0, self.quantidade_vagas - 2)
            self.adicional_estacionamento = Decimal("250.00") + Decimal(extras) * Decimal("60.00")


class Orcamento:
    TAXA_CONTRATUAL = Decimal("2000.00")

    def __init__(self, cliente, imovel, parcelas_contrato):
        if not 1 <= parcelas_contrato <= 5:
            raise ValueError("A taxa contratual deve ser parcelada de 1 a 5 vezes.")
        self.cliente = cliente
        self.imovel = imovel
        self.parcelas_contrato = parcelas_contrato
        self.aluguel_mensal = imovel.calcular_aluguel()
        self.valores_parcelas = self.calcular_parcelas()

    def calcular_parcelas(self):
        valor = arredondar(self.TAXA_CONTRATUAL / self.parcelas_contrato)
        parcelas = [valor] * self.parcelas_contrato
        parcelas[-1] += self.TAXA_CONTRATUAL - sum(parcelas)
        return parcelas

    def exibir_resumo(self):
        print("\n" + "=" * 48)
        print("ORÇAMENTO RENTSMART - R.M IMÓVEIS")
        print("=" * 48)
        print(f"Cliente: {self.cliente}")
        print(f"Imóvel: {type(self.imovel).__name__}")
        print(f"Aluguel-base: {dinheiro(self.imovel.aluguel_base)}")
        if self.imovel.quartos:
            print(f"Quartos: {self.imovel.quartos}")
        print(f"Adicional por quartos: {dinheiro(self.imovel.adicional_quartos)}")
        print(f"Estacionamento: {dinheiro(self.imovel.adicional_estacionamento)}")
        print(f"Desconto: - {dinheiro(self.imovel.desconto)}")
        print("-" * 48)
        print(f"ALUGUEL MENSAL: {dinheiro(self.aluguel_mensal)}")
        print(f"Taxa contratual: {dinheiro(self.TAXA_CONTRATUAL)}")
        print(f"Parcelamento: {self.parcelas_contrato} parcela(s)")
        for numero, valor in enumerate(self.valores_parcelas, 1):
            print(f"  Parcela {numero}: {dinheiro(valor)}")
        print("A taxa contratual é separada do aluguel mensal.")

    def gerar_csv(self, nome="projecao_rentsmart.csv"):
        with open(nome, "w", newline="", encoding="utf-8-sig") as arquivo:
            writer = csv.writer(arquivo, delimiter=";")
            writer.writerow(["Mes", "Aluguel mensal (R$)", "Parcela taxa contratual (R$)", "Total previsto no mes (R$)"])
            for mes in range(1, 13):
                parcela = self.valores_parcelas[mes - 1] if mes <= self.parcelas_contrato else Decimal("0.00")
                total = self.aluguel_mensal + parcela
                writer.writerow([mes, f"{self.aluguel_mensal:.2f}".replace(".", ","), f"{parcela:.2f}".replace(".", ","), f"{total:.2f}".replace(".", ",")])
        print(f"\nCSV gerado: {nome}")


def ler_opcao(mensagem, opcoes):
    while True:
        valor = input(mensagem).strip().lower()
        if valor in opcoes:
            return valor
        print("Opção inválida. Tente novamente.")


def ler_int(mensagem, minimo, maximo=None):
    while True:
        try:
            valor = int(input(mensagem))
            if valor < minimo or (maximo is not None and valor > maximo):
                print("Valor fora do intervalo permitido.")
                continue
            return valor
        except ValueError:
            print("Digite um número inteiro válido.")


def sim_nao(mensagem):
    return ler_opcao(mensagem + " (s/n): ", {"s", "n"}) == "s"


def criar_imovel():
    print("\n1 - Apartamento\n2 - Casa\n3 - Estúdio")
    tipo = ler_opcao("Tipo de imóvel: ", {"1", "2", "3"})
    if tipo in ("1", "2"):
        quartos = ler_int("Quantidade de quartos (1 ou 2): ", 1, 2)
        vaga = sim_nao("Deseja uma vaga de garagem por R$ 300,00/mês?")
        if tipo == "1":
            criancas = sim_nao("O cliente possui crianças?")
            return Apartamento(quartos, criancas, vaga)
        return Casa(quartos, vaga)
    vagas = ler_int("Vagas no estúdio (0 ou 2 ou mais): ", 0)
    while vagas == 1:
        print("O pacote inicial contempla duas vagas. Informe 0 ou 2 ou mais.")
        vagas = ler_int("Quantidade de vagas: ", 0)
    return Estudio(vagas)


def main():
    print("=== RENTSMART - R.M IMÓVEIS ===")
    cliente = input("Nome do cliente: ").strip()
    while not cliente:
        print("O nome não pode ficar vazio.")
        cliente = input("Nome do cliente: ").strip()
    imovel = criar_imovel()
    parcelas = ler_int("Parcelas da taxa contratual (1 a 5): ", 1, 5)
    orcamento = Orcamento(cliente, imovel, parcelas)
    orcamento.exibir_resumo()
    orcamento.gerar_csv()


if __name__ == "__main__":
    main()
