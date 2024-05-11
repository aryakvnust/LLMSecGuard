import store from "@/store";
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    redirect: "/code",
  },
  {
    path: "/code",
    component: () => import("@/views/Home.vue"),
  },
  {
    path: "/overview",
    component: () => import("@/views/Overview.vue"),
  },
  {
    path: "/overview/:object",
    component: () => import("@/views/OverviewDetail.vue"),
  },
  {
    path: "/login",
    component: () => import("@/views/Login.vue"),
  },
  {
    path: "/models",
    component: () => import("@/views/rest/Models.vue"),
  },
  {
    path: "/analyzers",
    component: () => import("@/views/rest/Analyzers.vue"),
  },
  {
    path: "/vulnerability",
    component: () => import("@/views/rest/Vulnerability.vue"),
  },
  {
    path: "/rule",
    component: () => import("@/views/rest/Rule.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  store.dispatch("getUser");
  next();
});

export default router;
