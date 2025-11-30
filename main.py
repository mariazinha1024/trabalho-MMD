#maquinas = [nome, status, temperatura, data da ultima manutenção)
from datetime import datetime

maquinas = [
    ["Torno CNC", "operando", 72.5, "05/11/2025"],
    ["Prensa Hidráulica", "parada", 30.0, "01/11/2025"],
]

for m in maquinas:
    print("Nome:", m[0], "| Status:", m[1], "| Temp:", m[2], "| Última:", m[3])

maquinas.append(["Compressor de Ar", "operando", 45.0, "04/11/2025"])
maquinas.append(["Retífica", "operando", 60.0, "02/11/2025"])
maquinas

historico = {
    "Torno CNC": ["Troca de óleo - 01/11/2025", "Limpeza - 03/11/2025"],
    "Prensa Hidráulica": ["Troca de mangueira - 02/11/2025"]
}

for maquina, eventos in historico.items():
    print("Histórico da máquina", maquina)
    for ev in eventos:
        print("  -", ev)


def adicionar_manutencao(nome_maquina, descricao):
    if nome_maquina not in historico:
        historico[nome_maquina] = []
    historico[nome_maquina].append(descricao)

# teste
adicionar_manutencao("Compressor de Ar", "Troca de filtro - 06/11/2025")
historico

def registrar_medicao(linha):
    partes = linha.split(",")
    nome = partes[0].strip()
    temperatura = float(partes[1].strip())
    status = partes[2].strip()

    for m in maquinas:
        if m[0] == nome:
            m[1] = status
            m[2] = temperatura
            if m[1] == "em manutenção":
                m[3] = datetime.now().strftime("%d/%m/%Y")
            break

registrar_medicao("Torno CNC, 78.5, operando")
maquinas

def salvar_dados_maquinas(lista_maquinas, nome_arquivo="dados_maquinas.txt"):
    with open(nome_arquivo, "w") as arq:
        for m in lista_maquinas:
            linha = f"{m[0]};{m[1]};{m[2]};{m[3]}\n"
            arq.write(linha)
    print("Dados salvos em", nome_arquivo)

salvar_dados_maquinas(maquinas)

def carregar_dados_maquinas(nome_arquivo="dados_maquinas.txt"):
    maquinas_lidas = []
    try:
        with open(nome_arquivo, "r") as arq:
            for linha in arq:
                partes = linha.strip().split(";")
                nome = partes[0]
                status = partes[1]
                temperatura = float(partes[2])
                ultima = partes[3]
                maquinas_lidas.append([nome, status, temperatura, ultima])
    except FileNotFoundError:
        print("Arquivo não encontrado. Salve primeiro.")
    return maquinas_lidas

carregar_dados_maquinas()

def gerar_relatorio(nome_arquivo="relatorio_final.txt"):
    # máquina mais quente
    maquina_quente = max(maquinas, key=lambda x: x[2])

    with open(nome_arquivo, "w") as arq:
        arq.write("RELATÓRIO DE MÁQUINAS\n\n")
        arq.write(f"Máquina mais quente: {maquina_quente[0]} ({maquina_quente[2]} °C)\n\n")

        arq.write("Máquinas em manutenção ou paradas:\n")
        for m in maquinas:
            if m[1] in ["em manutenção", "parada"]:
                arq.write(f"- {m[0]} (última manutenção: {m[3]})\n")

        arq.write("\nQuantidade de manutenções registradas:\n")
        for nome, eventos in historico.items():
            arq.write(f"- {nome}: {len(eventos)} registro(s)\n")
    print("Relatório gerado em", nome_arquivo)

gerar_relatorio()


def modulo_extra(nome_arquivo="custos_manutencao.txt"):
    # dicionário de custos fixos
    custos = {
        "troca de óleo": 120.0,
        "limpeza": 60.0,
        "troca de rolamento": 300.0
    }

    total_geral = 0.0

    with open(nome_arquivo, "w") as arq:
        arq.write("RELATÓRIO DE CUSTOS DE MANUTENÇÃO\n\n")

        for maquina, eventos in historico.items():
            custo_maquina = 0.0

            for ev in eventos:
                desc = ev.lower()

                # verificar se a descrição contém uma das manutenções do dicionário
                for manut, valor in custos.items():
                    if manut in desc:
                        custo_maquina += valor

            total_geral += custo_maquina
            arq.write(f"{maquina}: R$ {custo_maquina:.2f}\n")

        arq.write("\nTOTAL GERAL: R$ {:.2f}\n".format(total_geral))

    print("Relatório de custos gerado em", nome_arquivo)



def main():
    print("=== Sistema de Manutenção de Máquinas ===")
    print("1 - Registrar medição")
    print("2 - Adicionar manutenção")
    print("3 - Salvar dados")
    print("4 - Gerar relatório")
    print("5 - Rodar módulo extra")
    opc = input("Escolha: ")

    if opc == "1":
        linha = input("Digite: nome, temperatura, status: ")
        registrar_medicao(linha)
    elif opc == "2":
        nome = input("Nome da máquina: ")
        desc = input("Descrição da manutenção: ")
        adicionar_manutencao(nome, desc)
    elif opc == "3":
        salvar_dados_maquinas(maquinas)
    elif opc == "4":
        gerar_relatorio()
    elif opc == "5":
        modulo_extra()
    else:
        print("Opção inválida")


if __name__ == "__main__":
   main()