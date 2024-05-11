/**
 * plugins/index.js
 *
 * Automatically included in `./src/main.js`
 */

// Plugins
import vuetify from "./vuetify";
import router from "@/router";
import store from "@/store";

export function registerPlugins(app) {
  // DEBUG
  window.app = app;
  window.router = router;
  window.store = store;

  app.use(vuetify);
  app.use(router);
  app.use(store);
}
