# Alert Management System

**Um sistema desktop para gerenciamento de alertas com interface gráfica e banco de dados SQL Server.**

---

## 📌 Visão Geral

O **Alert Management System** é um projeto pessoal desenvolvido em Python com `tkinter` para interface gráfica e `pyodbc` para integração com banco de dados SQL Server. O sistema permite criar, visualizar, cancelar e gerenciar alertas agendados, com notificações automáticas quando o horário programado é atingido.

---

## 🛠 Tecnologias Utilizadas


| Tecnologia     | Descrição                                                                |
| -------------- | ------------------------------------------------------------------------ |
| **Python**     | Linguagem principal do projeto.                                          |
| **Tkinter**    | Biblioteca para criação da interface gráfica.                            |
| **SQL Server** | Banco de dados relacional para armazenamento dos alertas.                |
| **PyODBC**     | Driver para conexão entre Python e SQL Server.                           |
| **Pandas**     | Utilizado para manipulação de dados retornados do banco.                 |
| **Threading**  | Implementação de threads para verificação contínua de alertas pendentes. |
| **TkCalendar** | Biblioteca para seleção de datas na interface.                           |


---

## 📂 Estrutura do Projeto

```
alert-management-system/
│
├── main.py                # Ponto de entrada da aplicação.
├── gui.py                 # Classe principal da interface gráfica (Application).
├── queries.py             # Funções de interação com o banco de dados.
├── README.md              # Documentação do projeto.
└── requirements.txt       # Dependências do projeto.
```

---

## 🔧 Configuração do Ambiente

### 1. Pré-requisitos

- Python 3.8 ou superior.
- SQL Server 2008 instalado e configurado.
- Biblioteca `pyodbc` configurada para conexão com o SQL Server.

### 2. Instalação das Dependências

```bash
pip install -r requirements.txt
```

### 3. Configuração do Banco de Dados

1. Crie um banco de dados chamado `ProjectDoug` no SQL Server.
2. Execute o script SQL abaixo para criar a tabela `Avisos`:
  ```sql
   CREATE TABLE Avisos (
       AvisoID INT PRIMARY KEY IDENTITY(1,1),
       Aviso VARCHAR(255) NOT NULL,
       DtCriacao DATETIME NOT NULL,
       DtFinalizado DATETIME NULL,
       DtAviso DATETIME NOT NULL,
       StatusID INT NOT NULL
   );
  ```
3. Atualize as credenciais de conexão no arquivo `queries.py`:
  ```python
   conn = pyodbc.connect(
       'DRIVER={SQL Server};'
       'SERVER=localhost\\SQLEXPRESS,3197;'
       'DATABASE=seu_banco;'
       'UID=seu_usuario;'
       'PWD=sua_senha;')
  ```

---

## 🚀 Como Executar

1. Clone o repositório:
  ```bash
   git clone https://github.com/menesesdouglas/alert-management-system.git
  ```
2. Navegue até o diretório do projeto:
  ```bash
   cd alert-management-system
  ```
3. Instale as dependências:
  ```bash
   pip install -r requirements.txt
  ```
4. Execute o sistema:
  ```bash
   python main.py
  ```

---

## 📝 Funcionalidades


| Funcionalidade               | Descrição                                                             |
| ---------------------------- | --------------------------------------------------------------------- |
| **Criar Alerta**             | Permite criar um novo alerta com texto, data e horário específicos.   |
| **Visualizar Alertas**       | Exibe todos os alertas ativos ou cancelados.                          |
| **Cancelar Alerta**          | Marca um alerta como cancelado.                                       |
| **Notificações Automáticas** | Exibe uma notificação quando um alerta atinge a data/hora programada. |


---

## 🔍 Detalhes Técnicos

### 1. Interface Gráfica

- Desenvolvida com `tkinter` e `ttk` para um design limpo e funcional.
- Utiliza `tkcalendar` para seleção de datas.
- Thread separada para verificação contínua de alertas pendentes.

### 2. Banco de Dados

- **Tabela `Avisos**`: Armazena os alertas com os campos:
  - `AvisoID`: Identificador único.
  - `Aviso`: Texto do alerta.
  - `DtCriacao`: Data de criação.
  - `DtFinalizado`: Data de finalização (nulo para alertas pendentes).
  - `DtAviso`: Data/hora programada para o alerta.
  - `StatusID`: Status do alerta (1: Pendente, 2: Finalizado, 3: Cancelado).

### 3. Lógica de Verificação

- A thread `verify_pending_allerts` verifica a cada 5 segundos se há alertas pendentes.
- Se a data/hora atual for maior ou igual à data/hora do alerta, uma notificação é exibida e o status é atualizado para "Finalizado".

---

## 📊 Status dos Alertas


| StatusID | Descrição  |
| -------- | ---------- |
| 1        | Pendente   |
| 2        | Finalizado |
| 3        | Cancelado  |

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

## 📬 Contato

Douglas Meneses  
[LinkedIn](https://www.linkedin.com/in/menesesdouglas)  
[GitHub](https://github.com/menesesdouglas)
[E-mail](menesesdouglas.fx@gmail.com)