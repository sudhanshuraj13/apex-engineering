#!/usr/bin/env node
/**
 * Cross-platform NPX / Global CLI Wrapper for Apex-Engineering (v3.3)
 * Delegates `npx apex-engineering` or `apex` commands to `scripts/bharat_harness.py`.
 */
const { spawnSync } = require("child_process");
const path = require("path");

const harnessScript = path.resolve(__dirname, "..", "scripts", "bharat_harness.py");
const args = process.argv.slice(2);

function resolvePythonBin() {
  for (const cmd of ["python3", "python", "py"]) {
    const check = spawnSync(cmd, ["--version"], { stdio: "ignore", shell: true });
    if (check.status === 0) return cmd;
  }
  console.error("[APEX ERROR] Python 3.10+ is required to run Apex-Engineering.");
  process.exit(1);
}

const pyBin = resolvePythonBin();
const result = spawnSync(pyBin, [harnessScript, ...args], {
  stdio: "inherit",
  env: process.env
});

process.exit(result.status !== null ? result.status : 0);