/**
 * Metro configuration for React Native
 * https://github.com/facebook/react-native
 *
 * @format
 */


const { mergeConfig } = require("metro-config");
let Metro = require("metro");
const defaultConfig = Metro.loadConfig();

const pathRoot = __dirname;
const pathSep = require('path').sep;
const pathBaseModules = pathRoot + pathSep + 'bundles' + pathSep + 'modules' + pathSep + 'base_modules.ios.json';
console.info(pathBaseModules);
const currentBaseModules = require(pathBaseModules);
const currentModules = {}

function createModuleIdFactory() {
  let currentModuleId = 10000; //Object.keys(currentBaseModules).length;
  return path => {
    let rPath = path.substring(pathRoot.length);
    console.info(rPath);
    if (currentBaseModules.hasOwnProperty(rPath)) {
      console.info(`Base Module ID: ${currentBaseModules[rPath]}`);
      return currentBaseModules[rPath];
    } if (currentModules.hasOwnProperty(rPath)) {
      console.info(`Module ID: ${currentModules[rPath]}`);
      return currentModules[rPath];
    } else {
      let moduleId = currentModuleId;
      console.info(`${rPath} => ${moduleId}`);
      currentModuleId = currentModuleId + 1;
      currentModules[rPath] = currentModuleId;
      console.info(`Module ID: ${moduleId}`);
      return moduleId;
    }
  };
}

function processModuleFilter(module) {
  let path = module["path"];
  if (path.indexOf("__prelude__") >= 0 ||
    path.indexOf("/node_modules/react-native/Libraries/polyfills") >= 0 ||
    path.indexOf("source-map") >= 0 ||
    path.indexOf("/node_modules/metro/src/lib/polyfills/") >= 0) {
    return false;
  }
  if (path.indexOf("require-") >= 0) {
    path = path.substring("require-".length);
  }
  let rPath = path.substring(pathRoot.length);
  if (currentBaseModules.hasOwnProperty(rPath)) {
    // console.info(`[processModuleFilter]: Base Modules xxxx ${rPath} xxxx`);
    return false;
  } else {
    // console.info(`[processModuleFilter]: Modules => ${path}`);
    console.info(module);
    return true;
  }
}

const modulesBundleConfig = {
  // resolver: {
  //   /* resolver options */
  // },
  // transformer: {
  //   /* transformer options */
  // },
  serializer: {
    createModuleIdFactory: createModuleIdFactory,
    processModuleFilter: processModuleFilter,
  },
  // server: {
  //   /* server options */
  // }
  /* general options */
};

module.exports = mergeConfig(defaultConfig, modulesBundleConfig);