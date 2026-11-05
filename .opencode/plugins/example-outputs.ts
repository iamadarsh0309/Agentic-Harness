import { readdir } from "node:fs/promises"
import { join } from "node:path"
import { Plugin } from "@opencode/plugin"

interface ExampleResult {
  name: string
  exitCode: number
  firstLine: string
}

export default Plugin.define({
  id: "applymaxxing.example-outputs",
  setup: async (ctx) => {
    const projectRoot = ctx.location.directory

    await ctx.tool.transform((tools) => {
      tools.add({
        name: "example_outputs",
        description:
          "Run every examples/*.slop program and report each one's exit code and first output line",
        input: {
          type: "object",
          properties: {},
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async () => {
          const examplesDir = join(projectRoot, "examples")
          const files = (await readdir(examplesDir))
            .filter((file) => file.endsWith(".slop"))
            .sort()

          const examples: ExampleResult[] = await Promise.all(
            files.map(async (file) => {
              const process = Bun.spawn(
                ["uv", "run", "--no-active", "sloperator.py", join("examples", file)],
                {
                  cwd: projectRoot,
                  stdout: "pipe",
                  stderr: "pipe",
                },
              )

              const [stdout, exitCode] = await Promise.all([
                new Response(process.stdout).text(),
                process.exited,
              ])

              return {
                name: file,
                exitCode,
                firstLine: stdout.split("\n")[0] ?? "",
              }
            }),
          )

          return { content: JSON.stringify({ examples }) }
        },
      })
    })
  },
})
