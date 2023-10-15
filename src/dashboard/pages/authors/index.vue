<template>
  <div>
    <NavBar />
    <b-container>
      <h3 class="mt-3">Authors</h3>
      <b-input-group prepend="Search Authors" class="my-3">
        <b-form-input v-model="searchQuery" @input="searchAuthors"></b-form-input>

        <b-input-group-append>
          <b-button v-b-modal.modal-add-author variant="info">Add</b-button>

          <AddAuthorModal @update-table-data="updateTable" />
          <EditAuthorModal :authorToEdit="authorToEdit" @update-table-data="updateTable" />
        </b-input-group-append>
      </b-input-group>
      <div class="scrollable-container">
        <b-list-group v-if="searchQueryResults.length > 0">
          <b-list-group-item v-for="(author, index) in searchQueryResults" :key="index"
            >{{ author.name }} (Book Count: {{ author.book_count }})</b-list-group-item
          >
        </b-list-group>
      </div>

      <div class="my-2">
        <b-pagination
          v-model="currentPage"
          :total-rows="totalRows"
          :per-page="perPage"
          align="center"
          aria-controls="my-table"
        ></b-pagination>
        <b-table id="my-table" :items="items" :fields="tableFields" @row-clicked="editAuthor" hover>
          <template #cell(book_count)="data" class="">{{ data.value }}</template>

          <template #cell(action)="data">
            <b-button @click="deleteAuthor(data.item.id)" variant="danger">Delete</b-button>
          </template>
        </b-table>
      </div>
    </b-container>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import AddAuthorModal from '@/components/AddAuthorModal.vue';
import EditAuthorModal from '@/components/EditAuthorModal.vue';

export default {
  components: {
    NavBar,
    AddAuthorModal,
    EditAuthorModal,
  },

  watch: {
    currentPage(newPage) {
      this.fetchData(newPage);
    },
  },

  data() {
    return {
      tableFields: [
        {
          key: 'id',
        },
        {
          key: 'name',
        },
        {
          key: 'book_count',
          label: 'Books (count)',
          thStyle: 'width: 100px',
        },
        {
          key: 'action',
          class: 'text-center',
        },
      ],
      tableDataType: 'authors',
      searchQuery: '',
      searchQueryResults: [],

      currentPage: 1,
      totalRows: 0,
      totalPages: 0,
      perPage: 10,
      items: [],
      hasNextPage: false,
      hasPrevPage: false,

      newAuthor: {
        name: '',
      },
      authorToEdit: {},
    };
  },
  async asyncData({ $axios }) {
    const skip = 0;
    const limit = 10;

    let promise = $axios.get(`/authors/?skip=${skip}&limit=${limit}`);

    try {
      const { data } = await promise;
      return {
        items: data.data,
        currentPage: data.current_page,
        totalRows: data.total_count,
        totalPages: data.total_pages,
        hasNextPage: data.has_next_page,
        hasPrevPage: data.has_prev_page,
      };
    } catch (error) {}
  },

  methods: {
    fetchData(currentPage) {
      const skip = (currentPage - 1) * this.perPage;
      const limit = this.perPage;

      this.$axios
        .get(`/authors/?skip=${skip}&limit=${limit}`)
        .then((response) => {
          const data = response.data;
          this.items = data.data;
          this.currentPage = data.current_page;
          this.totalRows = data.total_count;
          this.totalPages = data.total_pages;
          this.hasNextPage = data.has_next_page;
          this.hasPrevPage = data.has_prev_page;
        })
        .catch((error) => {
          this.$toast.error(error);
        });
    },

    searchAuthors() {
      if (this.searchQuery) {
        this.$axios
          .get(`authors/search/?query=${this.searchQuery}`)
          .then((response) => {
            this.searchQueryResults = response.data;
          })
          .catch((error) => {
            console.error(error);
          });
      } else {
        this.searchQueryResults = [];
      }
    },

    updateTable() {
      this.fetchData(this.currentPage);
    },

    async deleteAuthor(authorId) {
      try {
        await this.$axios.delete(`/authors/${authorId}`);

        // Update the table data by removing the deleted author
        this.fetchData(this.currentPage);

        this.$toast.show('Author deleted successfully');
      } catch (error) {
        this.$toast.show('Something went wronge');
      }
    },

    editAuthor(authorToEdit) {
      this.authorToEdit = authorToEdit;
      this.$bvModal.show('modal-edit-author');
    },
  },
};
</script>


<style>
.scrollable-container {
  max-height: 180px;
  overflow-y: scroll;
}
</style>

