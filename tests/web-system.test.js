const fs = require('fs');
const assert = require('assert');

const css = fs.readFileSync('assets/valo-web.css', 'utf8');
const edu = fs.readFileSync('edu/index.html', 'utf8');

assert(css.includes('--valo-max:'), 'shared system must define canonical content width');
assert(css.includes('.site-nav'), 'shared system must define site navigation');
assert(css.includes('.section-grid'), 'shared system must define editorial section grid');
assert(css.includes('.button'), 'shared system must define canonical buttons');
assert(!css.includes('border-radius:32px'), 'shared system must avoid oversized default radii');
assert(edu.includes('/assets/valo-web.css'), '/edu/ must consume shared web system');

console.log('VALO web system contract OK');
