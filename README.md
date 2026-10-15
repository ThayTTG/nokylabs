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

## Como editar

Tudo o que muda com frequência fica no começo do `<script>` do `index.html`:

- `SITE`: e-mail de contato e usuário do GitHub.
- `APPS`: textos, recursos, passo a passo, dúvidas e downloads de cada projeto.
- `NEWS`: a lista da página Novidades.

### Quando lançar um app

1. Publique o `.zip` num Release do repositório do app.
2. No `index.html`, troque `status: "soon"` por `status: "available"` na plataforma certa do app.
3. No `catalogo.json`, troque `"published": false` por `true` no mesmo app.
4. Faça o commit. O site e o launcher passam a oferecer o download.

As páginas usam endereços com `#` (ex.: `#cubebin`), então tudo funciona no GitHub Pages sem configuração extra.
