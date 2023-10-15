<template>
  <div>
    <NavBar />
    <h1>Books and Authors</h1>

    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Book Name</th>
          <th>Author</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in booksWithAuthors" :key="index">
          <td>{{ item.id }}</td>
          <td>{{ item.name }}</td>
          <td>{{ item.author.name }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination -->
    <div>
      <button @click="loadNewPage(currentPage - 1)" :disabled="!hasPrevPage">Previous</button>
      <button @click="loadNewPage(currentPage + 1)" :disabled="!hasNextPage">Next</button>
    </div>
  </div>
</template>


  <script>
import NavBar from '@/components/NavBar.vue';

export default {
  data() {
    return {
      booksWithAuthors: [],
      currentPage: 1,
      totalPage: 1,
      hasPrevPage: false,
      hasNextPage: false,
      limit: 10,
    };
  },
  async asyncData({ query }) {
    const skip = parseInt(query.skip) || 0;
    const limit = parseInt(query.limit) || 10;

    try {
      const response = await this.getBooks(skip, limit);

      return {
        booksWithAuthors: response.data,
        currentPage: response.current_page,
        totalPage: response.total_pages,
        hasPrevPage: response.has_prev_page,
        hasNextPage: response.has_next_page,
        limit,
      };
    } catch (error) {
      console.error('Error fetching books:', error);
      return {
        booksWithAuthors: [],
        currentPage: 1,
        totalPage: 1,
        hasPrevPage: false,
        hasNextPage: false,
        limit,
      };
    }
  },
  methods: {
    loadNewPage(page) {
      if (page < 1 || page > this.totalPage) {
        return;
      }
      const skip = (page - 1) * this.limit;
      this.$router.push({ query: { skip, limit: this.limit } });
    },
  },
  components: {
    NavBar,
  },
};
</script>
