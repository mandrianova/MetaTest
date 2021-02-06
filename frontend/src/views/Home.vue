<template>
  <b-container class="mx-0 px-0">
    <b-container>
      <b-row class="my-5 d-flex justify-content-between">
        <h1>Список психотерапевтов</h1>
        <b-button variant="outline-primary" v-on:click="updateData" v-bind:disabled="updating">
          <b-spinner v-if="updating" small></b-spinner>
          {{ updating ? "Обновление" : "Обновить данные" }}
        </b-button>
      </b-row>
    </b-container>
    <b-alert v-if="message" v-bind:variant="message_type" show="">
        {{message}}
    </b-alert>
    <Loader v-if="loading" />
    <DoctorList
      v-else-if="doctors.length"
      :doctors="doctors" :page="currentPage"
    />
    <p v-else>Нет данных</p>
    <b-pagination-nav class="my-3"
      v-if="count > 10" :link-gen="linkGen" :number-of-pages="Math.floor(count / 10) + 1" use-router
                      @change="getDoctors"
    ></b-pagination-nav>
  </b-container>
</template>

<script>
// @ is an alias to /src
import DoctorList from '@/components/DoctorList'
import Loader from '@/components/Loader'
import MetaResource from '@/services/Meta'

const service = new MetaResource()

export default {
  name: 'Home',
  props: ['currentPage'],
  data () {
    return {
      doctors: [],
      loading: true,
      updating: false,
      message: '',
      message_type: '',
      count: 0
    }
  },
  components: {
    DoctorList, Loader
  },
  methods: {
    getDoctors (page = this.currentPage) {
      service.getDoctorList(page)
        .then(json => {
          this.doctors = json.results
          this.count = json.count
          this.message = ''
          this.loading = false
        }).catch(() => {
          this.message = 'Ошибка на сервере'
          this.message_type = 'danger'
          this.loading = false
        })
    },
    updateData () {
      this.updating = true
      service.getUpdate()
        .then(json => {
          this.message = json.message
          this.message_type = json.message_type
          this.updating = false
          if (this.message_type === 'success') {
            this.getDoctors()
          }
        }).catch(() => {
          this.message = 'Ошибка на сервере'
          this.message_type = 'danger'
          this.updating = false
        })
    },
    linkGen (pageNum) {
      return pageNum === 1 ? '?' : `?page=${pageNum}`
    }
  },
  mounted () {
    this.getDoctors()
  },
  computed: {
    getPage () {
      this.getDoctors(this.currentPage)
      return this.currentPage
    }
  }
}
</script>
