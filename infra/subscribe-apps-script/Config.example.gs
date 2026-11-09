// Copy to Config.gs and fill in. Config.gs is git-ignored. setup() in Code.gs copies these into Script properties.
var CONFIG = {
  SITE_URL: "https://ajoly35.github.io/gen-ai-living-review",
  SEND_TOKEN: "REPLACE_WITH_openssl_rand_-hex_32",
  SENDER_NAME: "AI Economics Brief",
  REPLY_TO: "a.p.joly@lse.ac.uk",
  EXEC_URL: "https://script.google.com/macros/s/DEPLOYMENT_ID/exec"   // the web app URL, so confirm/unsubscribe links never point at the wrong deployment
};
