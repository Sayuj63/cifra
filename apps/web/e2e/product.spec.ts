import { expect, test } from "@playwright/test";

test("candidate receives real prediction and explanation", async ({ page }) => {
  test.setTimeout(70_000); // The first local SHAP request can initialize slowly.
  const errors: string[] = [];
  page.on("pageerror", error => errors.push(error.message));
  await page.goto("/estimate");
  await expect(page.getByRole("button", { name: /Estimate salary/ })).toBeEnabled();
  await page.getByRole("button", { name: /Estimate salary/ }).click();
  await expect(page.getByText("Estimated annual compensation", { exact: false })).toBeVisible();
  await expect(page.getByText("Why this estimate?")).toBeVisible({ timeout: 30_000 });
  await expect(page.getByText("Tree SHAP grouped by raw feature", { exact: false })).toBeVisible();
  await expect(page.getByText("90% prediction interval", { exact: false })).toBeVisible();
  await page.screenshot({ path: "test-results/estimate-desktop.png", fullPage: true });
  expect(errors).toEqual([]);
});

test("analysis routes load real reports on mobile", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  await page.getByRole("button", { name: "Menu" }).click();
  await page.getByRole("link", { name: "Model Lab", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Five regressors. One evaluation protocol." })).toBeVisible();
  await expect(page.getByText("Champion", { exact: true })).toBeVisible();
  await page.getByRole("button", { name: "Menu" }).click();
  await page.getByRole("link", { name: "Fairness" }).click();
  await expect(page.getByText("Errors and coverage by city")).toBeVisible();
  await page.screenshot({ path: "test-results/fairness-mobile.png", fullPage: true });
});

test("growth curve responds to a profile change through the API", async ({ page }) => {
  await page.goto("/explain");
  const selectedEstimate = page.getByText(/^8 years: ₹/);
  await expect(selectedEstimate).toBeVisible();
  const before = await selectedEstimate.textContent();
  const response = page.waitForResponse(r => r.url().endsWith("/curve") && r.request().method() === "POST");
  await page.getByLabel("City").selectOption("Kolkata");
  await response;
  await expect(selectedEstimate).not.toHaveText(before ?? "");
  await expect(page.getByText("Tree SHAP grouped by raw feature", { exact: false })).toBeVisible();
});
