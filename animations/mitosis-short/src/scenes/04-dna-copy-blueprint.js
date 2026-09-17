// STUB
// Placeholder for shot 04 'dna-copy-blueprint' (schematic). The scene agent replaces this whole file.
FILM.scene({
  id: 'dna-copy-blueprint',
  draw(ctx, t, info) {
    const L = info.lib, P = L.pal;
    const p = L.clamp(t / info.dur);
    L.blueprint(ctx);
    L.guideCircle(ctx, 540, 860, 340, { alpha: 0.4 });
    L.glowDot(ctx, 540, 860, 10 + 8 * p, { rays: 12, rot: p * Math.PI });
    L.text(ctx, 'STUB 04', 540, 330, { size: 60, weight: 600, align: 'center', color: P.magenta });
    L.text(ctx, info.shot.title || 'dna-copy-blueprint', 540, 1420, { size: 44, align: 'center', color: P.lavender });
    L.text(ctx, 'dna-copy-blueprint', 540, 1480, { size: 30, align: 'center', color: P.lavender, alpha: 0.6 });
    ctx.fillStyle = P.lineWhite;
    ctx.fillRect(140, 1526, 800 * p, 6);
  },
});
