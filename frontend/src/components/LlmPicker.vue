<template>
  <v-select
      :model-value="$store.state.model"
      :items="$store.state.models"
      item-title="name"
      item-value="id"
      density="compact"
      variant="solo-filled"
      flat
      hide-details
      class="mb-2"
      @update:model-value="id => $store.commit('setModel', id)"
  >
    <template #append>
      <v-btn
          icon="mdi-refresh"
          size="24"
          :loading="$store.state.loading"
          @click.capture="$store.dispatch('getLlmModels')"
      />
    </template>

    <template #append-inner>
      <v-chip v-if="$store.state.model === $store.state.topModel" color="success">TOP</v-chip>
    </template>
  </v-select>
</template>
<script>
export default {
  name: 'LlmPicker'
}
</script>