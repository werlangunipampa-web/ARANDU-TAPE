/* ARANDU A9.7 — intenções puras, independentes de mouse, câmera ou GJS.
 * Coordenadas em pixels lógicos do monitor atual. Sem dados de usuário.
 */
export const MARGEM = 100;
export function normalizeArea(area) {
    if (!area || !['x','y','width','height'].every(k => Number.isFinite(area[k])) ||
        area.width < 360 || area.height < 260)
        return null;
    return {x:area.x,y:area.y,width:area.width,height:area.height};
}
export function classifyDrop(area, x, y) {
    const a=normalizeArea(area);
    if (!a || !Number.isFinite(x) || !Number.isFinite(y)) return null;
    if (x < a.x || x > a.x+a.width || y < a.y || y > a.y+a.height)
        return null;
    const nx=(x-a.x)/a.width;
    const upper=Math.min(MARGEM,a.height*0.18);
    const lower=Math.min(MARGEM,a.height*0.18);
    if (y<=a.y+upper) {
        if (nx<0.28) return 'esquerda';
        if (nx>0.72) return 'direita';
        return 'imersao';
    }
    if (y>=a.y+a.height-lower) {
        if (nx<0.23) return 'encerrar';
        if (nx>=0.28 && nx<=0.72) return 'recolher';
    }
    return null;
}
export function halfArea(area, side) {
    const a=normalizeArea(area);
    if (!a || !['esquerda','direita'].includes(side)) return null;
    const gap=10,half=Math.floor((a.width-gap)/2);
    return {x:a.x+(side==='direita'?half+gap:0),y:a.y,
        width:side==='esquerda'?half:a.width-half-gap,height:a.height};
}
export function resizeArea(frame, work, dx, dy, minW=240, minH=160) {
    const a=normalizeArea(work);
    if (!a || !frame || ![frame.x,frame.y,frame.width,frame.height,dx,dy].every(Number.isFinite))
        return null;
    const availableW=Math.floor(a.x+a.width-frame.x);
    const availableH=Math.floor(a.y+a.height-frame.y);
    if (availableW<minW || availableH<minH) return null;
    return {x:frame.x,y:frame.y,
        width:Math.min(availableW,Math.max(minW,Math.round(frame.width+dx))),
        height:Math.min(availableH,Math.max(minH,Math.round(frame.height+dy)))};
}
export function safeMove(frame,work,dx,dy) {
    const a=normalizeArea(work);
    if(!a||!frame||![frame.x,frame.y,frame.width,frame.height,dx,dy].every(Number.isFinite))
        return null;
    return {x:Math.max(a.x-frame.width+88,Math.min(a.x+a.width-88,Math.round(frame.x+dx))),
        y:Math.max(a.y,Math.min(a.y+a.height-36,Math.round(frame.y+dy)))};
}
