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
      <p>Selected Author: {{ bookToEdit.author?.name }} <b-button size="sm" @click="toggleChangeAuthor">Change Author</b-button></p>

      <AuthorTreeSelect v-if="updatingAuthor" v-model="bookToEdit.author_id" :value="bookToEdit.author_id" />

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
      updatingAuthor: false,
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
        const payload = { ...this.bookToEdit };
        if (!this.updatingAuthor) {
          delete payload.author_id;
        }
        const { data } = await this.$axios.patch(`/books/${this.bookToEdit.id}`, payload);
        this.$toast.show('Updated Book');
        this.hideModal();
        this.editedBook.name = '';
        this.$emit('update-table-data');
      } catch (error) {
        throw error;
      }
    },
    toggleChangeAuthor(){
      this.updatingAuthor = !this.updatingAuthor
    }
  },
  components: { AuthorTreeSelect },
  watch: {
    bookToEdit(newVal) {
      this.editedBook = {
        name: newVal.name,
        author_id: newVal.author_id,
        num_pages: newVal.num_pages
      };
    },
  },
};
</script>

  <style>
</style>


