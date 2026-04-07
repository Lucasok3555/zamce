#!/usr/bin/env python3
"""
Mini Navegador Python - Versão Terminal com Interface Web Simples
Um navegador minimalista que busca e exibe conteúdo de páginas web.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re


class MiniNavegador:
    def __init__(self):
        self.sessao = requests.Session()
        self.sessao.headers.update({
            'User-Agent': 'Mozilla/5.0 (Mini Navegador Python)'
        })
        self.sessao.verify = False  # Desativa verificação SSL para ambientes de teste
        self.url_atual = None
        self.historico = []
        
        # Suprime warnings de SSL
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def buscar_pagina(self, url):
        """Busca uma página web e retorna o conteúdo"""
        try:
            # Adiciona http:// se não tiver protocolo
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            resposta = self.sessao.get(url, timeout=10)
            resposta.raise_for_status()
            
            # Atualiza URL atual (pode ter redirecionamento)
            self.url_atual = resposta.url
            
            # Salva no histórico
            self.historico.append(self.url_atual)
            
            return resposta.text
        except requests.exceptions.RequestException as e:
            return f"Erro ao carregar página: {e}"
    
    def extrair_texto(self, html):
        """Extrai texto legível do HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove scripts e styles
        for script in soup(['script', 'style', 'meta', 'link']):
            script.decompose()
        
        # Obtém texto
        texto = soup.get_text(separator='\n')
        
        # Limpa linhas em branco extras
        linhas = [linha.strip() for linha in texto.splitlines()]
        texto_limpo = '\n'.join(linha for linha in linhas if linha)
        
        return texto_limpo[:5000]  # Limita tamanho
    
    def extrair_links(self, html):
        """Extrai todos os links da página"""
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            texto = link.get_text(strip=True)[:50]
            url_completa = urljoin(self.url_atual, href)
            
            if texto:
                links.append({'texto': texto, 'url': url_completa})
        
        return links[:20]  # Limita a 20 links
    
    def mostrar_pagina(self, url):
        """Busca e mostra uma página de forma formatada"""
        print(f"\n{'='*60}")
        print(f"Carregando: {url}")
        print('='*60)
        
        html = self.buscar_pagina(url)
        
        if html.startswith("Erro"):
            print(html)
            return
        
        print(f"\n📄 URL Atual: {self.url_atual}")
        print(f"\n{'─'*60}")
        print("CONTEÚDO DA PÁGINA:")
        print('─'*60)
        
        texto = self.extrair_texto(html)
        print(texto)
        
        # Mostra links encontrados
        links = self.extrair_links(html)
        if links:
            print(f"\n{'─'*60}")
            print("LINKS ENCONTRADOS:")
            print('─'*60)
            for i, link in enumerate(links, 1):
                print(f"{i}. {link['texto']}")
                print(f"   → {link['url'][:60]}...")
        
        print(f"\n{'='*60}")
    
    def mostrar_historico(self):
        """Mostra o histórico de navegação"""
        if not self.historico:
            print("\nHistórico vazio.")
            return
        
        print("\n📚 HISTÓRICO DE NAVEGAÇÃO:")
        for i, url in enumerate(self.historico[-10:], 1):  # Últimos 10
            print(f"{i}. {url}")
    
    def menu(self):
        """Exibe o menu principal"""
        print("\n" + "="*60)
        print("🌐 MINI NAVEGADOR PYTHON")
        print("="*60)
        print("Comandos disponíveis:")
        print("  [URL]     - Navegar para uma URL")
        print("  h         - Mostrar histórico")
        print("  r         - Recarregar página atual")
        print("  q         - Sair")
        print("="*60)


def main():
    navegador = MiniNavegador()
    
    print("\n🌐 Bem-vindo ao Mini Navegador Python!")
    print("Digite uma URL para começar (ex: example.com)")
    
    while True:
        navegador.menu()
        
        if navegador.url_atual:
            print(f"Página atual: {navegador.url_atual}")
        
        entrada = input("\n🔍 Digite comando ou URL: ").strip()
        
        if not entrada:
            continue
        
        comando = entrada.lower()
        
        if comando == 'q':
            print("\nObrigado por usar o Mini Navegador Python! 👋")
            break
        elif comando == 'h':
            navegador.mostrar_historico()
        elif comando == 'r':
            if navegador.url_atual:
                navegador.mostrar_pagina(navegador.url_atual)
            else:
                print("\nNenhuma página carregada ainda.")
        else:
            # Assume que é uma URL
            navegador.mostrar_pagina(entrada)


if __name__ == "__main__":
    main()
