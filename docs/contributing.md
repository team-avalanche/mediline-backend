# Contributing

- For writing proper markdown, download the given VS Code Extension
  - **Markdown All in One** by *Yu Zhang* v3.5.1 or above
  - Try to minimize the error squiggles produce by this extension.
  - Although we are not enforcing it.

- For Python, the code style is enforced by `black`, `isort` and `ruff`.
  - While you are coding you can run `./scripts/lint.sh`
    - to run black, isort and ruff on your code.
  - black and isort automatically formats your code.
  - ruff will produce errors.
    - You may need to manually fix them,
    - or for some cases that can be autofixed with `ruff --fix .`

- Learn about [pre-commit](https://pre-commit.com) and use it correctly.
  - We are using it to enforce code quality.
  - `pre-commit install` to install git hooks.
  - Run `pre-commit`to run checks on **staged changes** manually.
  - If you see any errors produced by `black`, `isort` or `ruff` fix them.
  - Stage those file changes, by `git add`
  - Run `pre-commit` again, to see green "Passed" messages.
  - Now commit your staged changes and push to GitHub.
  - If you dont fix these issues,
    - the checks run on GitHub actions would produce "failed",
    - and your PR would not be accepted.
- Check Git Guidelines on team's discord.
