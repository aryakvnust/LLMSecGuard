<template>
  <v-container>
    <v-row>
      <v-col>
        <v-toolbar color="transparent" flat>
          <v-toolbar-title>Rules</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            @click="
              () => {
                rule = new Rule();
                rule.id = undefined;
              }
            "
          >
            Create Rule
          </v-btn>
        </v-toolbar>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-data-table
          :headers="headers"
          :items="rules"
          :items-length="count"
          @update:options="getRules"
          @click:row="(event, { item }) => (rule = item)"
        >
          <template v-slot:item.language="{ item }">
            {{
              languageTypes.find((c) => c.value == item.language)?.title || "-"
            }}
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>

  <v-dialog
    :model-value="rule.id !== null"
    max-width="700px"
    @update:modelValue="
      (val) => {
        if (!val) rule = new Rule();
      }
    "
  >
    <v-card>
      <v-card-title>Details</v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field
            v-model="rule.name"
            label="Name"
            class="mb-4"
          ></v-text-field>

          <v-textarea
            v-model="rule.description"
            label="Description"
            class="mb-4"
          ></v-textarea>

          <v-textarea
            v-model="rule.rule"
            label="Rule"
            class="mb-4"
            style="font-family: monospace"
          ></v-textarea>

          <v-select
            v-model="rule.language"
            :items="languageTypes"
            label="Language"
            class="mb-4"
          ></v-select>

          <v-autocomplete
            v-model="rule.analyzer"
            :items="analyzers"
            item-title="name"
            item-value="id"
            label="Analyzer"
            class="mb-4"
            :loading="analyzerTimer !== null"
            @update:search="getAnalyzers"
          ></v-autocomplete>

          <v-autocomplete
            v-model="rule.vulnerability"
            :items="vulnerabilities"
            item-title="name"
            item-value="id"
            label="Vulnerability"
            class="mb-4"
            :loading="vulnerabilitiesTimer !== null"
            @update:search="getVulnerabilities"
          ></v-autocomplete>
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>

        <v-btn color="red" @click="rule = new Rule()">Cancel</v-btn>
        <v-btn
          v-if="rule.id === undefined"
          color="primary"
          variant="flat"
          append-icon="mdi-content-save-check"
          :loading="posting"
          @click="postSave"
        >
          Save
        </v-btn>
        <v-btn
          v-else-if="rule.id"
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

class Rule {
  id = null;
  name = "";
  description = "";
  severity = "l";
  is_public = false;
}

export default defineComponent({
  data: () => ({
    loading: false,
    posting: false,
    count: 0,
    Rule,
    rules: [],
    rule: new Rule(),
    languageTypes: [],

    analyzers: [],
    analyzerTimer: null,

    vulnerabilities: [],
    vulnerabilitiesTimer: null,

    headers: [
      { title: "Name", value: "name" },
      { title: "Language", value: "language" },
    ],
  }),
  mounted() {
    this.getRules();
  },
  methods: {
    async getRules(options = { page: 1, itemsPerPage: 20 }) {
      this.loading = true;

      try {
        const { data: opts } = await axios.options("/analyzer/rule/");
        this.languageTypes = opts.actions.POST.language.choices.map((c) => ({
          title: c.display_name,
          value: c.value,
        }));

        if(this.analyzers.length === 0) this.getAnalyzers(undefined);
        if(this.vulnerabilities.length === 0) this.getٰVulnerabilities(undefined);

        const { data } = await axios.get("/analyzer/rule/", {
          params: {
            page: options.page,
            page_size: options.itemsPerPage,
          },
        });
        this.count = data.count;
        this.rules = data.results;
      } catch (err) {
        console.error(err);
      }
      this.loading = false;
    },
    getAnalyzers(value) {
      clearTimeout(this.analyzerTimer);
      this.analyzerTimer = setTimeout(async () => {
        try {
          const { data } = await axios.get("/analyzer/analyzer/", {
            params: {
              search: value,
              page_size: 200,
            },
          });
          this.analyzers = data.results;
          this.analyzerTimer = null;
        } catch (err) {
          console.error(err);
        }
      }, 500);
    },
    getٰVulnerabilities(value) {
      clearTimeout(this.vulnerabilitiesTimer);
      this.vulnerabilitiesTimer = setTimeout(async () => {
        try {
          const { data } = await axios.get("/vulnerabilities/vulnerability/", {
            params: {
              search: value,
              page_size: 200,
            },
          });
          this.vulnerabilities = data.results;
          this.vulnerabilitiesTimer = null;
        } catch (err) {
          console.error(err);
        }
      }, 500);
    },
    async postSave() {
      this.posting = true;
      try {
        const { data } = await axios.post(`/analyzer/rule/`, this.rule);
        this.rule = data;
      } catch (err) {
        console.error(err);
      }
      this.posting = false;
    },
    async patchSave() {
      this.posting = true;
      try {
        const { data } = await axios.patch(
          `/analyzer/rule/${this.rule.id}/`,
          this.rule
        );
        this.rule = new Rule();
      } catch (err) {
        console.error(err);
      }
      this.posting = false;
    },
  },
});
</script>
