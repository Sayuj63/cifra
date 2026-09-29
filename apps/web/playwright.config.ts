import { defineConfig, devices } from "@playwright/test";
import { existsSync } from "node:fs";
import path from "node:path";

const venvPython = path.resolve(__dirname, "../../.venv/Scripts/python.exe");
const python = process.platform === "win32" && existsSync(venvPython) ? `"${venvPython}"` : "python";

export default defineConfig({
  testDir: "./e2e",
  timeout: 30_000,
  retries: 0,
  use: { baseURL: "http://localhost:3000", ...devices["Desktop Chrome"], channel: "msedge" },
  webServer: [
    { command: `${python} -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000`, cwd: path.resolve(__dirname, "../.."), url: "http://localhost:8000/api/v1/health", reuseExistingServer: true, timeout: 30_000 },
    { command: "npm run dev -- --hostname localhost", cwd: __dirname, url: "http://localhost:3000", reuseExistingServer: true, timeout: 60_000 },
  ],
});
