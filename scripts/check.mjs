import assert from 'node:assert/strict';
import { readFile, stat } from 'node:fs/promises';
import { projects, categories, projectsIn } from '../dist/projects.js';

const html = await readFile(new URL('../dist/index.html', import.meta.url), 'utf8');
assert.equal(projects.length, 7);
assert.equal(new Set(projects.map(project => project.name)).size, projects.length);
assert.equal(projectsIn('All').length, projects.length);
assert.deepEqual(categories.slice(1).map(category => projectsIn(category).length), [1, 2, 4]);
assert.ok(projects.some(project => project.live) && projects.some(project => project.download));
assert.ok(projects.every(project => project.repo.startsWith('https://github.com/armaankhan2905/')));
const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(([, id]) => id);
assert.equal(new Set(ids).size, ids.length);
for (const [, id] of html.matchAll(/aria-labelledby="([^"]+)"/g)) assert.ok(ids.includes(id));
for (const [, file] of html.matchAll(/(?:src|href)="(assets\/[^"]+|styles\.css|app\.js)"/g)) {
  assert.ok((await stat(new URL(`../dist/${file}`, import.meta.url))).size > 0, file);
}
assert.equal((await readFile(new URL('../dist/assets/Armaan_Khan_Resume.pdf', import.meta.url))).subarray(0, 4).toString(), '%PDF');
console.log('Portfolio data, filters, accessibility references, and local assets passed.');
