# Product Domain Depot

## Why

This repository manages product documentation and development artifacts across multiple business domains. Each domain contains products with their PRDs, development guides, solution architectures, and linked code repositories.

## What

Documentation artifact storage for product requirements, development guides, solution designs, and architectures across multiple business domains. Code repositories are stored separately and referenced via config files.

**Structure:**
```
domains/{domain}/{product}/
├── config.json          # Repository definitions with localPath mappings
├── prds/                # Product requirement documents
├── dev-guides/          # Development guides
├── solution-architectures/
├── solution-designs/
└── local/               # Local workspace files
```

## How

### Workspace Rules

**Always check active workspace first:** `echo $ACTIVE_WORKSPACE`

**File operations:**
- Write/modify: ONLY within `$ACTIVE_WORKSPACE`
- Read: `$ACTIVE_WORKSPACE` + repositories at `$REPOS_LOCATION` (read-only)
- Save temporary working files (drafts, notes, generated content) to `${ACTIVE_WORKSPACE}/local/`

**Accessing code repositories:**
1. Read `${ACTIVE_WORKSPACE}/config.json` for repository definitions
2. Use `localPath` field (resolves `${REPOS_LOCATION}/repo-name`) to locate code
3. Read code from resolved paths for context (read-only)

### Environment Variables

- `$ACTIVE_WORKSPACE` - Current workspace path (e.g., `domains/Origination/rocket-flow`)
- `$REPOS_LOCATION` - Base path for code repositories (e.g., `/Users/ddavis25/repos`)

### Skills

Use the Skill tool for specialized workflows:

- **prd-ops**: Creating, editing, or managing Product Requirement Documents
- **git-ops**: Git operations (branches, commits, pull requests)
- **ado-ops**: Retrieving, creating, or updating AD user-stories and features

When working in these areas, always use the corresponding skill.