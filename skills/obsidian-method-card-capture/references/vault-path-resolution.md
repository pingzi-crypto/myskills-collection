# Method Vault Paths

Read the shared family protocol first:

- [../../shared/learning-card-core/references/vault-path-protocol.md](../../shared/learning-card-core/references/vault-path-protocol.md)

## Method-Specific Derived Paths

Once `VAULT_ROOT` is resolved, derive these paths:

- Method template: `<VAULT_ROOT>/模板/学习卡片模板/card/Method Card.md`
- Method card directory: `<VAULT_ROOT>/学习/Cards/Methods`
- Existing card search root: `<VAULT_ROOT>/学习/Cards`

## Method-Specific Safety Notes

- If the method output directory is missing, create it before writing.
- If the method template path is missing, stop and report the template layout
  mismatch.
