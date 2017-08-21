module.exports = {
    "env": {
        "browser": true,
        "jquery": true
    },
    "extends": "eslint:recommended",
    "globals": {
        "$$": true,
        "forEach": true,
        "map": true,
        "setStyle": true,
        "MochiKit": true,
        "queryString": true,
        "serializeJSON": true,
        "hideElement": true,
        "getElementsByTagAndClassName": true,
        "showElement": true,
        "logDebug": true,
        "addElementClass": true,
        "removeElementClass": true,
        "filter": true,
        "loadJSONDoc": true,
        "list": true,
        "range": true,
        "itemgetter": true,
        "findValue": true,
        "setDisplayForElement": true,
        "DIV": true,
        "swapDOM": true,
        "zip": true,
        "getNodeAttribute": true,
        "log": true
    },
    "rules": {
        "indent": [
            "error",
            4
        ],
        "linebreak-style": [
            "error",
            "unix"
        ],
        "no-unused-vars": [
            "error",
            {"vars": "all", "args": "none"}
        ],
        "quotes": [
            "error",
            "single"
        ],
        "semi": [
            "error",
            "always"
        ]
    }
};
