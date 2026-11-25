/* ARANDU Espaços Vivos — laboratório GNOME 46.
 * Explicit commands only; no global mouse grabs, decoration changes or subprocess.
 */
import Clutter from 'gi://Clutter';
import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
import Meta from 'gi://Meta';
import St from 'gi://St';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import * as PanelMenu from 'resource:///org/gnome/shell/ui/panelMenu.js';
import * as PopupMenu from 'resource:///org/gnome/shell/ui/popupMenu.js';
import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';
import {WindowIntentGate} from './window-intent-gate.mjs';
import {halfArea,resizeArea} from './espacos-math.mjs';
import {edgeAt,handlePosition,resizeFromEdge} from './edge-geometry.mjs';

const UUID='arandu-spaces-lab@arandulab';
const FOUNDATION='arandu-foundation@arandulab';
const call=(w,method)=>typeof w?.[method]==='function' && w[method]()===true;
const plainRect=r=>r && ({x:r.x,y:r.y,width:r.width,height:r.height});
const same=(a,b)=>a&&b&&['x','y','width','height'].every(k=>a[k]===b[k]);

export default class SpacesLab extends Extension {
    enable() {
        this._signals=[];
        this._targetSignals=[];
        this._previewTimeout=0;
        this._pending=null;
        this._edgeEnabled=false;this._edgeTimer=0;this._edgeGrab=null;this._edge=null;
        this._enabled=true;
        this._gate=new WindowIntentGate(()=>this._context());
        this._indicator=new PanelMenu.Button(0,'Espaços Vivos · laboratório',false);
        this._indicator.add_child(this._icon('alca-viva.svg'));
        this._preview=new St.Widget({style_class:'arandu-lab-preview',reactive:false,visible:false});
        Main.layoutManager.addTopChrome(this._preview,{affectsStruts:false,affectsInputRegion:false,trackFullscreen:true});
        this._edgeGlow=new St.Widget({style_class:'arandu-lab-edge-glow',reactive:false,visible:false});
        Main.layoutManager.addTopChrome(this._edgeGlow,{affectsStruts:false,affectsInputRegion:false,trackFullscreen:true});
        this._edgeHandle=new St.Button({style_class:'arandu-lab-edge-handle',reactive:true,can_focus:false,
            visible:false,accessible_name:'Flecha Viva · redimensionar'});
        this._edgeHandle.set_size(24,24);
        Main.layoutManager.addTopChrome(this._edgeHandle,{affectsStruts:false,affectsInputRegion:true,trackFullscreen:true});
        this._edgeHandle.connect('button-press-event',(_actor,event)=>this._edgePress(event));

        this._status=new PopupMenu.PopupMenuItem('Selecione uma janela normal.',{reactive:false,can_focus:false});
        this._indicator.menu.addMenuItem(this._status);
        this._actions={};
        this._action('imersao','Imersão · ampliar',()=>this._request('imersao'),'flecha-azul.svg');
        this._action('recolher','Recolher · minimizar',()=>this._request('recolher'));
        this._action('esquerda','Confluência esquerda',()=>this._request('esquerda'));
        this._action('direita','Confluência direita',()=>this._request('direita'));
        this._indicator.menu.addMenuItem(new PopupMenu.PopupSeparatorMenuItem());
        this._action('edges','Flechas Vivas · ativar nesta sessão',()=>{
            this._cancel();this._edgeEnabled=!this._edgeEnabled;this._sync();
        });
        this._action('resize','Prévia de redimensionamento',()=>this._startResize(),'flecha-amarela.svg');
        for(const [id,label,dx,dy] of [
            ['wplus','Largura + 48 px',48,0],['wminus','Largura − 48 px',-48,0],
            ['hplus','Altura + 48 px',0,48],['hminus','Altura − 48 px',0,-48]]){
            this._action(id,label,()=>this._adjust(dx,dy));
        }
        this._action('apply','Confirmar redimensionamento',()=>this._applyResize());
        this._indicator.menu.addMenuItem(new PopupMenu.PopupSeparatorMenuItem());
        this._action('encerrar','Solicitar encerramento',()=>this._request('encerrar'));
        this._action('confirm','Confirmar encerramento',()=>this._confirmClose());
        this._action('cancel','Cancelar intenção / prévia',()=>{this._cancel();this._sync();});
        // Critical cancellation subscriptions must succeed; otherwise fail closed.
        const events=[
            [global.display,'notify::focus-window',()=>{this._cancel();this._watchTarget();this._sync();}],
            [global.display,'grab-op-begin',()=>{this._cancel();this._sync();}],
            [Main.sessionMode,'updated',()=>{this._cancel();this._sync();}],
            [Main.layoutManager,'monitors-changed',()=>{this._cancel();this._sync();}],
            [Main.overview,'showing',()=>{this._cancel();this._sync();}],
            [Main.overview,'hidden',()=>this._sync()],
            [Main.extensionManager,'extension-state-changed',()=>{this._cancel();this._sync();}]
        ];
        this._safeEvents=events.map(([obj,name,fn])=>this._watch(obj,name,fn)).every(Boolean);
        this._watch(this._indicator.menu,'open-state-changed',(_menu,open)=>{if(open){this._hideEdge();if(this._pending?.kind==='edge')this._cancel();}this._sync();});
        this._watch(global.stage,'captured-event',(_stage,event)=>{
            if(this._pending?.kind==='edge'){
                if(event.type()===Clutter.EventType.MOTION){this._edgeMotion(event);return Clutter.EVENT_STOP;}
                if(event.type()===Clutter.EventType.BUTTON_RELEASE && event.get_button()===1){
                    this._edgeRelease(event);return Clutter.EVENT_STOP;
                }
            }
            if(this._pending && event.type()===Clutter.EventType.KEY_PRESS &&
                event.get_key_symbol()===Clutter.KEY_Escape){this._cancel();this._sync();}
            return Clutter.EVENT_PROPAGATE;
        });
        Main.panel.addToStatusArea(UUID,this._indicator);
        this._watchTarget();this._sync();
    }
    _icon(name) {
        return new St.Icon({gicon:new Gio.FileIcon({file:this.dir.get_child('assets').get_child(name)}),
            style_class:'system-status-icon'});
    }
    _action(id,label,fn,icon=null) {
        const item=new PopupMenu.PopupMenuItem(label);
        if(icon)item.add_child(this._icon(icon));
        item.connect('activate',()=>{try{fn();}catch(_){this._cancel();this._sync();Main.notify('ARANDU','Operação recusada ou indisponível.');}});
        this._indicator.menu.addMenuItem(item);this._actions[id]=item;
    }
    _watch(obj,signal,fn,bag=this._signals) {
        try{bag.push([obj,obj.connect(signal,fn)]);return true;}catch(_){return false;}
    }
    _disconnect(bag){for(const [obj,id] of bag){try{obj.disconnect(id);}catch(_){}}bag.length=0;}
    _watchTarget(){
        this._disconnect(this._targetSignals);
        const w=global.display.focus_window;
        if(w)for(const signal of ['unmanaged','position-changed','size-changed','notify::minimized','notify::fullscreen'])
            this._watch(w,signal,()=>{this._cancel();this._sync();},this._targetSignals);
    }
    _context() {
        const foundation=Main.extensionManager.lookup(FOUNDATION);
        const w=global.display.focus_window;
        // ExtensionState.ENABLED is 1 in GNOME 46. Do not compete with Foundation.
        const sessionOK=this._enabled && this._safeEvents===true && foundation?.state!==1 && !Main.sessionMode.isLocked &&
            !Main.sessionMode.isGreeter && !Main.overview.visible;
        const normal=!!(sessionOK && w && w.get_window_type()===Meta.WindowType.NORMAL &&
            !w.skip_taskbar && !w.minimized && !w.is_fullscreen() && !w.get_transient_for());
        if(!normal)return {allowed:false,focus:null,capabilities:{}};
        const work=plainRect(w.get_work_area_current_monitor());
        const frame=plainRect(w.get_frame_rect());
        const free=call(w,'allows_move')&&call(w,'allows_resize')&&!w.get_maximized();
        return {allowed:true,focus:w,work,frame,capabilities:{
            imersao:call(w,'can_maximize'),recolher:call(w,'can_minimize'),
            esquerda:free,direita:free,resize:free,encerrar:call(w,'can_close')}};
    }
    _sync(){
        if(!this._indicator)return;
        let c;try{c=this._context();}catch(_){c={allowed:false,capabilities:{}};}
        const p=this._pending;
        const targetName=p?.kind==='close'?(p.target.get_title?.()||'Janela ativa').replace(/[\r\n\t]/g,' ').slice(0,60):'';
        this._status.label.text=p?.kind==='close'?'Encerrar: '+targetName+'? (20 s)':
            p?.kind==='resize'?'Prévia ativa · ajuste ou confirme (20 s)':
            c.allowed?'Janela ativa · escolha uma ação':'Indisponível: sessão, janela ou Foundation ativa';
        for(const name of ['imersao','recolher','esquerda','direita','resize','encerrar'])
            this._actions[name].setSensitive(!p&&c.capabilities[name]===true);
        for(const name of ['wplus','wminus','hplus','hminus','apply'])
            this._actions[name].setSensitive(p?.kind==='resize');
        this._actions.confirm.setSensitive(p?.kind==='close');
        this._actions.cancel.setSensitive(!!p);
        this._actions.edges.label.text='Flechas Vivas · '+(this._edgeEnabled?'desativar':'ativar')+' nesta sessão';
        this._syncEdgeTimer(c);
    }
    _cancel(){
        if(this._edgeGrab){const grab=this._edgeGrab;this._edgeGrab=null;try{grab.dismiss();}catch(_){}}
        this._hideEdge();
        this._gate?.cancel();this._pending=null;
        if(this._previewTimeout){GLib.Source.remove(this._previewTimeout);this._previewTimeout=0;}
        this._preview?.hide();
    }
    _hideEdge(){
        this._edge=null;this._edgeHandle?.hide();this._edgeGlow?.hide();
    }
    _syncEdgeTimer(c){
        const ready=this._edgeEnabled&&c?.capabilities?.resize===true&&
            !this._indicator?.menu?.isOpen;
        if(!ready){
            if(this._edgeTimer){GLib.Source.remove(this._edgeTimer);this._edgeTimer=0;}
            this._hideEdge();return;
        }
        if(!this._edgeTimer)this._edgeTimer=GLib.timeout_add(GLib.PRIORITY_DEFAULT,90,()=>{
            try{this._sampleEdge();}catch(_){this._cancel();}
            return GLib.SOURCE_CONTINUE;
        });
    }
    _sampleEdge(){
        if(this._pending?.kind==='edge')return;
        const c=this._context();
        if(!this._edgeEnabled||!c.capabilities.resize||this._pending||this._indicator.menu.isOpen){
            this._hideEdge();return;
        }
        if(!resizeFromEdge(c.frame,c.work,'se',0,0)){this._hideEdge();return;}
        const [x,y,mods]=global.get_pointer();
        const pressed=Clutter.ModifierType.BUTTON1_MASK|Clutter.ModifierType.BUTTON2_MASK|Clutter.ModifierType.BUTTON3_MASK;
        if(mods&pressed){this._hideEdge();return;}
        // Do not move a revealed button underneath the pointer.
        const old=this._edge;
        if(old&&old.target===c.focus&&same(old.frame,c.frame)&&
            x>=old.pos.x-3&&x<=old.pos.x+27&&y>=old.pos.y-3&&y<=old.pos.y+27)return;
        const direction=edgeAt(c.frame,x,y);
        if(!direction){this._hideEdge();return;}
        const pos=handlePosition(c.frame,direction,x,y);
        if(!pos){this._hideEdge();return;}
        if(!old||old.direction!==direction||!this._edgeHandle.get_child()){
            const icon=this._icon('arco-'+direction+'.svg');icon.set_icon_size(18);this._edgeHandle.set_child(icon);
        }
        this._edge={direction,pos,target:c.focus,frame:c.frame};
        this._edgeHandle.set_position(pos.x,pos.y);this._edgeHandle.show();
        this._edgeGlow.set_position(c.frame.x,c.frame.y);
        this._edgeGlow.set_size(c.frame.width,c.frame.height);this._edgeGlow.show();
    }
    _edgePress(event){
        if(event.get_button()!==1||!this._edge||!this._edgeEnabled)return Clutter.EVENT_PROPAGATE;
        const e=this._edge,c=this._context();
        if(c.focus!==e.target||!same(c.frame,e.frame)||!c.capabilities.resize||
            !this._gate.begin(c.focus,'resize',{explicit:true}))return Clutter.EVENT_PROPAGATE;
        const [x,y]=event.get_coords();
        try{
            this._edgeGrab=global.stage.grab(this._edgeHandle);
            if(!this._edgeGrab||(this._edgeGrab.get_seat_state()&Clutter.GrabState.POINTER)===0)throw Error('grab');
            this._pending={kind:'edge',target:c.focus,frame:c.frame,work:c.work,direction:e.direction,x,y,moved:false};
            this._edgeGlow.hide();this._expire();this._sync();
        }catch(_){this._cancel();this._sync();}
        return Clutter.EVENT_STOP;
    }
    _edgeMotion(event){
        const p=this._pending;if(p?.kind!=='edge')return false;
        try{
            const c=this._context(),[x,y]=event.get_coords();
            if(c.focus!==p.target||!same(c.frame,p.frame)||!same(c.work,p.work))throw Error('context');
            if(Math.hypot(x-p.x,y-p.y)<4&&!p.moved)return true;
            const shape=resizeFromEdge(p.frame,p.work,p.direction,x-p.x,y-p.y);
            if(!shape||!this._gate.preview(shape))throw Error('preview');
            p.moved=true;this._preview.set_position(shape.x,shape.y);
            this._preview.set_size(shape.width,shape.height);this._preview.show();
            return true;
        }catch(_){this._cancel();this._sync();return false;}
    }
    _edgeRelease(event){
        const p=this._pending;
        if(p?.kind!=='edge')return;
        if(!this._edgeMotion(event)||!p.moved){this._cancel();this._sync();return;}
        const result=this._gate.release({explicit:true});
        this._cancel();try{this._execute(result);}finally{this._sync();}
    }
    _expire(){
        if(this._previewTimeout)GLib.Source.remove(this._previewTimeout);
        this._previewTimeout=GLib.timeout_add(GLib.PRIORITY_DEFAULT,20000,()=>{
            this._previewTimeout=0;this._cancel();this._sync();return GLib.SOURCE_REMOVE;
        });
    }
    _request(intent){
        this._cancel();
        const c=this._context();
        if(!this._gate.begin(c.focus,intent,{explicit:true})){this._sync();return;}
        const result=this._gate.release({explicit:true});
        if(result?.kind==='confirmation-required'){
            this._pending={kind:'close',target:c.focus,frame:c.frame};this._expire();this._sync();
            return;
        }
        this._execute(result);this._sync();
    }
    _confirmClose(){
        const p=this._pending;
        if(p?.kind!=='close')return;
        const result=this._gate.confirmClose(p.target,{explicit:true});
        this._cancel();this._execute(result);this._sync();
    }
    _startResize(){
        this._cancel();
        const c=this._context();
        if(!this._gate.begin(c.focus,'resize',{explicit:true})){this._sync();return;}
        this._pending={kind:'resize',target:c.focus,frame:c.frame,work:c.work,dx:48,dy:48};
        this._updatePreview();
    }
    _adjust(dx,dy){
        const p=this._pending;if(p?.kind!=='resize')return;
        p.dx=Math.max(-p.frame.width,Math.min(p.work.width,p.dx+dx));
        p.dy=Math.max(-p.frame.height,Math.min(p.work.height,p.dy+dy));
        this._updatePreview();
    }
    _updatePreview(){
        const p=this._pending;if(p?.kind!=='resize')return;
        const c=this._context();
        if(c.focus!==p.target || !same(c.frame,p.frame) || !same(c.work,p.work)){
            this._cancel();this._sync();return;
        }
        const shape=resizeArea(p.frame,p.work,p.dx,p.dy);
        if(!shape || !this._gate.preview(shape)){this._cancel();this._sync();return;}
        this._preview.set_position(shape.x,shape.y);this._preview.set_size(shape.width,shape.height);
        this._preview.show();this._expire();this._sync();
    }
    _applyResize(){
        const p=this._pending;if(p?.kind!=='resize')return;
        const c=this._context();
        if(c.focus!==p.target || !same(c.frame,p.frame) || !same(c.work,p.work)){this._cancel();this._sync();return;}
        const result=this._gate.release({explicit:true});this._cancel();this._execute(result);this._sync();
    }
    _execute(result){
        if(result?.kind!=='action')return false;
        const c=this._context(),w=result.target,intent=result.intent;
        if(c.focus!==w||c.capabilities[intent]!==true)return false;
        switch(intent){
        case 'imersao':w.maximize(Meta.MaximizeFlags.BOTH);break;
        case 'recolher':w.minimize();break;
        case 'encerrar':w.delete(global.get_current_time());break;
        case 'esquerda':case 'direita':{
            const r=halfArea(c.work,intent);if(!r)return false;
            w.move_resize_frame(true,r.x,r.y,r.width,r.height);break;
        }
        case 'resize':{
            const r=result.shape;if(!r)return false;
            w.move_resize_frame(true,r.x,r.y,r.width,r.height);break;
        }
        default:return false;
        }
        return true;
    }
    disable(){
        this._enabled=false;this._edgeEnabled=false;this._cancel();
        if(this._edgeTimer){GLib.Source.remove(this._edgeTimer);this._edgeTimer=0;}
        for(const actor of [this._edgeHandle,this._edgeGlow])if(actor){Main.layoutManager.removeChrome(actor);actor.destroy();}
        this._edgeHandle=null;this._edgeGlow=null;
        this._disconnect(this._targetSignals||[]);
        this._disconnect(this._signals||[]);
        if(this._preview){Main.layoutManager.removeChrome(this._preview);this._preview.destroy();}
        this._indicator?.destroy();
        this._indicator=null;this._preview=null;this._gate=null;this._actions={};
    }
}
