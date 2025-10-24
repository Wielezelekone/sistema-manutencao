
import re
import json
from datetime import datetime
from collections import defaultdict

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    print("❌ matplotlib não está instalado. Rode 'pip install matplotlib' no terminal.")
    exit()

veiculos = {}

def salvar_dados():
    with open("veiculos.json", "w", encoding="utf-8") as f:
        json.dump(veiculos, f, ensure_ascii=False, indent=4)

def carregar_dados():
    global veiculos
    try:
        with open("veiculos.json", "r", encoding="utf-8") as f:
            veiculos = json.load(f)
    except FileNotFoundError:
        veiculos = {}

def menu():
    print("\n--- Sistema de Manutenção de Veículos ---")
    print("1. Cadastrar veículo")
    print("2. Registrar manutenção")
    print("3. Ver manutenções de um veículo")
    print("4. Atualizar quilometragem")
    print("5. Verificar revisões pendentes")
    print("6. Listar todos os veículos")
    print("7. Relatórios")
    print("0. Sair")

def validar_placa(placa):
    padrao = re.compile(r'^[A-Z]{3}\d{1}[A-Z]{1}\d{2}$|^[A-Z]{3}\d{4}$')
    return bool(padrao.match(placa))

def cadastrar_veiculo():
    while True:
        placa = input("Digite a placa do veículo: ").upper()
        if not validar_placa(placa):
            print("❌ Formato de placa inválido! Use AAA1A23 ou AAA1234")
            continue
        if placa in veiculos:
            print("❌ Veículo já cadastrado.")
            return
        break

    marca = input("Digite a marca do veículo: ").title()
    modelo = input("Digite o modelo do veículo: ").title()

    while True:
        tipo = input("Tipo do veículo (carro, moto ou caminhão): ").lower()
        if tipo in ['carro', 'moto', 'caminhão']:
            break
        print("❌ Tipo inválido! Digite 'carro', 'moto' ou 'caminhão'.")

    while True:
        try:
            ano = int(input("Digite o ano do veículo (ex: 2020): "))
            break
        except ValueError:
            print("❌ Ano inválido! Digite um número válido.")

    while True:
        try:
            km = int(input("Digite a quilometragem atual do veículo: "))
            break
        except ValueError:
            print("❌ Quilometragem inválida! Digite um número válido.")

    while True:
        try:
            intervalo_oleo = int(input("Intervalo de troca de óleo (km): "))
            break
        except ValueError:
            print("❌ Intervalo inválido! Digite um número válido.")

    while True:
        try:
            intervalo_pneu = int(input("Intervalo de troca de pneus (km): "))
            break
        except ValueError:
            print("❌ Intervalo inválido! Digite um número válido.")

    veiculos[placa] = {
        'marca': marca,
        'modelo': modelo,
        'ano': ano,
        'tipo': tipo,
        'quilometragem': km,
        'manutencoes': [],
        'ultima_troca_oleo': km,
        'ultima_troca_pneu': km,
        'intervalo_oleo': intervalo_oleo,
        'intervalo_pneu': intervalo_pneu,
        'historico_km': [(datetime.now().strftime("%d/%m/%Y"), km)]
    }

    print(f"\n✅ Veículo {placa} ({marca} {modelo} {ano}) cadastrado com sucesso!")
    salvar_dados()

def registrar_manutencao():
    placa = input("Digite a placa do veículo: ").upper()

    if placa not in veiculos:
        print("❌ Veículo não encontrado!")
        return

    print("\nTipos de manutenção disponíveis:")
    print("1 - Troca de óleo")
    print("2 - Troca de pneus")
    print("3 - Outra manutenção")

    while True:
        try:
            tipo = int(input("Escolha o tipo de manutenção: "))
            if tipo not in [1, 2, 3]:
                raise ValueError
            break
        except ValueError:
            print("❌ Tipo inválido! Escolha 1, 2 ou 3.")

    descricao = input("Descreva a manutenção realizada: ")
    
    while True:
        custo_str = input("Digite o custo da manutenção: R$ ").replace(',', '.')
        try:
            custo = float(custo_str)
            break
        except ValueError:
            print("❌ Custo inválido! Use números, ex: 150.50")

    while True:
        try:
            nova_km = int(input("Digite a quilometragem atual: "))
            if nova_km < veiculos[placa]['quilometragem']:
                print("❌ Quilometragem menor que a atual!")
                continue
            break
        except ValueError:
            print("❌ Quilometragem inválida! Digite um número válido.")

    veiculos[placa]['quilometragem'] = nova_km
    veiculos[placa]['historico_km'].append((datetime.now().strftime("%d/%m/%Y"), nova_km))

    if tipo == 1:
        veiculos[placa]['ultima_troca_oleo'] = nova_km
    elif tipo == 2:
        veiculos[placa]['ultima_troca_pneu'] = nova_km

    veiculos[placa]['manutencoes'].append({
        'data': datetime.now().strftime("%d/%m/%Y"),
        'tipo': tipo,
        'descricao': descricao,
        'custo': custo,
        'km': nova_km
    })

    print(f"\n✅ Manutenção registrada para o veículo {placa}!")
    salvar_dados()

