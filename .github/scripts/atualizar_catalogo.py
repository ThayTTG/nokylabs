#!/usr/bin/env python3
"""
Robô do catálogo da NokyLabs.

Para cada app do catalogo.json (e para o próprio launcher), olha o último
lançamento no GitHub e, se houver versão nova, atualiza sozinho:

  • "version"            → número da tag (v1.2.0 → 1.2.0)
  • "url"                → link FIXO daquela versão (…/releases/download/v1.2.0/arquivo.zip)
  • "sha256"             → impressão digital do pacote
  • "published"          → true

Antes de aceitar uma versão nova, ele baixa o .zip e confere se o executável
indicado em "executable" está mesmo lá dentro. Se não estiver, a atualização
daquele app é recusada (o catálogo continua na versão anterior, que funciona)
e o workflow termina com erro, para aparecer em vermelho na aba Actions.

Só usa a biblioteca padrão do Python. Uso:
    python atualizar_catalogo.py catalogo.json            (atualiza o arquivo)
    python atualizar_catalogo.py catalogo.json --conferir (só valida, não grava)
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile

API = "https://api.github.com"
LINK = re.compile(
    r"^https://github\.com/(?P<dono>[^/]+)/(?P<repo>[^/]+)/releases/"
    r"(?:latest/download|download/(?P<tag>[^/]+))/(?P<arquivo>[^/?#]+)$"
)

problemas: list[str] = []


def aviso(msg: str) -> None:
    print(f"::warning::{msg}")


def erro(msg: str) -> None:
    print(f"::error::{msg}")
    problemas.append(msg)


# ---------------------------------------------------------------- leitura

def sem_comentarios(texto: str) -> str:
    """Remove comentários // e /* */ fora de strings (o launcher aceita JSON com comentários)."""
    saida, i, dentro, n = [], 0, False, len(texto)
    while i < n:
        c = texto[i]
        if dentro:
            saida.append(c)
            if c == "\\":
                saida.append(texto[i + 1]); i += 2; continue
            if c == '"':
                dentro = False
        elif c == '"':
            dentro = True; saida.append(c)
        elif texto.startswith("//", i):
            while i < n and texto[i] != "\n":
                i += 1
            continue
        elif texto.startswith("/*", i):
            fim = texto.find("*/", i + 2)
            i = n if fim < 0 else fim + 2
            continue
        else:
            saida.append(c)
        i += 1
    # vírgulas sobrando antes de } ou ] também são aceitas pelo launcher
    return re.sub(r",(\s*[}\]])", r"\1", "".join(saida))


def carregar(caminho: str) -> dict:
    with open(caminho, encoding="utf-8") as f:
        return json.loads(sem_comentarios(f.read()))


# ---------------------------------------------------------------- GitHub

