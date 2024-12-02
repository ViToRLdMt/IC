import os

def convert_fe_ga203(input_files, output_file):
    """
    Converte arquivos Fe on Ga203 aplicando subtrações iterativas com base no terceiro valor do bloco.
    Mantém o valor base da segunda coluna na primeira linha de cada bloco.
    Remove os espaços entre as linhas no arquivo de saída.

    Args:
        input_files (list): Lista de caminhos dos arquivos de entrada.
        output_file (str): Caminho do arquivo de saída.
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
                    print(f"Total de arquivos encontrados: {len(all_files)}")
                    for file_name in all_files:
                        full_path = os.path.join(input_file, file_name)
                        print(f"Lendo o arquivo: {full_path}")
                        if os.path.isfile(full_path):
                            with open(full_path, 'r') as infile:
                                combined_file.write(infile.read())
                                combined_file.write("\n")  # Adiciona uma nova linha entre arquivos
                        else:
                            print(f"O arquivo não foi encontrado: {full_path}")
                else:
                    print(f"Lendo o arquivo individual: {input_file}")
                    with open(input_file, 'r') as infile:
                        combined_file.write(infile.read())
                        combined_file.write("\n")  # Adiciona uma nova linha entre arquivos
            else:
                print(f"Arquivo ou diretório não encontrado: {input_file}")

    # Agora, converte o arquivo combinado
    with open(combined_input_file, 'r') as infile, open(output_file, 'w') as outfile:
        base_values = None  # Para armazenar os valores base do bloco
        current_value = None  # Valor corrente para subtrações progressivas
        is_first_line = True  # Flag para controlar a primeira linha do bloco

        for line in infile:
            parts = line.strip().split()

            # Mantém as linhas de texto ou cabeçalhos sem alteração
            if any(c.isalpha() for c in line):
                outfile.write(line)
                continue

            # Verifica se a linha contém os valores base (início de um bloco)
            if len(parts) >= 3 and all(p.lstrip('-').replace('.', '', 1).isdigit() for p in parts[:3]):
                # Define os valores base do bloco
                base_values = [float(parts[0]), float(parts[1]), float(parts[2])]
                current_value = base_values[0]  # Inicializa o valor corrente com o primeiro valor do bloco
                is_first_line = True  # Reseta o controle de primeira linha
                # Escreve os valores "12" e "0" no início do bloco
                outfile.write(f"12  0  {line.strip()}\n")
                continue

            # Caso a linha contenha um único número válido (dados do bloco)
            if len(parts) == 1 and parts[0].replace('.', '', 1).isdigit():
                if base_values is not None and current_value is not None:
                    # Pega o valor original
                    original_value = int(float(parts[0]))

                    # Mantém o valor base na primeira linha
                    if is_first_line:
                        outfile.write(f"{original_value:<10}{current_value:<15.5f}\n")
                        is_first_line = False  # Desativa o controle de primeira linha
                    else:
                        # Faz a subtração corretamente a partir da segunda linha
                        current_value += base_values[2]
                        outfile.write(f"{original_value:<10}{current_value:<15.5f}\n")
                continue

            # Mantém as linhas inválidas ou vazias como estão
            outfile.write(line)

    # Remove o arquivo temporário
    os.remove(combined_input_file)

    print(f"Conversão concluída! Arquivo salvo em: {output_file}")


# Inputs mantidos
input_files = input("Digite os caminhos dos arquivos de entrada : ").strip().split(',')
input_files = [file.strip() for file in input_files]  # Limpa espaços extras ao redor

output_file = input("Digite o caminho do arquivo de saída: ").strip()

convert_fe_ga203(input_files, output_file)
