## Supply-chain security rule

Never install packages, tools or other external dependencies without explicit permission from the user. This
includes `uv add`, but also `uv run --with` and `uvx`, their equivalents for `npm` and `npx`, and any other
package manager.