def pedir(url: str):
    cab = {"User-Agent": "NokyLabs-Robo-Catalogo", "Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith(API):
        cab["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=cab)
    return urllib.request.urlopen(req, timeout=300)


def ultimo_release(dono: str, repo: str) -> dict | None:
    try:
        with pedir(f"{API}/repos/{dono}/{repo}/releases/latest") as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None  # repositório ainda sem lançamento (ou ainda não existe)
        aviso(f"{dono}/{repo}: o GitHub respondeu {e.code}. Tento de novo na próxima rodada.")
        return None
    except (urllib.error.URLError, TimeoutError) as e:
        aviso(f"{dono}/{repo}: sem resposta do GitHub ({e}). Tento de novo na próxima rodada.")
        return None


def baixar(url: str, destino: str) -> str:
    """Baixa para o disco e devolve o SHA-256 em maiúsculas."""
    h = hashlib.sha256()
    with pedir(url) as r, open(destino, "wb") as f:
        while bloco := r.read(1 << 20):
            h.update(bloco)
            f.write(bloco)
    return h.hexdigest().upper()


def executavel_no_zip(caminho: str, executavel: str) -> bool:
    """O launcher aceita o executável na raiz do .zip ou dentro de uma única pasta."""
    with zipfile.ZipFile(caminho) as z:
        nomes = [n.replace("\\", "/") for n in z.namelist()]
    alvo = executavel.replace("\\", "/").lower()
    raiz = {n.split("/", 1)[0] for n in nomes if n.strip("/")}
    for n in nomes:
        n = n.lower()
        if n == alvo:
            return True
        if len(raiz) == 1 and "/" in n and n.split("/", 1)[1] == alvo:
            return True
    return False


NOVIDADES = re.compile(r"<!--\s*novidades\s*-->(.*?)<!--\s*/novidades\s*-->", re.DOTALL | re.IGNORECASE)


def extrair_notas(corpo: str | None) -> str:
    """As notas ficam entre <!-- novidades --> e <!-- /novidades --> no texto do lançamento."""
    m = NOVIDADES.search(corpo or "")
    if not m:
        return ""
    notas = m.group(1).strip()
    return "" if notas == "Melhorias e correções." else notas[:1500]


# ---------------------------------------------------------------- versões

def partes(v: str) -> tuple[int, ...]:
    nums = re.findall(r"\d+", v.split("-")[0])
    return tuple(int(x) for x in nums) + (0,) * (4 - len(nums))


# ---------------------------------------------------------------- trabalho

def atualizar_item(nome: str, item: dict) -> bool:
    """Atualiza um app (ou o launcher). Devolve True se algo mudou."""
    downloads = item.get("downloads") or {}
    plataformas = [(k, d) for k, d in downloads.items() if isinstance(d, dict) and d.get("url")]
    if not plataformas:
        return False

    repos = {}
    for chave, d in plataformas:
        m = LINK.match(d["url"])
        if not m:
            aviso(f"{nome}/{chave}: o link não é de um Release do GitHub, então o robô não mexe nele.")
            continue
        repos.setdefault((m["dono"], m["repo"]), []).append((chave, d, m["arquivo"]))

    mudou = False
    for (dono, repo), itens in repos.items():
        rel = ultimo_release(dono, repo)
        if rel is None:
            print(f"· {nome}: {dono}/{repo} ainda não tem lançamento. Nada a fazer.")
            continue

        tag = rel["tag_name"]
        versao = tag.lstrip("vV")
        atual = str(item.get("version", "0.0.0"))
        if partes(versao) < partes(atual):
            aviso(f"{nome}: o último lançamento ({tag}) é mais antigo que o catálogo ({atual}). Mantido como está.")
            continue

        anexos = {a["name"]: a for a in rel.get("assets", [])}
        notas = extrair_notas(rel.get("body"))
        novos = {}
        ajustes = False
        for chave, d, arquivo in itens:
            anexo = anexos.get(arquivo)
            if anexo is None:
                erro(f"{nome}/{chave}: o lançamento {tag} não tem o arquivo {arquivo}.")
                continue

            url = f"https://github.com/{dono}/{repo}/releases/download/{tag}/{arquivo}"
            digest = (anexo.get("digest") or "").removeprefix("sha256:").upper()
            ja_igual = (
                d.get("url") == url and d.get("published") is True
                and digest and str(d.get("sha256", "")).upper() == digest
            )
            if ja_igual:
                # Mesmo pacote: só completa o tamanho, se faltar.
                if anexo.get("size") and d.get("size") != anexo["size"]:
                    d["size"] = anexo["size"]
                    ajustes = True
                continue

            # Versão nova (ou dados incompletos): baixa e confere de verdade.
            with tempfile.TemporaryDirectory() as tmp:
                local = os.path.join(tmp, arquivo)
                print(f"· {nome}/{chave}: baixando {arquivo} ({tag}) para conferir…")
                sha = baixar(anexo["browser_download_url"], local)
                if digest and digest != sha:
                    erro(f"{nome}/{chave}: o SHA-256 baixado não bate com o informado pelo GitHub.")
                    continue
                exe = d.get("executable", "")
                if arquivo.lower().endswith(".zip") and exe and not executavel_no_zip(local, exe):
                    erro(f"{nome}/{chave}: o {arquivo} de {tag} não contém o {exe}. "
                         f"Se o executável mudou de nome, corrija o \"executable\" no catálogo.")
                    continue
            novos[chave] = {"url": url, "sha256": sha, "published": True, "size": anexo.get("size")}

        # Notas da mesma versão que chegaram depois (ex.: lançamento editado).
        if versao == atual and notas and item.get("notes") != notas:
            item["notes"] = notas
            ajustes = True

        if not novos:
            if ajustes:
                print(f"✓ {nome}: informações da versão {versao} completadas")
                mudou = True
            continue
        for chave, valores in novos.items():
            downloads[chave].update(valores)
        if versao != atual:
            print(f"✓ {nome}: {atual} → {versao}")
            item["version"] = versao
            # Notas novas vêm do lançamento; sem elas, as antigas saem (eram da versão anterior).
            item["notes"] = notas
        else:
            print(f"✓ {nome}: dados da versão {versao} corrigidos")
        mudou = True
    return mudou


def validar(cat: dict) -> None:
    """Confere a estrutura básica; qualquer problema vira erro no workflow."""
    ids = set()
    itens = [("launcher", cat.get("launcher") or {})] + [(a.get("id", "?"), a) for a in cat.get("apps", [])]
    for nome, item in itens:
        if nome != "launcher":
            if not item.get("id") or not item.get("name"):
                erro(f"Há um app sem \"id\" ou \"name\".")
            if nome in ids:
                erro(f"O id \"{nome}\" aparece duas vezes.")
            ids.add(nome)
        for chave, d in (item.get("downloads") or {}).items():
            if d is None:
                continue
            if d.get("published", True):
                for campo in ("url", "executable", "sha256"):
                    if not str(d.get(campo, "")).strip():
                        erro(f"{nome}/{chave}: está publicado mas falta \"{campo}\".")
                if "/releases/latest/" in str(d.get("url", "")):
                    erro(f"{nome}/{chave}: use o link fixo da versão, não o \"latest\" "
                         f"(senão o SHA-256 deixa de bater no próximo lançamento).")
            if re.search(r"[^0-9A-Fa-f]", str(d.get("sha256", ""))):
                erro(f"{nome}/{chave}: o sha256 tem caracteres inválidos.")


def main() -> int:
    caminho = sys.argv[1] if len(sys.argv) > 1 else "catalogo.json"
    so_conferir = "--conferir" in sys.argv

    try:
        cat = carregar(caminho)
    except (OSError, ValueError) as e:
        erro(f"Não consegui ler o {caminho}: {e}")
        return 1

    mudou = False
    if not so_conferir:
        if cat.get("launcher"):
            mudou |= atualizar_item("launcher", cat["launcher"])
        for app in cat.get("apps", []):
            if app.get("requestAccess"):
                # Uso restrito: o robô nunca publica download desse app.
                print(f"· {app.get('id', '?')}: uso restrito (requestAccess). Nada a fazer.")
                continue
            mudou |= atualizar_item(app.get("id", "?"), app)

    validar(cat)

    if mudou:
        with open(caminho, "w", encoding="utf-8", newline="\n") as f:
            json.dump(cat, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("Catálogo atualizado.")
    elif not so_conferir:
        print("Nada mudou: o catálogo já está em dia.")

    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"mudou={'sim' if mudou else 'nao'}\n")

    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
