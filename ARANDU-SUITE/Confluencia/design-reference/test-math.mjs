import assert from 'node:assert/strict';
import { normalizeArea,classifyDrop,halfArea,resizeArea,safeMove } from './espacos-math.mjs';

const area={x:-1200,y:30,width:1200,height:800};
assert.equal(normalizeArea({...area,width:100}),null);
assert.equal(classifyDrop(area,-600,60),'imersao');
assert.equal(classifyDrop(area,-600,800),'recolher');
assert.equal(classifyDrop(area,-1100,800),'encerrar');
assert.equal(classifyDrop(area,-600,400),null);
assert.equal(classifyDrop(area,1,400),null);
assert.equal(halfArea(area,'esquerda').width+halfArea(area,'direita').width+10,1200);
const frame={x:-1000,y:100,width:500,height:400};
assert.deepEqual(resizeArea(frame,area,10000,10000),{x:-1000,y:100,width:1000,height:730});
assert.deepEqual(safeMove(frame,area,-10000,-10000),{x:-1612,y:30});
console.log('Convergência gráfica: 9 verificações matemáticas aprovadas.');
