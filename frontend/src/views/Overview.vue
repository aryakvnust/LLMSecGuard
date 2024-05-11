<template>
  <v-container>
    <v-row>
      <v-col>
        <h2>Overview</h2>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-data-table :headers="headers" :items="overview" :loading="loading" item-key="id" class="elevation-1">
          <template v-slot:item.open="{ item }">
            <v-btn :to="`/overview/${tobase64(JSON.stringify(item))}/`" variant="flat" color="primary"> Details </v-btn>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "@/plugins/axios";
import { defineComponent, h } from "vue";

export default defineComponent({
  data: () => ({
    loading: false,
    dialog: null,
    chart: [],
    overview: [],
    headers: [
      { title: "Model", value: "objects.model.name" },
      { title: "Branch", value: "objects.branch" },
      { title: "Score", value: "total_count" },
      { title: "Open", value: "open" },
    ],
  }),
  mounted() {
    this.getData();
  },
  methods: {
    tobase64(str) {
      return btoa(str);
    },
    async getData() {
      this.loading = true;
      try {
        const { data } = await axios.get("/analyzer/benchmark/overview/", {
          isPublic: true,
        });
        this.overview = data;
      } catch (err) {
        console.log(err);
      }
      this.loading = false;
    },
  },
});
</script>
