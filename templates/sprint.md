---
id: 
status: active
start: 
end: 
repos: []
projects: []
goal: 
---

## Tasks

```dataview
TABLE project, repo, status, priority, due
FROM "tasks"
WHERE sprint = ""
SORT repo ASC, priority DESC
```
