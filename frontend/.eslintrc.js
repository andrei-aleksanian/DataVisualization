module.exports = {
  env: {
    browser: true,
    es2021: true,
    jest: true,
  },
  ignorePatterns: ['node_modules', 'build', 'public', '.eslintrc.js'],
  extends: ['plugin:react/recommended', 'airbnb-typescript', 'plugin:prettier/recommended', 'prettier'],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    project: 'tsconfig.json',
    tsconfigRootDir: __dirname,
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 12,
    sourceType: 'module',
  },
  plugins: ['react', 'react-hooks', '@typescript-eslint', 'prettier'],
  rules: {
    'react/react-in-jsx-scope': 'off',
    'react/jsx-props-no-spreading': 'off'
  },
};
