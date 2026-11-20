import { categories, projects, projectsIn } from './projects.js';
import { playHomeMotion, playLaptopMotion, closeLaptop } from './motion.js';

const $ = selector => document.querySelector(selector);
const home = $('#home-view');
const desktop = $('#projects-view');
const folders = $('#folders');
const filters = $('#filters');
const projectWindow = $('#project-dialog');
const recycle = $('#recycle');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
let category = 'All';
let previousPage;
let lastDesktopScroll = 0;
let restoreProject;

function element(tag, text, className) {
  const item = document.createElement(tag);
  if (text) item.textContent = text;
  if (className) item.className = className;
  return item;
}

function screenChange() {
  const showProjects = location.hash === '#projects';
  if (showProjects === previousPage) return;
  function update() {
    if (projectWindow.open) projectWindow.close();
    if (recycle.open) recycle.close();
    home.hidden = showProjects;
    desktop.hidden = !showProjects;
    if (showProjects) playLaptopMotion();
    else playHomeMotion();
    document.title = showProjects ? 'Projects | Armaan Khan' : 'Armaan Khan — Portfolio';
    if (previousPage !== undefined || showProjects) {
      const heading = $(showProjects ? '#projects-heading' : '#hero-name');
      heading.focus({ preventScroll: true });
      window.scrollTo(0, showProjects ? lastDesktopScroll : 0);
    }
    previousPage = showProjects;
  }
  if (document.startViewTransition && previousPage !== undefined && !reducedMotion.matches) {
    document.startViewTransition(update);
  } else {
    update();
  }
}
let navigating = false;
async function navigate(hash) {
  if (navigating) return;
  if (location.hash === hash) return;
  navigating = true;
  if (hash === '#home') await closeLaptop();
  history.pushState(null, '', hash);
  screenChange();
  navigating = false;
}
$('#open-projects').addEventListener('click', () => {
  lastDesktopScroll = 0;
  navigate('#projects');
});
document.querySelectorAll('[data-home]').forEach(button => button.addEventListener('click', () => navigate('#home')));
window.addEventListener('popstate', screenChange);
window.addEventListener('hashchange', screenChange);
screenChange();

$('#project-count').textContent = projects.length;
for (const project of projects) {
  const dot = element('span', project.name);
  dot.style.setProperty('--dot', project.color);
  $('#project-preview').append(dot);
}

for (const item of categories) {
  const button = element('button', item, 'bevel');
  button.type = 'button';
  button.setAttribute('aria-pressed', String(item === category));
  button.addEventListener('click', () => {
    category = item;
    for (const filter of filters.children) filter.setAttribute('aria-pressed', String(filter === button));
    renderFolders();
  });
  filters.append(button);
}

function renderFolders() {
  folders.replaceChildren(...projectsIn(category).map(project => {
    const button = element('button', '', 'folder');
    button.type = 'button';
    button.setAttribute('aria-label', 'Open project folder: ' + project.name);
    const icon = element('span', '', 'folder-icon');
    const image = element('img');
    image.src = 'assets/folder.svg';
    image.alt = '';
    icon.append(image);
    if (project.badge) icon.append(element('span', project.badge, 'file-badge'));
    button.append(icon, element('span', project.name), element('small', project.category));
    button.addEventListener('click', () => openProject(project));
    const item = element('li');
    item.append(button);
    return item;
  }));
}
renderFolders();

function actionLink(label, href, style) {
  const link = element('a', label, 'button ' + style);
  link.href = href;
  link.target = '_blank';
  link.rel = 'noopener';
  return link;
}

function openProject(project) {
  restoreProject?.remove();
  restoreProject = undefined;
  projectWindow.classList.remove('maximized');
  $('#maximize').setAttribute('aria-label', 'Maximize');
  $('#window-name').textContent = project.name + '.exe';
  $('#window-category').textContent = project.category;
  $('#window-meta').textContent = project.meta;
  $('#dialog-title').textContent = project.name;
  $('#dialog-tagline').textContent = project.tagline;
  $('#dialog-description').textContent = project.description;
  $('#dialog-highlights').replaceChildren(...project.highlights.map(text => element('li', text)));
  $('#dialog-tech').replaceChildren(...project.tech.map(text => element('li', text)));
  const actions = [];
  if (project.download) actions.push(actionLink('↓ ' + project.download.label, project.download.url, 'primary'));
  if (project.live) actions.push(actionLink('Launch Build ↗', project.live, 'primary'));
  actions.push(actionLink('Source Code ↗', project.repo, project.live ? 'secondary' : 'primary'));
  const close = element('button', 'Close', 'button dialog-close');
  close.type = 'button';
  close.addEventListener('click', () => projectWindow.close());
  $('#window-actions').replaceChildren(...actions, close);
  projectWindow.showModal();
  $('.window-content').scrollTop = 0;
}

$('#maximize').addEventListener('click', event => {
  const full = projectWindow.classList.toggle('maximized');
  event.currentTarget.setAttribute('aria-label', full ? 'Restore window size' : 'Maximize');
});
$('#minimize').addEventListener('click', () => {
  projectWindow.close();
  restoreProject = element('button', '▣ ' + $('#window-name').textContent, 'bevel restore-project');
  restoreProject.type = 'button';
  restoreProject.addEventListener('click', () => {
    projectWindow.showModal();
    restoreProject.remove();
    restoreProject = undefined;
  });
  $('.task').after(restoreProject);
  restoreProject.focus();
});
$('#trash').addEventListener('click', () => recycle.showModal());
document.querySelectorAll('[data-close]').forEach(button => button.addEventListener('click', () => button.closest('dialog').close()));
document.querySelectorAll('dialog').forEach(dialog => dialog.addEventListener('click', event => {
  if (event.target !== dialog) return;
  const { left, right, top, bottom } = dialog.getBoundingClientRect();
  if (event.clientX < left || event.clientX > right || event.clientY < top || event.clientY > bottom) dialog.close();
}));

const clock = new Intl.DateTimeFormat('en-US', { hour: 'numeric', minute: '2-digit' });
function showTime() {
  const now = new Date();
  document.querySelectorAll('.clock').forEach(time => {
    time.textContent = clock.format(now);
    time.dateTime = now.toISOString();
  });
}
showTime();
setInterval(showTime, 1000);


const resumeScroll = $('#resume-scroll');
const scrollToggle = $('#scroll-toggle');
const scrollImage = resumeScroll.querySelector('img');
function setScroll(open) {
  resumeScroll.classList.toggle('is-open', open);
  scrollToggle.setAttribute('aria-expanded', String(open));
  scrollToggle.firstElementChild.textContent = open ? 'Roll it back up ↑' : 'Click to unroll ↓';
  if (!open) resumeScroll.scrollIntoView({ block: 'center', behavior: reducedMotion.matches ? 'auto' : 'smooth' });
}
// Start loading the résumé image as soon as someone shows interest, so it is ready when the paper unrolls.
const preloadResume = () => { scrollImage.loading = 'eager'; };
resumeScroll.addEventListener('pointerenter', preloadResume, { once: true });
scrollToggle.addEventListener('focus', preloadResume, { once: true });
scrollToggle.addEventListener('click', event => {
  event.stopPropagation();
  setScroll(!resumeScroll.classList.contains('is-open'));
});
resumeScroll.addEventListener('click', () => {
  if (!resumeScroll.classList.contains('is-open')) setScroll(true);
});
