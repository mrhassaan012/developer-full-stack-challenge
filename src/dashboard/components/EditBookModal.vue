<template>
  <b-modal id="modal-edit-book" size="lg" title="Edit Book">
    <template #modal-header>
      <div class="d-flex justify-content-between">
        <h5 class="mb-0">Edit Book</h5>
      </div>
    </template>
    <form @submit.prevent="editBook">
      <b-form-group label="Book Name:" label-for="bookNameInput">
        <p>id: {{ bookToEdit.id }}</p>
        <b-form-input id="bookNameInput" v-model="bookToEdit.name" required placeholder="Name"></b-form-input>
      </b-form-group>
      <b-form-group label="Total Pages:" label-for="bookPagesInput">
        <b-form-input id="bookPagesInput" v-model="bookToEdit.num_pages" type="number" required></b-form-input>
      </b-form-group>
      <p>Selected Author: {{ bookToEdit.author?.name }}</p>
      <AuthorTreeSelect v-model="bookToEdit.author_id" :value="bookToEdit.author_id" />

      <b-button type="submit" variant="primary">Update Book</b-button>
    </form>
    <!-- Custom modal footer -->
    <template #modal-footer>
      <b-button variant="warning" @click="hideModal">Cancel</b-button>
    </template>
  </b-modal>
</template>


<script>
import AuthorTreeSelect from './AuthorTreeSelect.vue';

export default {
  data() {
    return {
      editedBook: {
        name: '',
        author_id: null,
        num_pages: 0,
      },
    };
  },
  props: {
    bookToEdit: Object,
  },
  methods: {
    hideModal() {
      this.$bvModal.hide('modal-edit-book');
      this.$emit('update-table-data');
    },

    async editBook() {
      try {
        const { data } = await this.$axios.patch(`/books/${this.bookToEdit.id}`, this.editedBook);
        this.$toast.show('Updated Book');
        this.hideModal();
        this.editedBook.name = '';
        this.$emit('update-table-data');
      } catch (error) {
        throw error;
      }
    },
  },
  components: { AuthorTreeSelect },
  watch: {
    bookToEdit(newVal) {
      this.editedBook = {
        name: newVal.name || '',
        author_id: newVal.author_id || null,
      };
    },
  },

  computed: {
    selectedOption() {
      // Find the option with the matching ID
      return this.options.find((option) => option.id === this.selectedOptionId) || null;
    },
  },
};
</script>

  <style>
</style>


