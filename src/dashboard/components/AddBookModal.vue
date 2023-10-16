<template>
  <b-modal id="modal-add-book" size="lg">
    <template #modal-header>
      <div class="d-flex justify-content-between">
        <h5 class="mb-0">Add Book</h5>
      </div>
    </template>
    <form @submit.prevent="addBook">
      <b-form-group label="Book Name:" label-for="bookNameInput">
        <b-form-input id="bookNameInput" v-model="newBook.name" required></b-form-input>
      </b-form-group>
      <b-form-group label="Total Pages:" label-for="bookPagesInput">
        <b-form-input id="bookPagesInput" v-model="newBook.num_pages" type="number" required></b-form-input>
      </b-form-group>

      <b-form-group label="Author:" label-for="bookAuthorInput">
        <AuthorTreeSelect v-model="newBook.author_id" id="bookAuthorInput" class="mt-2" />
      </b-form-group>
      <b-button type="submit" variant="primary">Add Book</b-button>
    </form>
    <!-- Custom modal footer -->
    <template #modal-footer>
      <b-button variant="primary" size="sm" class="float-right" @click="hideModal"> Close </b-button>
    </template>
  </b-modal>
</template>

<script>
import AuthorTreeSelect from './AuthorTreeSelect.vue';

export default {
  data() {
    return {
      newBook: {
        name: '',
        author_id: null,
        num_pages: 0,
      },
    };
  },
  methods: {
    hideModal() {
      this.$bvModal.hide('modal-add-book');
      this.newBook.name = '';
      this.newBook.author_id = null;
      this.newBook.num_pages = 0;
    },
    async addBook() {
      try {
        const { data } = await this.$axios.post('/books/', this.newBook);
        this.$toast.show('Added New Book');
        this.hideModal();
        this.newBook.name = '';
        this.newBook.author_id = null;
        this.newBook.num_pages = 0;
        this.$emit('update-table-data');
      } catch (error) {
        this.$toast.error(error);
        throw error;
      }
    },
  },
  components: { TreeSelect: AuthorTreeSelect },
};
</script>

    <style>
</style>
