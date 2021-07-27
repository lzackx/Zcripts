/**
 * Metro configuration for React Native
 * https://github.com/facebook/react-native
 *
 * @format
 */


const { mergeConfig } = require("metro-config");
let Metro = require("metro");
const defaultConfig = Metro.loadConfig();

const pathSep = require('path').sep;
const fs = require("fs");


function createModuleIdFactory() {
    const pathRoot = __dirname;
    const pathBaseModules = pathRoot + pathSep + 'bundles' + pathSep + 'modules' + pathSep + 'base_modules.ios.json';
    console.info(pathBaseModules);
    let currentModuleId = 0;
    let currentBaseModules = require(pathBaseModules);
    return path => {
        let rPath = path.substring(pathRoot.length);
        console.log(`path: ${path}`);
        console.log(`rPath: ${rPath}`);
        if (!currentBaseModules.hasOwnProperty(rPath)) {
            let moduleId = currentModuleId;
            currentModuleId = currentModuleId + 1;
            currentBaseModules[rPath] = moduleId;
            console.info(`${rPath} => ${moduleId}`);
            fs.writeFileSync(pathBaseModules, JSON.stringify(currentBaseModules));
            return moduleId;
        } else {
            return currentBaseModules[rPath];
        }
    };
}

function processModuleFilter(module) {
    console.log(module);
    return true;
}

const baseBundleConfig = {
    // resolver: {
    //     /* resolver options */
    // },
    // transformer: {
    //     /* transformer options */
    // },
    serializer: {
        createModuleIdFactory: createModuleIdFactory,
        processModuleFilter: processModuleFilter,
    },
    // server: {
    //     /* server options */
    // }
    /* general options */
};

module.exports = mergeConfig(defaultConfig, baseBundleConfig);