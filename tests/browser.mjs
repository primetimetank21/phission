import assert from "node:assert/strict";
import fs from "node:fs/promises";
import { execFileSync } from "node:child_process";
import path from "node:path";
import { chromium } from "playwright";
import AxeBuilder from "@axe-core/playwright";

// Run against an already-started local production server, never a public inbox.
const origin = new URL(process.env.PHISSION_URL || "http://127.0.0.1:3000")
  .origin;
assert.ok(
  /^http:\/\/(127\.0\.0\.1|localhost)(:\d+)?$/.test(origin),
  "Use a loopback HTTP server",
);
const out = path.resolve(".scratch/browser-validation");
await fs.mkdir(out, { recursive: true });
const report = {
  startedAt: new Date().toISOString(),
  url: origin,
  label: "Local production build, not deployed",
  checks: [],
  accessibility: [],
  requests: [],
  websockets: [],
  errors: [],
  externalAttempts: [],
  behaviorIssues: [],
  captures: [],
};
report.sourceCommit = execFileSync("git", ["rev-parse", "HEAD"], {
  encoding: "utf8",
}).trim();
report.sourceDirty =
  execFileSync("git", ["status", "--porcelain"], {
    encoding: "utf8",
  }).trim() !== "";
const browser = await chromium.launch({ headless: true });
report.browser = browser.version();
const contexts = [];
function check(name, condition) {
  assert.ok(condition, name);
  report.checks.push(name);
}
async function context(options = {}) {
  const ctx = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    ...options,
  });
  contexts.push(ctx);
  await ctx.route("**/*", (route) => {
    const u = route.request().url();
    if (/^https?:/.test(u) && new URL(u).origin !== origin) {
      report.externalAttempts.push(u);
      return route.abort();
    }
    return route.continue();
  });
  ctx.on("request", (r) =>
    report.requests.push({
      method: r.method(),
      url: r.url(),
      type: r.resourceType(),
    }),
  );
  ctx.on("page", (page) => {
    page.on("pageerror", (e) => report.errors.push(e.message));
    page.on("websocket", (ws) => report.websockets.push(ws.url()));
  });
  return ctx;
}
async function ready(ctx) {
  const page = await ctx.newPage();
  const response = await page.goto(origin);
  check("Root returns HTTP 200", response.status() === 200);
  await page.locator(".message-card").first().waitFor();
  check(
    "Exactly five synthetic messages",
    (await page.locator(".message-card").count()) === 5,
  );
  return page;
}
async function select(page, sender) {
  await page.getByRole("button", { name: new RegExp(sender) }).click();
  await page.waitForFunction(
    (name) =>
      document
        .querySelector(".message-card[aria-pressed=true]")
        ?.textContent.includes(name),
    sender,
  );
  await page.waitForFunction(
    () => document.activeElement?.id === "message-heading",
  );
  await page.locator(".result").waitFor({ state: "detached" });
  check(
    `Message selection moves focus: ${sender}`,
    await page
      .locator("#message-heading")
      .evaluate((el) => document.activeElement === el),
  );
  check(
    `Result resets on message selection: ${sender}`,
    (await page.locator(".result").count()) === 0,
  );
}
async function analyze(page, index, title, score) {
  await page.locator(".link-choice").nth(index).click();
  await page.waitForFunction(
    (i) =>
      document
        .querySelectorAll(".link-choice")
        [i]?.getAttribute("aria-pressed") === "true",
    index,
  );
  await page.locator(".result").waitFor({ state: "detached" });
  await page
    .getByRole("button", { name: "Run demo analysis", exact: true })
    .click();
  await page.getByRole("heading", { name: title, exact: true }).waitFor();
  await page.getByText(score, { exact: true }).waitFor();
  check(
    `Correct result: ${title} (${score})`,
    (await page.locator(".score-label").innerText()) === score,
  );
  const selected = await page
    .locator(".link-choice[aria-pressed=true] .url-text")
    .innerText();
  check(
    "Verdict stays bound to selected destination",
    (await page.locator(".result-target").innerText()) === selected,
  );
}
async function axe(page, name) {
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"])
    .analyze();
  const violations = results.violations.map((v) => ({
    id: v.id,
    impact: v.impact,
    description: v.description,
    nodes: v.nodes.map((n) => ({
      target: n.target,
      summary: n.failureSummary,
    })),
  }));
  report.accessibility.push({
    name,
    violations,
    incomplete: results.incomplete.map((v) => ({
      id: v.id,
      nodes: v.nodes.length,
    })),
    passes: results.passes.length,
  });
  if (violations.length === 0)
    report.checks.push(`No automated WCAG violations: ${name}`);
}
async function capture(page, name, options = { fullPage: true }) {
  await page.screenshot({ path: `${out}/${name}.png`, ...options });
  report.captures.push({
    file: `${name}.png`,
    url: page.url(),
    viewport: page.viewportSize(),
    theme: "light",
    emulated: true,
    capturedAt: new Date().toISOString(),
  });
}
try {
  const desktopContext = await context();
  const page = await ready(desktopContext);
  check(
    "Explicit synthetic notice",
    await page
      .getByText("Synthetic emails. No inbox connection.", { exact: true })
      .isVisible(),
  );
  check(
    "Analysis initially disabled",
    await page
      .getByRole("button", { name: "Run demo analysis", exact: true })
      .isDisabled(),
  );
  check(
    "No active email destination links",
    (await page.locator('a[href*=".example"], a[href*=".test"]').count()) === 0,
  );
  await axe(page, "desktop initial");
  await capture(page, "desktop-inbox");
  await analyze(
    page,
    0,
    "Lower signal, not a guarantee",
    "Fixture score: 0 / 100",
  );
  await capture(page, "desktop-zero");
  await page.locator(".link-choice").nth(1).click();
  await page.waitForFunction(() => document.querySelector(".result") === null);
  check(
    "Changing links removes prior verdict",
    (await page.locator(".result").count()) === 0,
  );
  await analyze(
    page,
    1,
    "Lower signal, not a guarantee",
    "Fixture score: 12 / 100",
  );
  await select(page, "Account Support");
  await analyze(page, 0, "High concern", "Fixture score: 96 / 100");
  check(
    "Query and fragment preserved",
    (await page.locator(".result-target").innerText()) ===
      "https://account-review.test/verify?source=email&step=confirm#account",
  );
  await axe(page, "desktop high concern");
  await capture(page, "desktop-high");
  await page.locator(".result").screenshot({ path: `${out}/result-high.png` });
  const second = await ready(await context());
  check(
    "New session has no inherited result",
    (await second.locator(".result").count()) === 0,
  );
  await select(second, "People Team");
  await analyze(second, 0, "Reasons for caution", "Fixture score: 80 / 100");
  check(
    "Independent session leaves first verdict unchanged",
    (await page.locator("#result-title").innerText()) === "High concern",
  );
  await select(page, "Parcel Desk");
  check(
    "Attachment boundary is visible",
    (await page.locator(".coverage").innerText()) ===
      "Partial coverage. Attachments are not analyzed.",
  );
  await analyze(page, 0, "No verdict available", "No usable score");
  await axe(page, "desktop unknown");
  await capture(page, "desktop-unknown");
  await select(page, "robin@garden");
  check(
    "No-links state is explicit",
    await page
      .getByText("No HTTP(S) links found in readable text", { exact: true })
      .isVisible(),
  );
  check(
    "No-links state is not a safety claim",
    await page.getByText(/This is not a safety verdict/).isVisible(),
  );
  check(
    "No analysis button for no-links message",
    (await page
      .getByRole("button", { name: "Run demo analysis", exact: true })
      .count()) === 0,
  );

  const keyboard = await ready(
    await context({ viewport: { width: 1280, height: 900 } }),
  );
  await keyboard.keyboard.press("Tab");
  check(
    "First keyboard target is skip link",
    (await keyboard.evaluate(() => document.activeElement.textContent)) ===
      "Skip to demo",
  );
  await keyboard.keyboard.press("Enter");
  await keyboard.waitForFunction(() => document.activeElement.id === "demo");
  check(
    "Skip link focuses workspace",
    (await keyboard.evaluate(() => document.activeElement.id)) === "demo",
  );
  await keyboard.keyboard.press("Tab");
  check(
    "Keyboard enters message list",
    await keyboard.evaluate(() =>
      document.activeElement.classList.contains("message-card"),
    ),
  );
  await keyboard.keyboard.press("Space");
  await keyboard.waitForFunction(
    () => document.activeElement?.id === "message-heading",
  );
  await keyboard.keyboard.press("Tab");
  check(
    "Keyboard reaches link selection",
    await keyboard.evaluate(() =>
      document.activeElement.classList.contains("link-choice"),
    ),
  );
  await keyboard.keyboard.press("Space");
  await keyboard.waitForFunction(
    () =>
      document.querySelector(".link-choice")?.getAttribute("aria-pressed") ===
        "true" && !document.querySelector(".primary-button")?.disabled,
  );
  await keyboard.keyboard.press("Tab");
  await keyboard.keyboard.press("Tab");
  check(
    "Keyboard reaches analysis button",
    (await keyboard.evaluate(() => document.activeElement.textContent)) ===
      "Run demo analysis",
  );
  const focusStyle = await keyboard.evaluate(() => ({
    style: getComputedStyle(document.activeElement).outlineStyle,
    width: getComputedStyle(document.activeElement).outlineWidth,
  }));
  check(
    "Visible keyboard focus outline",
    focusStyle.style === "solid" && parseInt(focusStyle.width) >= 2,
  );
  await keyboard.keyboard.press("Enter");
  await keyboard.getByText("Fixture score: 0 / 100", { exact: true }).waitFor();
  check(
    "Keyboard-only analysis completes",
    (await keyboard.locator("[role=status]").innerText()) ===
      "Simulated result: Lower signal, not a guarantee.",
  );

  const mobile = await ready(
    await context({
      viewport: { width: 390, height: 844 },
      isMobile: true,
      hasTouch: true,
      reducedMotion: "reduce",
    }),
  );
  await capture(mobile, "mobile-inbox");
  await select(mobile, "People Team");
  check(
    "Deceptive HTML label exposed separately",
    (await mobile.locator(".link-label").innerText()) ===
      "Label in email: “Open the staff portal”",
  );
  await analyze(mobile, 0, "Reasons for caution", "Fixture score: 80 / 100");
  await axe(mobile, "mobile caution, reduced motion");
  await capture(mobile, "mobile-caution");
  await mobile.locator(".result").scrollIntoViewIfNeeded();
  await capture(mobile, "mobile-result", { fullPage: false });
  await mobile
    .getByRole("link", { name: "← Back to messages", exact: true })
    .click();
  await mobile.waitForFunction(
    () => document.activeElement.id === "inbox-title",
  );
  check(
    "Mobile return link focuses inbox",
    (await mobile.evaluate(() => document.activeElement.id)) === "inbox-title",
  );
  check(
    "Reduced motion disables card transitions",
    (await mobile
      .locator(".message-card")
      .first()
      .evaluate((el) => getComputedStyle(el).transitionDuration)) === "0s",
  );
  for (const width of [320, 390, 640, 768, 1024, 1440]) {
    await mobile.setViewportSize({ width, height: 900 });
    check(
      `No horizontal overflow at ${width}px`,
      await mobile.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    );
  }
  await mobile.setViewportSize({ width: 320, height: 800 });
  await capture(mobile, "narrow-320");

  const nojs = await (await context({ javaScriptEnabled: false })).newPage();
  const nojsResponse = await nojs.goto(origin);
  check("No-JS page returns HTTP 200", nojsResponse.status() === 200);
  check(
    "No-JS introduction readable",
    await nojs.getByRole("heading", { level: 1 }).isVisible(),
  );
  check(
    "No-JS limitation explicit",
    (await nojs.locator("noscript").innerText()) ===
      "This demo needs JavaScript and a running Reflex server. No mailbox or scanning service is connected.",
  );
  const missing = await (await context()).newPage();
  const notFound = await missing.goto(`${origin}/does-not-exist/nested`);
  check("Unknown nested route returns HTTP 404", notFound.status() === 404);
  check("No application JavaScript errors", report.errors.length === 0);
  check(
    "No attempted external browser requests",
    report.externalAttempts.length === 0,
  );
  check(
    "All WebSockets stay on local origin",
    report.websockets.every((u) => new URL(u).host === new URL(origin).host),
  );
  check("No keyboard/navigation issues", report.behaviorIssues.length === 0);
  check(
    "All automated accessibility scans passed",
    report.accessibility.every((r) => r.violations.length === 0),
  );
  report.ok = true;
} catch (error) {
  report.ok = false;
  report.failure = error.stack;
  console.error(error);
  process.exitCode = 1;
} finally {
  for (const ctx of contexts) await ctx.close();
  await browser.close();
  report.finishedAt = new Date().toISOString();
  await fs.writeFile(
    `${out}/browser-results.json`,
    JSON.stringify(report, null, 2),
  );
  console.log(
    JSON.stringify(
      {
        ok: report.ok,
        checks: report.checks.length,
        accessibility: report.accessibility,
        errors: report.errors,
        externalAttempts: report.externalAttempts,
        behaviorIssues: report.behaviorIssues,
        failure: report.failure,
      },
      null,
      2,
    ),
  );
}
