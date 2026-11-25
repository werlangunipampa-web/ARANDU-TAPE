import assert from 'node:assert/strict';
import {DIRECTIONS,edgeAt,handlePosition,resizeFromEdge} from './edge-geometry.mjs';
const f={x:-1000,y:100,width:500,height:400},w={x:-1200,y:30,width:1200,height:800};
const points=[[-750,100],[-500,100],[-500,300],[-500,500],[-750,500],[-1000,500],[-1000,300],[-1000,100]];
const expected=[
{x:-1000,y:130,width:500,height:370},{x:-1000,y:130,width:540,height:370},
{x:-1000,y:100,width:540,height:400},{x:-1000,y:100,width:540,height:430},
{x:-1000,y:100,width:500,height:430},{x:-960,y:100,width:460,height:430},
{x:-960,y:100,width:460,height:400},{x:-960,y:130,width:460,height:370}];
for(let i=0;i<8;i++){
    const e=DIRECTIONS[i];
    assert.equal(edgeAt(f,...points[i]),e);
    assert.deepEqual(resizeFromEdge(f,w,e,40,30),expected[i]);
    const p=handlePosition(f,e,...points[i]);
    assert(p.x>=f.x&&p.x+24<=f.x+f.width&&p.y>=f.y&&p.y+24<=f.y+f.height);
}
assert.equal(edgeAt(f,-750,300),null);
assert.equal(edgeAt(f,-750,60),null);
assert.equal(resizeFromEdge(f,w,'nw',9999,9999).width,240);
assert.equal(resizeFromEdge(f,w,'nw',9999,9999).height,160);
assert.equal(resizeFromEdge(f,w,'nw',-9999,-9999).x,-1200);
assert.equal(resizeFromEdge(f,w,'nw',-9999,-9999).y,30);
assert.equal(resizeFromEdge(f,w,'se',Infinity,0),null);
assert.equal(resizeFromEdge({...f,x:-1300},w,'e',10,0),null);
console.log('Geometria: oito direções, âncoras opostas e limites aprovados.');
