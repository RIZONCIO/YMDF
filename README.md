# 🎵 YMDF — YouTube Media Downloader

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/github/license/RIZONCIO/YMDF)
![Stars](https://img.shields.io/github/stars/RIZONCIO/YMDF?style=social)
![Issues](https://img.shields.io/github/issues/RIZONCIO/YMDF)
![Last Commit](https://img.shields.io/github/last-commit/RIZONCIO/YMDF)
![Repo Size](https://img.shields.io/github/repo-size/RIZONCIO/ymdf)
![Languages](https://img.shields.io/github/languages/top/RIZONCIO/ymdf)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![Version](https://img.shields.io/badge/Version-1.0-orange.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

</div>

### 🚀 Baixe músicas e vídeos do YouTube de forma simples, rápida e inteligente

---

## 📌 Visão Geral

O **YMDF (YouTube Media Downloader Fast)** é uma ferramenta de linha de comando projetada para baixar **áudios (MP3)** e **vídeos (MP4)** com eficiência, automação e segurança.

Ele foi pensado para ser **simples para iniciantes**, mas poderoso o suficiente para usuários avançados.

---

## ✨ Funcionalidades

### 🎯 Principais

- 🎵 Download de áudio em **alta qualidade (até 320kbps)**
- 🎬 Download de vídeo em **HD / 4K**
- 📋 Suporte completo a **playlists**
- ⏱️ Filtro automático de vídeos longos (>10 min)
- ⏳ Delay inteligente para evitar bloqueios
- 💾 Registro de falhas para reprocessamento
- 🖼️ Inclusão de **capa e metadados nos MP3**

### ⚙️ Técnicas

- ✅ Instala dependências automaticamente
- ✅ Verifica FFmpeg sozinho
- ✅ Resolve links encurtados (youtu.be)
- ✅ Suporte a playlists aninhadas
- ✅ Contagem regressiva entre downloads

---

## 📊 Comparação Rápida

| Recurso            | YMDF |
| ------------------ | ---- |
| Interface amigável | ✅    |
| Automação          | ✅    |
| Playlists          | ✅    |
| Anti-bloqueio      | ✅    |
| Alta qualidade     | ✅    |

---

## 📋 Pré-requisitos

### 💻 Sistemas suportados

- Windows 10/11
- macOS Catalina ou superior
- Linux (Ubuntu, Debian, Fedora, Mint)

### 🌐 Internet

- Mínimo: 5 Mbps
- Recomendado: 10+ Mbps

---

## 🐍 Instalação do Python

Baixe o Python:

- Windows: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
- macOS: [https://www.python.org/downloads/macos/](https://www.python.org/downloads/macos/)
- Linux: [https://python.org.br/instalacao-linux/](https://python.org.br/instalacao-linux/)

---

## 🎬 Instalação do FFmpeg

O **FFmpeg** é obrigatório para:

- Converter vídeos em MP3
- Extrair áudio corretamente
- Adicionar capas nos arquivos

### 🪟 Windows (Recomendado)

1. Baixe: [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)
2. Extraia para: `C:\ffmpeg`
3. Adicione ao PATH: `C:\ffmpeg\bin`
4. Teste no terminal:

```bash
ffmpeg -version
```

---

## 📥 Instalação do YMDF

### Método recomendado

```bash
git clone https://github.com/seu-usuario/ymdf.git
cd ymdf
python YMDF.py
```

Ou simplesmente baixe o arquivo `.py`.

---

## 📖 Como Usar

### 🚀 Execução

```bash
python YMDF.py
```

### 🧭 Fluxo do Programa

1. Escolha entrada:

   - URLs diretas
   - Arquivo de links

2. Cole as URLs

3. Escolha formato:

   - mp3
   - mp4

4. (Opcional) Configure qualidade

5. Inicie download

---

## 📂 Usando arquivo de URLs

Crie um arquivo `links.txt`:

```txt
https://youtube.com/watch?v=VIDEO1
https://youtube.com/watch?v=VIDEO2
https://youtube.com/playlist?list=PLAYLIST
```

Depois selecione a opção correspondente no programa.

---

## ⚙️ Configurações Avançadas

Você pode ajustar:

- 🎧 Qualidade do áudio
- 📉 Limite de downloads
- ⏱️ Tempo de delay

---

## 🛠️ Solução de Problemas

### ❌ FFmpeg não encontrado

- Verifique o PATH
- Reinicie o terminal

### ❌ Download falhando

- Confira sua internet
- Tente novamente mais tarde

### ❌ Vídeo não baixa

- Pode estar bloqueado ou privado

---

## ❓ FAQ

### O programa é seguro?

Sim, não coleta dados e roda localmente.

### Posso baixar playlists?

Sim, totalmente suportado.

### Funciona em qualquer sistema?

Sim, Windows, macOS e Linux.

---

## 📄 Licença

Distribuído sob licença MIT.

---

### ⭐ Se curtir o projeto, considere dar uma estrela!

