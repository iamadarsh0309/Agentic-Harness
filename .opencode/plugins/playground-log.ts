import { appendFile, mkdir } from "node:fs/promises"
import { join } from "node:path"
import { Plugin } from "@opencode/plugin"

const MARKER = "playground/server.py"

export default Plugin.define({
  id: "applymaxxing.playground-log",
  setup: async (ctx) => {
    const projectRoot = ctx.location.directory
    const logPath = join(projectRoot, "logs", "plugin-playground.log")

    await ctx.shell.hook("create.before", async (input) => {
      if (!input.command.includes(MARKER)) return

      await mkdir(join(projectRoot, "logs"), { recursive: true })
      await appendFile(logPath, "playground shell request\n")
    })
  },
})
