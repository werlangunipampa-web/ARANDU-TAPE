// Ensaio da lógica compartilhada. Usa objetos de teste em lugar de uma sessão GNOME.
const assert = require('assert').strict;
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const base = path.resolve(__dirname, '..');
const template = fs.readFileSync(path.join(base, 'shell/implementation.js.in'), 'utf8');
const geom = fs.readFileSync(path.join(base, 'app/assets/geometria.json'), 'utf8');
const dynamic = fs.readFileSync(path.join(base, 'shell/rios-dinamicos.json'), 'utf8');
const code = template.replace('__LAYOUT__', geom).replace('__DYNAMIC_RIVERS__',dynamic);
let next = 1;
const pending = new Map();
class Actor {
    constructor(options={}) {
        Object.assign(this,options);
        this.children=[]; this.handlers=new Map(); this.visible=options.visible ?? true;
    }
    connect(name,fn) {const id=next++;this.handlers.set(id,[name,fn]);return id;}
    disconnect(id) {assert(this.handlers.delete(id));}
    emit(name,...args) {for(const [n,f] of this.handlers.values())if(n===name)f(this,...args);}
    add_child(child) {this.children.push(child);child.parent=this;}
    get_parent(){return this.parent;}
    remove_child(child) {this.children=this.children.filter(x=>x!==child);child.parent=null;}
    set_child(child) {this.add_child(child);}
    set_size(w,h) {this.size=[w,h];}
    set_width(w) {this.width=w;}
    set_height(h) {this.height=h;}
    contains(other) {while(other){if(other===this)return true;other=other.parent;}return false;}
    set_position(x,y) {this.pos=[x,y];}
    set_scale(x,y) {this.scale=[x,y];}
    set_style(s){this.style=s;}
    set_label(v){this.label=v;}
    add_style_class_name(s){this.classes??=new Set();this.classes.add(s);}
    remove_style_class_name(s){this.classes?.delete(s);}
    grab_key_focus(){this.focused=true;}
    set_pivot_point() {}
    hide(){this.visible=false;} show(){this.visible=true;}
    destroy() {if(this.parent)this.parent.remove_child(this);this.destroyed=true;}
}
class Panel extends Actor {
    constructor(){super();this.menu={addAction:(s,f)=>({label:{set_text(){}},click:f})};}
}
const prefs=new Map([['recent','[]'],['frequency','{}'],['medallion-scale',1],['high-contrast',false],['scan-interval-ms',3500],['panel-mode','visible'],['monitor-target','focused'],['fixed-monitor-index',0],['navigation-idle-ms',10000]]);
const settings={get_string:k=>prefs.get(k),set_string:(k,v)=>prefs.set(k,v),
    get_double:k=>prefs.get(k)||0,set_double:(k,v)=>prefs.set(k,v),
    get_boolean:k=>!!prefs.get(k),set_boolean:(k,v)=>prefs.set(k,v),
    get_int:k=>prefs.get(k)??3500,set_int:(k,v)=>prefs.set(k,v),
    get_strv:k=>prefs.get(k)??['<Super><Alt>space'],set_strv:(k,v)=>prefs.set(k,v)};
let privacy=true;
class Privacy extends Actor {get_boolean(){return privacy;}}
let service=false, key=false, actions=[], windowList=[], focused=null;
const tracked=new Set();const bg=new Actor();const chrome=new Actor();
const layout=Object.assign(new Actor(),{
    _backgroundGroup:bg,primaryMonitor:{index:0,x:0,y:0,width:1366,height:768},
    monitors:[{index:0,x:0,y:0,width:1366,height:768},{index:1,x:1366,y:0,width:1080,height:900},{index:2,x:2446,y:0,width:1200,height:900}],
    getWorkAreaForMonitor:i=>({x:layout.monitors[i].x,y:30,width:layout.monitors[i].width,height:layout.monitors[i].height-30}),
    addChrome(actor){chrome.add_child(actor);},removeChrome(actor){chrome.remove_child(actor);},
    trackChrome(actor){tracked.add(actor);},untrackChrome(actor){assert(tracked.delete(actor));}
});
const overview=new Actor();overview.visible=false;
let pointer=[10,1], hideConflict=false;
const stage=new Actor();stage.set_key_focus=actor=>stage.keyFocus=actor;stage.get_key_focus=()=>stage.keyFocus;
const panelActor=Object.assign(new Actor(),{addToStatusArea(){}});
const main={layoutManager:layout,overview,sessionMode:{isLocked:false},panel:panelActor,extensionManager:{lookup:()=>hideConflict?{state:1}:null},
    wm:{addKeybinding(){key=true;},removeKeybinding(){key=false;}},
    activateWindow(w){focused=w;},notify(){}};
