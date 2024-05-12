<template>
  <v-container class="fill-height pa-0" fluid>
    <v-row class="fill-height">
      <v-col cols="6" class="py-2" style="background-color: #1e1e1e">
        <MonacoEditor
          :value="code"
          language="cpp"
          theme="vs-dark"
          @change="edited"
        />
      </v-col>

      <!-- Results -->
      <v-col
        cols="6"
        class="px-4"
        style="
          position: relative;
          overflow-y: scroll;
          max-height: calc(100vh - 108px);
        "
      >
        <v-card rounded="lg" class="mr-3 mb-4">
          <v-card-text>
            <div
              v-html="summary || `<span> Summary not available </span>`"
            ></div>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              prepend-icon="mdi-refresh"
              color="primary"
              :loading="analyzing"
              @click="postAnalyze"
            >
              Analyze
            </v-btn>
          </v-card-actions>
        </v-card>

        <v-card v-if="fixed" class="mb-4">
          <v-card-title>Fixed Code:</v-card-title>
          <v-card-text>
            <pre><code v-text="fixed"></code></pre>
          </v-card-text>
        </v-card>

        <v-expansion-panels class="pr-4">
          <v-expansion-panel
            v-for="(result, i) in results"
            :key="`result-${i}`"
            rounded="lg"
          >
            <v-expansion-panel-title>
              {{ result.rule.name }}
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-divider class="my-4"></v-divider>
              <pre><code v-text="`${result.line.toString().padEnd(3, ' ')}: ${result.code}`"></code></pre>
              <v-divider class="my-4"></v-divider>

              {{ result.rule.description }}
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>

        <!-- Analyze Overlay -->
        <v-overlay
          :model-value="!analyzed"
          class="align-center justify-center"
          persistent
          contained
        >
          <v-container fluid style="width: 100%">
            <v-row>
              <v-col>
                <p class="text-center">You haven't analyzed your code yet.</p>
              </v-col>
            </v-row>

            <v-row>
              <v-col>
                <v-btn
                  variant="flat"
                  color="primary"
                  block
                  :loading="analyzing"
                  @click="postAnalyze"
                >
                  Analyze
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-overlay>
      </v-col>
    </v-row>
  </v-container>

  <v-dialog v-model="promptModal" max-width="700px">
    <!-- TextArea -->
    <v-card v-if="!prompt.response" rounded="lg">
      <v-card-text>
        <v-textarea v-model="prompt.text" label="Prompt ..."></v-textarea>
      </v-card-text>

      <v-card-actions class="px-4 py-2">
        <v-spacer></v-spacer>
        <v-btn color="red" @click="promptModal = false">Close</v-btn>
        <v-btn
          color="primary"
          append-icon="mdi-send"
          variant="flat"
          :loading="prompt.loading"
          @click="postPrompt"
        >
          Submit
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- Response -->
    <v-card v-else rounded="lg">
      <v-card-text>
        <pre v-text="prompt.response" style="text-wrap: balance;"></pre>
      </v-card-text>

      <v-card-actions class="px-4 py-2">
        <v-spacer></v-spacer>
        <v-btn color="red" @click="prompt.response = ''">Discard</v-btn>
        <v-btn
          color="primary"
          append-icon="mdi-check"
          variant="flat"
          @click="
            () => {
              code = prompt.response;
              promptModal = false;
              prompt.response = '';
            }
          "
        >
          Import
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import MonacoEditor from "monaco-editor-vue3";
import axios from "@/plugins/axios";
import MarkdownIt from "markdown-it";

export default {
  components: {
    MonacoEditor,
  },
  data: () => ({
    analyzed: false,
    analyzing: false,
    code: `int main() {
    int x = 0;
    int y = x + 1;
    int a = y + 1;

    std::cout << x;
    return 0;
}`,
    results: [],
    fixed: null,
    summary: null,
    prompt: {
      loading: false,
      text: "",
      response: "",
    },
  }),
  mounted() {
    window.mrk = new MarkdownIt();
  },
  computed: {
    promptModal: {
      get() {
        return this.$route.query.prompt === "true";
      },
      set(val) {
        this.$router.push({ query: { prompt: val ? "true" : undefined } });
      },
    },
  },
  methods: {
    log: console.log,
    edited(code, changes) {
      console.log(changes), (this.code = code);
    },
    async postAnalyze() {
      this.analyzing = true;
      try {
        const { data } = await axios.post("/analyzer/analyzer/analyze/", {
          lang: this.$store.state.language,
          code: this.code,
        });
        await this.postJudge();

        this.results = data.results;
        this.fixed = data.fix || null;
        this.analyzed = true;
      } catch (error) {
        console.error(error);
      }
      this.analyzing = false;
    },
    async postJudge() {
      try {
        const { data } = await axios.post("/analyzer/analyzer/judge/", {
          code: this.code,
        });

        const mrk = new MarkdownIt();
        this.summary = mrk.render(data.description);
      } catch (err) {
        console.error(err);
      }
    },
    async postPrompt() {
      this.prompt.loading = true;
      try {
        const { data } = await axios.post("/prompt-agent/models/1/query/", {
          prompt: this.prompt.text,
        });

        this.prompt.response = data.results;
        console.log(data);
      } catch (error) {
        console.error(error);
      }
      this.prompt.loading = false;
    },
  },
};
</script>

<style scoped>
.monaco-editor {
  width: 100%;
  height: 100%;
}
</style>
