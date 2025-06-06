import eslint from "@eslint/js";
import eslintPluginPrettierRecommended from "eslint-plugin-prettier/recommended";
import { globalIgnores } from "eslint/config";
import globals from "globals";
import parser from "vue-eslint-parser";
import tseslint from "typescript-eslint";
import typescriptEslint from "@typescript-eslint/eslint-plugin";
import withNuxt from "./.nuxt/eslint.config.mjs";

export default withNuxt(
  eslint.configs.recommended,
  tseslint.configs.recommended,
  eslintPluginPrettierRecommended,
  [
    globalIgnores([
      ".nuxt/**/*",
      ".output/**/*",
      "assets/uswds/**/*",
      "dist/**/*",
      "node_modules/**/*",
    ]),
    {
      plugins: {
        "@typescript-eslint": typescriptEslint,
      },

      languageOptions: {
        globals: {
          ...globals.browser,

          emit: true,
          navigateTo: true,
          useCookie: true,
          useFetch: true,
          useRoute: true,
          useRuntimeConfig: true,

          // Functions
          cancelFormSubmission: true,
          fetchArtifact: true,
          handleHttpError: true,
          inputErrorAlert: true,
          isValidArtifact: true,
          isValidEvidence: true,
          isValidReport: true,
          isValidTestResults: true,
          isValidTestSuite: true,
          loadFindings: true,
          requestErrorAlert: true,
          resetFormErrors: true,
          successfulArtifactSubmission: true,
          useClassificationOptions: true,
          useProblemTypeOptions: true,
          isValidNegotiation: true,

          // Types
          Dictionary: true,
          MetricDescriptor: true,
          GoalDescriptor: true,
          ModelIODescriptor: true,
          ModelDescriptor: true,
          LabelDescriptor: true,
          FieldDescriptor: true,
          DataDescriptor: true,
          SystemDescriptor: true,
          QASDescriptor: true,
          TestResults: true,
          User: true,
          UserUpdateBody: true,
        },

        parser: parser,
        ecmaVersion: "latest",
        sourceType: "module",

        parserOptions: {
          parser: "@typescript-eslint/parser",
        },
      },

      rules: {
        "vue/multi-word-component-names": [
          "error",
          {
            ignores: ["index"],
          },
        ],

        "vue/no-mutating-props": [
          "error",
          {
            shallowOnly: true,
          },
        ],

        "vue/no-required-prop-with-default": "off",

        "@typescript-eslint/no-unused-vars": [
          "error",
          {
            varsIgnorePattern: "emits|props",
          },
        ],
      },
    },
  ],
);
