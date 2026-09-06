import fs from 'fs';
const src = fs.readFileSync('C:/Users/tshau/Documents/Study Vault/admin/build-status.html','utf8');
function grab(startMarker){
  const i = src.indexOf(startMarker);
  if(i<0) throw new Error('not found '+startMarker);
  let j = src.indexOf('{', i);
  let depth=0, k=j;
  for(; k<src.length; k++){
    if(src[k]==='{') depth++;
    else if(src[k]==='}'){ depth--; if(depth===0){ k++; break; } }
  }
  return src.slice(j,k);
}
const EXCLUDED_FAMILIES = eval('('+grab('var EXCLUDED_FAMILIES =')+')');
const ENTRY_TIER        = eval('('+grab('var ENTRY_TIER =')+')');
const BUILD_NOTES       = eval('('+grab('var BUILD_NOTES =')+')');
// subjectFamily function, verbatim
const fnStart = src.indexOf('function subjectFamily(name) {');
const fnEnd = src.indexOf('\n    }', fnStart)+6;
const fnSrc = src.slice(fnStart, fnEnd);
fs.writeFileSync('_build_status_maps.json', JSON.stringify({EXCLUDED_FAMILIES,ENTRY_TIER,BUILD_NOTES,subjectFamilySource:fnSrc},null,1));
console.log('excluded',Object.keys(EXCLUDED_FAMILIES).length,'tier',Object.keys(ENTRY_TIER).length,'notes',Object.keys(BUILD_NOTES).length);
console.log(fnSrc);
