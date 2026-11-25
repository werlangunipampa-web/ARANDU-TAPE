/* Eight edge directions, pure logical-pixel geometry. */
export const DIRECTIONS=Object.freeze(['n','ne','e','se','s','sw','w','nw']);
const valid=r=>r&&['x','y','width','height'].every(k=>Number.isSafeInteger(r[k]))&&r.width>0&&r.height>0;
const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
export function edgeAt(frame,x,y,threshold=12){
    if(!valid(frame)||frame.width<80||frame.height<80||![x,y,threshold].every(Number.isFinite)||threshold<=0)return null;
    const l=frame.x,t=frame.y,r=l+frame.width,b=t+frame.height;
    if(x<l-threshold||x>r+threshold||y<t-threshold||y>b+threshold)return null;
    const h=Math.abs(x-l)<=threshold?'w':Math.abs(x-r)<=threshold?'e':'';
    const v=Math.abs(y-t)<=threshold?'n':Math.abs(y-b)<=threshold?'s':'';
    return v+h||null;
}
export function handlePosition(frame,edge,x,y,size=24){
    if(!valid(frame)||!DIRECTIONS.includes(edge)||![x,y,size].every(Number.isFinite)||size<=0||frame.width<size||frame.height<size)return null;
    const l=frame.x,t=frame.y,r=l+frame.width,b=t+frame.height;
    // Put the small control inside the frame. No invisible interactive strips.
    return {x:Math.round(edge.includes('w')?l:edge.includes('e')?r-size:clamp(x-size/2,l+size,r-2*size)),
            y:Math.round(edge.includes('n')?t:edge.includes('s')?b-size:clamp(y-size/2,t+size,b-2*size))};
}
export function resizeFromEdge(frame,work,edge,dx,dy,minW=240,minH=160){
    if(!valid(frame)||!valid(work)||!DIRECTIONS.includes(edge)||
        ![dx,dy,minW,minH].every(Number.isFinite)||minW<=0||minH<=0)return null;
    let l=frame.x,t=frame.y,r=l+frame.width,b=t+frame.height;
    const wl=work.x,wt=work.y,wr=wl+work.width,wb=wt+work.height;
    if(l<wl||t<wt||r>wr||b>wb||frame.width<minW||frame.height<minH)return null;
    dx=Math.round(dx);dy=Math.round(dy);
    if(edge.includes('w'))l=clamp(l+dx,wl,r-minW);
    if(edge.includes('e'))r=clamp(r+dx,l+minW,wr);
    if(edge.includes('n'))t=clamp(t+dy,wt,b-minH);
    if(edge.includes('s'))b=clamp(b+dy,t+minH,wb);
    return {x:l,y:t,width:r-l,height:b-t};
}
