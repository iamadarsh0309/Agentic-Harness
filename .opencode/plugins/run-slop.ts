import { Plugin } from "@opencode/plugin"

export default Plugin.define({
  id: "applymaxxing.run-slop",
  setup: async (ctx) => {
    const projectRoot = ctx.location.directory

    await ctx.tool.transform((tools) => {
      tools.add({
        name: "run_slop",
        description: "Run a SlopLang program with Sloperator and return its output",
        input: {
          type: "object",
          properties: {
            path: { type: "string" },
          },
          required: ["path"],
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async (input) => {
          const { path } = input as { path: string }
          const process = Bun.spawn(["uv", "run", "--no-active", "sloperator.py", path], {
            cwd: projectRoot,
            stdout: "pipe",
            stderr: "pipe",
          })

          const [stdout, stderr, exitCode] = await Promise.all([
            new Response(process.stdout).text(),
            new Response(process.stderr).text(),
            process.exited,
          ])

          return { content: JSON.stringify({ stdout, stderr, exitCode }) }
        },
      })
    })
  },
})
