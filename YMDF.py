import subprocess
import sys
import os
import time
import shutil
import json
from urllib.parse import urlparse, parse_qs

VERIFICACAO_REALIZADA = False
FFMPEG_DISPONIVEL = False
DEPENDENCIAS_INSTALADAS = False

def instalar_dependencias():
    global DEPENDENCIAS_INSTALADAS
    
    dependencias = ['yt-dlp', 'rich']
    faltando = []
    
    for dep in dependencias:
        try:
            __import__(dep.replace('-', '_'))
        except ImportError:
            faltando.append(dep)
    
    if faltando:
        print(f"\n📦 Instalando dependências: {', '.join(faltando)}")
        for dep in faltando:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", dep])
                print(f"  ✅ {dep} instalado")
            except subprocess.CalledProcessError:
                print(f"  ❌ Erro ao instalar {dep}")
                print(f"     Instale manualmente: pip install {dep}")
                return False
        DEPENDENCIAS_INSTALADAS = True
        return True
    
    DEPENDENCIAS_INSTALADAS = True
    return True

def verificar_ffmpeg():
    global FFMPEG_DISPONIVEL
    ffmpeg_path = shutil.which('ffmpeg')
    FFMPEG_DISPONIVEL = ffmpeg_path is not None
    return FFMPEG_DISPONIVEL

def verificar_dependencias_silencioso():
    global VERIFICACAO_REALIZADA
    
    if VERIFICACAO_REALIZADA:
        return True
    
    dependencias_ok = instalar_dependencias()
    
    ffmpeg_ok = verificar_ffmpeg()
    
    VERIFICACAO_REALIZADA = True
    
    if not ffmpeg_ok:
        print("\n" + "="*60)
        print("⚠️  FFmpeg não encontrado!")
        print("="*60)
        print("\n📌 O FFmpeg é necessário para:")
        print("   • Converter vídeos para MP3")
        print("   • Extrair áudio corretamente")
        print("   • Incorporar capas nos arquivos")
        
        print("\n📥 Instalação rápida:")
        print("\n🐧 Linux (Ubuntu/Debian):")
        print("   sudo apt update && sudo apt install ffmpeg")
        
        print("\n🍎 MacOS:")
        print("   sudo brew install ffmpeg")
        
        print("\n🪟 Windows:")
        print("   1. Baixe: https://www.gyan.dev/ffmpeg/builds/")
        print("   2. Extraia para C:\\ffmpeg")
        print("   3. Adicione C:\\ffmpeg\\bin ao PATH")
        print("   4. Reinicie o terminal")
        
        print("\n💡 Após instalar, execute o programa novamente!")
        print("="*60 + "\n")
        
        resposta = input("❓ Deseja continuar mesmo sem FFmpeg? (s/n): ").strip().lower()
        if resposta != 's':
            print("❌ Programa cancelado")
            return False
        else:
            print("\n⚠️  Continuando sem FFmpeg - funcionalidades limitadas!")
            print("   • Downloads MP4 funcionarão normalmente")
            print("   • Downloads MP3 podem falhar\n")
            time.sleep(2)
    
    return True

def importar_bibliotecas():
    global Console, Panel, Prompt, Confirm, Table, Progress, SpinnerColumn, TextColumn, BarColumn, Live, Text, rprint
    
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.layout import Layout
    from rich.live import Live
    from rich.text import Text
    from rich import print as rprint
    
    return Console()

console = None

def extrair_urls_playlist(playlist_url):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(f"[cyan]Extraindo URLs da playlist...", total=None)
        
        result = subprocess.run(
            [
                sys.executable, "-m", "yt_dlp",
                "--flat-playlist",
                "--print", "%(webpage_url)s",
                "--print", "%(duration)s",
                "--print", "%(title)s",
                "--no-warnings",
                playlist_url
            ],
            capture_output=True,
            text=True
        )
        
        progress.update(task, completed=True)
    
    if result.returncode != 0:
        console.print(f"[red]❌ Erro ao extrair playlist: {result.stderr}[/red]")
        return []
    
    lines = result.stdout.strip().split('\n')
    urls_com_info = []
    
    for i in range(0, len(lines) - 2, 3):
        url = lines[i].strip()
        duracao_str = lines[i + 1].strip() if i + 1 < len(lines) else "0"
        titulo = lines[i + 2].strip() if i + 2 < len(lines) else "Título desconhecido"
        
        try:
            duracao = float(duracao_str) if duracao_str and duracao_str != 'None' else 0
        except:
            duracao = 0
            
        if url and ('youtube.com' in url or 'youtu.be' in url):
            urls_com_info.append({
                'url': url,
                'duracao': duracao,
                'titulo': titulo
            })
    
    console.print(f"[green]✅ Encontrados {len(urls_com_info)} vídeos na playlist[/green]")
    return urls_com_info

