import random
import sys
import os
import importlib.util
import inspect
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QTextEdit, QLabel, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QMovie, QIcon, QColor

# ====== DEFINIR CAMINHO DOS ASSETS ======
ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')

# ====== FUNÇÃO: asset ======
def asset(nome_arquivo):
    """Retorna o caminho completo de um arquivo na pasta 'assets'"""
    return os.path.join(ASSETS_PATH, nome_arquivo)

# ====== FUNÇÃO: carregar_funcoes_scripts ======
def carregar_funcoes_scripts(nomes_arquivos):
    """Carrega funções de múltiplos arquivos Python da pasta 'files'"""
    funcoes = []
    for nome_arquivo in nomes_arquivos:
        caminho = os.path.join(os.path.dirname(__file__), 'files', nome_arquivo)
        spec = importlib.util.spec_from_file_location(nome_arquivo, caminho)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        funcoes.extend([
            func for nome, func in inspect.getmembers(modulo, inspect.isfunction)
        ])
    return funcoes

# ====== CLASSE: Worker ======
class Worker(QThread):
    """Thread para executar funções sem travar a interface"""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, nome, func):
        super().__init__()
        self.nome = nome
        self.func = func

    def run(self):
        try:
            self.func()
            self.finished.emit(f"Função {self.nome} executada com sucesso.")
        except Exception as e:
            self.error.emit(str(e))

