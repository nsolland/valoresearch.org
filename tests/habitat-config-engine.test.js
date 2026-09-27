const test=require('node:test');const assert=require('node:assert/strict');
const {evaluateOption,pareto,configure}=require('../habitat/config-engine/model.js');
const scenario=require('../habitat/config-engine/norway-valo30.js');
test('currency changes landed economics',()=>{const o={origin:'X',currency:'EUR',materialCost:100,laborHours:0};assert.equal(evaluateOption(o,{fx:{EUR:10}}).metrics.cost,1000);});
test('automation reduces modeled labor cost',()=>{const b={origin:'NO',currency:'NOK',materialCost:0,laborHours:100,laborRate:100,automation:0};assert.ok(evaluateOption({...b,automation:.8},{fx:{NOK:1}}).metrics.cost<evaluateOption(b,{fx:{NOK:1}}).metrics.cost);});
test('pareto removes option worse on every axis',()=>{const a={metrics:{cost:1,leadTime:1,risk:1,co2:1,capital:1}},b={metrics:{cost:2,leadTime:2,risk:2,co2:2,capital:2}};assert.deepEqual(pareto([a,b]),[a]);});
test('Norway scenario returns module Pareto sets',()=>{const r=configure(scenario);assert.equal(r.status,'ILLUSTRATIVE_INPUTS_NOT_EVIDENCE');assert.ok(r.evaluated.every(m=>m.pareto.length));});
