<template>
  <v-container class="fill-height pa-0" fluid>
    <v-row class="fill-height">
      <v-col cols="6"></v-col>
      <v-col cols="6" class="pr-4" style="background-color: #1e1e1e">
        <v-tabs v-model="tab" color="primary" grow>
          <v-tab value="login">Login</v-tab>
          <v-tab value="signup">Sign up</v-tab>
        </v-tabs>

        <v-window v-model="tab">
          <!-- Login -->
          <v-window-item value="login" class="py-10 px-4">
            <v-form v-model="login.valid" @submit.prevent="postLogin">
              <v-text-field
                v-model="login.username"
                label="Username"
                :rules="[validators.required]"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="login.password"
                label="Password"
                :rules="[validators.required]"
                :type="login.showPassword ? 'text' : 'password'"
                :append-icon="login.showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="login.showPassword = !login.showPassword"
                class="mb-4"
              ></v-text-field>
            </v-form>

            <v-btn
              color="primary"
              class="mt-4"
              block
              :disabled="!login.valid"
              :loading="loading"
              @click="postLogin"
            >
              Login
            </v-btn>
          </v-window-item>

          <!-- Sign Up -->
          <v-window-item value="signup" class="py-10 px-4">
            <v-form v-model="signUp.valid" @submit.prevent="postSignup">
              <v-text-field
                v-model="signUp.firstName"
                label="First Name"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="signUp.lastName"
                label="Last Name"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="signUp.email"
                label="Email"
                :rules="[validators.required, validators.email]"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="signUp.username"
                label="Username"
                :rules="[validators.required]"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="signUp.password"
                label="Password"
                :type="signUp.showPassword ? 'text' : 'password'"
                :append-icon="signUp.showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :rules="[validators.required, validators.password]"
                class="mb-4"
                @click:append="signUp.showPassword = !signUp.showPassword"
              ></v-text-field>
            </v-form>

            <v-btn
              color="primary"
              class="mt-4"
              block
              :disabled="!login.valid"
              :loading="loading"
              @click="postSignup"
            >
              Sign Up
            </v-btn>
          </v-window-item>
        </v-window>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "@/plugins/axios";
import { defineComponent } from "vue";

export default defineComponent({
  data: () => ({
    tab: "login",
    loading: false,
    login: {
      valid: false,
      showPassword: false,
      username: "",
      password: "",
    },
    signUp: {
      valid: false,
      showPassword: false,
      username: "",
      email: "",
      firstName: "",
      lastName: "",
      password: "",
    },
    validators: {
      required: (v) => !!v || "This field is required",
      email: (v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
      password: (v) =>
        v.length >= 8 || "Password must be at least 8 characters",
    },
  }),
  methods: {
    async postLogin() {
      this.loading = true;
      try {
        const { data } = await axios.post(
          "/auth/token/",
          {
            username: this.login.username,
            password: this.login.password,
          },
          { isPublic: true }
        );

        window.localStorage.setItem("LLMAccess", data.access);
        window.localStorage.setItem("LLMRefresh", data.refresh);

        this.$store.dispatch("getUser");
        this.$router.push("/");
      } catch (error) {
        console.error(error);
      }
      this.loading = false;
    },
    async postSignup() {
      this.loading = true;

      try {
        const { data } = await axios.post(
          "/auth/sign-up/",
          {
            username: this.signUp.username,
            email: this.signUp.email,
            first_name: this.signUp.firstName,
            last_name: this.signUp.lastName,
            password: this.signUp.password,
          },
          {
            isPublic: true,
          }
        );
        this.login.username = username;
        this.tab = "login";
      } catch (error) {
        console.error(error);
      }

      this.loading = false;
    },
  },
});
</script>
