import { appendFile, mkdir } from "node:fs/promises"
import { join } from "node:path"
import { Plugin } from "@opencode/plugin"

const FILE_CHANGING_TOOLS = new Set(["edit", "write", "patch"])

export default Plugin.define({
  id: "applymaxxing.edit-log",
  setup: async (ctx) => {
    const projectRoot = ctx.location.directory
    const logPath = join(projectRoot, "logs", "plugin-tools.log")

    await ctx.tool.hook("execute.after", async (input) => {
      if (!FILE_CHANGING_TOOLS.has(input.tool)) return
      if (input.status !== "completed") return

      await mkdir(join(projectRoot, "logs"), { recursive: true })
      await appendFile(logPath, JSON.stringify({ tool: input.tool, status: "completed" }) + "\n")
    })
  },
})
