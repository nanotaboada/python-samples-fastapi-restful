// .commitlint.config.mjs
import conventional from '@commitlint/config-conventional';

export default {
    ...conventional,
    rules: {
        'header-max-length': [2, 'always', 80],
        'body-max-line-length': [2, 'always', 80],
    },
    ignores: [
        // skip any commit whose body contains the Dependabot signature
        (message) => message.includes('Signed‑off‑by: dependabot[bot]'),
        // skip any Dependabot‑style bump header
        (message) => /^chore\(deps(-dev)?\): bump /.test(message),
    ],
};
