<%*
const file = tp.file.find_tfile(tp.file.path(true));
if (!file) { new Notice("No active file."); return; }

// Only run on task files
if (!file.path.startsWith("tasks/")) {
  new Notice("Not a task file.");
  return;
}

// Update status → done in frontmatter
const content = await app.vault.read(file);
const updated = content.replace(/^status:.+$/m, "status: done");
await app.vault.modify(file, updated);

// Move to tasks/done/
const newPath = "tasks/done/" + file.name;
await app.fileManager.renameFile(file, newPath);

new Notice("✓ Task marked done and moved to tasks/done/");
-%>