const apps=new Map();
function win(id,title,appId,space=0) {
    if (!apps.has(appId))apps.set(appId,{get_id:()=>appId,get_name:()=>appId,create_icon_texture:()=>new Actor(),activate:()=>actions.push(appId)});
    return {get_title:()=>title,get_stable_sequence:()=>id,get_window_type:()=>0,
        get_wm_class:()=>appId,get_workspace:()=>({index:()=>space}),get_monitor:()=>space,app:apps.get(appId)};
}
const display=Object.assign(new Actor(),{get_tab_list:()=>windowList});
Object.defineProperty(display,'focus_window',{get:()=>focused});
const fake={
    Main:main,PanelMenu:{Button:Panel},Clutter:{FixedLayout:class{},EventType:{MOTION:1,BUTTON_RELEASE:2,KEY_PRESS:3,BUTTON_PRESS:4,TOUCH_BEGIN:5},KEY_Return:13,KEY_KP_Enter:65421,KEY_space:32,KEY_Right:65363,KEY_Left:65361,KEY_Escape:65307,EVENT_PROPAGATE:false,EVENT_STOP:true},
    GLib:{get_user_cache_dir:()=>'/tmp',mkdir_with_parents:()=>0,file_test:()=>false,FileTest:{EXISTS:1},file_set_contents:()=>{},get_monotonic_time:()=>0,Source:{remove:id=>pending.delete(id)},build_filenamev:xs=>xs.join('/'),
        timeout_add:(_priority,_ms,fn)=>{const id=next++;pending.set(id,fn);return id;},SOURCE_REMOVE:false,SOURCE_CONTINUE:true},
    Gio:{DBus:{session:{}},Settings:Privacy,DBusExportedObject:{wrapJSObject:()=>({export(){service=true;},unexport(){service=false;}})},
        File:{new_for_path:v=>({get_uri:()=>'file://'+v})},FileIcon:class{},
        DesktopAppInfo:{new:()=>({launch(){actions.push('map');},launch_action(r){actions.push(r);}})}},
    Meta:{WindowType:{NORMAL:0,DIALOG:3,MODAL_DIALOG:4},TabList:{NORMAL_ALL:1},KeyBindingFlags:{NONE:0}},
    Shell:{WindowTracker:{get_default:()=>({get_window_app:w=>w.app})},AppSystem:{get_default:()=>({lookup_app:k=>apps.get(k)})},ActionMode:{NORMAL:1,OVERVIEW:2}},
    St:{Widget:Actor,Icon:Actor,Button:Actor,BoxLayout:Actor,Label:Actor,ScrollView:Actor,PolicyType:{NEVER:0,AUTOMATIC:1}},global:{get_pointer:()=>pointer,display,window_manager:new Actor(),stage,
        create_app_launch_context:()=>({}),get_current_time:()=>2}
};
const Session=vm.runInNewContext(code+'\nTapeSession;',fake);
const a=win(12,'Caderno','editor.desktop');const b=win(32,'Nascentes','editor.desktop',1);
const c=win(45,'Pasta Campo','files.desktop');const own=win(67,'Arandu Tape','org.arandulab.Tape.desktop');
windowList=[a,b,c,own];focused=a;
const s=new Session('/teste',settings);s.start();
assert(service && key);assert.equal(s.root.get_parent(),bg);
assert(s.helpButton && s.helpBox);
assert(s.controlScroll && s.controlBox);
assert.equal(s.controlScroll.visible,false);
s.toggleAccessibility();assert.equal(s.controlScroll.visible,true);
s.toggleAccessibility();assert.equal(s.controlScroll.visible,false);
assert.equal(s.setMedallionScale(1.2),true);
assert.equal(settings.get_double('medallion-scale'),1.2);
assert.equal(s.setMedallionScale(1.3),false);
s.setHighContrast(true);assert.equal(settings.get_boolean('high-contrast'),true);
assert.equal(s.setSwitchShortcut('s'),true);
assert.deepEqual([...settings.get_strv('arandu-varredura-acionar')],['<Super><Alt>s']);
s.resetAccessibility();
assert.equal(settings.get_double('medallion-scale'),1);
assert.equal(settings.get_boolean('high-contrast'),false);
assert.deepEqual([...settings.get_strv('arandu-varredura-acionar')],['<Super><Alt>space']);
assert.equal(settings.get_string('panel-mode'),'visible');
assert.equal(s.helpBox.visible,false);
s.toggleHelp();assert.equal(s.helpBox.visible,true);
s.toggleHelp();assert.equal(s.helpBox.visible,false);
s.toggleHelpButton();assert.equal(s.helpButton.visible,false); // Semente recolhida: botão oculto
s.setExpanded(true);assert.equal(s.helpButton.visible,true);
// O ? repousa aos 6 s; os aplicativos e os rios permanecem visíveis.
assert(s.helpSleepId && pending.has(s.helpSleepId));
const helpSleepTick=pending.get(s.helpSleepId);
pending.delete(s.helpSleepId);helpSleepTick();
assert.equal(s.helpButton.opacity,0);
assert.equal(s.helpButton.reactive,false);
assert.equal(s.buttons.open[0].button.visible,true);
assert.equal(s.setMedallionScale(1.2),true);
assert.equal(s.buttons.open[0].button.scale[0],1.2);
s.setHighContrast(true);
assert(s.buttons.open[0].button.classes.has('arandu-node-high-contrast'));
s.resetAccessibility();
assert.equal(s.fabric.visible,true);
s.wakeSeed();
assert.equal(s.helpButton.opacity,255);
assert.equal(s.helpButton.reactive,true);
// Expandir pelo botão RIOS/Semente não ressuscita janelas auxiliares.
s.toggleHelp();s.toggleAccessibility();
assert.equal(s.helpBox.visible,true);
assert.equal(s.controlScroll.visible,true);
s.setExpanded(false);assert.equal(s.helpButton.visible,false);
assert.equal(s.helpBox.visible,false);
assert.equal(s.controlScroll.visible,false);
assert(s.seedSleepId && pending.has(s.seedSleepId));
const sleepingId=s.seedSleepId;const sleepTick=pending.get(sleepingId);pending.delete(sleepingId);sleepTick();
assert.equal(s.seed.opacity,31);
s.wakeSeed();assert.equal(s.seed.opacity,255);
s.position();assert(s.helpButton.pos[0]>s.seed.pos[0]);
// Painel completamente dentro da área útil e lista rolável.
assert(s.helpScroll && s.helpScroll.children.length===1);
assert(s.helpBox.pos[0]>=0 && s.helpBox.pos[1]>=0);
assert(s.helpBox.pos[0]+s.helpBox.width<=s.area.width);
assert(s.helpBox.pos[1]+s.helpBox.height<=s.area.height);

