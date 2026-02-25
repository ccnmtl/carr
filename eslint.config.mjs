import globals from 'globals';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import js from '@eslint/js';
import { FlatCompat } from '@eslint/eslintrc';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const compat = new FlatCompat({
    baseDirectory: __dirname,
    recommendedConfig: js.configs.recommended,
    allConfig: js.configs.all
});

export default [
    ...compat.extends('eslint:recommended'),
    {
        languageOptions: {
            globals: {
                ...globals.browser,
                ...globals.jquery,
                $$: true,
                forEach: true,
                map: true,
                setStyle: true,
                MochiKit: true,
                queryString: true,
                serializeJSON: true,
                hideElement: true,
                getElementsByTagAndClassName: true,
                showElement: true,
                logDebug: true,
                addElementClass: true,
                removeElementClass: true,
                filter: true,
                loadJSONDoc: true,
                list: true,
                range: true,
                itemgetter: true,
                findValue: true,
                setDisplayForElement: true,
                DIV: true,
                swapDOM: true,
                zip: true,
                getNodeAttribute: true,
                log: true,
                getElement: true,
            },
        },

        rules: {
            indent: ['error', 4],
            'linebreak-style': ['error', 'unix'],

            'no-unused-vars': ['error', {
                vars: 'all',
                args: 'none',
            }],

            quotes: ['error', 'single'],
            semi: ['error', 'always'],

            'max-len': [2, {
                code: 80,
                tabWidth: 4,
                ignoreUrls: true,
            }],

            'space-before-function-paren': ['error', 'never'],
            'space-in-parens': ['error', 'never'],
            'no-trailing-spaces': ['error'],

            'key-spacing': ['error', {
                beforeColon: false,
            }],

            'func-call-spacing': ['error', 'never'],
        },
    },
];
