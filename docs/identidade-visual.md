# Identidade visual da NokyLabs

Guia único para todos os apps da NokyLabs. Cada app mantém a sua **cor de identidade**; todo o resto segue este guia.

| App | Cor de identidade |
|---|---|
| NokyLabs Launcher | `#8B5CF6` (roxo da marca) |
| HotSwap | `#3B82F6` |
| CubeBin | `#C4362E` |
| YT-DLP GUI | `#8B5CF6` com magenta `#D946EF` |
| Avaliador Acadêmico | `#3D8BE8` |

### Princípio
**Todos os apps da NokyLabs são da mesma família**: mesmo fundo escuro levemente arroxeado, mesmas superfícies, bordas, tipografia, cantos arredondados, botões, espaçamentos e ícones. **O que muda de app para app é só a cor de destaque** (a "cor de identidade"), usada em botões principais, item ativo do menu, links, foco e no ícone do app.

Referência viva: o NokyLabs Launcher (Avalonia) e o YT-DLP GUI 2.0 (WinForms + Guna.UI2), que já seguem este guia. Site: https://thayttg.github.io/nokylabs/

### Cores neutras (iguais em todos os apps)

| Papel | Hex | Uso |
|---|---|---|
| Fundo | `#0F0B1A` | fundo da janela / área de conteúdo |
| Barra lateral | `#140F24` | menu lateral, rodapé, barra de título |
| Superfície | `#1B1530` | cards, painéis, listas |
| Superfície hover | `#231B3E` | card/linha com o mouse por cima |
| Superfície elevada | `#2A2149` | menus suspensos, tooltips, campos em foco |
| Borda | `#2C2347` | bordas de 1 px e divisórias |
| Texto | `#F2EEFF` | títulos e texto principal |
| Texto secundário | `#A99FC7` | descrições, rótulos |
| Texto apagado | `#6E6491` | dicas, rodapés, desabilitado |

Estados (sempre com ícone ou texto junto, nunca só a cor):

| Estado | Hex | "Suave" (fundo) |
|---|---|---|
| Sucesso | `#34D399` | mesma cor com 14% de opacidade |
| Atenção | `#FBBF24` | 14% |
| Perigo | `#F87171` | 14% |

### Cor de identidade (a do app)
A partir da cor do app, derive sempre as mesmas 6 variações (os valores do seu app estão na seção do app, mais abaixo):

| Nome | Regra | Uso |
|---|---|---|
| `Accent` | a cor do app | botão principal, foco, item ativo |
| `AccentHover` | um pouco mais clara | hover do botão principal |
| `AccentPressed` | um pouco mais escura | clique |
| `AccentLight` | bem clara | texto sobre fundo suave, links |
| `AccentSoft` | `Accent` com 16% de opacidade | fundo do item ativo, botão "suave", avisos |
| `AccentSoftHover` | `Accent` com 26% | hover dos itens suaves, borda de card em hover |

### Tipografia
Fonte do sistema: **Segoe UI Variable** (Windows 11), caindo para **Segoe UI**. Tamanhos em pontos de WPF (px lógicos; no WinForms, divida por ~1,33):

| Estilo | Tamanho | Peso | Cor |
|---|---|---|---|
| Título da página | 28 | Bold | Texto |
| Título de seção / card | 16 | SemiBold | Texto |
| Corpo | 14 | Regular | Texto |
| Botão / rótulo | 13 | SemiBold | conforme o botão |
| Secundário | 13 | Regular | Texto secundário |
| Pequeno / dica | 12 | Regular | Texto apagado |

### Formas e espaçamentos
- Cantos: **cards 16**, **botões e campos 10**, avisos 12, item de menu lateral 10, "pílulas"/etiquetas 999 (totalmente redondas), ícone do app 13 (num quadrado de 42).
- Espaçamento em múltiplos de 4: entre cards 16–18, padding de card **20**, de botão **16×9**, de campo **12×9**, de item do menu **12×10**.
- Bordas de 1 px na cor Borda. **Sem sombras pesadas**; profundidade vem das superfícies mais claras.
- Transições de 150 ms em fundo e borda no hover (onde o framework permitir).

