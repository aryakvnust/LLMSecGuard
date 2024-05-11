<template>
  <v-container>
    <v-row>
      <v-col>
        <h2>Overview</h2>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-card>
          <v-card-text>
            <v-row>
              <v-col cols="2"> Model: </v-col>
              <v-col>
                <p>
                  <b>{{ data.objects?.model?.name }}</b>
                </p>
                <p>{{ data.objects?.model?.description }}</p>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="2"> Branch: </v-col>
              <v-col>
                <b>{{ data.objects?.branch }}</b>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-card :loading="loading">
          <v-card-text v-if="!loading">
            <apexchart type="bar" :options="options" :series="series"></apexchart>
          </v-card-text>
          <v-card-text v-else class="text-center">Loading Data...</v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-table>
          <thead>
            <tr>
              <th class="text-left">Property</th>
              <th class="text-left">Value</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in Object.keys(data).filter((k) => keys.includes(k))" :key="item">
              <td>{{ formatString(item) }}</td>
              <td>{{ data[item] }}</td>
            </tr>
          </tbody>
        </v-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "@/plugins/axios";
import { defineComponent } from "vue";
import VueApexCharts from "vue3-apexcharts";

export default defineComponent({
  components: { apexchart: VueApexCharts },
  data: () => ({
    loading: false,
    data: {},
    keys: [
      "is_extremely_malicious",
      "is_potentially_malicious",
      "is_non_malicious",
      "malicious_percentage",
      "injection_successful_count",
      "injection_unsuccessful_count",
      "total_count",
      "injection_successful_percentage",
      "injection_unsuccessful_percentage",
    ],

    // CHART
    options: {
      theme: {
        mode: "dark",
      },
      xaxis: {
        categories: [],
      },
    },
    series: [],
  }),
  mounted() {
    this.data = this.getData();
    this.getChart();
  },
  methods: {
    getData() {
      try {
        return JSON.parse(atob(this.$route.params.object));
      } catch (err) {
        console.error(err);
        return {};
      }
    },
    async getChart() {
      this.loading = true;
      try {
        const { data } = await axios.get("/analyzer/monthly-sum-cache/chart_data/", {
          params: { model: this.data.objects.model.id },
        });
        this.options.xaxis.categories = data.map((d) => d.date);
        this.series = [
          {
            name: "Usage",
            color: "#008FFB",
            data: data.map((d) => d.usage),
          },
          {
            name: "Error",
            color: "#FF4560",
            data: data.map((d) => d.errors),
          },
        ];
      } catch (err) {
        console.error(err);
      }
      this.loading = false;
    },
    formatString(str) {
      const words = str.split("_");
      const capitalizedWords = words.map((word) => word.charAt(0).toUpperCase() + word.slice(1));
      return capitalizedWords.join(" ");
    },
  },
});
</script>
