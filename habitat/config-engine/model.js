(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.HabitatConfig=api;})(globalThis,function(){
const AXES=['cost','leadTime','risk','co2','capital'];
const MODULES=['structure','envelope','roof','floor','bathroom','kitchen','technical_spine','energy','foundation','interior'];
function n(v,d=0){v=Number(v);return Number.isFinite(v)?v:d}
function mergeContext(j={},p={},s={}){return {fx:{...(j.fx||{}),...(s.fx||{})},tariff:{...(j.tariff||{}),...(s.tariff||{})},localLaborRate:n(j.localLaborRate),jurisdiction:j.id,production:p.id};}
function evaluateOption(o,ctx={}){
 const fx=n(ctx.fx?.[o.currency],1),tariff=n(ctx.tariff?.[o.origin],0);
 const material=n(o.materialCost)*fx,labor=n(o.laborHours)*n(o.laborRate)*fx*(1-n(o.automation));
 const logistics=n(o.transport)+n(o.packaging),compliance=n(o.compliance),local=n(o.localAssemblyHours)*n(ctx.localLaborRate);
 const defects=(material+labor+local)*n(o.defectRate);
 const gross=material+labor+logistics+compliance+local+defects;
 const cost=gross*(1+tariff)-n(o.residualValue);
 return {...o,metrics:{cost,leadTime:n(o.leadDays)+n(o.localAssemblyDays),risk:n(o.complianceRisk)+n(o.supplyRisk)+n(o.defectRate)+n(o.fxRisk),co2:n(o.embodiedCo2)+n(o.transportCo2),capital:cost*n(o.cashCycleDays)/365}};
}
function compatible(o,j,p){const req=o.requires||{};return (!req.jurisdictions||req.jurisdictions.includes(j.id))&&(!req.productionProfiles||req.productionProfiles.includes(p.id))&&!(o.excludes||[]).some(x=>(j.constraints||[]).includes(x));}
function dominates(a,b){return AXES.every(k=>a.metrics[k]<=b.metrics[k])&&AXES.some(k=>a.metrics[k]<b.metrics[k])}
function pareto(options){return options.filter((a,i)=>!options.some((b,j)=>i!==j&&dominates(b,a)))}
function configure({jurisdiction,productionProfiles,modules,scenario={}}){
 const profiles=productionProfiles||[];const evaluated=(modules||[]).map(m=>{const options=[];
  for(const p of profiles)for(const o of (m.options||[]))if(compatible(o,jurisdiction,p))options.push(evaluateOption({...o,productionProfile:p.id},mergeContext(jurisdiction,p,scenario)));
  return {...m,options,pareto:pareto(options)};});
 return {jurisdiction:jurisdiction.id,status:scenario.status||'ILLUSTRATIVE_INPUTS_NOT_EVIDENCE',evaluated};
}
return {AXES,MODULES,mergeContext,evaluateOption,compatible,dominates,pareto,configure};
});
