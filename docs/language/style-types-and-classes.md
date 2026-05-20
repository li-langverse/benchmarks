# Types, classes, and naming (Li style)

## PascalCase vs camelCase

| Surface | Convention | Examples |
|---------|--------------|----------|
| **Types / objects** | **PascalCase** | `Point`, `Vault`, `ParticleBatch` |
| **Functions, locals, fields** | **camelCase** or **snake_case** in tests | `par_decorated`, `csv_parse` |
| **Modules** | short lowercase | `io`, `csv`, `summary` |

On **`lic` `main` today**, encapsulation uses **`type Name = object`** with **`public` / `private` fields** — not a separate `class` keyword. See the real test composite below.

---

## Real code: public vs private fields

From [`lic` encapsulation tests](https://github.com/li-langverse/lic/tree/main/li-tests/encapsulation) ([`examples/object_encapsulation.li`](examples/object_encapsulation.li) — compiles as typecheck negative for `leak`):

```li
type Point = object
  public x: int
  private tag: int

type Vault = object
  public open: int
  private secret: int

def leak(v: Vault) -> int
  requires true
  ensures true
  decreases 0
=
  return v.secret   # rejected: private field access outside Vault
```

| Modifier | Meaning in current `lic` tests |
|----------|--------------------------------|
| **public** | Field visible to clients of the type |
| **private** | Field only legal inside methods tied to the defining type |

---

## Shareable (editor screenshot, local)

Regenerate (not committed): `python3 scripts/render-li-code-image.py --all` → `docs/language/assets/li-code-encapsulation-editor.png`

**Proof note:** contracts on exported APIs are the usual audit surface — see [`provability-gaps`](https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md).
