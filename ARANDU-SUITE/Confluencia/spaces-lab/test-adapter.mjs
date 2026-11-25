import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {WindowIntentGate} from '../design-reference/window-intent-gate.mjs';
import {halfArea,resizeArea} from '../design-reference/espacos-math.mjs';

let id=0;
class Actor {
    constructor(opts={}){Object.assign(this,opts);this.signals=new Map();this.children=[];this.visible=opts.visible??true;}
    connect(n,fn){this.signals.set(++id,[n,fn]);return id;}
    disconnect(n){assert(this.signals.delete(n));}
    emit(n,...args){for(const [name,fn] of [...this.signals.values()])if(name===n)fn(this,...args);}
    add_child(a){this.children.push(a);}
    setSensitive(v){this.sensitive=v;}
    show(){this.visible=true;}
    hide(){this.visible=false;}
    set_position(x,y){this.pos=[x,y];}
    set_size(w,h){this.size=[w,h];}
    destroy(){this.destroyed=true;}
}
class Item extends Actor {constructor(text,opts){super(opts);this.label={text};}}
class Button extends Actor {constructor(){super();this.menu=new Actor();this.menu.addMenuItem=i=>this.menu.add_child(i);}}
const timers=new Map(),chrome=new Set(),calls=[];
const work={x:-1200,y:30,width:1200,height:800};
const frame={x:-1000,y:100,width:500,height:400};
const win=Object.assign(new Actor(),{
    get_window_type:()=>1,is_fullscreen:()=>false,get_transient_for:()=>null,
    get_work_area_current_monitor:()=>work,get_frame_rect:()=>frame,get_maximized:()=>0,
    allows_move:()=>true,allows_resize:()=>true,can_maximize:()=>true,can_minimize:()=>true,can_close:()=>true,
    maximize:f=>calls.push(['max',f]),minimize:()=>calls.push(['min']),
    delete:t=>calls.push(['close',t]),move_resize_frame:(...a)=>calls.push(['resize',...a])
});
const display=new Actor({focus_window:win});
const manager=new Actor();let foundation=false;manager.lookup=()=>foundation?{state:1}:null;
const layout=new Actor();layout.addTopChrome=(a,o)=>{assert.equal(o.affectsInputRegion,false);assert.equal(o.affectsStruts,false);chrome.add(a);};
layout.removeChrome=a=>assert(chrome.delete(a));
const main={layoutManager:layout,extensionManager:manager,sessionMode:new Actor({isLocked:false}),
    overview:new Actor({visible:false}),panel:{addToStatusArea(){}},notify(){}};
const stage=new Actor();
const fake={Clutter:{EventType:{KEY_PRESS:1},KEY_Escape:65307,EVENT_PROPAGATE:false},
    Gio:{FileIcon:Actor},St:{Icon:Actor,Widget:Actor},Meta:{WindowType:{NORMAL:1},MaximizeFlags:{BOTH:3}},
    GLib:{PRIORITY_DEFAULT:0,SOURCE_REMOVE:false,Source:{remove:n=>timers.delete(n)},
        timeout_add:(_p,_ms,fn)=>{timers.set(++id,fn);return id;}},
    Main:main,PanelMenu:{Button},PopupMenu:{PopupMenuItem:Item,PopupSeparatorMenuItem:Actor},
    Extension:class{constructor(){this.dir={get_child(){return this;}};}},WindowIntentGate,halfArea,resizeArea,
    global:{display,stage,get_current_time:()=>42}};
const code=fs.readFileSync(new URL('./extension.js',import.meta.url),'utf8')
    .replace(/^import .*;\s*$/gm,'').replace('export default class','class');
const Lab=vm.runInNewContext(code+'\nSpacesLab;',fake);
const lab=new Lab();lab.enable();
assert.equal(chrome.size,1);
assert.equal(lab._actions.imersao.sensitive,true);
assert.equal(lab._actions.confirm.sensitive,false);
lab._request('imersao');assert.deepEqual(calls.pop(),['max',3]);
lab._request('recolher');assert.deepEqual(calls.pop(),['min']);
lab._request('esquerda');assert.deepEqual(calls.pop(),['resize',true,-1200,30,595,800]);
lab._request('encerrar');assert.equal(calls.length,0);
assert.equal(lab._actions.confirm.sensitive,true);
lab._confirmClose();assert.deepEqual(calls.pop(),['close',42]);
lab._confirmClose();assert.equal(calls.length,0);
lab._request('encerrar');display.emit('notify::focus-window');lab._confirmClose();assert.equal(calls.length,0);
lab._startResize();assert.equal(lab._preview.visible,true);
assert.equal(calls.length,0);assert.deepEqual(lab._preview.size,[548,448]);
lab._adjust(48,-48);assert.deepEqual(lab._preview.size,[596,400]);
lab._applyResize();assert.deepEqual(calls.pop(),['resize',true,-1000,100,596,400]);
assert.equal(lab._preview.visible,false);
lab._startResize();win.emit('size-changed');lab._applyResize();assert.equal(calls.length,0);
lab._startResize();stage.emit('captured-event',{type:()=>1,get_key_symbol:()=>65307});assert.equal(lab._preview.visible,false);
lab._startResize();const [timer,fn]=[...timers][0];timers.delete(timer);fn();assert.equal(lab._preview.visible,false);
foundation=true;manager.emit('extension-state-changed');lab._request('encerrar');assert.equal(lab._pending,null);
foundation=false;main.sessionMode.isLocked=true;main.sessionMode.emit('updated');lab._request('imersao');assert.equal(calls.length,0);
main.sessionMode.isLocked=false;main.sessionMode.emit('updated');
lab._startResize();lab.disable();assert.equal(chrome.size,0);assert.equal(timers.size,0);
assert.equal(win.signals.size,0);assert.equal(display.signals.size,0);assert.equal(stage.signals.size,0);
console.log('Espaços Vivos lab: ações, confirmação, prévia, conflitos e desmontagem validados em mocks.');
