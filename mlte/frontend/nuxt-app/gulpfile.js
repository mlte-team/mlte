/* gulpfile.js */

/**
 * Import uswds-compile
 */

const uswds = require("@uswds/compile"); // eslint-disable-line @typescript-eslint/no-require-imports

/**
 * USWDS version
 * Set the major version of USWDS you're using
 * (Current options are the numbers 2 or 3)
 */
uswds.settings.version = 3;

/**
 * Path settings
 * Set as many as you need
 */
uswds.paths.dist.css = "./assets/uswds/css";
uswds.paths.dist.theme = "./sass/uswds";

/**
 * Exports
 * Add as many as you need
 */
exports.init = uswds.init;
exports.compile = uswds.compile;
exports.watch = uswds.watch;
