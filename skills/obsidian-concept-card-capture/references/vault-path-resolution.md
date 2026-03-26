# Vault Path Resolution

## Goal

Resolve one `VAULT_ROOT` before reading the concept template or writing any card.

All path operations in this skill should be derived from that root.

## Resolution Order

Resolve the vault root in this order:

1. Use an explicit vault path provided by the user in the current request.
2. Use a vault path already established earlier in the thread, if it is still clearly applicable.
3. Use the default local path `C:\Users\pz\Documents\Obsidian Vault` if it exists.
4. If none of the above is reliable, ask the user to confirm the vault root before proceeding.

## Derived Paths

Once `VAULT_ROOT` is resolved, derive these paths:

- Concept template: `<VAULT_ROOT>/模板/学习卡片模板/card/Concept Card.md`
- Concept card directory: `<VAULT_ROOT>/学习/Cards/Concepts`
- Existing card search root: `<VAULT_ROOT>/学习/Cards`

## Safety Rules

- Do not assume a hard-coded vault path when the current environment differs.
- Do not write outside the resolved vault root.
- If the resolved root exists but the derived template path is missing, stop and report that the template layout is inconsistent.
- If the concept output directory is missing, create it before writing the new card.

## User-Facing Behavior

When the vault root is ambiguous, ask a short direct question that requests only the vault root path.

When the vault root is resolved, use it consistently for:

- duplicate checks
- backlink discovery
- template inspection
- final file creation