def ver_manutencoes():
    placa = input("Digite a placa do veículo: ").upper()
    if placa not in veiculos:
        print("❌ Veículo não encontrado!")
        return

    manutencoes = veiculos[placa]['manutencoes']
    if not manutencoes:
        print("ℹ️ Nenhuma manutenção registrada.")
        return

    print(f"\n📋 Manutenções de {placa}:")
    for i, m in enumerate(manutencoes, 1):
        tipo = {1: 'Troca de óleo', 2: 'Troca de pneus', 3: 'Outra manutenção'}.get(m['tipo'])
        print(f"\n#{i} - {tipo}")
        print(f"Data: {m['data']} | KM: {m['km']} | Custo: R$ {m['custo']:.2f}")
        print(f"Descrição: {m['descricao']}")

def atualizar_quilometragem():
    placa = input("Digite a placa do veículo: ").upper()
    if placa not in veiculos:
        print("❌ Veículo não encontrado!")
        return

    while True:
        try:
            nova_km = int(input("Digite a nova quilometragem: "))
            if nova_km <= veiculos[placa]['quilometragem']:
                print("❌ A nova quilometragem deve ser maior que a atual!")
                continue
            break
        except ValueError:
            print("❌ Valor inválido! Digite um número válido.")

    veiculos[placa]['quilometragem'] = nova_km
    veiculos[placa]['historico_km'].append((datetime.now().strftime("%d/%m/%Y"), nova_km))
    print("✅ Quilometragem atualizada com sucesso!")
    salvar_dados()

def verificar_revisoes():
    placa = input("Digite a placa do veículo: ").upper()
    if placa not in veiculos:
        print("❌ Veículo não encontrado!")
        return

    v = veiculos[placa]
    km_atual = v['quilometragem']
    pendentes = []

    if km_atual - v['ultima_troca_oleo'] >= v['intervalo_oleo']:
        pendentes.append(f"Troca de óleo (última em {v['ultima_troca_oleo']} km)")

    if km_atual - v['ultima_troca_pneu'] >= v['intervalo_pneu']:
        pendentes.append(f"Troca de pneus (última em {v['ultima_troca_pneu']} km)")

    if pendentes:
        print("\n⚠️ Revisões pendentes:")
        for p in pendentes:
            print(f"- {p}")
    else:
        print("✅ Nenhuma revisão pendente!")

def listar_veiculos():
    if not veiculos:
        print("ℹ️ Nenhum veículo cadastrado.")
        return

    for placa, v in veiculos.items():
        print(f"\nPlaca: {placa} | {v['marca']} {v['modelo']} ({v['ano']})")
        print(f"Tipo: {v['tipo']} | KM: {v['quilometragem']} km")
        print(f"Últ. óleo: {v['ultima_troca_oleo']} km | Últ. pneus: {v['ultima_troca_pneu']} km")

def relatorios():
    if not veiculos:
        print("\nℹ️ Nenhum veículo cadastrado para gerar relatórios.")
        return

    print("\n📊 Relatórios disponíveis:")
    print("1 - Quantidade de manutenções por veículo")
    print("2 - Gasto total por mês")
    print("3 - Gasto por tipo de manutenção")
    print("4 - Gráfico de histórico de KM de um veículo")

    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        print("\n🔧 Manutenções por veículo:")
        for placa, dados in veiculos.items():
            print(f"{placa} - {len(dados['manutencoes'])} manutenções")

    elif opcao == '2':
        print("\n💰 Gasto total por mês:")
        gastos = defaultdict(float)
        for dados in veiculos.values():
            for m in dados['manutencoes']:
                mes = m['data'][3:]  # MM/AAAA
                gastos[mes] += m['custo']
        for mes, total in sorted(gastos.items()):
            print(f"{mes}: R$ {total:.2f}")

    elif opcao == '3':
        print("\n📋 Gasto por tipo de manutenção:")
        tipos = {1: "Troca de óleo", 2: "Troca de pneus", 3: "Outra manutenção"}
        gastos = defaultdict(float)
        for dados in veiculos.values():
            for m in dados['manutencoes']:
                tipo = tipos.get(m['tipo'], 'Desconhecido')
                gastos[tipo] += m['custo']
        for tipo, total in gastos.items():
            print(f"{tipo}: R$ {total:.2f}")

    elif opcao == '4':
        placa = input("Digite a placa do veículo: ").upper()
        if placa not in veiculos:
            print("❌ Veículo não encontrado!")
            return
        historico = veiculos[placa]['historico_km']
        datas = [d for d, _ in historico]
        kms = [km for _, km in historico]

        plt.figure(figsize=(10, 5))
        plt.plot(datas, kms, marker='o', linestyle='-', color='blue')
        plt.title(f"Histórico de Quilometragem - {placa}")
        plt.xlabel("Data")
        plt.ylabel("KM")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    else:
        print("❌ Opção inválida!")

def main():
    carregar_dados()
    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_veiculo()
        elif opcao == '2':
            registrar_manutencao()
        elif opcao == '3':
            ver_manutencoes()
        elif opcao == '4':
            atualizar_quilometragem()
        elif opcao == '5':
            verificar_revisoes()
        elif opcao == '6':
            listar_veiculos()
        elif opcao == '7':
            relatorios()
        elif opcao == '0':
            print("\n👋 Saindo do sistema...")
            salvar_dados()
            break
        else:
            print("\n❌ Opção inválida!")

        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()
