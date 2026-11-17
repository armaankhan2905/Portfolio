const reduce = matchMedia('(prefers-reduced-motion: reduce)');
const name = document.querySelector('#hero-name');
const realName = name.textContent;
const accessible = document.createElement('span');
accessible.className = 'sr-only';
accessible.textContent = realName;
const visual = document.createElement('span');
visual.setAttribute('aria-hidden', 'true');
const cells = [...realName].map(char => {
  const cell = document.createElement('span');
  cell.className = 'shuffle-char';
  const target = document.createElement('span');
  target.className = 'shuffle-target';
  target.textContent = char === ' ' ? '\u00a0' : char;
  const glyph = document.createElement('span');
  glyph.className = 'shuffle-glyph';
  glyph.textContent = target.textContent;
  cell.append(target, glyph);
  visual.append(cell);
  return {cell, glyph, char};
});
name.replaceChildren(accessible, visual);
let shuffle;
function settle() {
  clearInterval(shuffle);
  shuffle = null;
  for (const {cell, glyph, char} of cells) {
    glyph.textContent = char === ' ' ? '\u00a0' : char;
    cell.classList.remove('scrambling');
  }
}
function shuffleName() {
  if (reduce.matches || shuffle) return;
  let step = 0;
  const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#@$%&*';
  shuffle = setInterval(() => {
    if (reduce.matches || step >= cells.length * 4) return settle();
    for (const [index, {cell, glyph, char}] of cells.entries()) {
      const active = char !== ' ' && step < (index + 1) * 4;
      cell.classList.toggle('scrambling', active);
      const random = alphabet[Math.floor(Math.random() * alphabet.length)];
      glyph.textContent = !active ? (char === ' ' ? '\u00a0' : char) : /[a-z]/.test(char) ? random.toLowerCase() : random;
    }
    step++;
  }, 38);
}
name.addEventListener('pointerenter', shuffleName);

const about = document.querySelector('.notebook p');
const readable = document.createElement('span');
readable.className = 'sr-only';
readable.textContent = about.textContent;
const words = document.createElement('span');
words.setAttribute('aria-hidden', 'true');
let wordIndex = 0;
for (const child of [...about.childNodes]) {
  if (child.nodeName === 'MARK') {
    child.classList.add('reveal-word');
    child.style.setProperty('--delay', wordIndex++ * 26 + 'ms');
    words.append(child);
  } else {
    for (const token of child.textContent.split(/(\s+)/)) {
      if (!token.trim()) { words.append(document.createTextNode(token)); continue; }
      const word = document.createElement('span');
      word.className = 'reveal-word';
      word.textContent = token;
      word.style.setProperty('--delay', wordIndex++ * 26 + 'ms');
      words.append(word);
    }
  }
}
about.replaceChildren(readable, words);

const cards = [...document.querySelectorAll('.polaroid, .project-launch')];
for (const photo of cards) {
photo.addEventListener('pointermove', event => {
  if (reduce.matches || event.pointerType === 'touch') return;
  const box = photo.getBoundingClientRect();
  const x = (event.clientX - box.left) / box.width;
  const y = (event.clientY - box.top) / box.height;
  photo.style.transform = 'perspective(1000px) rotateX(' + (-(y-.5)*28) + 'deg) rotateY(' + ((x-.5)*28) + 'deg) scale(1.03)';
  photo.style.setProperty('--glare-x', x*100+'%');
  photo.style.setProperty('--glare-y', y*100+'%');
  photo.classList.add('tilting');
});
photo.addEventListener('pointerleave', () => {photo.style.transform = '';photo.classList.remove('tilting');});
}
function resetPhoto() {for (const card of cards) {card.style.transform = '';card.classList.remove('tilting');}}

const laptop = document.querySelector('.laptop');
export function playHomeMotion() {
  settle();
  shuffleName();
  about.classList.remove('revealing');
  void about.offsetWidth;
  about.classList.add('revealing');
}
export function playLaptopMotion() {
  laptop.classList.remove('opening');
  void laptop.offsetWidth;
  laptop.classList.add('opening');
}
export async function closeLaptop() {
  if (reduce.matches) return;
  const animation = laptop.animate([
    {transform:'perspective(1400px) rotateX(0deg)', opacity:1},
    {transform:'perspective(1400px) rotateX(-75deg)', opacity:0}
  ], {duration:420, easing:'ease-in', fill:'forwards'});
  await animation.finished.catch(() => {});
  animation.cancel();
}

// Same WebGL fluid/bloom cursor used by the reference portfolio.
const canvas = document.createElement('canvas');
canvas.id = 'glow-cursor';
canvas.setAttribute('aria-hidden', 'true');
document.body.append(canvas);
let glow;
function updateGlow() {
  glow?.destroy();
  glow = null;
  canvas.hidden = reduce.matches;
  if (!reduce.matches && window.createGlowCursor) {
    glow = window.createGlowCursor(canvas, {color:'#5f8bff',intensity:1.3,trailWidth:3,linger:1.4,glow:1.2,clickBurst:true,theme:'dark'});
  }
}
if (document.readyState === 'complete') updateGlow();
else window.addEventListener('load', updateGlow, {once:true});
reduce.addEventListener('change', () => {settle();resetPhoto();updateGlow();});
