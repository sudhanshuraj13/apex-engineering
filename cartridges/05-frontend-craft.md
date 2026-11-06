# 05 — Frontend Craft, React 19 & WCAG Accessibility Cartridge
**Fused Winners:** `impeccable`, `hallmark`, `vercel-react-best-practices`, `wcag-audit-patterns`

## 1. Negative Constraints (FORBIDDEN — Hallmark & Impeccable Design Floor)
- NEVER ship generic AI slop: no purple-to-blue gradients, card-inside-a-card layouts, or emoji icons (Hallmark Floor).
- NEVER use `transition: all` or animate layout properties (`width`, `height`, `top`); use discrete transforms and opacity.
- NEVER add `"use client"` to top-level page/layout trees when React Server Components (RSC) can fetch data on the server.
- NEVER use `useEffect` for data fetching or derived state calculations.
- NEVER hardcode raw hex colors (`#ff0000`); every color and font must map to declared design tokens (`bg-primary`, `text-muted-foreground`).
- NEVER leave interactive elements without instant `:focus-visible` outlines, ARIA labels, and explicit disabled/loading states.
- NEVER create unstyled empty states; provide intentional typography hierarchy, breathing room, and clear call-to-actions (Impeccable Craft).

## 2. Canonical Code Skeleton (Bespoke Accessible RSC + Optimistic Action Form)
```tsx
"use client";
import { useActionState } from "react";

export function BillingActionButton({ tenantId }: { tenantId: string }) {
  const [state, formAction, isPending] = useActionState(upgradePlanAction, { error: null });

  return (
    <form action={formAction} className="flex flex-col gap-3">
      <input type="hidden" name="tenantId" value={tenantId} />
      <button
        type="submit"
        disabled={isPending}
        aria-busy={isPending}
        className="inline-flex items-center justify-center rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow-sm transition-colors hover:bg-primary/90 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring disabled:opacity-50"
      >
        {isPending ? "Upgrading..." : "Upgrade to Enterprise"}
      </button>
      {state?.error && (
        <p role="alert" className="text-sm font-medium text-destructive">{state.error}</p>
      )}
    </form>
  );
}
```

## 3. Exit Gate & Handoff
- **Gate Check:** Production build/typecheck + `python scripts/apex_ctl.py verify` = `Exit Code 0`.
- **Next Recommended Skill:** `06-security-zero-trust`
