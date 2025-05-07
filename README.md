# 🎨 Interface PyQt5 para Execução de Scripts Automáticos

Sistema de interface gráfica ⚡ elegante e responsiva, que executa scripts Python com apenas um clique — sem travar a interface, com feedback visual e logs dinâmicos.  
Ideal para automação de rotinas contábeis, financeiras ou qualquer tarefa repetitiva.

---

## 🚀 Funcionalidades

- 🖱️ **Botões dinâmicos**: executam funções carregadas automaticamente de scripts Python.
- 🌀 **Fundo animado com GIFs**: troca automática a cada 5 segundos.
- 🌈 **Cores de botões aleatórias**: atualiza gradientes periodicamente para visual moderno.
- 📋 **Log detalhado**: histórico das execuções, com cores e status.
- ⏩ **Execução em fila (Thread-safe)**: múltiplas funções na sequência, sem travamento.

---

## 🛠️ Como configurar

1️⃣ Crie a pasta `files/` e adicione seus scripts Python com as funções que deseja executar.  
2️⃣ Edite esta linha no código para incluir o nome dos scripts:

```python
nomes_scripts = ['script1.py', 'script2.py']  # <<--- edite conforme necessário
````

3️⃣ Crie a pasta `assets/` e adicione:

* Gifs (`*.gif`) — serão usados como fundo animado
* Ícone `icon.png` — ícone da janela

---

## ▶️ Como rodar

```bash
pip install PyQt5
python nome_do_seu_arquivo.py
```

---

## 📂 Estrutura de pastas

```
📁 seu_projeto/
├── assets/
│   ├── icon.png
│   ├── gif1.gif
│   └── gif2.gif
├── files/
│   ├── script1.py
│   └── script2.py
└── interface.py
```

---

## 💡 Exemplo de função nos scripts

```python
# Dentro de files/script1.py

def minha_funcao():
    print("Minha função foi executada com sucesso!")
```

---

## ✨ Tecnologias

* [PyQt5](https://pypi.org/project/PyQt5/) — Interface gráfica moderna
* **Threading (QThread)** — Execução paralela sem travamento
* **Sistema de assets** — Carregamento dinâmico de GIFs, ícones e scripts

---

## 👨‍💻 Autor

Carlos Eduardo Costa Lima da Silva
**Automação & Reconciliação Contábil — C6 Bank** 🏦

---

## 📢 Observação

> O sistema foi projetado para ser **intuitivo**, **leve** e **customizável**.
> Basta adicionar novos scripts na pasta `files/` e a interface gera os botões automaticamente. 🛠️
