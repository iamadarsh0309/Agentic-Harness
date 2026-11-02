import { chromium } from "playwright";

const [, , outPath, widthArg] = process.argv;
const width = Number(widthArg ?? 375);

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width, height: 800 } });
await page.goto("http://localhost:8080", { waitUntil: "networkidle" });

await page.fill("#source", "hallucinate(“the slop must flow”)✨");
await page.click("#run");
await page.waitForFunction(
  () => document.getElementById("output").textContent !== "Running…",
);

const output = await page.textContent("#output");
const metrics = await page.evaluate(() => {
  const pre = document.getElementById("output");
  const rect = pre.getBoundingClientRect();
  return {
    viewport: window.innerWidth,
    documentScrollWidth: document.documentElement.scrollWidth,
    preWidth: Math.round(rect.width),
    preRight: Math.round(rect.right),
    overflowsViewport: rect.right > window.innerWidth,
  };
});

await page.screenshot({ path: outPath, fullPage: true });

// Long unbroken token must still wrap rather than widen the pane.
await page.fill(
  "#source",
  "hallucinate(“" + "slop".repeat(60) + "”)✨",
);
await page.click("#run");
await page.waitForFunction(
  () => document.getElementById("output").textContent !== "Running…",
);
const longLine = await page.evaluate(() => {
  const pre = document.getElementById("output");
  return {
    documentScrollWidth: document.documentElement.scrollWidth,
    preRight: Math.round(pre.getBoundingClientRect().right),
    overflowsViewport: pre.getBoundingClientRect().right > window.innerWidth,
  };
});

console.log(JSON.stringify({ output, ...metrics, longLine }, null, 2));
await browser.close();
