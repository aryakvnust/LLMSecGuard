import axios from "axios";
import store from "@/store";
import router from "@/router";

const options = {
  baseURL: process.env.VUE_APP_API_URL || "http://localhost:8000/api",
};

const instance = axios.create(options);

instance.interceptors.request.use(
  function (config) {
    const token = localStorage.getItem("LLMAccess");

    if (token && config.isPublic !== true) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  function (error) {
    return Promise.reject(error);
  }
);

instance.interceptors.response.use(
  function (response) {
    return response;
  },
  function (error) {
    if (error?.response?.status === 401) {
      store.dispatch("logout");
      router.push("/login");
    }

    store.commit("addMessage", {
      type: "error",
      text: "An error occurred while making the request",
      error,
    });

    return Promise.reject(error);
  }
);

export default instance;