### Componentes
- **Janela**: barra de título escura (código abaixo). Fundo `#0F0B1A`.
- **Menu lateral** (apps com várias telas): largura ~248, fundo Barra lateral, linha de 1 px na cor Borda separando do conteúdo. No topo, o **cabeçalho do app**: quadrado 42×42, canto 13, preenchido com um gradiente diagonal da `AccentPressed` para a `AccentLight` e o ícone do app em branco (traço ~2,9); ao lado, o nome do app (18, Bold) e embaixo "NokyLabs" (12, Texto apagado). Itens: ícone + texto (14, Medium, Texto secundário); hover = Superfície hover; ativo = fundo `AccentSoft` e texto/ícone `AccentLight`. No rodapé do menu, um card pequeno com a versão.
- **Cards**: fundo Superfície, borda 1 px, canto 16, padding 20. Hover: Superfície hover + borda `AccentSoftHover`.
- **Botões** (canto 10, padding 16×9, 13 SemiBold, sem borda):
  - *Principal*: fundo `Accent`, texto branco; hover `AccentHover`; clique `AccentPressed`.
  - *Suave*: fundo `AccentSoft`, texto `AccentLight`; hover `AccentSoftHover` com texto Texto.
  - *Contorno (ghost)*: transparente, borda 1 px, texto secundário; hover Superfície hover.
  - *Perigo*: fundo Perigo 14%, texto Perigo; hover fundo Perigo sólido com texto branco. Ações destrutivas sempre pedem confirmação.
  - Desabilitado: opacidade ~45%.
  - Em diálogos, ações à direita, a principal por último.
- **Campos de texto / combos**: fundo Superfície, borda 1 px, canto 10, padding 12×9; hover Superfície hover; foco com borda `Accent`.
- **Avisos**: fundo `AccentSoft` (ou Atenção/Perigo 14%), borda na versão 26%, canto 12, padding 14×10, ícone à esquerda.
- **Listas e tabelas**: sem linhas de grade pesadas; linhas separadas por 1 px Borda; hover Superfície hover; seleção `AccentSoft`. Cabeçalho em 12 SemiBold, Texto apagado, maiúsculas opcionais.
- **Barras de progresso**: altura 6, canto 3, trilho Superfície elevada, preenchimento `Accent`.
- **Rolagem**: barra fina (≈8 px), polegar Superfície elevada, sem setas, trilho transparente.
- **Menus de contexto / da bandeja**: fundo Superfície elevada, borda 1 px, canto 10 quando possível, itens 13 Regular com padding 10×8, hover `AccentSoft`, separadores Borda.
- **Ícones**: estilo traço (como Lucide): grade 24×24, traço 2 px, pontas e junções arredondadas, cor Texto secundário (ou `AccentLight` quando ativo). Nada de emoji na interface.
- **Tooltips**: Superfície elevada, borda 1 px, canto 8, texto 12.

### Tela "Sobre" (igual em todos)
Uma seção ou janela "Sobre" com: o cabeçalho do app (quadrado com gradiente + nome), a **versão lida do próprio assembly** (nunca escrita à mão), a frase "Parte da NokyLabs", e três links: **Site do app** (`https://thayttg.github.io/nokylabs/#<id-do-app>`), **Código no GitHub** e **Reportar um problema** (`https://github.com/ThayTTG/<repo>/issues/new`).

### Textos
Português do Brasil, tom acolhedor e direto, frases curtas, sem jargão técnico para o usuário final (a usuária é professora; os apps são usados por alunos e colegas). Botões com verbos ("Organizar agora", "Salvar perfil").

### Barra de título escura (Windows 10 1809+ e 11)
```csharp
[DllImport("dwmapi.dll")]
static extern int DwmSetWindowAttribute(IntPtr hwnd, int attr, ref int value, int size);

static void AplicarBarraEscura(IntPtr hwnd)
{
    try
    {
        int ligado = 1;
        if (DwmSetWindowAttribute(hwnd, 20, ref ligado, sizeof(int)) != 0)      // modo escuro
            DwmSetWindowAttribute(hwnd, 19, ref ligado, sizeof(int));           // builds antigos do Win10
        int titulo = 0x240F14;  // #140F24 em formato 0x00BBGGRR
        int borda  = 0x47232C;  // #2C2347
        int texto  = 0xFFEEF2;  // #F2EEFF
        DwmSetWindowAttribute(hwnd, 35, ref titulo, sizeof(int));  // só Win11; no 10 é ignorado
        DwmSetWindowAttribute(hwnd, 34, ref borda,  sizeof(int));
        DwmSetWindowAttribute(hwnd, 36, ref texto,  sizeof(int));
    }
    catch { /* sem suporte: fica a barra padrão */ }
}
// WinForms: chamar em OnHandleCreated(Handle).
// WPF: no SourceInitialized, com new WindowInteropHelper(this).Handle.
```