def coletar_todas_urls(fontes):
    todas_urls_com_info = []
    
    for fonte in fontes:
        if 'playlist' in fonte or ('list=' in fonte and 'watch' in fonte):
            urls_playlist = extrair_urls_playlist(fonte)
            todas_urls_com_info.extend(urls_playlist)
        else:
            todas_urls_com_info.append({
                'url': fonte,
                'duracao': None,
                'titulo': None
            })
    
    seen = set()
    urls_unicas = []
    for item in todas_urls_com_info:
        if item['url'] not in seen:
            seen.add(item['url'])
            urls_unicas.append(item)
    
    return urls_unicas

def obter_info_video(url):
    result = subprocess.run(
        [
            sys.executable, "-m", "yt_dlp",
            "--print", "%(title)s",
            "--print", "%(duration)s",
            "--no-warnings",
            "--quiet",
            url
        ],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        lines = result.stdout.strip().split('\n')
        titulo = lines[0] if lines else "Título desconhecido"
        try:
            duracao = float(lines[1]) if len(lines) > 1 and lines[1] else 0
        except:
            duracao = 0
        return titulo, duracao
    
    return "Título desconhecido", 0

def baixar_midia(urls, output_dir="downloads", max_videos=None, qualidade="0", 
                 formato="mp3", delay_segundos=5, max_duracao_minutos=10):
    global FFMPEG_DISPONIVEL
    
    os.makedirs(output_dir, exist_ok=True)
    
    if max_videos and len(urls) > max_videos:
        console.print(f"\n[yellow]⚠️ Limitando a {max_videos} vídeos[/yellow]")
        urls = urls[:max_videos]
    
    total = len(urls)
    ok = 0
    fail = []
    ignorados_duracao = []
    max_duracao_segundos = max_duracao_minutos * 60
    
    if formato == "mp3" and not FFMPEG_DISPONIVEL:
        console.print("\n[red]⚠️ ATENÇÃO: FFmpeg não está instalado![/red]")
        console.print("[red]Downloads MP3 provavelmente falharão![/red]")
        console.print("[dim]Considere instalar o FFmpeg para usar este recurso[/dim]\n")
        time.sleep(2)
    
    for i, item in enumerate(urls, 1):
        url = item['url']
        titulo = item.get('titulo')
        duracao = item.get('duracao')
        
        if titulo is None or duracao is None:
            console.print(f"[yellow]⏳ Obtendo informações do vídeo {i}/{total}...[/yellow]")
            titulo, duracao = obter_info_video(url)
        
        if duracao > 0 and duracao > max_duracao_segundos:
            minutos = duracao / 60
            console.print(f"[red]⏱️ Pulando: {titulo[:50]}... ({minutos:.1f} min > {max_duracao_minutos} min)[/red]")
            ignorados_duracao.append({
                'url': url,
                'titulo': titulo,
                'duracao': duracao,
                'minutos': minutos
            })
            continue
        
        console.print(f"\n[bold cyan][{i}/{total}] Baixando:[/bold cyan] [yellow]{titulo[:60]}[/yellow]")
        
        if duracao > 0:
            minutos = int(duracao // 60)
            segundos = int(duracao % 60)
            duracao_str = f"{minutos}:{segundos:02d}"
        else:
            duracao_str = "desconhecida"
        
        if formato == "mp3":
            cmd = [
                sys.executable, "-m", "yt_dlp",
                "-x",
                "--audio-format", "mp3",
                "--audio-quality", str(qualidade),
                "--embed-thumbnail",
                "--add-metadata",
                "--metadata-from-title", "%(artist)s - %(title)s",
                "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
                "--no-playlist",
                "--progress",
                "--newline",
                url,
            ]
        else:
            cmd = [
                sys.executable, "-m", "yt_dlp",
                "-f", "best[ext=mp4]",
                "--embed-thumbnail",
                "--add-metadata",
                "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
                "--no-playlist",
                "--progress",
                "--newline",
                url,
            ]
        
        info_table = Table(show_header=False, box=None)
        info_table.add_row("📹", f"[cyan]Título:[/cyan] {titulo[:50]}")
        info_table.add_row("⏱️", f"[cyan]Duração:[/cyan] {duracao_str}")
        info_table.add_row("📁", f"[cyan]Destino:[/cyan] {output_dir}")
        console.print(info_table)
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=False)
        download_time = time.time() - start_time
        
        if result.returncode == 0:
            ok += 1
            console.print(f"[green]✅ Download concluído! ({download_time:.1f}s)[/green]")
            
            if i < total:
                console.print(f"[yellow]⏳ Aguardando {delay_segundos}s...[/yellow]")
                for seg in range(delay_segundos, 0, -1):
                    console.print(f"   [dim]{seg}...[/dim]", end="\r")
                    time.sleep(1)
                console.print("   [green]Continuando![/green]    ")
        else:
            fail.append({'url': url, 'titulo': titulo})
            console.print(f"[red]❌ Falha ao baixar: {titulo[:50]}[/red]")
    
    return ok, fail, ignorados_duracao

def salvar_urls_em_arquivo(urls, arquivo="urls_coletadas.txt"):
    with open(arquivo, 'w', encoding='utf-8') as f:
        for item in urls:
            f.write(item['url'] + '\n')
    console.print(f"[green]📝 URLs salvas em: {arquivo}[/green]")

def mostrar_banner():
    banner = Panel.fit(
        "[bold cyan]🎵 YMDF - YouTube Media Downloader Premium 🎬[/bold cyan]\n"
        "[dim]✓ Limite de 10 minutos por vídeo[/dim]\n"
        "[dim]✓ Delay de 5 segundos entre downloads[/dim]",
        border_style="cyan"
    )
    console.print(banner)

def main():
    global console
    
    if not verificar_dependencias_silencioso():
        return
    
    console = importar_bibliotecas()
    
    mostrar_banner()
    
    console.print("\n[bold]📋 Opções de Entrada:[/bold]")
    console.print("   [cyan]1.[/cyan] URLs ou playlists")
    console.print("   [cyan]2.[/cyan] Ler arquivo de URLs")
    console.print("   [cyan]3.[/cyan] Sair")
    
    opcao = Prompt.ask("\n[bold yellow]Escolha[/bold yellow]", choices=["1", "2", "3"])
    
    if opcao == "3":
        console.print("[yellow]👋 Até logo![/yellow]")
        return
    
    urls_fonte = []
    
    if opcao == "1":
        console.print("\n[cyan]Cole as URLs (vazio para terminar):[/cyan]")
        console.print("[dim]Exemplo: https://youtube.com/playlist?list=... ou https://youtu.be/...[/dim]")
        while True:
            url = Prompt.ask("URL", default="")
            if not url:
                break
            urls_fonte.append(url)
            
    elif opcao == "2":
        arquivo = Prompt.ask("[cyan]Arquivo[/cyan]", default="links.txt")
        if os.path.exists(arquivo):
            with open(arquivo, 'r', encoding='utf-8') as f:
                urls_fonte = [linha.strip() for linha in f if linha.strip()]
            console.print(f"[green]✅ {len(urls_fonte)} URLs carregadas[/green]")
        else:
            console.print(f"[red]❌ Arquivo '{arquivo}' não encontrado![/red]")
            return
    
    if not urls_fonte:
        console.print("[red]❌ Nenhuma URL fornecida![/red]")
        return
    
    console.print("\n[cyan]🔍 Processando URLs e playlists...[/cyan]")
    todas_urls = coletar_todas_urls(urls_fonte)
    
    if not todas_urls:
        console.print("[red]❌ Nenhuma URL válida encontrada![/red]")
        return
    
    console.print(f"\n[bold green]✅ {len(todas_urls)} URLs únicas encontradas[/bold green]")
    
    if Confirm.ask("\n[cyan]💾 Salvar lista de URLs em arquivo?[/cyan]", default=False):
        salvar_urls_em_arquivo(todas_urls)
    
    # Configurações
    console.print("\n[bold]⚙️ Configurações de Download[/bold]")
    
    formato = Prompt.ask("[cyan]Formato de saída[/cyan]", choices=["mp3", "mp4"], default="mp3")
    
    if formato == "mp3":
        console.print("\n[bold]🎵 Qualidade do áudio MP3:[/bold]")
        console.print("  [green]0[/green] - Melhor qualidade (320kbps)")
        console.print("  [green]2[/green] - Boa qualidade (192kbps)")
        console.print("  [green]3[/green] - Qualidade média (128kbps)")
        console.print("  [green]9[/green] - Menor qualidade (64kbps)")
        qualidade = Prompt.ask("Escolha (0-9)", default="0")
    else:
        qualidade = "0"
        console.print("[green]🎬 Formato MP4 selecionado (melhor qualidade disponível)[/green]")
    
    max_videos_input = Prompt.ask("[cyan]Limitar número de vídeos[/cyan]", default="")
    max_videos = int(max_videos_input) if max_videos_input else None
    
    output_dir = Prompt.ask("[cyan]Pasta de destino[/cyan]", default=f"downloads_{formato}")
    

    console.print("\n[bold green]📊 Resumo do Download:[/bold green]")
    resumo_table = Table(show_header=False, box=None)
    resumo_table.add_row("🎵 Formato", f"[cyan]{formato.upper()}[/cyan]")
    resumo_table.add_row("📹 Total de vídeos", str(len(todas_urls) if not max_videos else min(len(todas_urls), max_videos)))
    resumo_table.add_row("⏱️ Limite de duração", "[yellow]10 minutos (fixo)[/yellow]")
    resumo_table.add_row("⏰ Delay entre downloads", "[yellow]5 segundos (fixo)[/yellow]")
    resumo_table.add_row("📁 Pasta de destino", output_dir)
    if formato == "mp3":
        resumo_table.add_row("🎚️ Qualidade", qualidade)
    console.print(resumo_table)
    
    if not Confirm.ask("\n[bold green]🚀 Iniciar download agora?[/bold green]"):
        console.print("[yellow]Download cancelado![/yellow]")
        return
    

    console.print("\n[bold cyan]🎬 INICIANDO DOWNLOADS...[/bold cyan]")
    console.print("[dim]⏱️ Vídeos com mais de 10 minutos serão ignorados automaticamente[/dim]")
    console.print("[dim]⏰ Aguardando 5 segundos entre cada download[/dim]\n")
    
    ok, fail, ignorados = baixar_midia(
        todas_urls, output_dir, max_videos, 
        qualidade, formato, 5, 10
    )
    

    console.print("\n[bold cyan]" + "="*60 + "[/bold cyan]")
    
    stats_table = Table(title="📈 Relatório Final", style="bold green")
    stats_table.add_column("Métrica", style="cyan")
    stats_table.add_column("Valor", style="green")
    stats_table.add_row("✅ Downloads bem-sucedidos", str(ok))
    stats_table.add_row("❌ Downloads com falha", str(len(fail)))
    stats_table.add_row("⏭️ Ignorados (>10 minutos)", str(len(ignorados)))
    
    total_processado = len(todas_urls[:max_videos]) if max_videos else len(todas_urls)
    stats_table.add_row("📊 Total processado", f"{ok + len(fail) + len(ignorados)}/{total_processado}")
    
    console.print(stats_table)
    
    if ignorados:
        console.print("\n[bold yellow]⏭️ Vídeos ignorados (excederam 10 minutos):[/bold yellow]")
        for item in ignorados[:5]:
            console.print(f"  • {item['titulo'][:50]}... ({item['minutos']:.1f} minutos)")
        if len(ignorados) > 5:
            console.print(f"  [dim]... e mais {len(ignorados) - 5} vídeos ignorados[/dim]")
    
    if fail:
        console.print(f"\n[bold red]❌ Falhas no download ({len(fail)}):[/bold red]")
        for item in fail[:5]:
            console.print(f"  • {item['titulo'][:50]}...")
        if len(fail) > 5:
            console.print(f"  [dim]... e mais {len(fail) - 5} falhas[/dim]")
        
        if Confirm.ask("\n[cyan]💾 Salvar URLs com falha em arquivo?[/cyan]"):
            with open("urls_falhas.txt", 'w', encoding='utf-8') as f:
                for item in fail:
                    f.write(item['url'] + '\n')
            console.print("[green]✅ URLs com falha salvas em 'urls_falhas.txt'[/green]")
    
    console.print(f"\n[bold green]📁 Arquivos salvos em: {os.path.abspath(output_dir)}[/bold green]")
    console.print("\n[bold cyan]🎉 Download concluído com sucesso! Até a próxima! 🎉[/bold cyan]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        if console:
            console.print("\n\n[yellow]⚠️ Programa interrompido pelo usuário![/yellow]")
        else:
            print("\n\n⚠️ Programa interrompido pelo usuário!")
        sys.exit(0)
    except Exception as e:
        if console:
            console.print(f"\n[red]❌ Erro inesperado: {e}[/red]")
        else:
            print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)