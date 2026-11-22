const assert=require('assert').strict;
const fs=require('fs');const path=require('path');
const code=fs.readFileSync(path.join(__dirname,'../shell/implementation.js.in'),'utf8');
for(const token of ["this.setExpanded(!this.expanded)","this.scheduleSeedSleep()","7000","6000","this.helpAwake=false","this.setSeedOpacity(31)","this.cancelSeedSleep()","this.seed.connect('notify::hover'"])
  assert(code.includes(token),`Contrato não contém: ${token}`);
assert(!code.includes('if(!this.expanded)this.hoverId=GLib.timeout_add'), 'Expansão automática por hover não permitida');
console.log('Contrato Semente 2.8.3: alternância manual, 7s, opacidade e interação encontrados.');
