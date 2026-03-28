# Mechanism Vault Paths

Read the shared family protocol first:

- [../../shared/learning-card-core/references/vault-path-protocol.md](../../shared/learning-card-core/references/vault-path-protocol.md)

## Mechanism-Specific Derived Paths

Once `VAULT_ROOT` is resolved, derive these paths:

- Mechanism template: `<VAULT_ROOT>/模板/学习卡片模板/card/Mechanism Card.md`
- Mechanism card directory: `<VAULT_ROOT>/学习/Cards/Mechanisms`
- Existing card search root: `<VAULT_ROOT>/学习/Cards`

## Mechanism-Specific Safety Notes

- If the mechanism output directory is missing, create it before writing.
- If the mechanism template path is missing, stop and report the template
  layout mismatch.