# ====== CLASSE: App ======
class App(QWidget):
    """Interface principal do aplicativo"""

    def __init__(self):
        super().__init__()
        self.fila = []
        self.executando = False
        self.thread = None
        self.gif_timer = QTimer()
        self.color_timer = QTimer()
        self.gif_list = [f for f in os.listdir(ASSETS_PATH) if f.endswith('.gif')]

        # ====== INICIALIZA A FILA DE GIFS JÁ NO INÍCIO ======
        self.gif_pool = self.gif_list.copy()
        random.shuffle(self.gif_pool)

        # ====== EDITAR AQUI OS SCRIPTS QUE VOCÊ QUER CARREGAR ======
        nomes_scripts = ['script1.py', 'script2.py']  # <<--- edite conforme necessário
        self.funcoes = carregar_funcoes_scripts(nomes_scripts)

        self.janela_largura = 720
        self.janela_altura = 500

        self.initUI()

    # ====== FUNÇÃO: initUI ======
    def initUI(self):
        self._setup_window()
        self._setup_background()
        self._setup_layout()
        self._setup_buttons()
        self._setup_log()
        self._start_gif_timer()
        self._start_color_timer()
        self.show()

    # ====== FUNÇÃO: _setup_window ======
    def _setup_window(self):
        self.setWindowIcon(QIcon(asset('icon.png')))
        self.setWindowTitle('MOVIMENTAÇÕES DA BIBA')
        flags = Qt.Window | Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint
        self.setWindowFlags(flags)
        self.setFixedSize(self.janela_largura, self.janela_altura)
        QTimer.singleShot(0, self._centralizar)

    # ====== FUNÇÃO: _centralizar ======
    def _centralizar(self):
        """Centraliza a janela na tela"""
        screen = QApplication.primaryScreen().availableGeometry()
        center_x = (screen.width() - self.width()) // 2
        center_y = (screen.height() - self.height()) // 2
        self.move(center_x, center_y)

    # ====== FUNÇÃO: resizeEvent ======
    def resizeEvent(self, event):
        """Ajusta o GIF sempre que a janela for redimensionada"""
        self._ajustar_gif_para_janela()

    # ====== FUNÇÃO: _ajustar_gif_para_janela ======
    def _ajustar_gif_para_janela(self):
        """Ajusta o tamanho do GIF para caber na janela"""
        if hasattr(self, 'movie') and self.movie:
            self.movie.setScaledSize(QSize(self.janela_largura, self.janela_altura))
        self.bg_label.resize(self.janela_largura, self.janela_altura)

    # ====== FUNÇÃO: _setup_background ======
    def _setup_background(self):
        self.bg_label = QLabel(self)
        self.bg_label.setAlignment(Qt.AlignCenter)
        self.movie = None
        self._trocar_gif()

    # ====== FUNÇÃO: _start_gif_timer ======
    def _start_gif_timer(self):
        self.gif_timer.timeout.connect(self._trocar_gif)
        self.gif_pool = self.gif_list.copy()
        random.shuffle(self.gif_pool)
        self.gif_timer.start(5000)

    # ====== FUNÇÃO: _trocar_gif ======
    def _trocar_gif(self):
        if not self.gif_pool:
            self.gif_pool = self.gif_list.copy()
            random.shuffle(self.gif_pool)

        novo_gif = self.gif_pool.pop()

        if self.movie:
            self.movie.stop()

        self.movie = QMovie(asset(novo_gif))
        self.bg_label.setMovie(self.movie)
        self.movie.start()
        self._ajustar_gif_para_janela()

    # ====== FUNÇÃO: moveEvent ======
    def moveEvent(self, event):
        QTimer.singleShot(100, self._centralizar)

    # ====== FUNÇÃO: _setup_layout ======
    def _setup_layout(self):
        self.main_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.button_layout)
        self.setLayout(self.main_layout)

    # ====== FUNÇÃO: _setup_buttons ======
    def _setup_buttons(self):
        self.botoes = []
        for func in self.funcoes:
            nome_funcao = func.__name__.replace('_', ' ').upper()
            button = QPushButton(nome_funcao)
            button.setStyleSheet(self._button_stylesheet("#ff6ec7", "#736efe"))
            button.clicked.connect(lambda _, n=nome_funcao, f=func: self._add_to_queue(n, f))
            button.setMinimumWidth(button.fontMetrics().boundingRect(nome_funcao).width() + 40)

            sombra = QGraphicsDropShadowEffect()
            sombra.setBlurRadius(15)
            sombra.setColor(QColor(0, 0, 0, 230))
            sombra.setOffset(2, 2)
            button.setGraphicsEffect(sombra)

            self.button_layout.addWidget(button)
            self.botoes.append(button)

    # ====== FUNÇÃO: _start_color_timer ======
    def _start_color_timer(self):
        self.color_timer.timeout.connect(self._trocar_cores_botoes)
        self.color_timer.start(5000)

    # ====== FUNÇÃO: _trocar_cores_botoes ======
    def _trocar_cores_botoes(self):
        cores = ["#ADD8E6", "#FFD700", "#FF6347", "#FFA500", "#90EE90"]
        cor1 = random.choice(cores)
        cor2 = random.choice(cores)
        while cor2 == cor1:
            cor2 = random.choice(cores)
        for botao in self.botoes:
            botao.setStyleSheet(self._button_stylesheet(cor1, cor2))

    # ====== FUNÇÃO: _button_stylesheet ======
    def _button_stylesheet(self, cor1, cor2):
        def hex_to_rgba(hex_cor, alpha=0.3):
            hex_cor = hex_cor.lstrip('#')
            r, g, b = tuple(int(hex_cor[i:i+2], 16) for i in (0, 2, 4))
            return f'rgba({r}, {g}, {b}, {alpha})'

        rgba1 = hex_to_rgba(cor1, 0.5)
        rgba2 = hex_to_rgba(cor2, 0.0)

        return f"""
            QPushButton {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {rgba1}, stop:1 {rgba2});
                color: white;
                border-radius: 8px;
                padding: 10px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {rgba2}, stop:1 {rgba1});
            }}
        """

    # ====== FUNÇÃO: _setup_log ======
    def _setup_log(self):
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            background-color: rgba(30, 30, 30, 120); /* Fundo ligeiramente mais claro para melhor contraste */
            color: #f0f0f0; /* Cor de texto padrão mais clara */
            border-radius: 8px;
            font-size: 15px;
            font-family: 'Segoe UI', monospace; /* Fonte mais moderna e legível */
        """)
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(15)
        sombra.setColor(QColor(0, 0, 0, 255))
        sombra.setOffset(2, 2)
        self.log_text.setGraphicsEffect(sombra)
        self.main_layout.addWidget(self.log_text)

        self.cores_funcoes = {}

# ====== FUNÇÃO: _gerar_cor_unica ======
    def _gerar_cor_unica(self):
        return "#{:06x}".format(random.randint(0xAAFFAA, 0xFFFFFF)) # Intervalo para cores mais claras

    # ====== FUNÇÃO: _log ======
    def _log(self, msg, tipo="info", nome_funcao=None):
        cores_tipos = {"info": "#b0ffb0", "erro": "#ff8080", "ok": "#80ffff"} # Neons claros
        cores_arco_iris = {"vermelho": "#ff69b4", "laranja": "#ffb347", "amarelo": "#ffff8f", # Rosa neon, laranja, amarelo claro
                           "verde": "#98fb98", "azul": "#add8e6", "anil": "#8a2be2",       # Verde claro, azul claro, violeta
                           "violeta": "#ee82ee"}                                          # Magenta
        cor = self.cores_funcoes.get(nome_funcao, cores_tipos.get(tipo, cores_arco_iris.get(tipo.lower(), "#b0ffb0")))
        self.log_text.append(f'<b><span style="color:{cor};">{msg}</span></b>') # Mantendo o negrito

    # ====== FUNÇÃO: _add_to_queue ======
    def _add_to_queue(self, nome, func):
        if nome not in self.cores_funcoes:
            self.cores_funcoes[nome] = self._gerar_cor_unica()
        self.fila.append((nome, func))
        if not self.executando:
            self._executar_proxima()

    # ====== FUNÇÃO: _executar_proxima ======
    def _executar_proxima(self):
        """Executa a próxima função da fila"""
        if not self.fila:
            return

        nome, func = self.fila.pop(0)
        self._log(f"Executando {nome}...", "info", nome_funcao=nome)
        self.thread = Worker(nome, func)
        self.thread.finished.connect(self._on_finished)
        self.thread.error.connect(self._on_error)
        self.executando = True
        self.thread.start()

    # ====== FUNÇÃO: _on_finished ======
    def _on_finished(self, msg):
        if self.thread:
            nome_funcao = self.thread.nome
            self._log(msg, "ok", nome_funcao=nome_funcao)
        else:
            self._log(msg, "ok")
        self.executando = False
        self._executar_proxima()

    # ====== FUNÇÃO: _on_error ======
    def _on_error(self, erro):
        if self.thread:
            nome_funcao = self.thread.nome
            self._log(f"Erro: {erro}", "erro", nome_funcao=nome_funcao)
        else:
            self._log(f"Erro: {erro}", "erro")
        self.executando = False
        self._executar_proxima()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
