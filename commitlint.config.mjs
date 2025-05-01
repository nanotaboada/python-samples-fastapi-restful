import conventional from "@commitlint/config-conventional";

export default {
  ...conventional,
  rules: {
    "header-max-length": [2, "always", 80],
    "body-max-line-length": [2, "always", 80],
  },
  ignores: [
    // bypass Dependabot-style commits
    (message) => /^chore\(deps(-dev)?\): bump /.test(message),
    (message) => /Signed-off-by: dependabot\[bot\]/.test(message),
  ],
};
