module.exports = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    // Force "type(scope): message" (scope obligatoire)
    "scope-empty": [2, "never"],
    // Types autorisés demandés
    "type-enum": [
      2,
      "always",
      ["feat", "fix", "docs", "style", "refactor", "test", "chore", "ci"],
    ],
    // Ex: "fix(api): corrige ..."
    "subject-empty": [2, "never"],
    "subject-case": [0],
  },
};
