#!/usr/bin/env python3
"""Mini navegador com interface gráfica em Python (Qt WebEngine)."""

import sys
from urllib.parse import quote_plus

try:
    from PyQt6.QtCore import QUrl
    from PyQt6.QtWidgets import (
        QApplication,
        QLineEdit,
        QMainWindow,
        QMessageBox,
        QPushButton,
        QStatusBar,
        QToolBar,
    )
    from PyQt6.QtWebEngineWidgets import QWebEngineView
except ImportError as exc:
    print(
        "Dependências ausentes. Instale com:\n"
        "  pip install PyQt6 PyQt6-WebEngine\n\n"
        f"Erro original: {exc}"
    )
    sys.exit(1)


class MiniNavegador(QMainWindow):
    """Navegador simples com suporte a HTML, CSS e JavaScript."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Navegador Python")
        self.resize(1200, 800)

        self.webview = QWebEngineView()
        self.setCentralWidget(self.webview)

        self._criar_barra_navegacao()
        self._conectar_eventos()

        self.webview.setUrl(QUrl("https://duckduckgo.com"))

    def _criar_barra_navegacao(self):
        toolbar = QToolBar("Navegação")
        self.addToolBar(toolbar)

        botao_voltar = QPushButton("←")
        botao_voltar.clicked.connect(self.webview.back)
        toolbar.addWidget(botao_voltar)

        botao_avancar = QPushButton("→")
        botao_avancar.clicked.connect(self.webview.forward)
        toolbar.addWidget(botao_avancar)

        botao_recarregar = QPushButton("⟳")
        botao_recarregar.clicked.connect(self.webview.reload)
        toolbar.addWidget(botao_recarregar)

        botao_home = QPushButton("🏠")
        botao_home.clicked.connect(lambda: self.webview.setUrl(QUrl("https://duckduckgo.com")))
        toolbar.addWidget(botao_home)

        self.campo_url = QLineEdit()
        self.campo_url.setPlaceholderText("Digite uma URL (ex: python.org) ou busca")
        self.campo_url.returnPressed.connect(self.navegar)
        toolbar.addWidget(self.campo_url)

        botao_ir = QPushButton("Ir")
        botao_ir.clicked.connect(self.navegar)
        toolbar.addWidget(botao_ir)

        self.setStatusBar(QStatusBar())

    def _conectar_eventos(self):
        self.webview.urlChanged.connect(self._atualizar_url)
        self.webview.loadStarted.connect(lambda: self.statusBar().showMessage("Carregando..."))
        self.webview.loadFinished.connect(self._finalizar_carregamento)

    def navegar(self):
        texto = self.campo_url.text().strip()
        if not texto:
            return

        if " " in texto and not texto.startswith(("http://", "https://")):
            busca = f"https://duckduckgo.com/?q={quote_plus(texto)}"
            self.webview.setUrl(QUrl(busca))
            return

        if not texto.startswith(("http://", "https://")):
            texto = "https://" + texto

        qurl = QUrl(texto)
        if qurl.isValid() and qurl.scheme() in {"http", "https"}:
            self.webview.setUrl(qurl)
        else:
            QMessageBox.warning(self, "URL inválida", "Digite uma URL válida.")

    def _atualizar_url(self, url: QUrl):
        self.campo_url.setText(url.toString())

    def _finalizar_carregamento(self, ok: bool):
        if ok:
            self.statusBar().showMessage("Página carregada.", 3000)
        else:
            self.statusBar().showMessage("Falha ao carregar página.", 5000)
            QMessageBox.warning(
                self,
                "Erro de carregamento",
                "Não foi possível abrir a página. Verifique a URL e sua conexão.",
            )


def main():
    app = QApplication(sys.argv)
    janela = MiniNavegador()
    janela.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
