module.exports = {
    "env": {
        "browser": true,
        "jquery": true
    },
    "extends": "eslint:recommended",
    "globals": {
        "$$": true,
        "addElementClass": true,
        "DIV": true,
        "filter": true,
        "findValue": true,
        "forEach": true,
        "getElementsByTagAndClassName": true,
        "getNodeAttribute": true,
        "hideElement": true,
        "itemgetter": true,
        "list": true,
        "loadJSONDoc": true,
        "log": true,
        "logDebug": true,
        "map": true,
        "MochiKit": true,
        "range": true,
        "removeElementClass": true,
        "serializeJSON": true,
        "setDisplayForElement": true,
        "setStyle": true,
        "student_quiz": true,
        "swapDOM": true,
        "showElement": true,
        "queryString": true,
        "zip": true
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
