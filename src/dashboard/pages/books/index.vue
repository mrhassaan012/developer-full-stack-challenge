  <template>
  <div>
    <NavBar />
    <b-container>
      <h3 class="mt-3">Books</h3>
      <b-input-group class="my-3">
        <b-form-input
          placeholder="Search Books (can search with author's name as well)"
          v-model="searchQuery"
          @input="searchBooks"
        ></b-form-input>

        <b-input-group-append>
          <b-button v-b-modal.modal-add-book variant="info">Add Book</b-button>

          <AddBookModal @update-table-data="updateTable" />
          <EditBookModal :bookToEdit="bookToEdit" @update-table-data="updateTable" />
        </b-input-group-append>
      </b-input-group>

      <div class="scrollable-container">
        <b-list-group v-if="searchQueryResults.length > 0">
          <b-list-group-item v-for="(book, index) in searchQueryResults" :key="index"
            >{{ book.name }} (Author's name: {{ book.author.name }})</b-list-group-item
          >
        </b-list-group>
      </div>

      <div class="my-2">
        <b-pagination
          v-if="totalRows > perPage"
          v-model="currentPage"
          :total-rows="totalRows"
          :per-page="perPage"
          align="center"
          aria-controls="my-table"
        ></b-pagination>
        <b-table id="my-table" :items="items" :fields="tableFields" @row-clicked="editBook" hover>
          <template #cell(author)="data" class="">{{ data.value.name }}</template>

          <template #cell(action)="data">
            <b-button @click="deleteBook(data.item.id)" variant="danger">Delete</b-button>
          </template>
        </b-table>
      </div>
    </b-container>
  </div>
</template>

  <script>
import NavBar from '@/components/NavBar.vue';
import AddBookModal from '@/components/AddBookModal.vue';
import EditBookModal from '@/components/EditBookModal.vue';

export default {
  components: {
    NavBar,
    AddBookModal,
    EditBookModal,
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
          key: 'author',
        },
        {
          key: 'num_pages',
          label: 'Pages',
        },
        {
          key: 'action',
          class: 'text-center',
        },
      ],
      searchQuery: '',
      searchQueryResults: [],

      currentPage: 1,
      totalRows: 0,
      totalPages: 0,
      perPage: 10,
      items: [],
      hasNextPage: false,
      hasPrevPage: false,

      newBook: {
        name: '',
        author_id: undefined,
      },
      bookToEdit: {},

      value: null,
      options: [],
    };
  },
  async asyncData({ $axios }) {
    const skip = 0;
    const limit = 10;

    let promise = $axios.get(`/books/?skip=${skip}&limit=${limit}`);

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
        .get(`/books/?skip=${skip}&limit=${limit}`)
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

    searchBooks() {
      if (this.searchQuery) {
        this.$axios
          .get(`books/search/?query=${this.searchQuery}`)
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

    async deleteBook(bookId) {
      try {
        await this.$axios.delete(`/books/${bookId}`);
        this.fetchData(this.currentPage);

        this.$toast.show('Book deleted successfully');
      } catch (error) {
        this.$toast.show('Something went wrong');
      }
    },

    editBook(bookToEdit) {
      this.bookToEdit = bookToEdit;
      this.$bvModal.show('modal-edit-book');
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

