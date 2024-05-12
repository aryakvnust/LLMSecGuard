<template>
  <v-container>
    <v-row>
      <v-col>
        <v-toolbar color="transparent" flat>
          <v-toolbar-title>Models</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            @click="
              () => {
                model = new LlmModel();
                model.id = undefined;
              }
            "
            >Create Model</v-btn
          >
        </v-toolbar>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-data-table
          :headers="headers"
          :items="models"
          :items-length="count"
          @update:options="getModels"
          @click:row="(event, { item }) => (model = item)"
        >
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>

  <v-dialog
    :model-value="model.id !== null"
    max-width="700px"
    @update:modelValue="
      (val) => {
        if (!val) model = new LlmModel();
      }
    "
  >
    <v-card>
      <v-card-title>Details</v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field
            v-model="model.name"
            label="Name"
            class="mb-4"
          ></v-text-field>

          <v-textarea
            v-model="model.description"
            label="Description"
            class="mb-4"
          ></v-textarea>

          <v-select
            v-model="model.model"
            :items="modelTypes"
            label="Model"
            class="mb-4"
          ></v-select>

          <v-text-field
            v-model="model.api_key"
            label="API Key"
            class="mb-4"
          ></v-text-field>

          <v-textarea
            v-model="model.summary"
            label="Summary"
            class="mb-4"
          ></v-textarea>
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>

        <v-btn color="red" @click="model = new LlmModel()">Cancel</v-btn>
        <v-btn
          v-if="model.id === undefined"
          color="primary"
          variant="flat"
          append-icon="mdi-content-save-check"
          :loading="posting"
          @click="postSave"
        >
          Save
        </v-btn>
        <v-btn
          v-else-if="model.id"
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

class LlmModel {
  id = null;
  name = "";
  description = "";
  model = "";
  api_key = "";
  summary = "";
}

export default defineComponent({
  data: () => ({
    loading: false,
    posting: false,
    count: 0,
    LlmModel,
    models: [],
    model: new LlmModel(),
    modelTypes: [],
    headers: [
      { title: "Name", value: "name" },
      { title: "Model", value: "model" },
    ],
  }),
  mounted() {
    this.getModels();
  },
  methods: {
    async getModels(options = { page: 1, itemsPerPage: 20 }) {
      this.loading = true;

      try {
        const { data: opts } = await axios.options("/prompt-agent/models/");
        this.modelTypes = opts.actions.POST.model.choices.map(
          (el) => el.value
        );

        const { data } = await axios.get("/prompt-agent/models/", {
          params: {
            page: options.page,
            page_size: options.itemsPerPage,
          },
        });
        this.count = data.count;
        this.models = data.results;
      } catch (err) {
        console.error(err);
      }
      this.loading = false;
    },
    async postSave() {
      this.posting = true;
      try {
        const { data } = await axios.post(`/prompt-agent/models/`, this.model);
        this.model = data;
      } catch (err) {
        console.error(err);
      }
      this.posting = false;
    },
    async patchSave() {
      this.posting = true;
      try {
        const { data } = await axios.patch(
          `/prompt-agent/models/${this.model.id}/`,
          this.model
        );
        this.model = new LlmModel();
      } catch (err) {
        console.error(err);
      }
      this.posting = false;
    },
  },
});
</script>
