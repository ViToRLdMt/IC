import os
import pandas as pd

def convert_fe_ga203(input_files, output_file, filtro=None):
    """
    Converte arquivos Fe on Ga203 aplicando subtrações iterativas com base no terceiro valor do bloco.
    Mantém o valor base da segunda coluna na primeira linha de cada bloco.
    Remove os espaços entre as linhas no arquivo de saída.
    Filtra blocos com base no número antes do "50.0".

    Args:
        input_files (list): Lista de caminhos dos arquivos de entrada.
        output_file (str): Caminho do arquivo de saída.
        filtro (int, opcional): Número do bloco a ser filtrado (por exemplo, 18 ou 21). Se None, não filtra.
    """
    # Caminho do arquivo temporário para combinar os arquivos de entrada
    combined_input_file = 'combined_input.txt'

    # Junta todos os arquivos de entrada em um único arquivo temporário
    with open(combined_input_file, 'w') as combined_file:
        for input_file in input_files:
            print(f"Verificando arquivo: {input_file}")
            if os.path.exists(input_file):
                if os.path.isdir(input_file):
                    # Se for um diretório, adiciona todos os arquivos
                    all_files = [f for f in os.listdir(input_file)]
                    all_files.sort()  # Ordena os arquivos em ordem lexicográfica crescente (por nome)
                    print(f"Arquivos encontrados no diretório {input_file}: {all_files}")
                    for file_name in all_files:
                        full_path = os.path.join(input_file, file_name)
                        if os.path.isfile(full_path):
                            with open(full_path, 'r') as infile:
                                combined_file.write(infile.read())
                                combined_file.write("\n")  # Adiciona uma nova linha entre arquivos
                else:
                    print(f"Lendo o arquivo individual: {input_file}")
                    with open(input_file, 'r') as infile:
                        combined_file.write(infile.read())
                        combined_file.write("\n")  # Adiciona uma nova linha entre arquivos
            else:
                print(f"Arquivo ou diretório não encontrado: {input_file}")

    # Agora, converte o arquivo combinado com Pandas
    with open(combined_input_file, 'r') as infile:
        lines = infile.readlines()

    data = []
    base_values = None
    current_value = None
    is_first_line = True
    bloco_num = None

    for line in lines:
        parts = line.strip().split()

        # Mantém as linhas de texto ou cabeçalhos sem alteração
        if any(c.isalpha() for c in line):
            if bloco_num is not None and (filtro is None or filtro == bloco_num):
                data.append([line.strip()])
            continue

        # Verifica se a linha contém os valores base (início de um bloco)
        if len(parts) >= 9 and all(p.lstrip('-').replace('.', '', 1).isdigit() for p in parts[:3]):
            base_values = [float(parts[0]), float(parts[1]), float(parts[2])]
            current_value = base_values[0]  # Inicializa o valor corrente com o primeiro valor do bloco
            is_first_line = True

            # Extrai o número do bloco (antes do "50.0")
            try:
                bloco_num = int(parts[7])  # O número do bloco está na 8ª posição (índice 7)
            except ValueError:
                bloco_num = None

            # Só adiciona o bloco se o filtro for None ou o número do bloco for o desejado
            if filtro is None or filtro == bloco_num:
                data.append([f"12  0  {line.strip()}"])
            continue

        # Caso a linha contenha um único número válido (dados do bloco)
        if len(parts) == 1 and parts[0].replace('.', '', 1).isdigit():
            if base_values is not None and current_value is not None:
                original_value = int(float(parts[0]))

                # Mantém o valor base na primeira linha
                if is_first_line:
                    if filtro is None or filtro == bloco_num:
                        data.append([f"{original_value:<10}{current_value:<15.5f}"])
                    is_first_line = False
                else:
                    # Faz a subtração corretamente a partir da segunda linha
                    current_value += base_values[2]
                    if filtro is None or filtro == bloco_num:
                        data.append([f"{original_value:<10}{current_value:<15.5f}"])
            continue

        # Mantém as linhas inválidas ou vazias como estão
        if filtro is None or filtro == bloco_num:
            data.append([line.strip()])

    # Cria um DataFrame a partir dos dados
    df = pd.DataFrame(data)

    # Salva o DataFrame no arquivo de saída
    df.to_csv(output_file, header=False, index=False, sep='\t', lineterminator='\n')

    # Remove o arquivo temporário
    os.remove(combined_input_file)

    print(f"Conversão concluída! Arquivo salvo em: {output_file}")


# Inputs mantidos
input_files = input("Digite os caminhos dos arquivos de entrada : ").strip().split(',')
input_files = [file.strip() for file in input_files]  # Limpa espaços extras ao redor

output_file = input("Digite o caminho do arquivo de saída: ").strip()

filtro = input("Digite o número do bloco para filtro (18, 21, etc.): ").strip()
filtro = int(filtro) if filtro.isdigit() else None

convert_fe_ga203(input_files, output_file, filtro)

