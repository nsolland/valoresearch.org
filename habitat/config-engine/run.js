const {configure}=require('./model');const {jurisdictions,productionProfiles}=require('./catalog');const modules=require('./modules');
function run(country='NO'){return configure({jurisdiction:jurisdictions[country],productionProfiles,modules,scenario:{status:'ILLUSTRATIVE_INPUTS_NOT_EVIDENCE'}})}
if(require.main===module){const r=run(process.argv[2]||'NO');console.log(JSON.stringify(r,null,2))}
module.exports={run};
