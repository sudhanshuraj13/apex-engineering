# 05 — Frontend Craft, React 19 & WCAG Accessibility Cartridge
**Fused Winners:** `vercel-react-best-practices`, `composition-patterns`, `wcag-audit-patterns`, `web-performance-optimization`

## 1. Negative Constraints (FORBIDDEN)
- NEVER add `"use client"` to top-level page/layout trees when React Server Components (RSC) can fetch data on the server.
- NEVER use `useEffect` for data fetching or derived state calculations.
- NEVER hardcode raw hex colors (`#ff0000`); use semantic design tokens (`bg-destructive`, `text-muted-foreground`).
- NEVER ship interactive elements without keyboard focus states, `aria-label` (for icon buttons), and explicit loading/disabled states.

## 2. Canonical Code Skeleton (Accessible RSC + Optimistic Action Form)
```tsx
"use client";
import { useActionState } from "react";

export function BillingActionButton({ tenantId }: { tenantId: string }) {
  const [state, formAction, isPending] = useActionState(upgradePlanAction, { error: null });

  return (
    <form action={formAction} className="flex flex-col gap-2">
      <input type="hidden" name="tenantId" value={tenantId} />
      <button
        type="submit"
        disabled={isPending}
        aria-busy={isPending}
        className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground focus-visible:outline-2 disabled:opacity-50"
      >
        {isPending ? "Upgrading..." : "Upgrade to Enterprise"}
      </button>
      {state?.error && (
        <p role="alert" className="text-sm text-destructive">{state.error}</p>
      )}
    </form>
  );
}
```

## 3. Exit Gate & Handoff
- **Gate Check:** Production build/typecheck + `python scripts/apex_ctl.py verify` = `Exit Code 0`.
- **Next Recommended Skill:** `06-security-zero-trust`
