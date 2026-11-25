/* Experimental authorization boundary for a future GNOME adapter.
 * No GJS imports, I/O, timers, window mutation or private-core dependency.
 * Caller must cancel on focus/session/monitor/native grab changes.
 */
const actions = new Set(['imersao','recolher','esquerda','direita','encerrar','resize']);
const validRect = r => r && ['x','y','width','height'].every(k=>Number.isSafeInteger(r[k]))
    && r.width>0 && r.height>0;
const inside = (r,w) => validRect(r) && validRect(w) && r.x>=w.x && r.y>=w.y
    && r.x+r.width<=w.x+w.width && r.y+r.height<=w.y+w.height;
const rect = r => Object.freeze({x:r.x,y:r.y,width:r.width,height:r.height});
const sameRect = (a,b) => validRect(a) && validRect(b) && ['x','y','width','height'].every(k=>a[k]===b[k]);

export class WindowIntentGate {
    #pending=null;
    #context;
    constructor(context) {
        if(typeof context!=='function') throw new TypeError('Context required');
        this.#context=context;
    }
    cancel() { this.#pending=null; }
    #read(target,intent) {
        try {
            const c=this.#context();
            return c && target && c.focus===target && c.allowed===true && c.capabilities?.[intent]===true ? c:null;
        } catch (_) {return null;}
    }
    begin(target,intent,{explicit=false}={}) {
        this.cancel();
        if(explicit!==true || !actions.has(intent))return false;
        const c=this.#read(target,intent);
        if(!c)return false;
        if(intent==='resize' && !validRect(c.work))return false;
        this.#pending={target,intent,work:validRect(c.work)?rect(c.work):null,phase:'pressed',preview:null};
        return true;
    }
    preview(shape) {
        const p=this.#pending;
        if(!p || p.intent!=='resize' || p.phase!=='pressed')return false;
        const c=this.#read(p.target,p.intent);
        if(!c || !sameRect(c.work,p.work)){this.cancel();return false;}
        p.preview=inside(shape,p.work)?rect(shape):null;
        return !!p.preview;
    }
    release({explicit=false}={}) {
        const p=this.#pending;
        if(!p || p.phase!=='pressed' || explicit!==true){this.cancel();return null;}
        const c=this.#read(p.target,p.intent);
        if(!c){this.cancel();return null;}
        if(p.intent==='encerrar'){
            p.phase='confirm';
            return Object.freeze({kind:'confirmation-required',target:p.target});
        }
        this.cancel();
        if(p.intent==='resize'){
            if(!sameRect(c.work,p.work) || !inside(p.preview,c.work))return null;
            return Object.freeze({kind:'action',target:p.target,intent:p.intent,shape:p.preview});
        }
        return Object.freeze({kind:'action',target:p.target,intent:p.intent});
    }
    confirmClose(target,{explicit=false}={}) {
        const p=this.#pending;
        this.cancel();
        if(!p || p.phase!=='confirm' || p.intent!=='encerrar' || p.target!==target ||
            explicit!==true || !this.#read(target,'encerrar'))return null;
        return Object.freeze({kind:'action',target,intent:'encerrar'});
    }
}
