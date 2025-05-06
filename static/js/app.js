import Alpine from "./module.esm.js";
import { app } from "./state.js";

Alpine.data("app", app);
Alpine.start();
export default app;
