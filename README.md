# What is the Price

Este projeto é um sistema de orçamento desenvolvido em Python que utiliza a biblioteca Tkinter para a interface gráfica e SQLite para o armazenamento dos dados. O sistema permite que o usuário:

- Cadastre novas combinações de opções de impressão, com parâmetros como acabamento, papel, impressão e faca.
- Calcule preços de produtos considerando valores base cadastrados e custos adicionais para furos, cortes e vincos (com os dois primeiros inclusos).
- Edite e exclua combinações já cadastradas por meio de uma interface intuitiva.
- Remova linhas de preços no cadastro de uma nova combinação, garantindo que a primeira linha (obrigatória) não seja removida.

## Funcionalidades

- **Consulta de preços:** Escolha uma combinação de acabamento, papel, impressão e faca e informe o número de furos, cortes e vincos. O sistema soma os custos adicionais (R$5,00 por furo, R$6,00 por corte e R$6,00 por vinco, acima dos dois inclusos) e exibe os valores finais.
- **Cadastro de combinações:** Permite cadastrar novas combinações com múltiplas linhas de preços. As linhas adicionais podem ser removidas, garantindo que a primeira linha, obrigatória, seja mantida.
- **Edição e exclusão:** Uma interface de gerenciamento permite visualizar todas as combinações cadastradas, editar ou excluir as que forem necessárias.
- **Integração com SQLite:** Os dados são armazenados em um banco de dados SQLite, com operações CRUD implementadas em um módulo dedicado.

## Requisitos

- Python 3.6 ou superior (recomendamos Python 3.13 para compatibilidade total com as versões atuais do Tkinter)
- Tkinter (geralmente incluído na instalação padrão do Python)
- SQLite (o módulo sqlite3 já vem incluso no Python)

## Instalação

1. **Clone o Repositório:**
`git clone https://github.com/seu-usuario/what-is-the-price.git`
`cd what-is-the-price`
2. **Verifique se o Tkinter está instalado:**
Execute o seguinte comando para testar se o Tkinter está funcionando:
`python -m tkinter`
3. **Execute o programa:**
`python main.py`

##Estrutura do Projeto

- **db_handler.py:** Módulo responsável pela conexão com o banco de dados SQLite, criação da tabela e operações CRUD (inserir, buscar, atualizar, excluir e listar combinações).
- **ui.py:** Contém a interface gráfica (Tkinter) que permite consultar preços, cadastrar novas combinações, editar e excluir combinações já cadastradas, além de gerenciar as linhas de preços (com a funcionalidade de remoção apenas a partir da segunda linha).
- **main.py:** Ponto de entrada da aplicação, que instancia a interface principal e inicia o loop do Tkinter.

## Uso

1. Consulta de Preços:

- Preencha o nome do orçamento (opcional) e selecione as opções desejadas (acabamento, papel, impressão, faca).
- Informe o número total de furos, cortes e vincos. (Os dois primeiros de cada item estão inclusos no preço base.)
- Clique em "Consultar Preços" para visualizar a tabela de preços com os valores finais, que já incluem os custos adicionais.

2. Cadastro de Nova Combinação:

- Clique em "Cadastrar Nova Combinação" para abrir a janela de cadastro.
- Selecione os parâmetros e insira as linhas de preços. A primeira linha é obrigatória e não pode ser removida; linhas adicionais poderão ser removidas com o botão "Remover".
- Clique em "Salvar" para inserir a nova combinação no banco de dados.

3. Gerenciamento de Combinações:

- Clique em "Gerenciar Combinações" para visualizar uma lista (Treeview) com todas as combinações cadastradas.
- Selecione uma combinação e escolha "Editar" para alterá-la ou "Excluir" para removê-la.

## Contribuições

Contribuições são bem-vindas! Se você deseja melhorar o projeto ou adicionar novas funcionalidades, por favor abra uma issue ou envie um pull request.
