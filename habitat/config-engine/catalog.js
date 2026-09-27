const jurisdictions={
 NO:{id:'NO',product:'VALO30',currency:'NOK',localLaborRate:750,fx:{NOK:1,EUR:11.7,CNY:1.45,TRY:.28},tariff:{NO:0,EE:0,PL:0,PT:0,TR:0,CN:0},constraints:['NO_MICROHOME_PROFILE'],drivers:['30 m² Norwegian product profile','Nordic climate','high local labor cost','short local logistics']},
 PT:{id:'PT',product:'Habitat PT — geometry open',currency:'EUR',localLaborRate:32,fx:{EUR:1,NOK:.085,CNY:.124,TRY:.024},tariff:{PT:0,EE:0,PL:0,TR:0,CN:0},constraints:[],drivers:['geometry not locked to Norway','cooling/moisture profile differs','EU production network']}
};
const productionProfiles=[
 {id:'NO_AUTO_TIMBER',country:'NO',mode:'automated timber/cassette',strengths:['local material','short iteration','low FX exposure']},
 {id:'BALTIC_TIMBER',country:'EE',mode:'timber shell/panel',strengths:['Nordic export experience','short sea/road freight']},
 {id:'CEE_INDUSTRIAL',country:'PL',mode:'industrial panel/hybrid',strengths:['EU logistics','manufacturing depth']},
 {id:'PT_TIMBER',country:'PT',mode:'timber frame',strengths:['regional material/labor','Portugal integration']},
 {id:'TR_HYBRID',country:'TR',mode:'steel/hybrid prefab',strengths:['industrial prefab','regional freight']},
 {id:'CN_FLATPACK',country:'CN',mode:'LGS/components flat-pack',strengths:['component ecosystem','scale']}
];
module.exports={jurisdictions,productionProfiles};
