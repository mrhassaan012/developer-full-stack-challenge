<template>
  <b-modal id="modal-add-author" size="lg">
    <template #modal-header>
      <div class="d-flex justify-content-between">
        <h5 class="mb-0">Add Author</h5>
      </div>
    </template>
    <form @submit.prevent="addAuthor">
      <b-form-group label="Author Name:" label-for="authorNameInput">
        <b-form-input id="authorNameInput" v-model="newAuthor.name" required></b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Add Author</b-button>
    </form>
    <!-- Custom modal footer -->
    <template #modal-footer>
      <b-button variant="primary" size="sm" class="float-right" @click="hideModal"> Close </b-button>
    </template>
  </b-modal>
</template>

  <script>
export default {
  data() {
    return {
      newAuthor: {
        name: '',
      },
    };
  },
  props: {},
  methods: {
    hideModal() {
      this.$bvModal.hide('modal-add-author');
      this.newAuthor.name = '';
    },

    async addAuthor() {
      try {
        const { data } = await this.$axios.post('/authors/', this.newAuthor);
        this.$toast.show('Added New Author');
        this.hideModal();
        this.newAuthor.name = '';
        this.$emit('update-table-data');
      } catch (error) {
        throw error;
      }
    },
  },
};
</script>

  <style>
</style>
