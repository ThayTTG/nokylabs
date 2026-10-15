# NokyLabs · site

Site oficial da NokyLabs: **https://thayttg.github.io/nokylabs/**

Utilitários, apps para a sala de aula e jogos, reunidos num só lugar.

## O que tem aqui

| Arquivo | Para que serve |
|---|---|
| `index.html` | O site inteiro (HTML, CSS e JS num arquivo só, sem framework) |
| `catalogo.json` | Catálogo oficial de apps lido pelo **NokyLabs Launcher** |
| `favicon.svg` | Ícone da aba |
| `404.html` | Página de "não encontrado", que volta para o início |
| `.nojekyll` | Diz ao GitHub Pages para publicar os arquivos como estão |
| `.github/` | O robô do catálogo e a verificação automática do site |
| `docs/identidade-visual.md` | Guia visual comum a todos os apps da NokyLabs |

## Como editar

Tudo o que muda com frequência fica no começo do `<script>` do `index.html`:

- `SITE`: e-mail de contato e usuário do GitHub.
- `APPS`: textos, recursos, passo a passo e dúvidas de cada projeto. Versões e downloads escritos ali
  são só a reserva: o site usa o que estiver no `catalogo.json`.
- `NEWS`: a lista da página Novidades.

### Quando lançar um app

1. No repositório do app, escreva o que mudou no `CHANGELOG.md` (seção `## [Não lançado]`),
   aumente o `<Version>` no `.csproj` e envie para o branch `release`.
   O GitHub compila, publica o lançamento com essas notas e registra a versão no CHANGELOG.
2. Pronto. Em até uma hora o **robô do catálogo** percebe a versão nova e atualiza o `catalogo.json`
   (versão, link, SHA-256, tamanho e novidades). Para não esperar: aba **Actions** › **Robô do catálogo** › **Run workflow**.
3. O site lê o próprio `catalogo.json`: versão, botão de download, tamanho e "Novidades da versão"
   se atualizam sozinhos. No `index.html` só ficam os textos (recursos, passo a passo, dúvidas).

## Robô do catálogo

Fica em `.github/scripts/atualizar_catalogo.py` e roda pelo workflow `robo-catalogo.yml`.
Para cada app, ele olha o último Release do repositório que aparece no link de download e:

- baixa o pacote e confere se o executável indicado em `executable` está lá dentro;
- grava o link **fixo daquela versão** (`.../releases/download/v1.2.0/...`) e o SHA-256;
- marca o download como publicado.

Se algo não bater (por exemplo, o executável mudou de nome), aquele app continua na versão
anterior, que segue funcionando, e o workflow fica vermelho com a explicação.
Quando o executável muda de nome de propósito, troque o `executable` no catálogo e, logo em
seguida, rode o robô (Actions › Robô do catálogo › Run workflow), para o catálogo não ficar
misturando o nome novo com o pacote antigo. Um app cujo
repositório ainda não tem lançamento é simplesmente ignorado até ter.

> Por que link fixo e não `releases/latest`? Porque o SHA-256 é de um arquivo específico. Com o
> "latest", no dia de um lançamento novo o link passaria a entregar o pacote novo com a impressão
> digital antiga, e o launcher recusaria a instalação.

## Formato do catálogo

```jsonc
{
  "schemaVersion": 1,
  "launcher": { "version": "…", "notes": "texto do aviso de atualização", "downloads": { … } },
  "apps": [
    {
      "id": "hotswap",              // único, nunca muda
      "name": "HotSwap",
      "description": "…",
      "version": "1.1.0",           // o robô atualiza
      "accent": "#818CF8",          // cor do card
      "icon": "M7,7 H20 …",         // caminho SVG (viewBox 24×24)
      "downloads": {
        "windows": {
          "url": "https://github.com/ThayTTG/HotSwap/releases/download/v1.1.0/HotSwap-win-x64.zip",
          "executable": "HotSwap.exe",
          "sha256": "…",
          "published": true         // false = "Download em breve"
        },
        "linux": null               // null ou ausente = indisponível nesse sistema
      }
    }
  ]
}
```

- Apps de navegador usam `"web": "link"` e `"webAction": "Jogar"` no lugar dos downloads.
- `"comingSoon": true` mostra o card como "Em breve".
- Para um app novo, basta colocar o link no formato `.../releases/latest/download/arquivo.zip`
  com `"published": false`: no primeiro lançamento o robô troca pelo link fixo e publica.

As páginas usam endereços com `#` (ex.: `#cubebin`), então tudo funciona no GitHub Pages sem configuração extra.
