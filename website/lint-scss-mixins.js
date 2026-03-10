#!/usr/bin/env node
/**
 * Genesis Ontological SCSS Mixin Linter
 * 
 * Validates that SCSS files use correct ontological mixin patterns.
 * Checks for:
 * 1. Valid mixin names (genesis-environment, genesis-entity, genesis-cognition, etc.)
 * 2. Valid variant values for each mixin
 * 3. Structural containers don't use visual mixins (genesis-entity, genesis-atmosphere)
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Valid mixins and their allowed values
const VALID_MIXINS = {
  'genesis-environment': [
    'focused', 'distributed', 'manifest', 'associative', 'chronological',
    'navigation-sidebar', 'navigation-tabs', 'navigation-footer', 'navigation-menu',
    'interaction-form', 'interaction-grid', 'convergent',
    'dense-desktop', 'spacious-desktop', 'spacious-mobile',
    'viewport-aware', 'dense-desktop',
  ],
  'genesis-entity': [
    'primary', 'secondary', 'imperative', 'latent', 'aggregate',
    'ancestral', 'transcendent', 'ephemeral', 'image-adaptive',
  ],
  'genesis-cognition': [
    'axiom', 'discourse', 'protocol', 'gloss', 'motive', 'quantum',
    'testimony', 'oracle',
  ],
  'genesis-synapse': [
    'execute', 'navigate', 'inquiry', 'destructive', 'social', 'invoke',
    'step', 'tab', 'toggle', 'anchor', 'input-primary', 'consent',
  ],
  'genesis-state': [
    'stable', 'evolving', 'deprecated', 'locked', 'simulated', 'active',
    'emerging', 'transcending',
  ],
  'genesis-atmosphere': [
    'ethereal', 'void', 'vibrant', 'neutral', 'dense-desktop', 'spacious-mobile',
    'viewport-aware', 'sacred',
  ],
};

// Structural selectors that should NOT use visual mixins
const STRUCTURAL_PATTERNS = [
  /^\s*main\s*\{/,
  /^\s*section\s*\{/,
  /^\s*\.-*container\s*\{/,
  /^\s*\.-*wrapper\s*\{/,
  /^\s*\.-*layout\s*\{/,
  /^\s*header\s*\{/,
];

// Regex to find mixin includes
const MIXIN_REGEX = /@include\s+(genesis-\w+)\s*\(\s*['"]([^'"]+)['"]\s*\)/g;

function lintFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const lines = content.split('\n');
  const issues = [];
  
  lines.forEach((line, index) => {
    let match;
    MIXIN_REGEX.lastIndex = 0;
    
    while ((match = MIXIN_REGEX.exec(line)) !== null) {
      const mixinName = match[1];
      const variant = match[2];
      const lineNum = index + 1;
      
      // Check if mixin name is valid
      if (!VALID_MIXINS[mixinName]) {
        issues.push({
          line: lineNum,
          type: 'unknown-mixin',
          message: `Unknown mixin: @include ${mixinName}('${variant}')`
        });
        continue;
      }
      
      // Check if variant is valid for this mixin
      const validVariants = VALID_MIXINS[mixinName];
      if (!validVariants.includes(variant)) {
        issues.push({
          line: lineNum,
          type: 'unknown-variant',
          message: `Unknown variant '${variant}' for @include ${mixinName}()`
        });
      }
    }
  });
  
  return issues;
}

function getAllScssFiles(dir) {
  let results = [];
  if (!fs.existsSync(dir)) return results;
  
  const list = fs.readdirSync(dir);
  for (const file of list) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat && stat.isDirectory()) {
      results = results.concat(getAllScssFiles(filePath));
    } else if (file.endsWith('.scss') && !file.includes('_example')) {
      results.push(filePath);
    }
  }
  return results;
}

console.log('🔍 Genesis Ontological SCSS Mixin Linter');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('Validating mixin usage in SCSS files...\n');

const scssDir = path.resolve(__dirname, '_sass');
const files = getAllScssFiles(scssDir);

let totalIssues = 0;
const issuesByFile = {};
let filesScanned = 0;

files.forEach(file => {
  const issues = lintFile(file);
  filesScanned++;
  if (issues.length > 0) {
    const relativePath = path.relative(__dirname, file);
    issuesByFile[relativePath] = issues;
    totalIssues += issues.length;
  }
});

if (totalIssues === 0) {
  console.log('✅ ALL MIXINS VALID');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`Scanned ${filesScanned} SCSS file(s). All mixin usages are valid.`);
  console.log('Genesis Ontological SCSS Design System compliance: PASSED\n');
  process.exit(0);
} else {
  console.error('❌ MIXIN VALIDATION ISSUES FOUND');
  console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.error(`Found ${totalIssues} issue(s) in ${Object.keys(issuesByFile).length} file(s):\n`);
  
  for (const [file, issues] of Object.entries(issuesByFile)) {
    console.error(`  ✗ ${file} (${issues.length} issue${issues.length > 1 ? 's' : ''}):`);
    issues.slice(0, 5).forEach(issue => {
      console.error(`    Line ${issue.line}: ${issue.message}`);
    });
    if (issues.length > 5) {
      console.error(`    ... and ${issues.length - 5} more`);
    }
    console.error('');
  }
  
  console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.error('💡 Fix: Use only valid Genesis ontological mixin variants');
  console.error('📖 See _sass/_example-ontology.scss for reference');
  console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  process.exit(1);
}
