# 07 — DevOps, Rootless Docker, CI/CD & OTel Cartridge
**Fused Winners:** `docker-expert`, `container-security-hardening`, `github-actions-templates`, `distributed-tracing`

## 1. Negative Constraints (FORBIDDEN)
- NEVER run production containers as `root`; always create and switch to a non-root `USER` (e.g., `node` or `appuser`).
- NEVER use `:latest` tags in `Dockerfile` base images; pin deterministic versions (`node:22-alpine`).
- NEVER deploy services without `/healthz` (liveness) and `/readyz` (DB/Redis readiness) endpoints and a `SIGTERM` graceful shutdown handler.

## 2. Canonical Code Skeleton (Multi-Stage Rootless Dockerfile + Graceful Drain)
```dockerfile
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build && npm prune --production

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -g 1001 -S appgroup && adduser -S appuser -u 1001 -G appgroup
COPY --from=builder --chown=appuser:appgroup /app/dist ./dist
COPY --from=builder --chown=appuser:appgroup /app/node_modules ./node_modules
USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s CMD wget -qO- http://localhost:3000/readyz || exit 1
CMD ["node", "dist/server.js"]
```

## 3. Exit Gate & Handoff
- **Gate Check:** Config/lint verification + `python scripts/apex_ctl.py verify` = `Exit Code 0`.
- **Next Recommended Skill:** `COMPLETE` (or `08-deep-debugger` on failure)