s.setBarMode('hidden');assert.equal(panelActor.visible,false);
s.setBarMode('visible');assert.equal(panelActor.visible,true);
// Sem mouse: visible -> auto -> hidden -> visible.
s.cycleBarMode();assert.equal(settings.get_string('panel-mode'),'auto');
s.cycleBarMode();assert.equal(settings.get_string('panel-mode'),'hidden');
s.cycleBarMode();assert.equal(settings.get_string('panel-mode'),'visible');

s.setBarMode('auto');s.barLastNear=Date.now()-4000;s.updateBar();assert.equal(panelActor.visible,true);
pointer=[150,240];s.barLastNear=Date.now()-9000;s.updateBar();assert.equal(panelActor.visible,false);
hideConflict=true;s.updateBar();assert.equal(panelActor.visible,true);
s.setBarMode('hidden');assert.equal(settings.get_string('panel-mode'),'auto');
hideConflict=false;s.setBarMode('hidden');assert.equal(panelActor.visible,false);
assert.equal(JSON.parse(s.Snapshot()).windows.length,3);
s.record();focused=b;s.record();focused=c;s.record();focused=a;s.record();
let snap=JSON.parse(s.Snapshot());
assert.equal(snap.recent[0].title,'Caderno');
assert.equal(snap.frequency.find(x=>x[0]==='editor.desktop')[1],3);
assert(s.Activate('32'));assert.equal(focused,b);assert.equal(s.Activate('200'),false);
s.setExpanded(true);assert.equal(s.buttons.open[0].button.visible,true);
// Assistive global navigation selects real medalhões without opening GTK.
// 3 monitores: o rio deve surgir na tela da janela ativa.
focused=b; // janela simulada no monitor 2
// Pop-ups deixados abertos não devem acompanhar a navegação por atalhos.
s.toggleHelp();assert.equal(s.helpBox.visible,true);
s.toggleAccessibility();assert.equal(s.controlScroll.visible,true);
s.selectRiver('open');
assert.equal(s.helpBox.visible,false);
assert.equal(s.controlScroll.visible,false);
s.toggleHelp();s.toggleAccessibility();
s.cancelSelection();
assert.equal(s.helpBox.visible,false);
assert.equal(s.controlScroll.visible,false);
s.selectRiver('open');
assert.equal(s.navRiver,'open');
assert.equal(s.navigationOverlay,true);
assert.equal(s.navigationMonitorIndex,1);
assert.equal(s.root.get_parent(),chrome);
assert.equal(s.root.pos[0],1366);
assert.equal(s.navigationOverlay,true);
assert.equal(settings.get_int('navigation-idle-ms'),10000);
assert.equal(JSON.parse(s.AssistiveStatus()).idleTimeoutMs,10000);
assert(s.navigationIdleTimer && pending.has(s.navigationIdleTimer));
const previousTimer=s.navigationIdleTimer;
s.navigationOutsideEvent({type:()=>4,get_source:()=>s.buttons.open[0].button});
assert.equal(pending.has(previousTimer),false);
assert(s.navigationIdleTimer && pending.has(s.navigationIdleTimer));
// Clique fora do ARANDU: recolher imediatamente, sem consumir o clique.
assert.equal(s.navigationOutsideEvent({type:()=>4,get_source:()=>new Actor()}),false);
assert.equal(s.navigationOverlay,false);
assert.equal(s.expanded,false);
assert.equal(s.navigationIdleTimer,0);
// Digitar no aplicativo com a mesma janela focada recolhe imediatamente.
s.selectRiver('open');
stage.set_key_focus(new Actor()); // campo de edição do aplicativo
assert.equal(s.navigationOutsideEvent({type:()=>3,get_source:()=>new Actor()}),false);
assert.equal(s.navigationOverlay,false);
assert.equal(s.expanded,false);
// Um toque na superfície transparente (root) também libera o aplicativo.
s.selectRiver('open');
assert.equal(s.navigationOutsideEvent({type:()=>4,get_source:()=>s.root}),false);
assert.equal(s.navigationOverlay,false);
assert.equal(s.expanded,false);
// Foco na janela já em uso não deve encerrar; trocar de janela sim.
s.selectRiver('open');
s.onFocusWindowChanged();
assert.equal(s.navigationOverlay,true);
focused=c;
s.onFocusWindowChanged();
assert.equal(s.navigationOverlay,false);
assert.equal(s.expanded,false);
focused=b;
s.selectRiver('open');
// Dez segundos sem ação: recolhimento seguro.
const elapsedNavigationTimer=s.navigationIdleTimer;
const timeoutTick=pending.get(elapsedNavigationTimer);
// O GLib remove automaticamente um timeout one-shot ao retornar SOURCE_REMOVE.
// O mock registra timers em Map e deve reproduzir essa remoção.
pending.delete(elapsedNavigationTimer);
assert.equal(timeoutTick(),false);
assert.equal(s.navigationOverlay,false);
assert.equal(s.expanded,false);
s.selectRiver('open');
assert.equal(s.setNavigationIdle(0),true);
assert.equal(s.navigationIdleTimer,0);
assert.equal(s.setNavigationIdle(10000),true);
s.cancelSelection();
assert.equal(s.navigationOverlay,false);
assert.equal(s.root.get_parent(),bg);
focused=a;
assert.equal(s.setMonitorTarget('fixed',2),true);
s.selectRiver('open');
assert.equal(s.navigationMonitorIndex,2);
assert.equal(s.root.pos[0],2446);
// Simular desligamento do terceiro monitor: recuperar no principal.
const disconnected=layout.monitors.pop();
s.position();
assert.equal(s.navigationMonitorIndex,0);
assert.equal(s.root.pos[0],0);
layout.monitors.push(disconnected);
s.cancelSelection();
assert.equal(s.setMonitorTarget('pointer'),true);
pointer=[1400,200];
s.selectRiver('open');
assert.equal(s.navigationMonitorIndex,1);
s.cancelSelection();
pointer=[10,1];
assert.equal(s.setMonitorTarget('focused'),true);
s.selectRiver('open');
assert.equal(s.navigationMonitorIndex,0);assert(s.navIndex>=0);
assert(s.buttons.open[s.navIndex].button.classes.has('arandu-node-selected'));
assert.equal(stage.get_key_focus(),s.buttons.open[s.navIndex].button);
assert(s.fabric.style.includes('-open.svg'));
const beforeEnter=focused;
assert.equal(s.navigationKeyEvent({type:()=>3,get_key_symbol:()=>13}),true);
assert.equal(s.expanded,false);
assert.equal(focused,a);
assert.equal(s.navigationOverlay,false);
assert.equal(s.root.get_parent(),bg);
assert.equal(s.navigationKeyEvent({type:()=>3,get_key_symbol:()=>65363}),false);
assert.notEqual(stage.get_key_focus(),null);
const retained=s.navIndex;
stage.set_key_focus(new Actor());
assert.equal(s.navigationKeyEvent({type:()=>3,get_key_symbol:()=>13}),false);
assert.equal(s.navIndex,retained);
s.selectRiver('open');
s.focusSelectedNode();
const first=s.navIndex;
s.moveSelection(1);assert.notEqual(s.navIndex,first);
s.activateSelection();assert.equal(s.expanded,false);
s.cancelSelection();assert.equal(s.navRiver,null);
s.selectRiver('frequent');assert.equal(s.navRiver,'frequent');
s.selectRiver('memory');assert.equal(s.navRiver,'memory');
// 7 segundos: somente a Semente central repousa, com os rios expandidos.
assert.equal(s.medallionSleepId,0);
assert(s.seedSleepId && pending.has(s.seedSleepId));
const savedRiver=s.navRiver, savedIndex=s.navIndex;
const quietTick=pending.get(s.seedSleepId);
pending.delete(s.seedSleepId);quietTick();
assert.equal(s.seed.opacity,31);
assert.equal(s.expanded,true);
assert.equal(s.navRiver,savedRiver);assert.equal(s.navIndex,savedIndex);
assert.equal(s.buttons[savedRiver][savedIndex].button.opacity,255);
assert.equal(s.buttons[savedRiver][savedIndex].button.reactive,true);
assert.equal(s.AssistiveCommand('node:next'),true);
assert.equal(s.seed.opacity,255);
assert.equal(s.buttons[s.navRiver][s.navIndex].button.opacity,255);
assert.equal(s.buttons[s.navRiver][s.navIndex].button.reactive,true);

