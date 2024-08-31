import Vuex from "vuex";
import axios from "@/plugins/axios";

const store = new Vuex.Store({
    state: {
        // Define your state properties here
        language: "cpp",
        model: 0,
        topModel: 0,
        footerActions: null,
        loading: false,
        user: {},
        models: {},
        messages: [],
    },
    mutations: {
        // Define your mutations here
        setUser(state, user) {
            state.user = user;
        },
        setModel(state, id) {
            state.model = id || 0;
        },
        setTopModel(state, id) {
            state.topModel = id;
        },
        setLoading(state, loading) {
            state.loading = loading;
        },
        setModels(state, models) {
            state.models = models;
        },
        addMessage(state, message) {
            state.messages.push(message);
        },
        removeMessage(state) {
            state.messages.shift();
        },
        setObject(state, object) {
            state.object = object || {};
        }
    },
    actions: {
        // Define your actions here
        async getUser({commit, dispatch}) {
            const token = window.localStorage.getItem("LLMAccess");
            if (!token) return;

            const {data} = await axios.get("/auth/users/me/");
            commit("setUser", data);
            dispatch("getLlmModels");
        },
        async getLlmModels({commit}) {
            commit("setLoading", true)

            try {
                const {data} = await axios.get("/prompt-agent/models/", {page_size: 200});
                commit("setModels", data.results);

                if (data.results.length > 0) {
                    const {data: top_model} = await axios.get("/benchmark-agent/benchmark/get_top_model/");
                    commit("setModel", top_model.id);
                    commit("setTopModel", top_model.id);
                }

            } catch (err) {
                console.error(err);
                throw err;
            } finally {
                commit("setLoading", false);
            }
        },
        logout({commit}) {
            window.localStorage.removeItem("LLMAccess");
            window.localStorage.removeItem("LLMRefresh");
            commit("setUser", {});
        }
    },
    getters: {
        // Define your getters here
    },
});

export default store;
