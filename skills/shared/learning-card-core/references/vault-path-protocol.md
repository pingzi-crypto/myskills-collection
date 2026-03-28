# Vault Path Protocol

## Goal

Resolve one `VAULT_ROOT` before reading templates, checking duplicates, or
writing any learning card.

All path operations in the learning-card family should be derived from that
single resolved root.

## Resolution Order

Resolve the vault root in this order:

1. Use an explicit vault path provided by the user in the current request.
2. Use a vault path already established earlier in the thread, if it is still
   clearly applicable.
3. Use the default local path `C:\Users\pz\Documents\Obsidian Vault` if it
   exists.
4. If none of the above is reliable, ask the user to confirm the vault root
   before proceeding.

## Family Path Rule

After `VAULT_ROOT` is resolved, each execution skill should derive:

- one card-type-specific template path
- one card-type-specific output directory
- one duplicate-check search root under `<VAULT_ROOT>/学习/Cards`

The exact template and output directory are still defined by the local
card-type spec.

## Safety Rules

- Do not assume a hard-coded vault path when the current environment differs.
- Do not write outside the resolved vault root.
- If the resolved root exists but a required template path is missing, stop and
  report that the template layout is inconsistent.
- If the target output directory is missing, create it before writing the new
  card.

## User-Facing Behavior

When the vault root is ambiguous, ask one short direct question that requests
only the vault root path.

When the vault root is resolved, use it consistently for:

- duplicate checks
- backlink discovery
- template inspection
- final file creation
