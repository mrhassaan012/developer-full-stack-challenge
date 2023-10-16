<template>
  <b-modal id="modal-edit-author" size="lg">
    <template #modal-header>
      <div class="d-flex justify-content-between">
        <h5 class="mb-0">Edit Author</h5>
      </div>
    </template>
    <form @submit.prevent="editAuthor">
      <b-form-group label="Author Name:" label-for="authorNameInput">
        <p>id: {{ authorToEdit.id }}</p>
        <b-form-input id="authorNameInput" v-model="authorToEdit.name" required></b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Edit Author</b-button>
    </form>
    <!-- Custom modal footer -->
    <template #modal-footer>
      <b-button variant="warning" @click="hideModal">Cancel</b-button>
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
  props: {
    authorToEdit: Object,
  },
  methods: {
    hideModal() {
      this.$bvModal.hide('modal-edit-author');
      this.$emit('update-table-data');
    },

    async editAuthor() {
      try {
        const payload = { name: this.authorToEdit.name };
        const { data } = await this.$axios.put(`/authors/${this.authorToEdit.id}`, payload);
        this.$toast.show('Edited New Author');
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


