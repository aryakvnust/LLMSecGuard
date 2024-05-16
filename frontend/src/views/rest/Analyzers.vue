<template>
  <v-container>
    <v-row>
      <v-col>
        <v-toolbar color="transparent" flat>
          <v-toolbar-title>Analyzers</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            @click="
              () => {
                analyzer = new CodeAnalyzer();
                analyzer.id = undefined;
              }
            "
          >
            Create Analyzer
          </v-btn>
        </v-toolbar>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-data-table
          :headers="headers"
          :items="analyzers"
          :items-length="count"
          @update:options="getAnalyzers"
          @click:row="(event, { item }) => (analyzer = item)"
        >
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>

  <v-dialog
    :model-value="analyzer.id !== null"
    max-width="700px"
    @update:modelValue="
      (val) => {
        if (!val) analyzer = new CodeAnalyzer();
      }
    "
  >
    <v-card>
      <v-card-title>Details</v-card-title>
      <v-card-text>
        <v-form>
            <v-text-field
            v-model="analyzer.name"
            label="Name"
            class="mb-4"
            ></v-text-field>

            <v-textarea
            v-model="analyzer.description"
            label="Description"
            class="mb-4"
            ></v-textarea>

            <v-text-field
            v-model="analyzer.url"
            label="API Key"
            class="mb-4"
            ></v-text-field>

            <v-text-field
            v-model="analyzer.api_key"
            label="API Key"
            class="mb-4"
            ></v-text-field>

            <v-textarea
            v-model="analyzer.summary"
            label="Summary"
            class="mb-4"
            ></v-textarea>
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>

        <v-btn color="red" @click="analyzer = new CodeAnalyzer()">Cancel</v-btn>
        <v-btn
          v-if="analyzer.id === undefined"
          color="primary"
          variant="flat"
          append-icon="mdi-content-save-check"
          :loading="posting"
          @click="postSave"
        >
          Save
        </v-btn>
        <v-btn
          v-else-if="analyzer.id"
          color="primary"
          variant="flat"
          append-icon="mdi-content-save-check"
          :loading="posting"
          @click="patchSave"
        >
          Update
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from "@/plugins/axios";
import { defineComponent } from "vue";

class CodeAnalyzer {
  id = null;
  name = "";
  description = "";
  url = "";
  api_key = "";
  summary = "";
}

export default defineComponent({
  data: () => ({
    loading: false,
    posting: false,
    count: 0,
    CodeAnalyzer,
    analyzers: [],
    analyzer: new CodeAnalyzer(),
    analyzerTypes: [],
    headers: [
      { title: "Name", value: "name" },
      { title: "Url", value: "url" },
    ],
  }),
  mounted() {
    this.getAnalyzers();
  },
  methods: {
    async getAnalyzers(options = { page: 1, itemsPerPage: 20 }) {
      this.loading = true;

      try {
        const { data } = await axios.get("/security-agent/analyzer/", {
          params: {
            page: options.page,
            page_size: options.itemsPerPage,
          },
        });
        this.count = data.count;
        this.analyzers = data.results;
      } catch (err) {
        console.error(err);
      }
      this.loading = false;
    },
    async postSave() {
      this.posting = true;
      try {
        const { data } = await axios.post(
          `/analyzer/analyzer/`,
          this.analyzer
        );
        this.analyzer = data;
      } catch (err) {
        console.error(err);
      }
      this.posting = false;
    },
    async patchSave() {
      this.posting = true;
      try {
        const { data } = await axios.patch(
          `/analyzer/analyzer/${this.analyzer.id}/`,
          this.analyzer
        );
        this.analyzer = new CodeAnalyzer();
      } catch (err) {
        console.error(err);
      }
      this.posting = false;
    },
  },
});
</script>
