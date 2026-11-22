# Engrenagem TOPBAR — configurações da Semente e Rios

A engrenagem da TOPBAR passa a exibir duas páginas: **Identidade visual** e **Semente e Rios**.

A página Semente e Rios lê o mesmo GSettings que a extensão `confluencia@arandulab`; as alterações de escala, contraste, tempo de varredura, recolhimento, monitor e flutuação não são copiadas para um esquema duplicado.

## Configurações adicionadas

- Tamanho dos medalhões: 85%, 100%, 120%.
- Alto contraste.
- Botão de ajuda (?).
- Varredura: 2 s, 3,5 s, 5 s.
- Recolhimento por inatividade: 10 s, 30 s, 60 s, desligado.
- Semente flutuante permanente (opcional, desativada por padrão).
- Monitor: janela ativa, ponteiro/toque, principal, fixo (1 a 3).
- Restaurar somente as preferências dos rios.

Se o esquema da Confluência não estiver instalado, a página informa isso e não altera nada.

## Atualização TOPBAR isolada (VAIO)

Basta atualizar `ARANDU-SUITE/TOPBAR/arandu-topbar@local/prefs.js`; não é necessário reinstalar Confluência nem substituir o código da TOPBAR funcional.

1. `git pull --ff-only`
2. Validar `node --check ARANDU-SUITE/TOPBAR/arandu-topbar@local/prefs.js`.
3. Fazer backup do `prefs.js` instalado.
4. Copiar `prefs.js` novo.
5. Encerrar sessão e entrar novamente, e abrir a engrenagem para verificar.

Não remova extensões históricas. Não use sudo.

**Status:** alteração em código publicada; ainda requer validação visual na instalação real GNOME 46/X11.
