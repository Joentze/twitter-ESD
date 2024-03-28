const axios = require('axios');

const SUPPORTED_HTTP_METHODS = new Set([
    "GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"
]);

async function invokeHttp(url, method = 'GET', json = null, options = {}) {
    let code = 200;
    let result = {};

    try {
        if (SUPPORTED_HTTP_METHODS.has(method.toUpperCase())) {
            const response = await axios({
                method: method,
                url: url,
                data: json,
                ...options
            });
            result = response.data;
        } else {
            throw new Error(`HTTP method ${method} unsupported.`);
        }
    } catch (error) {
        code = 500;
        result = {
            "code": code,
            "message": `Invocation of service fails: ${url}. ${error.message}`
        };
    }

    return result;
}

module.exports = { invokeHttp };

