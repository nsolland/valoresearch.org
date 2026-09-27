module.exports={
 name:'Norway / VALO30',status:'ILLUSTRATIVE_INPUTS_NOT_EVIDENCE',
 context:{fx:{NOK:1,EUR:11.7,CNY:1.45},tariff:{NO:0,EE:0,CN:0}},
 blockedConstraints:[],
 modules:[
 {id:'structure',options:[
  {id:'NO_TIMBER_AUTO',origin:'NO',currency:'NOK',materialCost:95000,laborHours:55,laborRate:650,automation:.55,transport:12000,packaging:4000,compliance:12000,defectRate:.02,residualValue:15000,leadDays:21,localAssemblyDays:2,complianceRisk:.08,supplyRisk:.08,embodiedCo2:1400,transportCo2:80,cashCycleDays:30},
  {id:'EE_TIMBER_SHELL',origin:'EE',currency:'EUR',materialCost:8500,laborHours:42,laborRate:28,automation:.4,transport:22000,packaging:5000,compliance:18000,defectRate:.025,residualValue:14000,leadDays:35,localAssemblyDays:2,complianceRisk:.12,supplyRisk:.12,embodiedCo2:1300,transportCo2:240,cashCycleDays:45},
  {id:'CN_LGS_FLATPACK',origin:'CN',currency:'CNY',materialCost:58000,laborHours:60,laborRate:55,automation:.35,transport:42000,packaging:9000,compliance:30000,defectRate:.04,residualValue:9000,leadDays:55,localAssemblyDays:4,complianceRisk:.25,supplyRisk:.22,embodiedCo2:3100,transportCo2:620,cashCycleDays:70}
 ]},
 {id:'technical_spine',options:[
  {id:'NO_LOCAL_MEP',origin:'NO',currency:'NOK',materialCost:70000,laborHours:70,laborRate:750,automation:.1,transport:3000,packaging:1000,compliance:8000,defectRate:.015,residualValue:5000,leadDays:14,localAssemblyDays:4,complianceRisk:.04,supplyRisk:.05,embodiedCo2:900,transportCo2:20,cashCycleDays:20},
  {id:'EU_PREFAB_SPINE',origin:'EE',currency:'EUR',materialCost:6200,laborHours:38,laborRate:30,automation:.35,transport:10000,packaging:2500,compliance:15000,defectRate:.02,residualValue:6000,leadDays:30,localAssemblyDays:2,complianceRisk:.1,supplyRisk:.1,embodiedCo2:820,transportCo2:110,cashCycleDays:40}
 ]}
]};
