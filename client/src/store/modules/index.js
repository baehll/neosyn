const files = import.meta.glob("./*.js", {eager: true});
const modules = {};

for (const path in files) {
    // create the module name from fileName
    // remove the store.js extension and capitalize
    const moduleName = path
        .replace(/(\.\/|\.store\.js)/g, '')
        .replace(/^\w/, c => c.toUpperCase())

    modules[moduleName] = files[path].default || files[path];
}

export default modules;