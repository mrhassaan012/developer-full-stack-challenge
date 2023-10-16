<template>
  <div id="app" class="my-3">
    <treeselect
      v-model="selectedAuthorId"
      :async="true"
      :load-options="loadOptions"
      :value="selectedAuthorId"
      placeholder="Select Author..."
      required
    />
  </div>
</template>

<script>
// import the component
import Treeselect from '@riophae/vue-treeselect';
import { ASYNC_SEARCH } from '@riophae/vue-treeselect';

import '@riophae/vue-treeselect/dist/vue-treeselect.css';

export default {
  props: {
    value: {
      type: [Number, null],
    },
  },
  components: { Treeselect },
  data() {
    return {
      options: [],
      selectedAuthorId: this.value,
    };
  },
  watch: {
    value(newVal, oldVal) {
      console.log('new', newVal, 'old', oldVal);
      if (newVal !== oldVal) {
        this.selectedAuthorId = newVal;
      }
    },
    selectedAuthorId(newValue) {
      this.$emit('input', newValue);
    },
  },

  methods: {
    loadOptions({ action, searchQuery, callback }) {
      if (action === ASYNC_SEARCH) {
        this.$axios.get(`/authors/?skip=0&limit=10`).then((response) => {
          const { data } = response;
          const items = data.data;
          const options = items.map((author) => ({
            id: author.id,
            label: `${author.name}`,
          }));
          callback(null, options);
        });
      }
    },
  },
};
</script>