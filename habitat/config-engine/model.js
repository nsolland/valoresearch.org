(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.HabitatConfig=api;})(globalThis,function(){
const AXES=['cost','leadTime','risk','co2','capital'];
function n(v,d=0){v=Number(v);return Number.isFinite(v)?v:d}
function evaluateOption(o,ctx={}){
 const fx=n(ctx.fx?.[o.currency],1), tariff=n(ctx.tariff?.[o.origin],0);
 const material=n(o.materialCost)*fx, labor=n(o.laborHours)*n(o.laborRate)*fx*(1-n(o.automation));
 const logistics=n(o.transport)+n(o.packaging), compliance=n(o.compliance), defects=(material+labor)*n(o.defectRate);
 const cost=(material+labor+logistics+compliance+defects)*(1+tariff)-n(o.residualValue);
 return {...o,metrics:{cost,leadTime:n(o.leadDays)+n(o.localAssemblyDays),risk:n(o.complianceRisk)+n(o.supplyRisk)+n(o.defectRate),co2:n(o.embodiedCo2)+n(o.transportCo2),capital:cost*n(o.cashCycleDays)/365}};
}
function dominates(a,b){return AXES.every(k=>a.metrics[k]<=b.metrics[k])&&AXES.some(k=>a.metrics[k]<b.metrics[k])}
function pareto(options){return options.filter((a,i)=>!options.some((b,j)=>i!==j&&dominates(b,a)))}
function configure(scenario){
 const evaluated=scenario.modules.map(m=>({...m,options:m.options.filter(o=>(o.constraints||[]).every(c=>!scenario.blockedConstraints?.includes(c))).map(o=>evaluateOption(o,scenario.context))}));
 return {...scenario,evaluated:evaluated.map(m=>({...m,pareto:pareto(m.options)}))};
}
return {evaluateOption,dominates,pareto,configure,AXES};
});
