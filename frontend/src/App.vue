<template>
  <v-theme-provider dark>
    <v-app>
      <v-app-bar density="compact" flat>
        <span class="mx-4">LLM-Guard</span>
        <v-btn to="/code" exact>Editor</v-btn>
        <v-btn to="/code?prompt=true" exact>Prompt</v-btn>
        <v-btn to="/overview" exact>Overview</v-btn>
        
        <v-spacer></v-spacer>

        <v-btn v-if="!user.id" to="/login">Login</v-btn>
        <v-menu v-else>
          <template v-slot:activator="{ props }">
            <v-avatar color="primary" class="mx-4" size="32" v-bind="props">
              {{ user.username[0] }}
            </v-avatar>
          </template>

          <v-list>
            <v-list-item>
              <v-list-item-title>@{{ user.username }}</v-list-item-title>
            </v-list-item>

            <v-divider></v-divider>

            <v-list-item to="/models" exact>
              <v-list-item-title> Models </v-list-item-title>
            </v-list-item>
            <v-list-item to="/analyzers" exact>
              <v-list-item-title> Analyzers </v-list-item-title>
            </v-list-item>
            <v-list-item to="/vulnerability" exact>
              <v-list-item-title> Vulnerabilities </v-list-item-title>
            </v-list-item>
            <v-list-item to="/rule" exact>
              <v-list-item-title> Rules </v-list-item-title>
            </v-list-item>

            <v-list-item>
              <v-btn
                color="red"
                width="200px"
                block
                @click="$store.dispatch('logout')"
              >
                Logout
              </v-btn>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-app-bar>

      <v-main>
        <RouterView></RouterView>
      </v-main>

      <v-footer app>
        <span class="mx-4">© 2021 LLM-Guard</span>
        <v-spacer></v-spacer>

        <div style="max-width: 200px">
          <v-select
            v-model="$store.state.language"
            :items="languages"
            variant="solo-filled"
            density="compact"
            flat
            hide-details
          ></v-select>
        </div>
      </v-footer>
    </v-app>
  </v-theme-provider>
</template>

<script>
import { defineComponent } from "vue";
import { mapState } from "vuex";

export default defineComponent({
  data: () => ({
    languages: [
      { title: "C++", value: "cpp" },
      { title: "Python", value: "python" },
      { title: "Java", value: "java" },
      { title: "JavaScript", value: "javascript" },
    ],
  }),
  computed: mapState({
    user: (state) => state.user || {},
  }),
});
</script>

<style>
::-webkit-scrollbar {
  display: none;
}

html,
body .v-main {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.v-overlay .v-overlay__scrim {
  background-color: rgba(
    var(--v-theme-on-surface),
    var(--v-overlay-opacity, 0.32)
  );
  backdrop-filter: blur(10px);
  opacity: 1 !important;
}
</style>