// Estado assistivo acessível sem ação: leitura não inicia nem ativa.
let assistive=JSON.parse(s.AssistiveStatus());
assert.equal(assistive.available,true);
assert.equal(assistive.scanning,false);
assert.equal(assistive.intervalMs,3500);
// Configuração de velocidade: alterar pela interface persiste e não ativa janela.
assert.equal(s.setScanInterval(5000),true);
assert.equal(settings.get_int('scan-interval-ms'),5000);
assert.equal(JSON.parse(s.AssistiveStatus()).intervalMs,5000);
assert.equal(s.setScanInterval(1234),false);
assert.equal(settings.get_int('scan-interval-ms'),5000);
assert.equal(s.setScanInterval(3500),true);
// A varredura inicia desligada, avança sem ativar e confirma sob comando explícito.
assert.equal(s.scanning,false);
s.selectRiver('open');
assert.equal(s.AssistiveCommand('scan:start'),true);
assert.equal(s.scanning,true);
assert.equal(s.navigationOverlay,true);
assert.equal(s.navigationIdleTimer,0);
assistive=JSON.parse(s.AssistiveStatus());
assert.equal(assistive.scanning,true);
assert.equal(assistive.river,'open');
assert(assistive.index>=0);
assert(assistive.selected && assistive.selected.title);
assert(s.scanTimer && pending.has(s.scanTimer));
// Alterar velocidade em movimento reinicia o timer, sem ativar a janela.
const oldScanTimer=s.scanTimer;
const beforeChangeSelection=s.navIndex;
const beforeChangeFocus=focused;
assert.equal(s.setScanInterval(5000),true);
assert.equal(s.scanning,true);
assert.equal(pending.has(oldScanTimer),false);
assert.equal(s.navIndex,beforeChangeSelection);
assert.equal(focused,beforeChangeFocus);
assert.equal(JSON.parse(s.AssistiveStatus()).intervalMs,5000);
const scanTick=pending.get(s.scanTimer);
const beforeTick=s.navIndex;
const focusedBeforeScan=focused;
assert.equal(scanTick(),true);
assert.notEqual(s.navIndex,beforeTick);
assert.equal(focused,focusedBeforeScan); // varredura não abre aplicativos sozinha
assert.equal(s.AssistiveCommand('scan:switch'),true);
assert.equal(s.scanning,false);
assert.equal(s.navigationOverlay,false);
assert.equal(s.scanTimer,0);
assert.equal(s.AssistiveCommand('scan:start'),true);
s.setExpanded(false);
assert.equal(s.scanning,false); // recolher cancela a varredura
assert.equal(s.AssistiveCommand('scan:start'),true);
assert.equal(s.AssistiveCommand('node:cancel'),true);
assert.equal(s.scanning,false);
assert.equal(s.navigationOverlay,false);
assert.equal(s.AssistiveCommand('scan:unknown'),false);
assert.equal(s.setScanInterval(3500),true);
const fixedRoot=s.root;
for(let i=0;i<60;i++){s.setExpanded(false);s.setExpanded(true);}
assert.equal(s.root,fixedRoot);assert.equal(fixedRoot.destroyed,undefined);
s.launch('memory');assert.equal(actions[actions.length-1],'Memory');
s.layerItem.click();assert.equal(s.root.get_parent(),chrome);assert(tracked.size>3);
s.layerItem.click();assert.equal(s.root.get_parent(),bg);assert.equal(tracked.size,0);
privacy=false;assert.equal(JSON.parse(s.Snapshot()).recent.length,0);
main.sessionMode.isLocked=true;assert.equal(JSON.parse(s.Snapshot()).windows.length,0);assert.equal(s.Activate('12'),false);
assert.equal(JSON.parse(s.AssistiveStatus()).available,false);
main.sessionMode.isLocked=false;privacy=true;s.Clear();assert.equal(JSON.parse(s.Snapshot()).recent.length,0);
const oldRoot=s.root;s.stop();assert.equal(panelActor.visible,true);assert(!key && !service && oldRoot.destroyed);assert.equal(pending.size,0);
console.log('Contrato do Shell validado com objetos de teste: janelas, foco, contagens, privacidade, camadas e 60 ciclos de expansão.');

assert.equal(s.AssistiveCommand('river:open'),true);
assert.equal(s.navRiver,'open');
assert.equal(s.AssistiveCommand('node:next'),true);
assert.equal(s.AssistiveCommand('node:cancel'),true);
assert.equal(s.navRiver,null);
assert.equal(s.AssistiveCommand('unknown:command'),false);
